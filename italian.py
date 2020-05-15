import random
import matplotlib.pyplot as plt
import collections #  добавила
import gspread
from oauth2client.service_account import ServiceAccountCredentials

WORDS_DICTIONARY = {}  # *ital_word*: *rus_word*
FORGOTTEN_WORDS = collections.Counter()


def create_basis(filename: str = 'italian.txt'):
    """ создает базу слов в Google Sheets
    """
               
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Italian Words').sheet1
    for row in range(1, sheet.row_count + 1):
        WORDS_DICTIONARY[sheet.row_values(row)[0] = sheet.row_values(row)[1]]        
    


def choose_word():
    """ спрашивает случайное слово из списка всех слов
        принимает ответ пользователя answer
        проверяет ответ пользователя
    """
    word = random.choice(list(WORDS_DICTIONARY.items()))
    return word


def check_answer(answer, word, language):
    right_answer = ''
    if language == 'ital -> rus':
        right_answer = word[1]
    elif language == 'rus -> ital':
        right_answer = word[0]
    if right_answer == answer:
        approval = ('GIUSTO!', 'BENE!', 'CORRETTAMENTE!', 'ESSATO!',
                    'CERTO!', 'BRAVO!', 'BRAVISSIMA!')
        return random.choice(approval)
    else:
        FORGOTTEN_WORDS[right_answer] += 1  # добавила этот кусок
        return f'Ti sbagli :(\nla risposta giusta: {right_answer}'


def drawing_bar():
    words = list(FORGOTTEN_WORDS.values())
    number = list(FORGOTTEN_WORDS.keys())

    plt.bar(number, words, color='pink')
    plt.title('Le parole che dimentichi')
    plt.ylabel('Volte')
    plt.xlabel('Parole')
    plt.savefig(r'grafico.png', dpi=1000, bbox_inches=0)


create_basis()
