import requests
import re
import os
import csv

top_100_spletna_stran = 'https://www.avto.net/Ads/results_100.asp?oglasrubrika=1&prodajalec=2'
directory_mapa = 'Projetka_naloga_Programiranje_1'
podatki_html = 'podatki.html'
podatki_csv = 'podatki.csv'

def download_url_to_string(url):
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja!')
        return ''
    return r.text


def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None



def save_frontpage(url, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as datoteka:
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
            r'<div class="ad.*?">'
            r'.*?'
            r'<div class="clear"></div>'
            )
    for ujemanje in re.finditer(vzorec, vsebina, re.DOTALL):
        nas_oglas = ujemanje.group(0)
        seznam_oglasov.append(nas_oglas)
    return seznam_oglasov


vzorec = re.compile(
    r'<table><tr><td><a title=(?P<ime>.*?) href=.*?'
    r'</a></h3>(?P<opis>.*?) <div class="additionalInfo">.*?'
    r'<div class="price">(?P<cena>.*?)</div>.*?',
    re.DOTALL
)



def izloci_podatke_oglasa(ujemanje_oglasa):
    podatki_oglasa = ujemanje_oglasa.groupdict()
    podatki_oglasa['opis'] = podatki_oglasa['opis'].strip()
    podatki_oglasa['ime'] = podatki_oglasa['ime'].strip()
    podatki_oglasa['ime'] = podatki_oglasa['ime'].strip('</span>')
    return podatki_oglasa

podatki_oglasov = []


def get_dict_from_ad_block(directory, filename):
    '''Build a dictionary containing the name, description and price
    of an ad block.'''
    seznam_oglasov = page_to_ads(directory, filename)
    izlusceno = izloci_podatke_oglasa(seznam_oglasov)
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
