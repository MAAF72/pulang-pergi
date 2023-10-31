import os
import json
import pytz
import datetime
import argparse
import api

COORDINATE_LATITUDE = float(os.environ['COORDINATE_LATITUDE'])
COORDINATE_LONGITUDE = float(os.environ['COORDINATE_LONGITUDE'])

parser = argparse.ArgumentParser()
parser.add_argument('--action', type=str, required=True)
args = parser.parse_args()

def CheckHoliday():
    try:
        f = open('holiday.json')
        data = json.load(f)

        now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

        if str(now.date()) in data:
            return True
    except Exception as e:
        api.Notify('Error occured in CheckHoliday:', e)

    return False

def Checkin():
    if CheckHoliday():
        return
    
    try:
        last_checkin = api.GetLastCheckin()

        now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

        if last_checkin != "" and last_checkin['date'] == str(now.date()):    
            if last_checkin['last_action'] == 1:
                api.Notify('Already checkin')
            else:
                api.Notify('Already absent')
            
            return
        
        lat_long = f'{str(COORDINATE_LATITUDE)},{str(COORDINATE_LONGITUDE)}'

        api.Checkin(lat_long)
    except Exception as e:
        api.Notify(e)
    else:
        api.Notify('Checkin success')

def Checkout():
    if CheckHoliday():
        return
    
    try:
        last_checkin = api.GetLastCheckin()

        now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

        if last_checkin['date'] == str(now.date()):
            if last_checkin['last_action'] == 2:
                api.Notify('Already checkout')

                return
        
        last_checkin_id = last_checkin['id']
        lat_long = f'{str(COORDINATE_LATITUDE)},{str(COORDINATE_LONGITUDE)}'

        api.Checkout(last_checkin_id, lat_long)
    except Exception as e:
        api.Notify(e)
    else:
        api.Notify('Checkout success')

if args.action == 'checkin':
    Checkin()
elif args.action == 'checkout':
    Checkout()
else:
    api.Notify('Unknown action')