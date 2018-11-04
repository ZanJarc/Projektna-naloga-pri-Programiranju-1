import requests
import re
import os
import csv
import json

avtonet_search_url = 'https://www.avto.net/'
directory_mapa = 'Mapa s podatki'
izluscena_imena = 'imena.html'
podatki_html = 'HTMLpodatki_imena.html'
podatki_csv = 'CSVpodatki_imena.csv'
imena_stolpcev = ['ime', 'letnik', 'kilometrina', 'motor', 'menjalnik', 'cena', 'cas']

def download_url_to_string(url):
    try:
        r = requests.get(url)
        r.encoding = 'windows-1250'
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja!')
        return ''
    return r.text


def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'a', encoding='utf-8') as file_out:
        file_out.write(text)
    return None



def save_frontpage(url, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    vsebina = download_url_to_string(url)
    with open(path, 'a', encoding='utf-8') as datoteka:
        datoteka.write(vsebina)
    print('shranjeno!')

def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, encoding='utf-8') as datoteka:
        return datoteka.read()


#dobimo samo tisti del html, kjer so imena
def page_to_names(directory, filename):
    vsebina = read_file_to_string(directory, filename)
    names = []
    vzorec = (
            r'<option value="">Izberite znamko</option>'
            r'.*?'
            r'</select>'
    )
    for ujemanje in  re.finditer(vzorec, vsebina, re.DOTALL):
        names.append(ujemanje.group(0))
    return names


def izlusci_znamke(directory, filename):
    list_of_names = []
    names = page_to_names(directory, filename)
    vzorec = (
        r'<option value=".+?">(?P<ime>.*?)</option>'
    )
    for ujemanje in re.finditer(vzorec, names[0], re.DOTALL):
        list_of_names.append(ujemanje.group('ime'))
    return list_of_names   


#dobimo samo tisti del html, ki vsebuje podatke o moznih modelih
def page_to_models(directory, filename):
    vsebina = read_file_to_string(directory, filename)
    text = []
    vzorec = (
            r'<select id="model" name="model">'
            r'.*?'
            r'</select>'
    )
    for ujemanje in  re.finditer(vzorec, vsebina, re.DOTALL):
        text.append(ujemanje.group(0))
    return text


#s tem dobimo vse mozne kombinacije
def izlusci_modele(directory, filename):
    list_of_models = []
    models = page_to_models(directory, filename)
    vzorec = (
        '<option value=".+?" class="(?P<znamka>.*?)">(?P<model>.*?)</option>'
    )
    for ujemanje in re.finditer(vzorec, models[0], re.DOTALL):
        if ujemanje.group('model') != "modela ni na seznamu":
            list_of_models.append('{} {}'.format(ujemanje.group('znamka'), ujemanje.group('model')))
    return list_of_models

#modeli urejeni po znamkah
def modeli_znamk(directory, filename):
    list_of_models = {}
    models = page_to_models(directory, filename)
    vzorec = (
        '<option value=".+?" class="(?P<znamka>.*?)">(?P<model>.*?)</option>'
    )
    for ujemanje in re.finditer(vzorec, models[0], re.DOTALL):
        if ujemanje.group('model') != "modela ni na seznamu":
            if ujemanje.group('znamka') in list_of_models:
                list_of_models[ujemanje.group('znamka')].append(ujemanje.group('model'))
            else:
                list_of_models[ujemanje.group('znamka')] = [ujemanje.group('model')]
    return list_of_models



   
                
