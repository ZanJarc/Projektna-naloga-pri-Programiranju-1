# Projektna naloga pri Programiranju 1
To bo moja projektna naloga pri predmetu Programiranje 1 v študijskem letu 2018/2019.

## S strani avto.net bom skoraj vsak dan shranil podatke iz rubrike Top100.
S tem bom dobil v nekaj tednih dokaj reprezentativen vzorec prodaje avtomobilov v Sloveniji.
https://www.avto.net

Zajel bom naslednje podatke:
- ime 
- model
- letnik 1. registracije
- prevozeni kilometri
- vrsta motorja
- prostornina motorja
- menjalnik'
- cena
- datum pridobitbe podatkov

S tem bom želel ugotoviti naslednje stvari:
-kakšen tip avtomobila se največkrat prodaja
-sprememba cene skozi cas

Proti koncu zadnjega oddajnega roka bom s strani avto.net vzel se 1000 oglasov in jih analiziral podobno kot bom analiziral podatke,
ki jih bom dopolnjeval vsak dan.

V mapi 'Mapa s podatki' se nahaja glavna .csv datoteka, 'avtomobili.csv'. Tukaj so shranjeni vsi zajemi. Mapa vsebuje se 'search stran', s pomočjo katere sem lahko naredil slovar znamk in modelov.

V mapi 'Dnevni podatki' pa se nahajajo podatki za vsak dan zajema posebej. Npr. datoteka 'CSV 5. 11' vsebuje csv podatke za dan 5. 11., medtem ko datoteka 'HTML 5. 11' shranjena stran zajema za dan 5. 11.

Datoteka 'zajem_podatkov_avtonet' pa je python datoteka, s katero sem s spletne strani uspel pridobiti in zapisati podatke.
Datoteka 'Analiza.ipynb' vsebuje lglavno poročilo.
