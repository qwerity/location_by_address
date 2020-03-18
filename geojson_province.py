import requests
import time


provinces = [
    'Արմավիր',
    'Կոտայք',
    'Yerevan',
    'Արագածոտն',
    'Շիրակ',
    'Արարատ',
    'Գեղարքունիք',
    'Սյունիք',
    'Վայոց Ձոր',
    'Տավուշ'
]


opencagedata_url = 'https://api.opencagedata.com/geocode/v1/geojson'
opencagedata_params = {'no_annotations': '1', 'language': 'am', 'key': '641c51bed8ab490184632ad8526e29ad'}
def opencagedata_provinces_geojson():
    geojson = {}
    for province in provinces:
        if 'Yerevan' != province:
            query = province + 'ի մարզ'
        else:
            query = province

        opencagedata_params['q'] = query
        response = requests.get (opencagedata_url, params=opencagedata_params).json ()

        geojson[province] = response['features']
        print (province, geojson[province])

        time.sleep (0.01)
    return geojson


provinces_geojson = opencagedata_provinces_geojson()
