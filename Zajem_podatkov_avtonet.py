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
now = datetime.datetime.now()

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
    with open(path, 'w', encoding="windows-1250") as file_out:
        file_out.write(text)
    return None



def save_frontpage(url, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    vsebina = download_url_to_string(url)
    with open(path, 'w', encoding='windows-1250') as datoteka:
        datoteka.write(vsebina)
    print('shranjeno!')



def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, encoding='windows-1250') as datoteka:
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










def izloci_podatke_oglasa(ujemanje_oglasa):
    
    podatki_oglasa = ujemanje_oglasa.groupdict()
    podatki_oglasa['cas'] = (now.day, now.month)
    return podatki_oglasa






def get_dict_from_ad_block(directory, filename):
    podatki_oglasov = []
    '''Build a dictionary containing the name, description and price
    of an ad block.'''
    seznam_oglasov = page_to_ads(directory, filename)
    vsebina = read_file_to_string(directory, filename)
    vzorec = re.compile(
    r'<a class="Adlink" href=".*">\n\n<span>(?P<ime>.*)</span>\n\n</a>.*?'
    r'<li>Letnik 1.registracije:(?P<letnik>\d*)</li>(\n){2}\s*?<li>(?P<kilometrina>.*)?</li><li>(?P<motor>.*)</li><li>(?P<menjalnik>.*)</li>.*?',
    re.DOTALL
    )
    for oglas in seznam_oglasov:
        for ujemanje in vzorec.finditer(oglas):
                podatki_oglasov.append(izloci_podatke_oglasa(ujemanje))
    return podatki_oglasov


# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def ads_from_file(directory, filename):
    slovar_oglasov = get_dict_from_ad_block(directory, filename)
    '''Parse the ads in filename/directory into a dictionary list.'''
    return slovar_oglasov


"""def write_csv(fieldnames, rows, directory, filename):
    '''Write a CSV file to directory/filename. The fieldnames must be a list of
    strings, the rows a list of dictionaries each mapping a fieldname to a
    cell-value.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return print('napisal sem csv!')"""

def zapisi_csv(slovarji, imena_polj, directory, filename):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)
    print('Napisal sem csv!')


def zapisi_json(slovarji, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as json_datoteka:
        json.dump(slovarji, json_datoteka, indent=5, ensure_ascii=False)

