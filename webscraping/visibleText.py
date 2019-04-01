'''
Credit also goes to
    DevWL who posted about removing excess content in html
        https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
'''

from bs4.element import Comment
from bs4 import BeautifulSoup

def tag_visible(element) -> bool:
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body: 'html') -> list:
    ''' remove all tag data from html '''
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return list(visible_texts)
