import re
import json

name_dbreference= {}

for i in range(1,12):
    with open("./dbpedia_data/companies/list_companies_urls"+str(i)+".json", 'r+') as myfile:
        data=myfile.read()
    list_companies = json.loads(data)
    print("list_companies_urls"+str(i))
    for name in list_companies:
        name = name.replace("http://dbpedia.org/resource/","")
        name_dbreference[name.replace("_", " ")] = name

f = open("./dict_company_name_dbreference.json", "w+")
json_data = json.dumps(name_dbreference)
f.write(json_data)  
