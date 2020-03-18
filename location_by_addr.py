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
opencagedata_params = {'no_annotations': '1', 'language': 'am', 'key': '641c51bed8ab490184632ad8526e29ad'}
def opencagedata_provinces():
    column = 'Մարզ'
    column_frame = pd.DataFrame (dfs, columns=[column])

    tmp = {}
    addresses = {}
    for index, province in column_frame.iterrows():
        if province[column] not in tmp:
            if 'Երևան' != province[column]:
                query = province[column] + 'ի ' + column
            else:
                query = province[column]

            opencagedata_params['q'] = query
            response = requests.get (opencagedata_url, params=opencagedata_params).json ()

            if query not in tmp:
                for result in response['results']:
                    if result['components']['_type'] == 'state' or 'Երևան' == province[column]:
                        tmp[province[column]] = str(result['geometry']['lat']) + "," + str(result['geometry']['lng'])
                        addresses[index] = str(result['geometry']['lat']) + "," + str (result['geometry']['lng'])
                        break
            else:
                addresses[index] = "not_found"

            print (index, addresses[index])

            time.sleep (0.01)
    return addresses


def opencagedata_address():
    province_column_name = 'Մարզ'
    address_column_name = 'Հասցե'
    column_frame = pd.DataFrame (dfs, columns=[province_column_name, address_column_name])

    addresses = {}
    for index, row in column_frame.iterrows():
        if 'Երևան' != row[province_column_name]:
            query = row[province_column_name] + 'ի ' + province_column_name
        else:
            query = row[province_column_name]
        query += ' ' + row[address_column_name]

        opencagedata_params['q'] = query
        response = requests.get (opencagedata_url, params=opencagedata_params).json()

        if response['total_results'] > 0:
            for result in response['results']:
                print (query)
                print (result['geometry'])
                addresses[index] = str(result['geometry']['lat']) + "," + str(result['geometry']['lng'])
                break
        else:
            addresses[index] = "not_found"

        time.sleep (0.01)
    return addresses

def opencagedata_province_city():
    teghakayum_column_name = 'Տեղակայում'
    address_column_name = 'Հասցե'
    column_frame = pd.DataFrame (dfs, columns=[teghakayum_column_name, address_column_name])

    tmp = {}
    addresses = {}
    for index, row in column_frame.iterrows():
        if (len(row[teghakayum_column_name].split()) > 1):
            query = row[teghakayum_column_name]
        else:
            query = row[address_column_name].split()[0] + ', ' + row[teghakayum_column_name]

        query = query.replace('ՄԵԾ ՊԱՌՆԻ', 'ՄԵԾ ՊԱՐՆԻ')
        query = query.replace('ԼՈՌԻ', 'ԼՈՐԻ')
        query = query.replace('ԱՐԳԱՎԱՆԴ, ԱՐԱՐԱՏ', 'Argavand, Ararat')

        if query not in tmp:
            opencagedata_params['q'] = query
            response = requests.get (opencagedata_url, params=opencagedata_params).json()

            if response['total_results'] > 0:
                for result in response['results']:
                    addresses[index] = [query, str(result['geometry']['lat']) + "," + str (result['geometry']['lng'])]
                    tmp[query] = addresses[index]
                    break
            else:
                query += 'ի մարզ'
                opencagedata_params['q'] = query
                response = requests.get (opencagedata_url, params=opencagedata_params).json ()

                if response['total_results'] > 0:
                    for result in response['results']:
                        addresses[index] = [query, str(result['geometry']['lat']) + "," + str (result['geometry']['lng'])]
                        tmp[query] = addresses[index]
                        break
                else:
                    addresses[index] = "not_found"
        else:
            addresses[index] = tmp[query]

        print (index, addresses[index])

        time.sleep (0.01)

    return addresses


# provinces = opencagedata_provinces()
# print(provinces)
# addresses = opencagedata_address()
# for index in addresses:
#     print (addresses[index])

province_city = opencagedata_province_city()
file = open("data/opencagedata_province_city.txt", "w")
for index in province_city:
    file.write(str(index) + ';' + province_city[index][0] + ';' + province_city[index][1] + "\n")
file.flush()
file.close()
