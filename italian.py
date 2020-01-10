import random
def italianWords():
    with open('italian.txt', 'r', encoding='utf-8') as f:
        myList = []
        for line in f:
            ital, rus = line.split('-')
            rus = rus.strip()
            myList.append((ital, rus))
        while True:
            right = ['GIUSTO!', 'BENE!', 'CORRETTAMENTE!',
                     'ESSATO!', 'CERTO!', 'BRAVO!', 'BRAVISSIMA!']
            rightNumber = random.randint(0, len(right) - 1)
            number = random.randint(0, len(myList) - 1)
            print(myList[number][0])
            myInput = input('la risposta: ').strip().lower()
            if myInput == '':
                break
            if myInput == myList[number][1]:
                print(right[rightNumber], '\n')
            else:
                print('SBAGLIATO :(')
                print('la risposta giusta:', myList[number][1], '\n')

def newWords():
    myList = []
    myInput = input('Inserisci la parola italiana e la parola russa.'
                    '\nPer esempio: cioccolato - шоколад.\n-> ')
    myList.append(tuple(myInput.split('-')))
    while True:
        myInput = input('\nInserisci la parola italiana e la parola russa.\n-> ')
        if myInput == '':
            break
        myList.append(tuple(myInput.split('-')))
    print(myList)

newWords()