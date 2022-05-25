import datetime
import os

import apiclient
import httplib2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from oauth2client.service_account import ServiceAccountCredentials
from notifiers import get_notifier

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

CREDENTIALS_FILE = 'creds.json'
SPREADSHEET_ID = "1_1zak7utADCdIv3df9bbTFfEtPkTn9GY6cKNhJF9iJE"


def load_google_sheets_to_list():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='A:D',
        majorDimension='ROWS'
    ).execute()
    return [dict(zip(['id', 'number_order', 'price', 'date_delivery'], l)) for l in values.get('values')[1:]]


def bot():
    last_day = datetime.date.today() - datetime.timedelta(days=1)
    google_sheets_dict = load_google_sheets_to_list()
    while True:
        if datetime.date.today() != last_day:
            last_day = datetime.date.today()
            message = '\n\n'.join(
                map(str, [i for i in google_sheets_dict if
                          datetime.datetime.strptime(i.get('date_delivery'), '%d.%m.%Y').date() == last_day]))
            get_notifier('telegram').notify(token=TOKEN, chat_id=CHAT_ID,
                                            message=f'Сегодня ({datetime.date.today()}) прошел срок:\n\n{message}')


if __name__ == "__main__":
    bot()
