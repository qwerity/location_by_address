import pandas as pd
import requests
import time

dfs = pd.read_excel("tuberculosis.xlsx", sheet_name="tuberculosis")

opencagedata_url = 'https://api.opencagedata.com/geocode/v1/json'
opencagedata_params = {'no_annotations': '1', 'language': 'am', 'key': '641c51bed8ab490184632ad8526e29ad'}

def opencagedata_city_locations():
    teghakayum_column_name = 'Տեղակայում'
    address_column_name = 'Հասցե'
    column_frame = pd.DataFrame (dfs, columns=[teghakayum_column_name, address_column_name])

    city_locations = {}
    for index, row in column_frame.iterrows():
        if (len(row[teghakayum_column_name].split()) > 1):
            query = row[teghakayum_column_name]
        else:
            query = row[address_column_name].split()[0] + ', ' + row[teghakayum_column_name]

        query = query.replace('ՄԵԾ ՊԱՌՆԻ', 'ՄԵԾ ՊԱՐՆԻ')
        query = query.replace('ԼՈՌԻ', 'ԼՈՐԻ')
        query = query.replace('ԱՐԳԱՎԱՆԴ, ԱՐԱՐԱՏ', 'Argavand, Ararat')

        if query not in city_locations:
            opencagedata_params['q'] = query
            response = requests.get (opencagedata_url, params=opencagedata_params).json()

            if response['total_results'] > 0:
                for result in response['results']:
                    city_locations[query] = [query, str(result['geometry']['lat']) + "," + str (result['geometry']['lng'])]
                    break
            else:
                query += 'ի մարզ'
                opencagedata_params['q'] = query
                response = requests.get (opencagedata_url, params=opencagedata_params).json ()

                if response['total_results'] > 0:
                    for result in response['results']:
                        city_locations[query] = [query, str(result['geometry']['lat']) + "," + str (result['geometry']['lng'])]
                        break
                else:
                    city_locations[query] = "not_found"

        print (index, city_locations[query])

        time.sleep (0.01)

    return city_locations

city_locations = opencagedata_province_city()
file = open("opencagedata_city.txt", "w")
for index in province_city:
    file.write(str(index) + ';' + province_city[index][0] + ';' + province_city[index][1] + "\n")
file.flush()
file.close()
