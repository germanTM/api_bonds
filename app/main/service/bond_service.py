import requests

def get_mxn_usd_currency_exchange():
    token = "cdd13fea7fa8ad76d0cf6d4530222848d56c6f7980e5a23b43dd29948dc5b3"
    parameters = {
        'token': token
    }
    request = requests.get('https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno', parameters).json()
    return request

    
    