import telebot
import italian
import os

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])  # decorator
def start_message(message):
    bot.send_message(message.chat.id, 'Ciao🤩!')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/ciao o ciao – damandare la parola\n'
                                      'sonostanca o sonostanco – finire di praticare\n'
                                      '/grafico - dimostrare le parole in cui fai gli sbagli spesso')


@bot.message_handler(commands=['ciao'])
def ciao_message_ask_tema(message):
    keyboard_tema = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_tema.row('il cibo 🍝', 'la casa 🏡', 'i lavori di casa 🧺')
    bot.send_message(message.chat.id, 'Scegli il tema', reply_markup=keyboard_tema)
    bot.register_next_step_handler(message, ciao_message_register_tema)


def ciao_message_register_tema(message):
    possible_answers = ('il cibo 🍝', 'la casa 🏡', 'i lavori di casa 🧺')
    tema = message.text.strip().lower()
    if tema in possible_answers:
        italian.create_basis(tema)
        bot.register_next_step_handler(message, ciao_message_ask_language)
    else:
        bot.send_message(message.chat.id, "L'errore❗️")

# NEW___________

def ciao_message_ask_language(message):
    keyboard_modello = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_modello.row('ital🇮🇹 -> rus🇷🇺', 'rus🇷🇺 -> ital🇮🇹')
    bot.send_message(message.chat.id, 'Scegli il modello', reply_markup=keyboard_modello)
    bot.register_next_step_handler(message, ciao_message_register_language)

    
def ciao_message_register_language(message):
    possible_answers = ('ital🇮🇹 -> rus🇷🇺', 'rus🇷🇺 -> ital🇮🇹')
    language = message.text.strip().lower()
    if language in possible_answers:
        ciao_message_ask(message, language)
    else:
        bot.send_message(message.chat.id, "L'errore❗️")
                      
    
def ciao_message_ask(message, language):
    if message.text.strip().lower() not in ('sono stanca', 'sono stanco'):  # proverka na ustalost'
        user_id = message.chat.id
        word = italian.choose_word()
        if language == 'ital🇮🇹 -> rus🇷🇺':
            bot.send_message(message.chat.id, word[0])
        elif language == 'rus🇷🇺 -> ital🇮🇹':
            bot.send_message(message.chat.id, word[1])
        bot.send_message(user_id, 'Aspetto la tua risposta ⏰')
        bot.register_next_step_handler(message, ciao_message_check_answer, word, language)
    else:
        sonostanco_message(message)
        

def ciao_message_check_answer(message, word, language):
    answer = message.text.strip().lower()
    if answer not in ('sono stanca', 'sono stanco'):
        user_id = message.chat.id
        my_decision = italian.check_answer(answer, word, language)
        bot.send_message(user_id, my_decision)
        ciao_message_ask(message, language)
    else:
        sonostanco_message(message)


def sonostanco_message(message):
    bot.send_message(message.chat.id, 'Hai lavorato bene 🤗!')
    
    
@bot.message_handler(commands=['grafico'])
def send_drawing_bar(message):
    italian.drawing_bar()
    bar = open('grafico.png', 'rb')
    bot.send_photo(message.chat.id, photo=bar)


@bot.message_handler(content_types=['text'])
def ciao_text_message(message):
    if str(message.text).strip().lower() == 'ciao':
        ciao_message_ask_language(message)
    else:
        bot.send_message(message.chat.id, 'Non so questo comando ☹️')



bot.polling(none_stop=True)
