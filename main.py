import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import logging
from umeh import fuzzy_search, get_course_info, get_comment_info
from utils import generate_course_keyboard, check_code, generate_course_info_markdown, generate_course_prof_keyboard, \
    generate_prof_info_markdown

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DIR = os.getcwd()

API_SERVER = "https://api.telegram.org/bot"

DEV_MODE = True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hello, this is What2Reg @UM Bot build by UMHelper Team.',
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text=update.message.text.upper()
    if check_code(text):
        course_info= get_course_info(text)
        print(course_info)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=generate_course_info_markdown(course_info['course_info']),
            reply_markup=InlineKeyboardMarkup(generate_course_prof_keyboard(course_info['prof_info'],text)),
            parse_mode='Markdown'
        )
        return

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Please enter the course code you want to check',
    )

async def course_prof_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_data=update.callback_query.data.split('@')
    course=query_data[0]
    prof=query_data[1]
    comment_info=get_comment_info(prof,course)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=generate_prof_info_markdown(comment_info['prof_info'],course,len(comment_info['comments'])),
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='View Comments', callback_data='view_comments@{}@{}'.format(course,prof))]]
        )
    )

async def view_comments_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query_data=update.callback_query.data.split('@')
    course = query_data[1]
    prof = query_data[2]
    comment_info = get_comment_info(prof, course)
    print(comment_info)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*{}*-*{}*'.format(course,prof),
        parse_mode='Markdown'
    )
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
    print(res)
    keyboard=generate_course_keyboard(res['course_info'])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Please select the course you want to check',
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
    view_comments_query_handler = CallbackQueryHandler(view_comments_query, pattern=r'view_comments@[A-Z]{4}[0-9]{4}@.*')
    bot.add_handler(start_handler)
    bot.add_handler(message_handler)
    bot.add_handler(search_handler)
    bot.add_handler(course_prof_query_handler)
    bot.add_handler(view_comments_query_handler)

    bot.run_polling()


if __name__ == '__main__':
    os.environ['UMEH_TG_BOT_TOKEN'] = ''
    main(os.environ['UMEH_TG_BOT_TOKEN'])
