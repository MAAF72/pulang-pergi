import os
import requests
import json
import base64

HOST = os.environ['HOST']
TOKEN = os.environ['TOKEN']

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_CHAT_ID = os.environ['BOT_CHAT_ID']

def GetHeaders():
    headers = {
        'content-type': 'application/json',
        'user-agent': 'Dalvik/2.1.0 (Linux; U; Android 13; RMX3360)',
        'host': HOST,
        'connection': 'Keep-Alive',
    }

    return headers

def Checkin(lat_long):
    payload = json.dumps({
        'token': TOKEN,
        'location': base64.b64encode(lat_long.encode('ascii')).decode('ascii'),
        'lat_long': lat_long,
        'message': '',
        'location_type': 2,
        'in_out': 1,
        'udid': '',
        'purpose': ''
    })

    response = requests.request('POST', f'https://{HOST}/Mobileapi/CheckInPost', headers=GetHeaders(), data=payload)

    if response.status_code < 200 or response.status_code > 299:
        print(response.text)
        
        raise Exception('API error Checkin')
    
    return True

def Checkout(last_checkin_id, lat_long):
    payload = json.dumps({
        'checkin_id': last_checkin_id,
        'token': TOKEN,
        'location': base64.b64encode(lat_long.encode('ascii')).decode('ascii'),
        'lat_long': lat_long,
        'message': '',
        'location_type': 2,
        'in_out': 2,
        'udid': '',
        'purpose': ''
    })

    response = requests.request('POST', f'https://{HOST}/Mobileapi/CheckInPost', headers=GetHeaders(), data=payload)

    if response.status_code < 200 or response.status_code > 299:
        print(response.text)
        
        raise Exception('API error Checkout')
    
    return True

def GetLastCheckin():
    payload = json.dumps({
        'token': TOKEN,
    })

    response = requests.request('POST', f'https://{HOST}/Mobileapi/LastCheckIndeatils', headers=GetHeaders(), data=payload)

    if response.status_code < 200 or response.status_code > 299:
        print(response.text)

        raise Exception('API error GetLastCheckin')
    
    data = response.json()['message']

    return data

def Notify(message):
    response = requests.request('GET', f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={BOT_CHAT_ID}&text={message}')

    if response.status_code < 200 or response.status_code > 299:
        print(response.text)

        raise Exception('API error Notify')

    return True