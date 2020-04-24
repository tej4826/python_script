import urllib.request
from bs4 import BeautifulSoup
import requests, warnings
def get_questions(in_url):
    res = urllib.request.urlopen(in_url)
    soup = BeautifulSoup(res.read(), 'html.parser')
    get_names = lambda f: [v for k,v in f.attrs.items() if 'label' in k]
    get_name = lambda f: get_names(f)[0] if len(get_names(f))>0 else 'unknown'
    all_questions = soup.form.findChildren(attrs={'name': lambda x: x and x.startswith('entry.')})
    return {get_name(q): q['name'] for q in all_questions}
def submit_response(form_url, cur_questions, verbose=True, **answers):
    submit_url = form_url.replace('/viewform', '/formResponse')
    form_data = {'draftResponse':[],
                'pageHistory':0}
    for v in cur_questions.values():
        form_data[v] = ''
    for k, v in answers.items():
        if k in cur_questions:
            form_data[cur_questions[k]] = v
        else:
            warnings.warn('Unknown Question: {}'.format(k), RuntimeWarning)
    if verbose:
        print(form_data)
    user_agent = {'Referer':form_url,
                  'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
    form_data['entry.1156409']='Tej Prakash'
    form_data['entry.210055283']='190905'
    form_data['entry.192452008']='Yes'
    form_data['entry.446099277']='https://github.com/tej4826/python_script'
    print(form_data)
    return requests.post(submit_url, data=form_data, headers=user_agent)
TEST_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfxsg59ggPdonbOLakPTwn_qQk-P0euw531kGt2pdDxSlnB9Q/viewform"

anno_questions = get_questions(TEST_FORM_URL)
print(anno_questions)
#for i in range (5):
    #submit_response(TEST_FORM_URL, anno_questions)