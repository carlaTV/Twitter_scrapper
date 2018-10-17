#!/usr/bin/env pythontext = '🚨IMÁGENES DE LA ALARMA DE INCENDIO EN AVENIDA NUEVA ORIENTE 1055 FRENTE AL SUPERMERCADO UNO🚨 @Jzg1985 @LuisRivas_440 @FR_256 @Amigos_Informa @radioisadorafm @FabricianoGonz1 @delafu344 https://t.co/zhjmo5Sml6'

# -*- coding: utf-8 -*-

from TwitterSearch import *
import json

def writeOpening():
    with open('../Output_files/retrieved_tweets_italy.json', 'w') as fd:
        fd.write("{\n")
        fd.write("\t\"tweets\": [\n")

def writeEnding():
    with open('../Output_files/retrieved_tweets_italy.json','a') as fd:
        fd.write("}\n")
    fd.close()

def writeJson_geolocated(output):
    with open('../Output_files/retrieved_tweets_italy.json', 'a') as fd:
        username, text, place = output
        fd.write("\t\t{\n\n")
        fd.write("\t\t\t\"username\" : \" %s \",\n" %username)
        fd.write("\t\t\t\"profile_geolocation\" : \"None\", \n")
        fd.write("\t\t\t\"text\" : \" %s \",\n" %text)
        fd.write("\t\t\t\"twit_geolocation\" : \" %s \"\n" % place)
        fd.write("\t\t},\n")

def writeJson_NOgeolocated(output):
    with open('../Output_files/retrieved_tweets_italy.json', 'a') as fd:
        username, location_profile, text = output
        # fd.write("\"tweets:\" [ { \n")
        fd.write("\t\t{\n\n")
        fd.write("\t\t\t\"username\" : \" %s \",\n" %username)
        fd.write("\t\t\t\"profile_geolocation\" : \" %s \",\n" %location_profile)
        fd.write("\t\t\t\"text\" : \" %s \",\n" %text)
        fd.write("\t\t\t\"twit_geolocation\" : \" None \"\n")
        fd.write("\t\t},\n")

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['inondazione','fuoco','valanga','incendi'],True) #True enables keyword OR keyword. default is False, which is AND
    tso.set_language('it')
    tso.set_include_entities(True)
    tso.arguments.update({'tweet_mode': 'extended'})
    tso.arguments.update({'retweet_mode': 'extended'})

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(consumer_key='**',
        consumer_secret='**',
        access_token='**-**',
        access_token_secret='**')
    i = 0
    writeOpening()
    for tweet in ts.search_tweets_iterable(tso):

        place = tweet['place']
        profile = tweet['user']
        loc_profile = profile['location']


        # if not tweet['full_text'].startswith('RT'):

        if place:
            if place[u'country'] == 'Italy' or place[u'country'] == 'Italia'.decode('utf8'):
                if tweet[u'full_text'].startswith('RT'):
                    output_json = (tweet['user']['screen_name'].encode('utf8'), '\'RT\' '+ tweet[u'retweeted_status'][u'full_text'].encode('utf8'), place[u'full_name'].encode('utf8'))
                    writeJson_geolocated(output_json)
                else:
                    output_json = (tweet['user']['screen_name'].encode('utf8'), tweet['full_text'].encode('utf8'), place[u'full_name'].encode('utf8'))
                    writeJson_geolocated(output_json)



                if loc_profile is not None and "Italia".decode('utf8') in loc_profile or "Italy" in loc_profile:
                    if tweet[u'full_text'].startswith('RT'):
                        output_json = (tweet['user']['screen_name'].encode('utf8'), loc_profile.encode('utf8'), '\'RT\' '+tweet[u'retweeted_status'][u'full_text'].encode('utf8'))
                        writeJson_NOgeolocated(output_json)

                    else:
                        output_json = (tweet['user']['screen_name'].encode('utf8'), loc_profile.encode('utf8'), tweet['full_text'].encode('utf8'))
                        writeJson_NOgeolocated(output_json)
        else:
            if loc_profile is not None:
                if "Italia".decode('utf8') in loc_profile or "Italy" in loc_profile:
                    if tweet[u'full_text'].startswith('RT'):
                        output_json = (tweet['user']['screen_name'].encode('utf8'), loc_profile.encode('utf8') ,'\'RT\' '+tweet[u'retweeted_status'][u'full_text'].encode('utf8'))
                        # print output_json
                        writeJson_NOgeolocated(output_json)
                    else:
                        output_json = (tweet['user']['screen_name'].encode('utf8'), loc_profile.encode('utf8'),tweet['full_text'].encode('utf8'))
                        writeJson_NOgeolocated(output_json)

    writeEnding()

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)