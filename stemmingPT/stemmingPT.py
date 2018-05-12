#!/usr/bin/env python
# -*- Coding: UTF-8 -*-

__author = 'Eduardo S. Pereira'
__data = '17/01/2017'

'''
Portuguese Stemming Algorithm based  in the description in the site:
http://snowball.tartarus.org/algorithms/portuguese/stemmer.html
'''

import string
import re
from unicodedata import normalize

import os
#_locFiles = os.getcwd() + '/applications/init/private/extraSteaming/'
_locFiles = './dataModel/'


def remover_acentos(txt, codif='utf-8-sig'):
    return normalize('NFKD', txt.decode(codif)).encode('ascii', 'ignore')

pt_stopwords = None
suffix_01 = None
vowel = None

suffix_02 = None


conso = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm'
         'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

with open(_locFiles + 'stopWord_PT.txt', 'r') as txt:
    pt_s = list(txt.readlines())
    pt_s += [remover_acentos(pi) for pi in pt_s]
    pt_s = list(set(pt_s))
    pt_stopwords = [li.replace('\n', '') for li in pt_s]

with open(_locFiles + 'vowels.txt', 'r') as txt:
    vowel = [li.replace('\n', '') for li in list(txt.readlines())]

with open(_locFiles + "suffix_01.txt", 'r') as sfx:
    suffix_01 = [li.replace('\n', '') for li in list(sfx.readlines())]

with open(_locFiles + "suffix_02.txt", 'r') as sfx:
    suffix_02 = [li.replace('\n', '') for li in list(sfx.readlines())]


def regR1(text, t1=True):
    '''R1 is the region after the first non-vowel following a vowel,
    or is the null region at the end of the word if there is no such non-vowel.
    R2 is the region after the first non-vowel following a vowel in R1,
     or is the null region at the end of the word if there is no such non-vowel.
    '''
    r1 = None
    t = 1
    for ti in text[1:]:
        if(ti not in vowel):
            if(t + 1 < len(text)):
                if(text[t + 1] in vowel):
                    if(t1):
                        t += 1
                    r1 = text[t:]
                    break
        t += 1

    return r1


def regR2(text):
    r1 = regR1(text)
    if(r1 is None):
        return None
    return regR1(r1)


def regRV(text):
    rv = None
    if(len(text) > 3):
        if(text[1] not in vowel):
            return regR1(text[1:], t1=False)
        if(text[0] in vowel and text[1] in vowel):
            return regR1(text[1:])

        if(text[0] not in vowel and text[1] in vowel):
            return text[3:]

    return rv


def suffixRemoval(text):
    if text in pt_stopwords:
        return None
    text = cleanText(text)
    if(len(text) == 0):
        return None

    if('-' in text):
        if(text.split('-')[1] in ['lha', 'lhas', 'lhe', 'lhes', 'lho',  'lhos',
                                  'se', 'le', 'la', 'las', 'lo', 'los', 'os',
                                  'no', 'nos',  'a', 'as', 'o', 'os', 'te',
                                  'me', 'mi']):
            text = text.split('-')[0]

    txt = _suffixRemoval(text)
    if(txt is not None):
        if(len(txt) >= 3):
            return replaceTwoOrMore(remover_acentos(txt))
    if(len(text) >= 3):
        return replaceTwoOrMore(remover_acentos(text))
    return None


def _suffixRemoval(text):

    r2 = regR2(text)
    r1 = regR1(text)
    if(r2 is not None):
        if(r2 in suffix_01):
            return text[0:len(text) - len(r2)]

        #
        if('log\xc3\xadas' in r2):
            return text.replace('log\xc3\xadas', 'log')
        if('log\xc3\xada' in r2):
            return text.replace('log\xc3\xada', 'log')

        #
        if('uciones' in r2):
            return text.replace('uciones', 'u')
        if('uci\xc3\xb3n' in r2):
            return text.replace('uci\xc3\xb3n', 'u')

        #
        if('\xc3\xaancias' in r2):
            text.replace('\xc3\xaancias', 'ente')
        if('\xc3\xaancia' in r2):
            text.replace('\xc3\xaancias', 'ente')
        #
        if('amente' in r2):
            tmp = text[:text.find('amente')][-2:]
            if(tmp == 'iv'
               or
               tmp == 'at'
               or
               tmp == 'os'
               or
               tmp == 'ic'
               or
               tmp == 'ad'
               ):
                return text.replace('amente', '')
        #
        if('mente' in r2):
            return text.replace('mente', '')

        #
        if('idades' in r2):
            return text.replace("idades", '')
        if('idade' in r2):
            return text.replace('idade', '')

        if('iva' in r2):
            return text.replace('iva', '')
        if('ivo' in r2):
            return text.replace('ivo', '')
        if('ivas' in r2):
            return text.replace('ivas', '')
        if('ivos' in r2):
            return text.replace('ivos', '')

    if(r1 is not None):
        if('amente' in r1):
            return text.replace('amente', '')

    rv = regRV(text)
    if(rv is not None):
        if(rv in suffix_02):
            return text[0:len(text) - len(rv)]
        if('ci' in rv[-2:]):
            return text[0:-1]

        if('os' in rv[-2:]):
            return text[0:-2]

        if(rv[-1] in ['a', 'i', 'o', '\xc3\xa1',
                      '\xc3\xad', '\xc3\xb3']):
            return text[0:-1]

        if(rv[-1] in ['e', '\xc3\xa9', '\xc3\xaa']):
            if(text[-3:-1] == 'gu' or text[-3:-1] == 'ci'):
                return text[0:-2]
            return text[0:-1]

        if('ou' in rv[-2:]):
            return text[0:-2]
        if('eu' in rv[-2:]):
            return text[0:-2]
        if('iu' in rv[-2:]):
            return text[0:-2]

    return None


def replaceTwoOrMore(s):
    # Retirar caracter repetido

    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    r = pattern.sub(r"\1\1", s)
    stripped = (c for c in r if 32 < ord(c) < 165)
    return ''.join(stripped)


def cleanText(text):

    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', ' ', text)

    # Tag html
    text = re.sub('<[^>]+>', ' ', text)

    # Remove Number
    text = re.sub(r'(?:(?:\d+,?)+(?:\.?\d+)?)', ' ', text)

    text = re.sub('@[^\s]+', ' ', text)
    text = re.sub('[\s]+', ' ', text)
    text = re.sub(r'#([^\s]+)', r'\1', text)
    remove = string.punctuation
    remove = remove.replace("-", "")  # don't remove hyphens
    pattern = r"[{}]".format(remove)  # create the pattern
    text = re.sub(pattern, "", text)
    return text

if(__name__ == "__main__"):
    print suffixRemoval('oceanolog\xc3\xada'), regR2('ess\xc3\xaancia'), regRV('trabajo')
    print regRV('aureo'), regRV('macho'), regRV('oliva'), suffixRemoval('confian\xc3\xa7a')
    print suffixRemoval('cart\xc3\xb3rio')

    with open('./dataModel/test.txt', 'r') as txt:
        text = ' '.join(list(txt.readlines())).lower().replace('\n', ' ')
        text = text.split('.')
        text = [txt.split(' ') for txt in text]
        func = lambda txt: [i for i in map(suffixRemoval, txt) if i != None]

        a = map(func, text)
        for ai in a:
            print ai
