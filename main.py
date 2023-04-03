import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging
from umeh import fuzzy_search, get_course_info, get_comment_info
from utils import generate_course_keyboard, check_code, generate_course_info_markdown, generate_course_prof_keyboard, \
    generate_prof_info_markdown, generate_prof_keyboard, generate_prof_markdown, generate_course_keybord_of_prof_info
from chatbot.ChatBot import ask
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DIR = os.getcwd()

API_SERVER = "https://api.telegram.org/bot"

DEV_MODE = True

import json
with open('language/ln_en.json', 'r') as f:
    ln = json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ln['GreetingText'],
    )


'''
{
    user_id: xxx,
}
'''
CURRENT_CHAT_WITH = []

'''
chat_id: {
    'prof': xxx,
    'course': xxx,
}
'''
CHAT_DETAIL = {}


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.text)
    text = update.message.text.upper()

    # check if it is a course code begin with four letters and four numbers
    if check_code(text):
        course_info = get_course_info(text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=generate_course_info_markdown(course_info['course_info']),
            reply_markup=InlineKeyboardMarkup(generate_course_prof_keyboard(course_info['prof_info'], text)),
            parse_mode='Markdown'
        )
        return

    user_id = update.message.from_user.id
    print(user_id)
    print(CURRENT_CHAT_WITH)
    if user_id in CURRENT_CHAT_WITH:
        res=ask(text,CHAT_DETAIL[update.effective_chat.id]['course'],CHAT_DETAIL[update.effective_chat.id]['prof'])
        print(res,type(res))
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=res,
        )
        return

    # check if it is a prof name or course name
    prof_info = fuzzy_search(text, 'prof')['prof_info']
    course_info = fuzzy_search(text, 'course')['course_info']

    print(prof_info)
    print(course_info)
    if len(prof_info) == 0 and len(course_info) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ln['NotFoundText'],
        )
        return

    if len(prof_info) == 0 and len(course_info) != 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ln['CourseProfSelectText'],
            reply_markup=ReplyKeyboardMarkup(generate_course_keyboard(course_info), one_time_keyboard=True)
        )
        return

    if len(prof_info) != 0 and len(course_info) == 0:
        if len(prof_info) > 1:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ln['ProfSelectText'],
                reply_markup=ReplyKeyboardMarkup(generate_prof_keyboard(prof_info), one_time_keyboard=True)
            )
            return
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=generate_prof_markdown(prof_info[0]),
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(generate_course_keybord_of_prof_info(prof_info[0]['courses']))
            )
            return
    if len(prof_info) != 0 and len(course_info) != 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ln['CourseProfSelectText'],
            reply_markup=ReplyKeyboardMarkup(generate_prof_keyboard(prof_info) + generate_course_keyboard(course_info),
                                             one_time_keyboard=True)
        )
        return
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ln["CourseCodeText"],
    )


async def end_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='End Chat',
    )
    CURRENT_CHAT_WITH.remove(user_id)
    del CHAT_DETAIL[user_id]


async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_data = update.callback_query.data.split('@')
    course = query_data[1]
    prof = query_data[2]
    user_id = update.callback_query.from_user.id
    print(user_id)
    CHAT_DETAIL[user_id] = {
        'prof': prof,
        'course': course,
    }
    CURRENT_CHAT_WITH.append(user_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='It is chat mode now, talking about {} in {}'.format(prof, course),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                text='End Chat',
                callback_data='end_chat@{}@{}'.format(course, prof),
            )]]
        )
    )


async def course_prof_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_data = update.callback_query.data.split('@')
    course = query_data[0]
    prof = query_data[1]
    comment_info = get_comment_info(prof, course)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=generate_prof_info_markdown(comment_info['prof_info'], course, len(comment_info['comments'])),
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(
                text=ln['ViewCommentsText'],
                callback_data='view_comments@{}@{}'.format(course, prof),
            )],
                [InlineKeyboardButton(
                    text='Start Chat with GPT about this course',
                    callback_data='start_chat@{}@{}'.format(course, prof),
                )]
            ]
        )
    )


async def show_more_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_data = update.callback_query.data.split('@')
    course = query_data[1]
    prof = query_data[2]
    start = int(query_data[3])
    comment_info = get_comment_info(prof, course)
    if len(comment_info['comments']) > start + 10:
        for comment in comment_info['comments'][start:start + 10]:
            if comment['content'] != '':
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=comment['content'],
                    parse_mode='Markdown'
                )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ln['ShowMoreCommentsBtnText'],
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    text='Show More Comments',
                    callback_data='show_more_comments@{}@{}@{}'.format(course, prof, start + 10),
                )]]
            )
        )
        return
    for comment in comment_info['comments'][start:]:
        if comment['content'] != '':
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=comment['content'],
                parse_mode='Markdown'
            )


async def view_comments_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_data = update.callback_query.data.split('@')
    course = query_data[1]
    prof = query_data[2]
    comment_info = get_comment_info(prof, course)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*{}*-*{}*'.format(course, prof),
        parse_mode='Markdown'
    )
    if len(comment_info['comments']) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='No comments found',
            parse_mode='Markdown'
        )
        return
    if len(comment_info['comments']) > 10:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Too many comments, only the first 10 comments are shown',
            parse_mode='Markdown')
        for comment in comment_info['comments'][:10]:
            if comment['content'] != '':
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=comment['content'],
                    parse_mode='Markdown'
                )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ln['ShowMoreCommentsBtnText'],
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    text=ln['ShowMoreCommentsText'],
                    callback_data='show_more_comments@{}@{}@{}'.format(course, prof, 10),
                )]]
            )
        )
        return
    else:
        for comment in comment_info['comments']:
            if comment['content'] != '':
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=comment['content'],
                    parse_mode='Markdown'
                )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = context.args[0]

    if len(code) < 4:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Too short 太短了！！！')
        return

    res = fuzzy_search(code, 'course')
    keyboard = generate_course_keyboard(res['course_info'])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ln["CourseSelectText"],
        reply_markup=ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


def main(token):
    bot = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    search_handler = CommandHandler('search', search)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)
    course_prof_query_handler = CallbackQueryHandler(course_prof_query, pattern=r'[A-Z]{4}[0-9]{4}@.*')
    view_comments_query_handler = CallbackQueryHandler(view_comments_query,
                                                       pattern=r'view_comments@[A-Z]{4}[0-9]{4}@.*')
    show_more_comment_handler = CallbackQueryHandler(show_more_comment,
                                                     pattern=r'show_more_comments@[A-Z]{4}[0-9]{4}@.*@.*')
    start_chat_handler = CallbackQueryHandler(start_chat, pattern=r'start_chat@[A-Z]{4}[0-9]{4}@.*')
    end_chat_handler = CallbackQueryHandler(end_chat, pattern=r'end_chat@.*')
    bot.add_handler(start_handler)
    bot.add_handler(message_handler)
    bot.add_handler(search_handler)
    bot.add_handler(course_prof_query_handler)
    bot.add_handler(view_comments_query_handler)
    bot.add_handler(show_more_comment_handler)
    bot.add_handler(start_chat_handler)
    bot.add_handler(end_chat_handler)
    if DEV_MODE:
        bot.run_polling()
    else:
        bot.run_webhook()


if __name__ == '__main__':
    os.environ['UMEH_TG_BOT_TOKEN'] = ''
    os.environ['OPENAI_API_KEY']='sk-'
    main(os.environ['UMEH_TG_BOT_TOKEN'])
