import bs4
import json
import requests

with open("./dict_companies_html.json", 'r+') as myfile:
    data=myfile.read()
dict_companies_html = json.loads(data)

with open("./dbpedia_companies_list.json", 'r+') as myfile:
    data=myfile.read()
companies_list = json.loads(data)



for i in range(3000,5000):

    page = companies_list[i]
    print(page)
    response = requests.get("https://en.wikipedia.org/wiki/"+page)


    if response:
        #html = bs4.BeautifulSoup(response.text, 'html.parser')
        #print(html)
        dict_companies_html[page] = str(response.text)

print(len(dict_companies_html))
f = open("./dict_companies_html.json", "w+")
json_data = json.dumps(dict_companies_html)
f.write(json_data)  
