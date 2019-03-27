'''
Credit also goes to
    DevWL who posted about removing excess content in html
        https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
'''
import re
import mechanicalsoup
from bs4 import BeautifulSoup
from bs4.element import Comment

url = "https://www.reg.uci.edu/perl/WebSoc"

def get_raw_listings(department: str, course_number = None) -> 'Response':
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True
    )
    browser.set_verbose(2)
    browser.open(url)
    form = browser.select_form(nr=1).form
    submit_button = form.findAll(name='input')[0]
    #set department
    form.find(name = 'option' , attrs = {'value':department})['selected']='selected'
    if (course_number != None):
        #set course number
        form.find("input", {"name": "CourseNum"})["value"] = course_number
    page = browser.submit(form)
    browser.close()
    return page

def tag_visible(element) -> bool:
    #DevWL
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def trim_results(to_trim: list) -> list:
    start_index = next((i for i, x in enumerate(to_trim) if x.startswith('Code')), -1)
    end_index = start_index + 1 + next((i for i, x in enumerate(to_trim[start_index:]) if x.startswith('Total Classes Displayed')), -1)
    results = []
    for i in range(len(to_trim[start_index: end_index])):
        if to_trim[start_index + i].find('\xa0') >= 2:
            results.append(to_trim[start_index + i].replace('\xa0','').strip())
        elif to_trim[start_index + i].startswith('STAFF'):
            continue
        elif to_trim[start_index + i] not in ['\n', '\t', '']:
            results.append(to_trim[start_index + i].strip())
    return results
        
def text_from_html(body: 'html') -> list:
    ''' remove all tag data from html '''
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return list(visible_texts)

def format_results(html):
    '''make a list of lists, one course/header for each row'''
    results = trim_results(text_from_html(html))
    completed = []
    index = 0
    while index < len(results):
        temp = []
        last_element = 1 + (next((j for j, x in enumerate(results) if x.startswith('FULL') or x.startswith('OPEN') or x.startswith('Status')), 999))
        temp = [words for words in results[:last_element] if words not in ['', '(', ')', 'same', 'as']]         
        results = results[last_element:]
        completed.append(temp)
    completed[-1][0] = int(re.search('\d+$', completed[-1][0]).group(0))
    return completed

#known issue
#['18200', 'EECS\xa0148,\xa0Lec\xa0A)', '34091', 'Dis', '1', '0', 'MARKOPOULOU, A.', 'M   8:00- 8:50', 'PCB 1200', '56', '16 / 17', 'n/a', '22', 'A', 'Bookstore', 'OPEN']

if __name__ == '__main__':
    dept = 'COMPSCI' #input("set department (e.g. COMPSCI):")
    course = '122' #input("set course number (e.g. 143a):")
    html = get_raw_listings(dept, course)
    results = format_results(html.text)
    print('results for', dept, course)
    if len(results) > 0:
        for line in results:
            print(line)
    else:
        print('None found')
