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
        print('Error occured in CheckHoliday:', e)

    return False

def Checkin():
    if CheckHoliday():
        return
    
    last_checkin = api.GetLastCheckin()

    if last_checkin['last_action'] == 1:
        now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

        if last_checkin['date'] == str(now.date()):
            print('Already checkin')

            return
    
    lat_long = f'{str(COORDINATE_LATITUDE)},{str(COORDINATE_LONGITUDE)}'

    api.Checkin(lat_long)

    print('Checkin success')


def Checkout():
    if CheckHoliday():
        return
    
    last_checkin = api.GetLastCheckin()

    if last_checkin['last_action'] == 2:
        now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))

        if last_checkin['date'] == str(now.date()):
            print('Already checkout')

            return
    
    last_checkin_id = last_checkin['id']
    lat_long = f'{str(COORDINATE_LATITUDE)},{str(COORDINATE_LONGITUDE)}'

    api.Checkout(last_checkin_id, lat_long)

    print('Checkout success')


if args.action == 'checkin':
    Checkin()
elif args.action == 'checkout':
    Checkout()
else:
    print('Unknown action')