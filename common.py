#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random

import vk

token = '1af01693c57766ded7a0575b61b7fc556e729bdfbd93ea77aa7a14f8199de872c608438f1e43bc3bd4c07'
vksession = vk.Session(access_token=token)
vkapi = vk.API(vksession, v='5.4', lang='ru')
# vkapi.func(**params)

appName='student'

import pandas as pd

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from vkGroupApi import *
import config
from db import DB


def many(user):
    pass


#######################################################
def uservk(user_id, userdb):
    # db = DB()
    # user = db.getUser(user_id)

    vk_url = "https://api.vk.com/method/"
    dom = 'sex, bdate,city, country'
    resp = requests.get(vk_url + 'users.get', '&user_ids={}&fields={}&v=5.53'.format(user_id, dom))
    result = resp.json()

    bdate = result['response'][0]['bdate']
    city = result['response'][0]['city']['title']
    sex = result['response'][0]['sex']
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    bdate = bdate.split('.')
    bdate = 2016-int(bdate[2])

    df2 = pd.DataFrame([[user_id, city, bdate, sex]], columns=['user_id', 'city', 'age', 'sex'])


    return  df2



def stripRead(read):
    # очищаем текст пользователя

    read = read.encode('utf8')
    read = read.decode('utf8').lower()
    read = read.strip('.').strip('!').strip('?').strip('/')

    return read


if __name__ == "__main__":


    # user = pd.DataFrame({
    #     'user_id': 0,
    #     'raiting': 0,
    #     'poruchitel_id': 0,
    #     'city': '',
    #     'age': 0,
    #     'sex': ''
    # }, index=[0])

    df_user = uservk(8438153)

    user = user.append(df_user, ignore_index=True)

    print user


