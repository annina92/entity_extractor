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

with open("./dict_companies_html_test.json", 'r+') as myfile:
    data=myfile.read()
dbpedia_companies_html = json.loads(data)

with open("../dict_companies_pages.json", 'r+') as myfile:
    data=myfile.read()
dict_companies_pages = json.loads(data)

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
#extract_test_data()

def extract_dbpedia_properties(company_name):
    metadata = ["wikiPageWikiLink", "wikiPageID", "wikiPageExternalLink", "wikiPageRevisionID", "abstract"]
    dbpedia_data = sparql_utility.query_for_information_entity_extraction(company_name)
    data = dbpedia_data["results"]["bindings"]

    dict_properties_values = {}
    for record in data:
        record_property = record["property"]["value"]
        record_value = record["value"]["value"]
        
        if "http://dbpedia.org/ontology/" in record_property and not any([x in record_property for x in metadata]):

            record_property = record_property.replace("http://dbpedia.org/ontology/", "")
            record_value = record_value.replace("http://dbpedia.org/resource/", "")
            dict_properties_values[record_value] = record_property
    
    return dict_properties_values


def extract_wiki_page_links(html_doc):
    entities_links = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    metadata = ["Wikipedia:", "Portal:", "Category:", "Help:", "Template:", "Template_talk"]
    links = soup.find_all('a')
    for link in links:
        if "<a href=\"/wiki/" in str(link):
            wikipedia_pattern = re.compile(r"^((?!Wikipedia:).)*$")
            

            match = wikipedia_pattern.match(str(link))
            if match and not any([x in str(link) for x in metadata]):
               entities_links.append(link)
    
    return entities_links

def extract_wiki_page_type(entity):

    dict_name_entityTag = {}
    dbpedia_data = sparql_utility.query_for_entity_classification(entity)
    data = dbpedia_data["results"]["bindings"]

    for record in data:
        record_property = record["property"]["value"]
        record_value = record["value"]["value"]
        if "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" in record_property:
            if "http://schema.org/" in record_value:
                if entity not in dict_name_entityTag:
                    dict_name_entityTag[entity] = []
                dict_name_entityTag[entity].append(record_value.replace("http://schema.org/", ""))

    return dict_name_entityTag


def match_dbpedia_properties_with_wiki_links(wiki_links, dbproperties):
    found = []
    not_found= []
    for link in wiki_links:
        entity_value = link.get("href").replace("/wiki/", "")
        entity_title = link.get("title")
    
        if entity_value in dbproperties:
            #print(entity_value+" : "+ dbproperties[entity_value])
            found.append(link)
        else:
            not_found.append(link)

    for link in not_found:
        entity_value = link.get("href").replace("/wiki/", "")
        entity_title = link.get("title")
        dict_entities = extract_wiki_page_type(entity_value)
        print(dict_entities)

def clean_page_text(page):
    tags_pattern = r"==.*=="
    empty_lines_pattern= r"^\s+$[\r\n]*"

    page = re.sub(tags_pattern, "", page)

    page = re.sub(empty_lines_pattern, "", page)

    return page
    
def main():
    company_name = "Haas Type Foundry"
    for word in dbpedia_companies_html:
        print(word)
    html_doc = dbpedia_companies_html[company_name]
    text = clean_page_text(dict_companies_pages[company_name])
    print(text)
    legit_wiki_links = extract_wiki_page_links(html_doc)
    print(legit_wiki_links)
    dbpedia_properties = extract_dbpedia_properties(company_name)
    print(dbpedia_properties)
    match_dbpedia_properties_with_wiki_links(legit_wiki_links, dbpedia_properties)

main()