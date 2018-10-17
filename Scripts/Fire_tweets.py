#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from TwitterSearch import *
import json
import datetime
import re
import spacy
import emoji
from geopy.geocoders import Nominatim

now = datetime.datetime.now()
if now.day < 10:
    day = str('0')+str(now.day)
else:
    day = str(now.day)
timestamp = str(now.year)+str(now.month)+day+'_'+str(now.hour)+str(now.minute)
filename = '../Output_files/retrieved_tweets_spain_'+timestamp+'.json'
nlp = spacy.load('es')
geolocator = Nominatim(user_agent="twitter_scrapper")

def findWholeWord(w):
    return re.compile(r'\b({0})\b\n'.format(w), flags=re.IGNORECASE).search

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def placeInSpain(place,geolocator):
    place_in_spain = False
    location = geolocator.geocode(place)
    if 'España'.decode('utf8') in location.address.encode('utf8'):
        place_in_spain = True
    return place_in_spain

def findPlace(text,nlp):
    inSpain = False
    with open('/home/carlatv/PycharmProjects/TwitterSearch/places','r') as f:
        place = f.read()
        place = place.decode('utf8')
        doc = nlp(text)
        for token in doc:
            if token.pos_ == 'PROPN' or 'NOUN':
                found = findWholeWord(token)(place)
                if found is not None:
                    inSpain = True
                    break
    return inSpain

def findStreet(text,nlp,geolocator):
    street_found = False
    street_name = ''
    inSpain = False
    with open('/home/carlatv/PycharmProjects/TwitterSearch/vias', 'r') as f:
        place = f.read()
        place = place.decode('utf8')
        doc = nlp(text.decode('utf8'))
        for token in doc:
            found = findWholeWord(token)(place)
            if found:
                street_found = True
            if street_found and token.pos_ == 'PROPN' or 'NOUN':
                street_name += str(token)+' '
            else:
                street_found = False
    location = geolocator.geocode(street_name)
    if 'España'.decode('utf8') in location.address.encode('utf8'):
        inSpain = True
    return inSpain


def split_hashtag(hashtag):
 fo = re.compile(r'#[A-Z]{2,}(?![a-z])|[A-Z][a-z]+')
 fi = fo.findall(hashtag)
 result = ''
 for var in fi:
     result += var + ' '
 print (result)


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
            ts = TwitterSearch(consumer_key = '\''+consumer_key+'\'',
            consumer_secret = '\''+consumer_secret+'\'',
            access_token = '\''+access_token+'\'',
            access_token_secret = '\''+access_token_secret+'\'')
            return ts


def writeOpening():
    with open(filename, 'w') as fd:
        fd.write("{\n")
        fd.write("\t\"tweets\": [\n")

def writeEnding():
    with open(filename,'a') as fd:
        fd.write("\t]\n")
        fd.write("}\n")
    fd.close()

def writeMiddle(username,place_profile,text, place_tweet,RT):
    with open(filename, 'a') as fd:
        fd.write("\t\t{\n\n")
        fd.write("\t\t\t\"username\" : \" %s \",\n" %username)
        fd.write("\t\t\t\"profile_geolocation\" : \"%s\", \n" %place_profile)
        fd.write("\t\t\t\"text\" : \" %s \",\n" %text.encode('utf8'))
        fd.write("\t\t\t\"tweet_geolocation\" : \" %s \",\n" % place_tweet)
        fd.write("\t\t\t\"RT\" : \" %s \",\n" % RT)
        fd.write("\t\t\t\"Tag\" : \" \"\n")
        fd.write("\t\t},\n")


try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['incendio'],True) #True enables keyword OR keyword. default is False, which is AND
    tso.set_language('es')
    tso.set_include_entities(True)
    tso.arguments.update({'tweet_mode': 'extended'})

    # it's about time to create a TwitterSearch object with our secret tokens

    ts = credentials()
    i = 0
    writeOpening()
    for tweet in ts.search_tweets_iterable(tso):
        text = tweet[u'full_text'].encode('utf8')
        text = 'en la calle Marina llueve mucho'
        try:
            place_tweet = tweet['place'].encode('utf8')
            if place_tweet:
                inSpain = placeInSpain(place_tweet,geolocator)
        except:
            inSpain = findPlace(text,nlp)
            if inSpain is False:
                inSpain = findStreet(text,nlp,geolocator)

        if inSpain:
            user = tweet['user']
            username = user['screen_name'].encode('utf8')
            place_profile = user['location'].encode('utf8')
            text = text.decode('utf8')
            RT = "no"

            if i < 5:
                print text
                if '#' in text:
                    text = split_hashtag(text)
                inSpain = findPlace(remove_emoji(text),nlp)
                print inSpain
            if text.startswith('RT'):
                RT = "yes"
                try:
                    text = tweet[u'retweeted_status'][u'full_text'].encode('utf8')
                except:
                    text = tweet['full_text'].encode('utf8')
            # if '"' in text:
            #     text = str(text).replace('"', '\\"')
            # if '\n' in text:
            #     text = str(text).replace('\n','')
            writeMiddle(user,place_profile,text,place_tweet,RT)

            i += 1


    writeEnding()

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)