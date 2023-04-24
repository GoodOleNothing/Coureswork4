import os

import requests
import json
from abc import ABC, abstractmethod


class AbReq(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def to_file(self):
        pass



class HH(AbReq):

    def __init__(self):
        self.response_json = None
        self.counter = 0
        self.reqs = []
        self.results = {}

    #def api_work(self, user_input):
    #    response = requests.get('https://api.hh.ru/vacancies', params={'text': user_input, 'page': 0,
    #                                                                   'per_page': 20})
    #    self.response_json = response.json()
    #    print(self.response_json)
    #    return self.response_json

    def get_vacancies(self, user_input, page_number=0):
        if page_number == 0:
            print(f'Страница: {page_number + 1}')
            page_number = 1
        else:
            print(f'Страница: {page_number}')
        response = requests.get('https://api.hh.ru/vacancies', params={'text': user_input, 'page': page_number - 1,
                                                                     'per_page': 100})
        self.response_json = response.json()
        for i in self.response_json['items']:
            self.counter += 1

            self.reqs.append({self.counter: i['snippet']['requirement']})
            self.reqs.append({self.counter: i['snippet']['responsibility']})
            if i['salary'] is None:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата не указана, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer
            elif i['salary']['from'] is None:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer
            elif i['salary']['to'] is None:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer
            else:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город: {i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer

    def requirements(self, vac_num=1):
        for i in self.reqs:
            if vac_num in i.keys():
                print(i[vac_num])

    #def sort_by_salary(self):
    #    sal = [i['salary']['from'] for i in self.response_json['items']]
    #    print(sal)


    def to_file(self, file_name = 'vacancies'):
        with open(file_name + '.json', 'w', encoding='UTF-8') as file:
            json.dump(self.results, file, indent=2, ensure_ascii=False)

class Superjobs(AbReq):

    def __init__(self ):
        self.response_json = None
        self.counter = 0

    def get_vacancies(self, user_input):
        headers = {"X-Api-App-Id": os.getenv('SJ_API')}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers,
                                params={'keyword': user_input, 'page': 0, 'per_page': 100})
        self.response_json = response.json()
        print(self.response_json)
        for i in self.response_json['objects']:
            #print(i['profession'])
            self.counter += 1

            #self.reqs.append({self.counter: i['snippet']['requirement']})
            #self.reqs.append({self.counter: i['snippet']['responsibility']})
            if i['salary'] is None:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата не указана, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата не указана, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer
            elif i['salary']['from'] is None:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer
            elif i['salary']['to'] is None:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город:{i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer
            else:
                try:
                    if i['address']['city'] is None:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                    else:
                        answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город: {i['address']['city']}, ссылка на вакансию: {i['alternate_url']}"
                        print(answer)
                        self.results[self.counter] = answer
                except TypeError:
                    answer = f"{self.counter}.{i['name']}, оплата: {i['salary']['from']} - {i['salary']['to']}, город не указан, ссылка на вакансию: {i['alternate_url']}"
                    print(answer)
                    self.results[self.counter] = answer

    def to_file(self):
        pass


sj = Superjobs()
sj.get_vacancies('Python')


#hh = HH()
#hh.api_work('рекрутер')
#hh.get_vacancies('рекрутер', 2)
#hh.requirements(1)
#hh.to_file()

#hh.sort_by_salary()
#sj = Superjobs('аа')
#sj.api_work()