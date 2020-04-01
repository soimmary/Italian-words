import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

WORDS_DICTIONARY = {}  # *ital_word*: *rus_word*
MODELLO_BY_ID = {}


def create_basis():
    """ создает базу слов из Google Sheet
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Italian Words').sheet1
    for row in range(1, sheet.row_count + 1):
        WORDS_DICTIONARY[sheet.row_values(row)[0]] = sheet.row_values(row)[1]


def choose_word():
    """ спрашивает случайное слово из списка всех слов
        принимает ответ пользователя answer
        проверяет ответ пользователя
    """
    word = random.choice(list(WORDS_DICTIONARY.items()))
    return word


def check_answer(answer, word, user_id):
    right_answer = ''
    if MODELLO_BY_ID[user_id] == 'ital -> rus':
        right_answer = word[1]
    elif MODELLO_BY_ID[user_id] == 'rus -> ital':
        right_answer = word[0]
    if right_answer == answer:
        approval = ('GIUSTO!', 'BENE!', 'CORRETTAMENTE!', 'ESSATO!',
                    'CERTO!', 'BRAVO!', 'BRAVISSIMA!')
        return random.choice(approval)
    else:
        return f'Ti sbagli :(\nla risposta giusta: {right_answer}'


create_basis()
