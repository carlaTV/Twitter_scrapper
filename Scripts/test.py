# -*- coding: utf-8 -*-

from geopy.geocoders import Nominatim
import re
import spacy

def findWholeWord(w):
    return re.compile(r'\b({0})\b\n'.format(w), flags=re.IGNORECASE).search

nlp = spacy.load('es')
geolocator = Nominatim(user_agent="twitter_scrapper")
street_name = 'En la calle Marina llueve mucho'
doc = nlp(street_name.decode('utf8'))
for token in doc:
    print token
    print token.pos_
#
# location = geolocator.geocode(street_name)
# print location.address
#
# def findPlace(text,nlp):
#     inSpain = False
#     with open('/home/carlatv/PycharmProjects/TwitterSearch/places','r') as f:
#         place = f.read()
#         place = place.decode('utf8')
#         doc = nlp(text.decode('utf8'))
#         for token in doc:
#             if token.pos_ == 'PROPN':
#                 found = findWholeWord(token)(place)
#                 if found is not None:
#                     inSpain = True
#     return inSpain
#
#
# def findStreet(text,nlp,geolocator):
#     street_found = False
#     street_name = ''
#     inSpain = False
#     with open('/home/carlatv/PycharmProjects/TwitterSearch/vias', 'r') as f:
#         place = f.read()
#         place = place.decode('utf8')
#         doc = nlp(text.decode('utf8'))
#         for token in doc:
#             found = findWholeWord(token)(place)
#             if found:
#                 street_found = True
#             if street_found and token.pos_ == 'PROPN':
#                 street_name += str(token)+' '
#             else:
#                 street_found = False
#     location = geolocator.geocode(street_name)
#     if 'España' in location.address:
#         inSpain = True
#     return inSpain
#
# inSpain = findPlace(text.encode('utf8'))
# print(inSpain)
# if inSpain is False:
#     inSpain = findStreet(text.decode('utf8'),nlp,geolocator)
#     print(inSpain)