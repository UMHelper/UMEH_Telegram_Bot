from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import os, requests

from chatbot.utils import get_comment_path,get_index_path

os.environ['OPENAI_API_KEY']='sk-'

def download_comment(course_code, prof_name):
    path = get_comment_path(course_code, prof_name)
    if os.path.exists(path):
        return
    url = 'https://mpserver.umeh.top/all_comment_info/?New_code={}&prof_name={}'.format(course_code, prof_name)
    comments = requests.get(url).json()['comments']

    file_lisit=os.listdir(path)
    max_id=-1
    new_file_id=-1
    for file in file_lisit:
        if int(file.split('.')[0])>max_id:
            max_id=int(file.split('.')[0])
    text = ""
    for comment in comments:
        if comment['content'] != "" and comment['id']>max_id:
            new_file_id=max(new_file_id,comment['id'])
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
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 1000

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    return service_context

def construct_index(course_code, prof_name):
    comment_path=get_comment_path(course_code, prof_name)
    index_path=get_index_path(course_code, prof_name)
    # check if index exists
    if os.path.exists(index_path):
        print('exist')
        return True
    documents = SimpleDirectoryReader(comment_path).load_data()
    index = GPTSimpleVectorIndex.from_documents(documents,service_context=get_service_context())
    index.save_to_disk(index_path)
    return True

def get_index(course_code, prof_name):
    index_path=get_index_path(course_code, prof_name)
    print(index_path)
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
    return index


def ask(question, course_code, prof_name):
    print(question,course_code, prof_name)
    download_comment(course_code, prof_name)
    construct_index(course_code, prof_name)

    index = get_index(course_code, prof_name)
    return index.query(question).response


if __name__ == '__main__':
    download_comment('TEST', 'TEST')
    construct_index('CISC1001', 'XU QIWEN')
    index=get_index('CISC1001', 'XU QIWEN')
    res=index.query('锐评这位老师')
    print(res.response,type(res.response))