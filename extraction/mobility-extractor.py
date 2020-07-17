from pandas import DataFrame
import requests

colunas = ['date', 'country', 'province', 'type', 'change']
df = DataFrame(columns=colunas)


def organize_data(json_response):
    for data in json_response:
        date = data['date'][:10]
        country = data['name']
        for aggregated in data['data']:
            df.loc[len(df)] = [
                date,
                country,
                'TOTAL-AGGREGATED',
                aggregated['type'],
                int(aggregated['change'])
            ]
        for province in data['regions']:
            for province_data in province['data']:
                df.loc[len(df)] = [
                    date,
                    country,
                    province['name'],
                    province_data['type'],
                    int(province_data['change'])
                ]


url = "https://google-mobility-data.p.rapidapi.com/api/data"

querystring = {"name":"UNITED STATES"}

headers = {
    'x-rapidapi-host': "google-mobility-data.p.rapidapi.com",
    'x-rapidapi-key': "API_CREDENTIAL"
    }

response = requests.request("GET", url, headers=headers, params=querystring).json()

organize_data(response)

df.to_excel(excel_writer=r'data/mobility_raw_data.xlsx', sheet_name='raw_data', index=False)
