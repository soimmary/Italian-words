import random

WORDSLIST = []


def createBasis(filename: str = 'italian.txt'):
    """ создает базу слов из ткстшника
        принимает название файла
    """
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            ital, rus = line.split('-')
            WORDSLIST.append((ital.strip().lower(), rus.strip().lower()))


def askItalianWord():
    """ спрашивает случайное слово из списка всех слов
    """
    number = random.randint(0, len(WORDSLIST) - 1)
    return WORDSLIST[number], number


def answerItalianWord(answer: str, number: int):
    """ проверяет ответ пользователя
        принимает ответ пользователя answer
        и индекс спрашиваемого слова number
    """
    if answer.strip().lower() == WORDSLIST[number][1]:
        rightWords = ['GIUSTO!', 'BENE!', 'CORRETTAMENTE!',
                      'ESSATO!', 'CERTO!', 'BRAVO!', 'BRAVISSIMA!']  # похвала
        rightNumber = random.randint(0, len(rightWords) - 1)
        return rightWords[rightNumber]
    else:
        return 'SBAGLIATO :(\nla risposta giusta: {}'.format(WORDSLIST[number][1])


def newWordsWithStr(wordNtranslation:str):
    wList = wordNtranslation.split('\n')
    for word in wList:
        ital, rus = word.split('-')
        WORDSLIST.append((ital.lower(), rus.lower()))


def save():
    info = ''
    for words in WORDSLIST:
        info += ' - '.join(words) + '\n'
    with open('words.txt', 'w', encoding='utf8') as f:
        print(info, file=f)


def newWordsWithFile(filename:str):
    with open(filename, 'r', encoding='utf8') as f:
        for word in f:
            pass

createBasis()