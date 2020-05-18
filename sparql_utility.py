from SPARQLWrapper import SPARQLWrapper, JSON
import json

with open("./dict_company_name_dbreference.json", 'r+') as myfile:
    data=myfile.read()
dict_company_name_dbreference = json.loads(data)


def query_for_companies():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix dbpedia-owl: <http://dbpedia.org/ontology/>

        select ?company {{
        select ?company { 
            ?company a dbpedia-owl:Company
        }
        order by ?company
        }} 
        OFFSET 100000
        LIMIT 10000
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    result_list = []

    for result in results["results"]["bindings"]:
        print(result["company"]["value"])
        result_list.append(result["company"]["value"])

    print(len(result_list))
    f = open("./list_companies_urls11.json", "w+")
    json_data = json.dumps(result_list)
    f.write(json_data)  
    print('---------------------------')

def query_for_organizations():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix dbpedia-owl: <http://dbpedia.org/ontology/>
        prefix dbpedia-dbr: <http://dbpedia.org/resource/>

        select ?Organisation {{
        select ?Organisation { 
            ?Organisation a dbpedia-owl:Public_company
        }
        order by ?Organisation
        }} 
        LIMIT 10000
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    result_list = []

    for result in results["results"]["bindings"]:
        print(result["Organisation"]["value"])
        result_list.append(result["Organisation"]["value"])

    print(len(result_list))
    f = open("./dbpedia_data/organizations/list_companies_urls1.json", "w+")
    json_data = json.dumps(result_list)
    f.write(json_data)  
    print('---------------------------')   


def query_for_information_entity_extraction(entity_name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    entity_name = dict_company_name_dbreference[entity_name]
    sparql.setQuery(
    "PREFIX db: <http://dbpedia.org/resource/>"
    "PREFIX prop: <http://dbpedia.org/property/>"
    "PREFIX onto: <http://dbpedia.org/ontology/>"
    
    "SELECT ?property ?value "
    "WHERE { db:"+entity_name+" ?property ?value  }"
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results

def query_for_entity_classification(entity_name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(
    "PREFIX db: <http://dbpedia.org/resource/>"
    "PREFIX prop: <http://dbpedia.org/property/>"
    "PREFIX onto: <http://dbpedia.org/ontology/>"
    
    "SELECT ?property ?value "
    "WHERE { db:"+entity_name+" ?property ?value  }"
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results

#query_for_entity_classification("Wyndham Capital Mortgage")

###
### https://stackoverflow.com/questions/20937556/how-to-get-all-companies-from-dbpedia
### http://dbpedia.org/ontology/Company
###