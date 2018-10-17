#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geopy.geocoders import Nominatim
import re
import spacy

def findWholeWord(w):
    return re.compile(r'\b({0})\b\n'.format(w), flags=re.IGNORECASE).search

text = 'EN AVENIDA DE NUEVA ORIENTE 1055 FRENTE A'
nlp = spacy.load('en')
geolocator = Nominatim(user_agent="twitter_scrapper")

location = geolocator.geocode('Zuera'.decode('utf8'))

print location.address.encode('utf8')