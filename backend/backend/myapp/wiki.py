import wikipedia
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

class Wiki():

    def __init__(self, name):
        self.name = name
        for entry in wikipedia.search(name):
            if entry == name:
                self.name = name
                break

        self.page = wikipedia.page(self.name, auto_suggest=False)
        print(self.page.url)

    def get_labels(self):

        title_uri = re.sub("\s", "_", self.page.title)
        uri = "https://en.wikipedia.org/wiki/" + title_uri
        page = requests.get(uri)
        soup = BeautifulSoup(page.content, "html.parser")

        links = soup.find_all('a')

        source_uri = ''
        if re.findall('\<span\>Edit\<\/span\>', str(links)):
            source_uri = 'https://en.wikipedia.org/w/index.php?title=' + title_uri + '&action=edit&editintro=Template:BLP_editintro'
        else:
            source_uri = 'https://en.wikipedia.org/w/index.php?title=' + title_uri + '&action=edit'


        source_page = requests.get(source_uri)
        source_soup = BeautifulSoup(source_page.content, "html.parser")

        wiki_source = source_soup.find(id="wpTextbox1", class_="mw-editfont-monospace")

        #Initital Label Cleaning
        labels = re.findall('(==+.*==+)', str(wiki_source))
        anchor_removal = re.compile('\{\{[\w]+\|')
        for idx, label in enumerate(labels):
            label = re.sub(anchor_removal, '', label)
            label = re.sub('\}\}', '', label)
            labels[idx] = label

        return labels

    def clean_labels(self, labels):
        cleaned_labels = []
        for label in labels:
            label = re.sub("=+", "", label)
            cleaned_labels.append(label)

        return cleaned_labels

    def get_summary(self):
        return (wikipedia.summary(self.name, auto_suggest=False).split('\n'))[0]

    def get_agenda(self):

        labels = self.get_labels()

        #Finding all subheadings for controversy
        contro_words = ['Controversies', 'Controversy']
        start_idx = 0
        end_idx = 0
        for idx, label in enumerate(labels):
            if any(contro_word in label for contro_word in contro_words):
                start_idx = idx+1
            elif (not(start_idx == 0) and not(label[:3] == '===')):
                end_idx = idx
                break

        #Final label cleaning
        labels = self.clean_labels(labels)
        contros = labels[start_idx:end_idx]

        naughty_words = ['abuse', 'crime', 'sexual assault', 'minors', 'fraud', 'scandal']

        for label in labels:
            if any(naughty_word in label for naughty_word in naughty_words):
                contros.append(label)


        if len(contros)==0:
            contros.append("No major controversies were found during our search.")

        return contros

    def get_views(self):

        labels = self.get_labels()

        print(labels)
        view_words = ['view', 'political', 'beliefs']
        start_idx = 0
        end_idx = 0
        for idx, label in enumerate(labels):
            if any(view_word in label.lower() for view_word in view_words):
                if start_idx == 0:
                    start_idx = idx+1
            elif (not(start_idx == 0) and not(label[:3] == '===')):
                end_idx = idx
                break


        views = (self.clean_labels(labels))[start_idx:end_idx]

        if len(views) == 0:
            views.append("No views were found in our search.")

        return views
