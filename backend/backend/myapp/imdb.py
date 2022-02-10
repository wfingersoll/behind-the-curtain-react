import collections
import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict


class IMDB:

    def __init__(self, movie):
        self.uri1 = "https://www.imdb.com/find?q="
        self.uri2 = "&ref_=nv_sr_sm"
        self.movie = movie.lower()

    def get_movie_page(self):

        movie_plus = ""
        movie_to_uri = self.movie.split(" ")

        for piece in movie_to_uri:
            movie_plus += piece
            movie_plus += "+"

        #Uri to search for movie
        full_uri = self.uri1 + movie_plus[:-1] + self.uri2

        #Get the search page
        page = requests.get(full_uri)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all('td', class_="result_text")

        #Get every title on the results
        titles = re.findall("\/title\/([a-zA-z0-9]+)\/\"\>([\w\s:-]+)</a>[^\<]+\(([0-9]+)\)", str(results))

        #Create a dictionary containing title, year, and id
        title_dict = collections.defaultdict(str)
        for count, title in enumerate(titles):
            if(title[1]+" ("+title[2]+")" in title_dict.keys()):
                title_dict[title[1] + " (" + title[2] + ") " + str(count)] = title[0]
            else:
                title_dict[title[1]+" ("+title[2]+")"] = title[0]

        #Attempt to find a link to the searched movie by comparing the titles found 
        #to the user's entered movie
        link = ''
        for key in title_dict.items():
            #Cleaning the key
            clean_key = re.sub("\(","",key[0])
            clean_key = re.sub("\)","",clean_key)
            clean_key = clean_key.lower()
            
            #Returning the link to identified movie            
            if (clean_key) == self.movie:
                link = key[1]
                return "https://www.imdb.com/title/" + link + "/?ref_=fn_al_tt_1"
        #If no results match the search return the first result
        try:
            link = list(title_dict.items())[0]
            return "https://www.imdb.com/title/" + link[1] + "/?ref_=fn_al_tt_1"
        except:
            return '0'

    def get_title(self, uri):

        page = requests.get(uri)
        soup = BeautifulSoup(page.content, "html.parser")

        html_title = soup.find("title")
        title = (re.findall('\>(.*)-', str(html_title)))[0]

        return title

    def get_cast(self, uri):

        page = requests.get(uri)
        soup = BeautifulSoup(page.content, "html.parser")

        cast = []
        top_cast = soup.find_all('a', class_="StyledComponents__ActorName-y9ygcu-1 eyqFnv")

        for member in top_cast:
            cast.append((re.findall("\>(.*)\<\/a\>", str(member)))[0])

        if (len(cast)) == 0:
            cast.append('N/A')

        return cast

    def get_crew(self, uri):

        uri = re.sub('\?ref_=fn_al_tt_1', "fullcredits/?ref_=tt_cl_sm", uri)
        page = requests.get(uri)
        soup = BeautifulSoup(page.content, "html.parser")

        print("URI: " + uri)

        crew = {"Directors": [],
                "Writers": [],
                "Producers": []
                }
        credits = soup.find_all('table', class_="simpleTable simpleCreditsTable")

        try:
            director_names = (re.findall('name\/.*\>(.*)', str(credits[0])))
        except:
            director_names = ['N/A']
        try:
            writer_names = (re.findall('name\/.*\>(.*)', str(credits[1])))
        except:
            writer_names = ['N/A']
        try:
            producer_names = (re.findall('name\/.*\>(.*)', str(credits[2])))
        except:
            producer_names = ['N/A']


        for name in director_names:
            crew['Directors'].append(name)

        for name in writer_names:
            crew['Writers'].append(name)

        for name in producer_names:
            crew['Producers'].append(name)

        return crew

    def get_special_credits(self, uri):

        uri = re.sub('\?ref_=fn_al_tt_1', "companycredits?ref_=tt_dt_co", uri)
        page = requests.get(uri)
        soup = BeautifulSoup(page.content, "html.parser")

        companies = {'Production': []}
        production_companies = soup.find_all('ul', class_='simpleList')

        for company in production_companies:
            companies['Production'].append((re.findall('\>(.*)\<\/a\>', str(company)))[0])

        if (len(companies)) == 0:
            companies['Production'] = 'N/A'

        return companies