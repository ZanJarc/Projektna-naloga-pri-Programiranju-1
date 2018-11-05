import requests
import re
import os
import csv
import json
import datetime


avtonet_url = 'https://www.avto.net/Ads/results_100.asp?oglasrubrika=1&prodajalec=2'
directory_mapa = 'Mapa s podatki'
izlusceni_oglasi = 'oglasi.html'
podatki_html = 'HTMLpodatki.html'
podatki_csv = 'CSVpodatki.csv'
podatki_json = 'JSONpodatki.json'
slovarji_html = 'slovarji.html'
directory_dnevno = 'Mapa s podatki/Dnevni podatki'
now = datetime.datetime.now()
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




def page_to_ads(directory, filename):
    vsebina = read_file_to_string(directory, filename)
    seznam_oglasov = []
    vzorec = (
            r'<!--------------------- DESCRIPTION  ------------------->'
            r'.*?'
            r'<!-- START BIG BANNER -->'
            )
    for ujemanje in re.finditer(vzorec, vsebina, re.DOTALL):
        nas_oglas = ujemanje.group(0)
        seznam_oglasov.append(nas_oglas)
    return seznam_oglasov



def save_ads(directory, podatki, filename):
    os.makedirs(directory, exist_ok=True)
    path_filename = os.path.join(directory, filename)
    vsebina = read_file_to_string(directory, podatki)
    vzorec = (
            r'<!--------------------- DESCRIPTION  ------------------->'
            r'.*?'
            r'<!-- START BIG BANNER -->'
            )
    with open(path_filename, 'w', encoding='utf-8') as datoteka:   
        for ujemanje in re.finditer(vzorec, vsebina, re.DOTALL):
            nas_oglas = ujemanje.group(0)
            datoteka.write(nas_oglas)  





#kako zaustavim for zanko
def izloci_podatke_oglasa(ujemanje_oglasa):
    podatki_oglasa = ujemanje_oglasa.groupdict()
    podatki_oglasa['cas'] = (now.day, now.month)
    podatki_oglasa['cena'] = podatki_oglasa['cena'] + '€'
    for model in MODELI:
        for ujemanje in re.finditer(model, podatki_oglasa['ime'], re.DOTALL):
            if ujemanje.group(0):
                podatki_oglasa['ime'] = ujemanje.group(0)
    return podatki_oglasa



def izloci_podatke_oglasa_BOLJSE(ujemanje_oglasa):
    podatki_oglasa = ujemanje_oglasa.groupdict()
    podatki_oglasa['cas'] = (now.day, now.month)
    podatki_oglasa['cena'] = podatki_oglasa['cena'] + '€'
    for znamka in MODELI_BOLJSE:
        if znamka.lower() in podatki_oglasa['ime'].lower():
            for model in MODELI_BOLJSE[znamka]:
                if '{} {}'.format(znamka, model).lower() in podatki_oglasa['ime'].lower():
                    podatki_oglasa['ime'] = '{} {}'.format(znamka, model)
    return podatki_oglasa






def get_dict_from_ad_block(directory, filename):
    podatki_oglasov = []
    '''Build a dictionary containing the name, description and price
    of an ad block.'''
    seznam_oglasov = page_to_ads(directory, filename)
    vsebina = read_file_to_string(directory, filename)
    vzorec = re.compile(
    r'<a class="Adlink" href=".*">\n\n<span>(?P<ime>.*)</span>\n\n</a>.*?'
    r'<li>Letnik 1.registracije:(?P<letnik>\d*)</li>(\n){2}\s*?<li>(?P<kilometrina>.*)?</li><li>(?P<motor>.*)</li><li>(?P<menjalnik>.*)</li>.*?'
    r'EUR=(?P<cena>\d*)',
    re.DOTALL
    )
    for oglas in seznam_oglasov:
        for ujemanje in vzorec.finditer(oglas):
                podatki_oglasov.append(izloci_podatke_oglasa(ujemanje))
    return podatki_oglasov



def get_dict_from_ad_block_BOLJSE(directory, filename):
    podatki_oglasov = []
    '''Build a dictionary containing the name, description and price
    of an ad block.'''
    seznam_oglasov = page_to_ads(directory, filename)
    vsebina = read_file_to_string(directory, filename)
    vzorec = re.compile(
    r'<a class="Adlink" href=".*">\n\n<span>(?P<ime>.*)</span>\n\n</a>.*?'
    r'<li>Letnik 1.registracije:(?P<letnik>\d*)</li>(\n){2}\s*?<li>(?P<kilometrina>.*)?</li><li>(?P<motor>.*)</li><li>(?P<menjalnik>.*)</li>.*?'
    r'EUR=(?P<cena>\d*)',
    re.DOTALL
    )
    for oglas in seznam_oglasov:
        for ujemanje in vzorec.finditer(oglas):
                podatki_oglasov.append(izloci_podatke_oglasa_BOLJSE(ujemanje))
    return podatki_oglasov





def pridobi_ceno(directory, filename):
    cene = []
    vsebina = read_file_to_string(directory, filename)
    vzorec = re.compile(
    r'<!------------ REDNA OBJAVA CENE ------------>\s*'
    r'(?P<cena>.*)\s*'
    r'<!------------ KOMENTAR CENE ----------->',
    re.DOTALL
    )
    for ujemanje in vzorec.finditer(vsebina):
        cene.append(ujemanje.groupdict())
    return cene




def ads_from_file(directory, filename):
    slovar_oglasov = get_dict_from_ad_block(directory, filename)
    return slovar_oglasov

def ads_from_file_BOLJSE(directory, filename):
    slovar = get_dict_from_ad_block_BOLJSE(directory, filename)
    return slovar



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
   



def zapisi_csv(slovarji, imena_polj, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'a', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)
    print('Napisal sem csv!')

def zapisi_csv_brez_headerja(slovarji, imena_polj, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'a', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        for slovar in slovarji:
            writer.writerow(slovar)

def zapisi_json(slovarji, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'a', encoding='utf-8') as json_datoteka:
        json.dump(slovarji, json_datoteka, indent=5, ensure_ascii=False)
    print('napisal sem json file!')



def naredi_vse_csv(url, directory_glavni, directory_dnevni, filename_glavni_csv, filename_dnevni_html, filename_dnevni_csv):
    save_frontpage(url, directory_dnevni, filename_dnevni_html) #naredimo HTML datoteko za danasnji dan

    slovar = get_dict_from_ad_block_BOLJSE(directory_dnevni, filename_dnevni_html)
    zapisi_csv_brez_headerja(slovar, imena_stolpcev, directory_glavni, filename_glavni_csv)
    zapisi_csv(slovar, imena_stolpcev, directory_dnevni, filename_dnevni_csv)

MODELI = izlusci_modele(directory_mapa, 'search_stran.html')
MODELI_BOLJSE = modeli_znamk(directory_mapa, 'search_stran.html')


