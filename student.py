#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import requests
import json
import time
import random
import tabulate

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#######################################################

from vkGroupApi import *
import config
from common import *

appName='student'
#
# userdb=pd.DataFrame({
#         'user_id':0,
#         'raiting':0,
#         'poruchitel_id':0,
# 		'city':'',
#         'age':0,
#         'sex':''
#      },index=[0])
#
# trans=pd.DataFrame({
#         'transaction_id':0,
#         'credit_id':0,
#         'poluch_id':0,
#         'summa':0,
#         'days_stop':0,
#         'credit_reiting':0,
#         'cust_reiting':0,
#     },index=[0]).set_index('transaction_id')
#
# credit=pd.DataFrame({
#         'credit_id':0,
#         'sum':0,
#         'procent':0,
#
#     },index=[0]).set_index('credit_id')
#

trans_dict={}
userdb={}


# print tabulate(user, headers='keys', tablefmt='psql')
# print tabulate(trans, headers='keys', tablefmt='psql')
# print tabulate(credit, headers='keys', tablefmt='psql')
#######################################################

######################################################
def uservk(user_id):
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

    df ={}

    df['user_id']=user_id
    df['city']=city
    df['bdate']=bdate
    df['sex']=sex

    return  df



def stripRead(read):
    # очищаем текст пользователя

    read = read.encode('utf8')
    read = read.decode('utf8').lower()
    read = read.strip('.').strip('!').strip('?').strip('/')

    return read

def is_number(var):
    try:
        if var == int(var):
            return True
    except Exception:
        return False

#######################################

print 'Started...'+appName


while True:

    lastMessages = messagesGet(200,appName)

    for row in lastMessages:
        status = 0
        if int(row['read_state']) == 0:

            # очищаем текст пользователя
            read = stripRead(row['body'])
            user_id = row['user_id']
            print 'user_id: ', user_id



            if not (user_id in trans_dict):
                print 'No user in db'

                if read in ['нужны деньги','да','кредит','хочу кредит']:
                    print 'OK Money'
                    df2 = uservk(row['user_id'])

                    data = {
                        user_id : df2
                    }
                    userdb.update(data)

                    data = {
                        user_id : {
                            'poluch_id':user_id
                        }
                    }
                    trans_dict.update(data)

                    messagesSend(row['user_id'], row['id'], 'Нужен кредит, сколько рублей?', appName=appName)

            else:

                if not 'summa' in trans_dict[user_id]:
                    print 'send how many'

                    read = int(read)

                    if read:

                        print 'Get Summ', read

                        if read>1000:

                            messagesSend(row['user_id'], row['id'], 'Сумма должна быть не больше 1000 руб', appName=appName)

                        else:

                            data = {
                                user_id: {
                                    'poluch_id': user_id,
                                    'summa': read
                                }
                            }
                            trans_dict.update(data)

                            messagesSend(row['user_id'], row['id'], 'Окей, когда отдашь?', appName=appName)

                    else:

                        messagesSend(row['user_id'], row['id'], 'Я не понял сумму...'+str(read), appName=appName)



                elif not 'days_stop' in trans_dict[user_id]:

                    if read:

                        data = {
                            user_id: {
                                'poluch_id': user_id,
                                'summa': trans_dict[user_id]['summa'],
                                'days_stop': read
                            }
                        }
                        trans_dict.update(data)

                        messagesSend(row['user_id'], row['id'], 'Окей, мы подбираем для Вас кредитора...', appName=appName)

                        time.sleep(2)

                        if 'bdate' in userdb[user_id]:
                            if userdb[user_id]['bdate'] > 18:
                                messagesSend(row['user_id'], row['id'], 'Кредит одобрен, под 30%. Кредитор vk.com/id182011714',
                                             appName=appName)

                                time.sleep(1)

                                messagesSend(row['user_id'], row['id'], 'Оцените кредитора после сделки от 1 до 5',
                                             appName=appName)
                            elif userdb[user_id]['bdate'] > 25:
                                messagesSend(row['user_id'], row['id'], 'Кредит одобрен, под 20%. Кредитор vk.com/id182011714 ',
                                             appName=appName)

                                time.sleep(1)
                                messagesSend(row['user_id'], row['id'], 'Оцените кредитора после сделки от 1 до 5',
                                             appName=appName)
                            else:
                                messagesSend(row['user_id'], row['id'], 'Кредит не одобряем, т.к. вам меньше 18 лет ',
                                             appName=appName)

                elif not 'credit_reiting' in trans_dict[user_id]:

                    if int(read)>0:

                        data = {
                            user_id: {
                                'poluch_id': user_id,
                                'summa': trans_dict[user_id]['summa'],
                                'days_stop': trans_dict[user_id]['days_stop'],
                                'credit_reiting': read
                            }
                        }
                        trans_dict.update(data)

                        messagesSend(row['user_id'], row['id'], 'Оценка установлена!', appName=appName)

                else:

                    messagesSend(row['user_id'], row['id'], 'Не понял команды... нужны деньги? (да)',
                                 appName=appName)

    print('-------------------------------------------------------------')
    print (trans_dict)
    print (userdb)


    time.sleep(5)
