import random
import matplotlib.pyplot as plt
import collections 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

WORDS_DICTIONARY = {}  # *ital_word*: *rus_word*
FORGOTTEN_WORDS = collections.Counter()


def create_basis(tema):
    """ создает базу слов в Google Sheets
    """
    global WORDS_DICTIONARY         
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    
# NEW ________
    sheet = client.open('Italian Words')
    work_sheet = sheet.worksheet('parole')
    large_dictionary = {}
    
    for row in range(1, work_sheet.row_count + 1):
        large_dictionary[work_sheet.row_values(row)[2]] = {}
    for row in range(1, work_sheet.row_count + 1):
        large_dictionary[work_sheet.row_values(row)[2]][work_sheet.row_values(row)[0]] \
            = work_sheet.row_values(row)[1]

    WORDS_DICTIONARY = large_dictionary[tema]
    return WORDS_DICTIONARY
# NEW ________    


def choose_word():
    """ спрашивает случайное слово из списка всех слов
        принимает ответ пользователя answer
        проверяет ответ пользователя
    """
    word = random.choice(list(create_basis().items()))
    return word


def check_answer(answer, word, language):
    right_answer = ''
    if language == 'ital🇮🇹 -> rus🇷🇺':
        right_answer = word[1]
    elif language == 'rus🇷🇺 -> ital🇮🇹':
        right_answer = word[0]
    if right_answer == answer:
        approval = ('Giusto☺️!', 'Bene🤓!', 'Correttamente🤩!', 'Essato☺️!',
                    'Certo🥰!', 'Bravo👏🏻!', 'Bravissima🥳!')
        return random.choice(approval)
    else:
        # new
        FORGOTTEN_WORDS[word[0]] += 1
        return f'Ti sbagli ☹️:(\nLa risposta giusta: {right_answer}'


def drawing_bar():
    words = list(FORGOTTEN_WORDS.values())
    number = list(FORGOTTEN_WORDS.keys())

    plt.figure(figsize=(16, 9))
    plt.bar(number, words, color='pink')
    plt.title('Le parole che dimentichi')
    plt.ylabel('Volte')
    plt.xlabel('Parole')
    plt.savefig(r'grafico.png', bbox_inches=0)


#create_basis(tema)
