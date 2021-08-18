import requests

""""Connect to Banxico api to get the current exchange rate of MXN based on the USD currency"""""
def get_mxn_usd_currency_exchange():
    token = "1cf29c237de7592c7fe8eaa2db02fbf2073cecaf738b3bdd82d34c55bed0cb48"
    parameters = {
        'token': token
    }
    request = requests.get('https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno', parameters).json()
    return request

    
    