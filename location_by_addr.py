import pandas as pd
import requests
import time

dfs = pd.read_excel("tuberculosis.xlsx", sheet_name="tuberculosis")

# provinces_dict = {'Արմավիր': '40.1158531,43.9365414', 'Կոտայք': '40.2803175,44.6545793', 'Երևան': '40.1776121,44.5125849', 'Արագածոտն': '40.479544,44.2949003', 'Շիրակ': '40.8140053,43.8798729', 'Արարատ': '39.9530516,44.8018061', 'Գեղարքունիք': '40.305261,45.4100132', 'Սյունիք': '39.35087,46.1550379', 'Վայոց Ձոր': '39.7538184,45.4236282', 'Տավուշ': '40.9728522,45.1534754'}
#
# def locationig_org(dict):
#     url = 'https://locationiq.org/v1/search.php'
#     params = {'key': '47b931129db812', 'format': 'json', 'countrycodes': 'am', 'addressdetails': 1, 'matchquality': 1}
#     for index, province in provinces.iterrows():
#         if province[province_column_name] in dict:
#             continue
#
#         query = province_column_name + ' ' + province[province_column_name]
#         params['q'] = query
#         response = requests.get (url, params = params).json()
#
#         for place in response:
#             if place['matchquality']['matchlevel'] == 'state':
#                 print(place)
#                 dict[province[province_column_name]] = {place['lat'], place['lon']}
#                 break
#
#         time.sleep(2)

opencagedata_url = 'https://api.opencagedata.com/geocode/v1/json'
def opencagedata_provinces():
    column = 'Մարզ'
    column_frame = pd.DataFrame (dfs, columns=[column])

    params = {'no_annotations': '1', 'language': 'am', 'key': '641c51bed8ab490184632ad8526e29ad'}

    provinces = {}
    for index, province in column_frame.iterrows():
        if province[column] not in provinces:
            if 'Երևան' != province[column]:
                query = province[column] + 'ի ' + column
            else:
                query = province[column]

            params['q'] = query
            response = requests.get (opencagedata_url, params=params).json ()

            for result in response['results']:
                if result['components']['_type'] == 'state' or 'Երևան' == province[column]:
                    print (province[column])
                    print (result['geometry'])
                    provinces[province[column]] = str(result['geometry']['lat']) + "," + str(result['geometry']['lng'])
                    break

            time.sleep (0.01)
    return provinces


def opencagedata_address():
    province_column_name = 'Մարզ'
    address_column_name = 'Հասցե'
    column_frame = pd.DataFrame (dfs, columns=[province_column_name, address_column_name])

    params = {'no_annotations': '1', 'language': 'am', 'key': '641c51bed8ab490184632ad8526e29ad'}

    addresses = {}
    for index, row in column_frame.iterrows():
        if 'Երևան' != row[province_column_name]:
            query = row[province_column_name] + 'ի ' + province_column_name
        else:
            query = row[province_column_name]
        query += ' ' + row[address_column_name]

        params['q'] = query
        response = requests.get (opencagedata_url, params=params).json()

        for result in response['results']:
            print (query)
            print (result['geometry'])
            addresses[index] = str(result['geometry']['lat']) + "," + str(result['geometry']['lng'])
            break

        time.sleep (0.01)
    return addresses


# provinces = opencagedata_provinces()
# print(provinces)
addresses = opencagedata_address()
for index in addresses:
    print (addresses[index])
