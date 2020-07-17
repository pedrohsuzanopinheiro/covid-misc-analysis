from datetime import datetime, timedelta
from time import sleep

from pandas import DataFrame
import requests

# limitação: 1 req/segundo e 50k reqs/mês
# início do covid nos eua: 21/01/2020

# data limite api mobilidade: 11/04/2020
# range: jan ~ abr

colunas = ['date', 'country', 'province', 'confirmed', 'recovered', 'deaths', 'active']
df = DataFrame(columns=colunas)

url = "https://covid-19-data.p.rapidapi.com/report/country/code"

headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "API_CREDENTIAL"
    }

start_date = datetime.strptime('22/01/2020', '%d/%m/%Y')
end_date = datetime.strptime('30/04/2020', '%d/%m/%Y')


def organize_data(json_response):
    for data in json_response:
        date = data['date']
        country = data['country']
        for province in data['provinces']:
            df.loc[len(df)] = [
                date,
                country,
                province['province'],
                province['confirmed'],
                province['recovered'],
                province['deaths'],
                province['active']
            ]


while start_date <= end_date:
    querystring = {"format":"json","date-format":"YYYY-MM-DD","date":str(start_date.date()),"code":"US"}
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    organize_data(response)
    sleep(1.5) # Tive problemas ao consumir a API a cada segundo. Acusava erro de exceção do limite.
    start_date += timedelta(days=1)

df.to_excel(excel_writer=r'data/covid_raw_data.xlsx', sheet_name='raw_data', index=False)
