import asyncio
import logging
import config_reader as config_reader
from aiogram.filters.command import Command
from message import MessageHandler, Commands
from aiogram import Bot, Dispatcher, types
import random
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level = logging.INFO)

# Создаем бота
bot = Bot(token=config_reader.config.bot_token.get_secret_value())

# Создаем диспетчер, который будет обрабатывать входящие сообщения
dp = Dispatcher()
commands = Commands().commands
right_ans = 0
wrong_ans = 0
mistake = "Sorry, I can't understand your message. Don't forget to put\'-\' between word and translation. Please try again /add_eng_words"

# Создаем обработчики для команд
#функция для команды /start
lang_message = MessageHandler(config_reader.name_dict_eng)
@dp.message(Command("start"))
async def start_command(message: types.Message): #
    await message.answer(commands["start"])

    #используем кнопки для выбора языка
    buttons = [[types.KeyboardButton(text="English"), types.KeyboardButton(text="Chinese")],]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.reply("Choose a language to learn", reply_markup = keyboard)

#выбираем язык для изучения, создаем экземпляр класса для выбранного языка
@dp.message(lambda message: message.text in ["English", "Chinese"])
async def button(message):
    global lang_message
    if message.text == "English":
        lang_message = MessageHandler(config_reader.name_dict_eng)
    elif message.text == "Chinese":
        lang_message = MessageHandler(config_reader.name_dict_ch)
    await message.answer("Good! Type /help to see what I can do.", reply_markup=types.ReplyKeyboardRemove())

@dp.message(Command("help"))
async def start_command(message):
    await message.answer(commands["help"])

#функция для команды /stop, удаляем пользователя из списков состояний
@dp.message(Command("stop"))
async def stop_command(message):
    global right_ans, wrong_ans
    right_ans = 0
    wrong_ans = 0
    lang_message.stop_command(message)
    await message.answer("Process was stopped.")

#функция для команды /add_words, добавляем пользователя в список состояния adding_words(добавление слов в словарь)
@dp.message(Command("add_words"))
async def start_command(message):
   lang_message.add_words_command(message)
   await message.answer(commands["add_words"])

#считываем слова пользователя, вызвавшего команду /add_words, добавляем слова в словарь 
@dp.message(lambda message: message.chat.id in lang_message.lang.adding_words)
async def to_dictionary(message):
    state = lang_message.to_dictionary(message)
    if state:
        await message.answer("success!")
    else:
        await message.answer(mistake)

#функция для команды /add_words_to_list, добавляем пользователя
#в список состояния adding_words_to_list(добавление слов в список изучения)
@dp.message(Command("add_words_to_list"))
async def to_learning_list_command(message):
   lang_message.lang.to_learning_list(message.chat.id)
   await message.answer(commands["add_words_to_list"])

#считываем слова пользователя, вызвавшего команду /add_words_to_list, добавляем слова в список изучения
@dp.message(lambda message: message.chat.id in lang_message.lang.adding_words_to_list)
async def add_words_to_list(message):
    state = lang_message.lang.add_words_to_list(message)
    if state:
        await message.answer("success!")
    else:
        await message.answer("There are no such words in your dictionary. Add it!")

#функция для команды /delete_words, добавляем пользователя в список состояния deleting_words(удаление слов из словаря)
@dp.message(Command("delete_words"))
async def delete_words_command(message):
    state = lang_message.delete_words_command(message)
    if state == False:
        await message.answer("Your dictionary is empty.")
    else:
        await message.answer(commands["delete_words"])

#считываем слова пользователя, вызвавшего команду /delete_words, удаляем эти слова из словаря
@dp.message(lambda message: message.chat.id in lang_message.lang.deleting_words)
async def from_dictionary(message):
    state = lang_message.from_dictionary(message)
    if state == True:
        await message.answer("These words were deleted.")
    else:
        await message.answer("There is no words \"" + ", ".join(state) + "\" in your dictionary")

#функция для команды /delete_words_from_list, добавляем пользователя в список
#состояния deleting_words_from_list(удаление слов из списка изучения)
@dp.message(Command("delete_words_from_list"))
async def delete_words_from_list_command(message):
    id = message.chat.id
    lists = lang_message.lang.learning_list
    if id not in list(lists.keys()) or len(lists[id]) == 0:
        await message.answer("Your list is empty.")
    else:
        lang_message.lang.deleting_words_from_list.append(message.chat.id)
        await message.answer(commands["delete_words_from_list"])

#считываем слова пользователя, вызвавшего команду /delete_words_from_list, удаляем эти слова из списка изучения
@dp.message(lambda message: message.chat.id in lang_message.lang.deleting_words_from_list)
async def delete_words_from_list(message):
    state = lang_message.lang.delete_words_from_list(message)
    if state == True:
        await message.answer("These words were deleted.")
    else:
        await message.answer("There is no words \"" +  ", ".join(state) + "\" in your dictionary")

#функция для команды /take_the_test, тестирование на знание слов из словаря, добавляем пользователя в список состояния learning_words
@dp.message(Command("take_the_test"))
async def take_the_test(message):
    state = lang_message.take_the_test(message)
    if state == False:
        await message.answer("Your dictionary is empty.")
    else:
        await message.answer(commands["take_the_test"])
        await message.answer(state)

#проверяем корректность введенного пользователем перевода
@dp.message(lambda message: message.chat.id in lang_message.lang.learning_words)
async def check_word_command(message):
    global right_ans, wrong_ans
    state = lang_message.check_word(message)
    if state == True:
        right_ans += 1
        await message.answer(f"Right! Result: \"{right_ans}/{(right_ans + wrong_ans)}\"")
    else:
        wrong_ans += 1
        await message.answer(f"No. It is \"{state}\". Result: {right_ans}/{(right_ans + wrong_ans)}")
    await message.answer("Next word: "+lang_message.lang.send_word(message.chat.id))

#функция для команды /print_dict, выводим слова и их перевод из словаря
@dp.message(Command("print_dict"))
async def print_dict_command(message):
    state = lang_message.print_dict(message)
    if state == False:
        await message.answer("Your dictionary is empty.")
    else: 
        await message.answer(state)

#функция для команды /print_dict, выводим слова из списка изучения
@dp.message(Command("print_list"))
async def print_list(message):
    id = message.chat.id
    lists = lang_message.lang.learning_list
    if id not in list(lists.keys()) or len(lists[id]) == 0:
        await message.answer("Your list is empty.")
    else:
        id = message.chat.id
        await message.answer("\n".join(lists[id]))
        
#функция для команды /learn_words_from_list, добавляем пользователя в список состояния learn_list
#изучаем слова из списка
@dp.message(Command("learn_words_from_list"))
async def learn_words_from_list(message):
    id = message.chat.id
    lists = lang_message.lang.learning_list
    if id not in list(lists.keys()) or len(lists[id]) == 0:
        await message.answer("Your list is empty.")
    else:
        await message.answer(commands["learn_words_from_list"])
        random_word = random.choice(lists[id])
        lang_message.lang.learn_list[id] = random_word
        await message.answer(random_word)

#проверяем корректность введенного пользователем перевода
@dp.message(lambda message: message.chat.id in lang_message.lang.learn_list)
async def check_word_from_list_command(message):
    id = message.chat.id
    lists = lang_message.lang.learning_list
    rus_word = lang_message.lang.translate(message.chat.id, lang_message.lang.learn_list[id])
    if message.text.strip() == rus_word:
        await message.answer(f"Right!")
    else:
        await message.answer(f"No. It is \"{rus_word}\".")
    random_word = random.choice(lists[id])
    while random_word == lang_message.lang.learn_list[id]:
        random_word = random.choice(lists[id])
    lang_message.lang.learn_list[id] = random_word
    await message.answer("Next word: "+random_word)

#функция для команды /get_new_eng_word, получаем английское слово, его транскрипцию и перевод 
#из англо-русского словаря, спарсинного с сайта
@dp.message(Command("get_new_eng_word"))
async def get_new_eng_word(message):
    eng_word, rus_word = lang_message.get_new_eng_word(message.chat.id)
    await message.answer(eng_word+" "+rus_word)
    await message.answer("Is this a new word for you?\nI suggest you add it to your dictionary!")

# Запускаем цикл обработки входящих сообщений
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
