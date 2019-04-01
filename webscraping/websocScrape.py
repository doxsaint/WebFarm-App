import re
import mechanicalsoup
import visibleText

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

def trim_line(line: str) -> str:
    forbidden = ['\n', '\t', ')', 'same', '(', 'as', ' ']
    while line.find('\xa0') > -1:
        line = line.replace('\xa0','')
    if line not in forbidden:
        return line.strip()
    return ''

def trim_results(to_trim: list) -> list:
    start_index = -9 + next((i for i, x in enumerate(to_trim) if x.startswith('Code')), -1)
    end_index = start_index + 1 + next((i for i, x in enumerate(to_trim[start_index:]) if x.startswith('Total Classes Displayed')), -1)
    trimmed = []
    skip = False
    for s in to_trim[start_index:end_index]:
        temp = trim_line(s)
        if temp != '':
            trimmed.append(temp)
    return trimmed

def format_results(trimmed):
    '''make a list of lists, one course/header for each row'''
    completed = []
    while 0 < len(trimmed):
        temp = []
        last_index = 1 + (next((j for j, x in enumerate(trimmed) if x.startswith('FULL') or x.startswith('OPEN') \
                                  or x.startswith('Status')) or x.startswith('Prerequisites'), 999))
        temp = [words for words in trimmed[:last_index]]
        trimmed = trimmed[last_index:]
        completed.append(temp) 
    #remove elements that are between, as well as including, '(' and ')'
    for grouping in range(len(completed)):
        temp = []
        skip = False
        for word in completed[grouping]:
            if word.startswith('('):
                skip = True
            if not skip:
                temp.append(word)
            if word.endswith(')'):
                skip = False
        completed[grouping] = temp
    return completed

def pull_listings(department: str, course_number = None):
    #FIXME: later on, add quarter lookup functionality
    '''interface with webSOC to grab all courses available for the
    current quarter within a department
    Pulls class information and headers for a course (or all courses if
    course_number is not provided) followed by each course listing'''
    html = get_raw_listings(department, course_number)
    visible = visibleText.text_from_html(html.text)
    trimmed = trim_results(visible)
    return format_results(trimmed)

if __name__ == '__main__':
    dept = 'COMPSCI' #input("set department (e.g. COMPSCI):")
    course = None #input("set course number (e.g. 143a):")
    results = pull_listings(dept, course)
    print('results for', dept, course)
    if len(results) > 0:
        for line in results:
            print(line)
    else:
        print('None found')
