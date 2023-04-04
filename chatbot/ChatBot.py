from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext, \
    QuestionAnswerPrompt
from langchain import OpenAI
import os, requests

from chatbot.utils import get_comment_path, get_index_path, get_course_info


def download_comment(course_code, prof_name):
    path = get_comment_path(course_code, prof_name)
    if len(os.listdir(path)) > 0:
        return
    url = 'https://mpserver.umeh.top/all_comment_info/?New_code={}&prof_name={}'.format(course_code, prof_name)
    comments = requests.get(url).json()['comments']
    file_lisit = os.listdir(path)
    max_id = -1
    new_file_id = -1
    for file in file_lisit:
        if int(file.split('.')[0]) > max_id:
            max_id = int(file.split('.')[0])
    text = ""
    for comment in comments:
        if comment['content'] != "" and comment['id'] > max_id:
            new_file_id = max(new_file_id, comment['id'])
            text += comment['content'] + '\n'
    if text == "":
        return
    file = open(path + '/{}.txt'.format(new_file_id), mode='a')
    file.write(text)
    file.close()


def get_service_context():
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 50

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    return service_context


def construct_index(course_code, prof_name):
    comment_path = get_comment_path(course_code, prof_name)
    index_path = get_index_path(course_code, prof_name)
    # check if index exists
    if os.path.exists(index_path):
        return True
    documents = SimpleDirectoryReader(comment_path).load_data()
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=get_service_context())
    index.save_to_disk(index_path)
    return True


def get_index(course_code, prof_name):
    index_path = get_index_path(course_code, prof_name)
    index = GPTSimpleVectorIndex.load_from_disk(index_path, service_context=get_service_context())
    return index


def ask(question, course_code, prof_name):
    download_comment(course_code, prof_name)
    construct_index(course_code, prof_name)
    index = get_index(course_code, prof_name)
    course_info = get_course_info(course_code)
    QA_PROMPT_TMPL = (
            "Course description: {}\n".format(course_info['courseDescription']) +
            "Here is some comment from student about the teacher in this course:\n"
            "{context_str}"
            "\n---------------------\n"
            "Given this information, please answer the question: give me a brief summary about this course based on the "
            "course description and {query_str}\n "
            "---------------------\n"
            "Your answer should be in same language with the question, i.e. English to English or Chinese to Chinese.\n"
            "你回答所使用的语言必须与问题所使用的语言一致，例如问题是中文，那么回答也必须是中文。\n"
    )
    QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)

    res = index.query(question, text_qa_template=QA_PROMPT)
    res = res.response
    print(res)
    return res


if __name__ == '__main__':
    ask("How about this course", 'CISC1001', 'XU QIWEN')
