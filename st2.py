#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spacy

nlp = spacy.load('en')
doc = nlp(u'hemos ido a Copenhaghe')

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)
    if token.is_stop:
        print token