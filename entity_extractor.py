from bs4 import BeautifulSoup
import json

import spacy
import json
import re
import numpy as np
import sparql_utility

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from nltk.tokenize import MWETokenizer
from nltk.corpus import words, stopwords, wordnet

from collections import Counter, defaultdict

with open("./dict_companies_html.json", 'r+') as myfile:
    data=myfile.read()
dbpedia_companies_html = json.loads(data)

def extract_test_data():
    dict_test = {}
    counter =0
    for company in dbpedia_companies_html:
        dict_test[company] = dbpedia_companies_html[company]
        counter +=1
        if counter>=20:
            break
    
    f = open("./dict_companies_html_test.json", "w+")
    json_data = json.dumps(dict_test)
    f.write(json_data)  
extract_test_data()

def extract_dbpedia_properties(company_name):
    dbpedia_data = sparql_utility.query_for_information_entity_extraction(company_name)
    r = dbpedia_data["property"]["value"]
    print(r)
    return 0



def extract_wiki_page_links(html_doc):
    entities_links = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    metadata = ["Wikipedia:", "Portal:", "Category:", "Help:"]
    links = soup.find_all('a')
    for link in links:
        if "<a href=\"/wiki/" in str(link):
            wikipedia_pattern = re.compile(r"^((?!Wikipedia:).)*$")
            

            match = wikipedia_pattern.match(str(link))
            if match and not any([x in str(link) for x in metadata]):
               entities_links.append(link)
    
    return entities_links

def main():
    company_name = "Wyndham Capital Mortgage"
    html_doc = dbpedia_companies_html[company_name]
    legit_wiki_links = extract_wiki_page_links(html_doc)

    dbpedia_properties = extract_dbpedia_properties(company_name)


main()