import datetime
from watcher.watcher import load_google_sheets_to_list

from notifiers import get_notifier

TOKEN = 'TOKEN'
CHAT_ID = 'CHAT_ID'


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
