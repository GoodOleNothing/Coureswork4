import requests
import json
import abc

#header = {'User-Agent': 'MyApp'}
word = 'таксист'
gg = requests.get('https://api.hh.ru/vacancies', params={'text': word, 'page': 0, 'per_page': 100})
ggg = gg.content.decode()
#print(json.loads(ggg))
print(gg)
#ggg = gg.json()
print(ggg)



