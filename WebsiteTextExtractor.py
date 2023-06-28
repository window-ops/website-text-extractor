from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import PySimpleGUI as sg


def program():
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(string=True)
        visible_texts = filter(tag_visible, texts)
        return u"\n".join(t.strip() for t in visible_texts)

    layout = [
        [sg.Text('Enter a URL:')],
        [sg.InputText(key='url')],
        [sg.Button('Get text from website')],
    ]

    window = sg.Window('Text from URL:', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        url = values['url']

        try:
            html = urllib.request.urlopen(url).read()

            visible_text = text_from_html(html)

            sg.PopupScrolled(visible_text, title="Text from Website:", size=(600, 400))
        except:
            sg.Popup("Could not display website. Don't forget to include https:// or http:// in the url input!")

    window.close()


program()