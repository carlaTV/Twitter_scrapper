#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geopy.geocoders import Nominatim
import re
import spacy
import json


def credentials():
    with open('/home/carlatv/PycharmProjects/Twitter_scrapper/credentials','r') as f:
        content = json.load(f)
        consumer_key = content['credentials']['consumer_key']
        consumer_secret = content['credentials']['consumer_secret']
        access_token = content['credentials']['consumer_secret']
        access_token_secret = content['credentials']['consumer_secret']
        if '*' in consumer_key:
            print 'Put your Twitter developer credentials in the file \'credentials\'. You can find them at https://apps.twitter.com/'
        else:
            consumer_key = '\''+consumer_key+'\''
            consumer_secret = '\''+consumer_secret+'\''
            access_token = '\''+access_token+'\'',
            access_token_secret = '\''+access_token_secret+'\''
            print consumer_key,consumer_secret,access_token,access_token_secret


credentials()