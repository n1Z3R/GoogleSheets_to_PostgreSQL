import time
from datetime import datetime
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine, Integer, Column, Date
from sqlalchemy.orm import sessionmaker, declarative_base

CREDENTIALS_FILE = 'creds.json'
SPREADSHEET_ID = "1_1zak7utADCdIv3df9bbTFfEtPkTn9GY6cKNhJF9iJE"

Base = declarative_base()
engine = create_engine('postgresql://postgres:postgres@localhost:5432/test')
session = sessionmaker(bind=engine)
s = session()


class GoogleSheetsTable(Base):
    __tablename__ = 'test_table'
    id = Column(Integer, primary_key=True)
    number_order = Column("заказ №", Integer)
    price = Column("стоимость,$", Integer)
    date_delivery = Column("срок поставки", Date)


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


def load_from_database():
    database_dict = []
    for row in s.query(GoogleSheetsTable).order_by(GoogleSheetsTable.id):
        database_dict.append({"id": str(row.id), "number_order": str(row.number_order), "price": str(row.price),
                              "date_delivery": datetime.strptime(str(row.date_delivery), '%Y-%m-%d').strftime(
                                  '%d.%m.%Y')})
    return database_dict


def main():
    database_dict = load_from_database()
    while True:
        google_sheets_dict = load_google_sheets_to_list()
        if database_dict == google_sheets_dict:
            pass
        else:
            database_dict_diff = [i for i in database_dict if i not in google_sheets_dict]
            google_sheets_dict_diff = [i for i in google_sheets_dict if i not in database_dict]
            for index, i in enumerate(database_dict_diff):
                for index_j, j in enumerate(google_sheets_dict_diff):
                    if i.get('id') in j.get('id'):
                        row = s.query(GoogleSheetsTable).filter_by(id=i.get('id')).one()
                        row.number_order = j.get("number_order")
                        row.price = j.get("price")
                        row.date_delivery = j.get("date_delivery")
                        s.add(row)
                        s.commit()
                        del database_dict_diff[index]
                        del google_sheets_dict_diff[index_j]
                        print("UPDATED:", j)
            for i in database_dict_diff:
                if i.get('id') not in google_sheets_dict_diff:
                    s.query(GoogleSheetsTable).filter_by(id=i.get('id')).delete()
                    s.commit()
                    print("DELETED:", i)
            for i in google_sheets_dict_diff:
                if i.get('id') not in database_dict_diff:
                    if len(i) == 4:
                        new = GoogleSheetsTable(id=i.get("id"), number_order=i.get("number_order"),
                                                price=i.get("price"),
                                                date_delivery=i.get("date_delivery"))
                        s.add(new)
                        s.commit()
                        print("ADDED:", i)
            database_dict = load_from_database()
        time.sleep(1)


if __name__ == "__main__":
    main()
