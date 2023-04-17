import os

import requests
import json
from abc import ABC, abstractmethod


class AbReq(ABC):

    @abstractmethod
    def api_work(self):
        pass

    @abstractmethod
    def to_file(self):
        pass


class HH(AbReq):

    def __init__(self):
        self.user_input = None
        self.response_json = None

    def api_work(self, user_input):
        response = requests.get('https://api.hh.ru/vacancies', params={'text': user_input, 'page': 1,
                                                                       'per_page': 20})
        self.response_json = response.json()
        print(self.response_json)
        return self.response_json

    def get_vacancies(self, user_input, page_number=0):
        print(f'Страница: {page_number}')
        #resp_list = []
        #for reqs in range(0, 1):
            #page = 1
        response = requests.get('https://api.hh.ru/vacancies', params={'text': user_input, 'page': page_number,
                                                                     'per_page': 100})
        self.response_json = response.json()
            #resp_list.append(response.json())
           # page += 1
        #self.response_json = resp_list
        for i in self.response_json['items']:
            if i['salary'] is None:
                try:
                    if i['address']['city'] is None:
                        print(f"{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}")
                    else:
                        print(f"{i['name']}, оплата не указана, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}")
                except TypeError:
                    print(f"{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}")
            elif i['salary']['from'] is None:
                try:
                    if i['address']['city'] is None:
                        print(f"{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}")
                    else:
                        print(f"{i['name']}, оплата: {i['salary']['to']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}")
                except TypeError:
                    print(f"{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}")
            elif i['salary']['to'] is None:
                try:
                    if i['address']['city'] is None:
                        print(f"{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}")
                    else:
                        print(f"{i['name']}, оплата: {i['salary']['from']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}")
                except TypeError:
                    print(f"{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}")
            else:
                try:
                    if i['address']['city'] is None:
                        print(f"{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}")
                    else:
                        print(f"{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город: {i['address']['city']}, ссылка на вакансию: {i['alternate_url']}")
                except TypeError:
                    print(f"{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}")
        #print(len(resp_list))
        #print(len(self.response_json))

    def to_file(self):
        pass


class Superjobs(AbReq):

    def __init__(self, user_input):
        self.user_input = user_input

    def api_work(self):
        headers = {"X-Api-App-Id": os.getenv('SJ_API')}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers,
                                params={'text': self.user_input, 'page': 0, 'per_page': 100})
        response_json = response.json()
        print(response_json)

    def to_file(self):
        pass



hh = HH()
hh.api_work('повар')
hh.get_vacancies('повар', 10)
#sj = Superjobs('аа')
#sj.api_work()