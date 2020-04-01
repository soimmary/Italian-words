import random

WORDS_DICTIONARY = {}  # *ital_word*: *rus_word*
MODELLO_BY_ID = {}


def create_basis(filename: str = 'italian.txt'):
    """ создает базу слов из ткстшника
        принимает название файла
    """
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            ital, rus = line.split('-')
            WORDS_DICTIONARY[ital.strip().lower()] = rus.strip().lower()


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
