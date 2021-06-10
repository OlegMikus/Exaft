import json

from SPARQLWrapper import SPARQLWrapper, JSON


def get_all_data(url: str, request: str):
    sparql = SPARQLWrapper(url)
    sparql.setQuery(request)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()["results"]["bindings"]


def get_boss(url: str, param: str, item: str):
    query_boss = 'SELECT  ?item ?itemLabel ?bossLabel WHERE { ' \
                 f'BIND(<{param}> AS ?item) ' \
                 'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } ' \
                 'OPTIONAL { ?item ' \
                 f'wdt:{item} ' \
                 '?boss. }}'
    sparql = SPARQLWrapper(url)
    sparql.setQuery(query_boss)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()["results"]["bindings"]


def get_links(url: str, link: str) -> dict:
    queryset = 'SELECT ?item ?inst ?placeLabel ?date ?twit ?Facebook ?site WHERE { ' \
               f'BIND(<{link}> AS ?item) ' \
               'SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } ' \
               'OPTIONAL { ?item wdt:P2003 ?inst. } ' \
               'OPTIONAL { ?item wdt:P2002 ?twit. } ' \
               'OPTIONAL { ?item wdt:P2013 ?Facebook. }' \
               ' OPTIONAL { ?item wdt:P856 ?site. }' \
               ' OPTIONAL { ?item wdt:P159 ?place. }' \
               ' OPTIONAL { ?item wdt:P571 ?date. }' \
               '}'
    sparql = SPARQLWrapper(url)
    sparql.setQuery(queryset)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()["results"]["bindings"][0]


def main():
    endpoint_url = "https://query.wikidata.org/sparql"
    query = """SELECT ?item ?label WHERE {
            ?item wdt:P31 wd:Q891723.
            SERVICE wikibase:label {
            bd:serviceParam wikibase:language "en".
            ?item rdfs:label ?label. } }
            LIMIT 100"""
    results = get_all_data(endpoint_url, query)

    output = []
    count_boss = 0
    count_area = 0
    for index, result in enumerate(results):
        link = result['item']['value']
        print(index)
        title = result['label']['value']
        bosses = get_boss(endpoint_url, link, 'P169')
        areas = get_boss(endpoint_url, link, 'P452')
        links = get_links(endpoint_url, link)

        try:
            date = links['date']['value'][0:10]
        except KeyError:
            date = None
        try:
            inst_link = 'https://www.instagram.com/' + links['inst']['value']
        except KeyError:
            inst_link = None

        try:
            twit_link = 'https://twitter.com/' + links['twit']['value']
        except KeyError:
            twit_link = None

        try:
            face_link = 'https://www.facebook.com/' + links['Facebook']['value']
        except KeyError:
            face_link = None
        try:
            off_site = links['site']['value']
        except KeyError:
            off_site = None
        try:
            location = links['placeLabel']['value']
        except KeyError:
            location = None

        for new_index, name in enumerate(areas):
            count_area += 1
            try:
                area_name = name['bossLabel']['value']
            except KeyError:
                area_name = None
            area = {
                "model": "api.areasofactivity",
                "pk": count_area,
                "fields": {
                    "company": index + 1,
                    "title": area_name
                }
            }
            output.append(area)

        for new_index, name in enumerate(bosses):
            count_boss += 1
            try:
                boss_name = name['bossLabel']['value']
            except KeyError:
                boss_name = None
            boss = {
                "model": "api.topmanagers",
                "pk": count_boss,
                "fields": {
                    "company": index + 1,
                    "name": boss_name
                }
            }
            output.append(boss)

        links = {
            "model": "api.links",
            "pk": index + 1,
            "fields": {
                "company": index + 1,
                "inst": inst_link,
                "facebook": face_link,
                "twitter": twit_link,
                "off_site": off_site
            }
        }
        output.append(links)
        org = {
            "model": "api.organization",
            "pk": index + 1,
            "fields": {
                "title": title,
                "creation_date": date,
                "location": location
            }
        }

        output.append(org)

    return output


with open('api/fixtures/test.json', 'w') as fout:
    json.dump(main(), fout)
