from language import Language
import json
import random
class Commands:
    def __init__(self):
        #ответы команд
        self.commands = {
            "start": "Hello! I will help you to learn english and chinese words. ",
            "help": "To start learning you should\n"
                    "add words to your dictionary by typing /add_words\n"
                    "or add words to your learning list from dictionary by typing /add_words_to_list "
                    "(if the word is not in your dictionary, it will not be added to the list)\n"
                    "To see your dictionary, type /print_dict.\n"
                    "To see your learning list, type /print_list.\n"
                    "In dictionaries you can delete word by typing /delete_words.\n"
                    "In learning list you can delete word by typing /delete_words_from_list.\n"
                    "If you want to start learning words from your list, type /learn_words_from_list\n"
                    "If you want to test yourself, type /take_the_test "
                    "and I will send you word from your dictionary, you should type translation\n"
                    "If you want to learn a new english word, type /get_new_eng_word",

            "add_words": "Send me words in this format:\n"
                        "word 1 - translation 1\n"
                        "word 2 - translation 2\n"
                        "To stop command type /stop",     

            "delete_words": "Send me words, which you want to "
                           "delete, in this format:\nword 1, "
                           "word 2, etc\n"
                           "To stop command type /stop",

            "add_words_to_list": "Send me words in this format:\n"
                        "word 1\n"
                        "word 2\n"
                        "To stop command type /stop", 

            "delete_words_from_list": "Send me words, which you want to "
                           "delete, in this format:\nword 1, "
                           "word 2, etc\n"
                           "To stop command type /stop",

            "take_the_test": "I will send you word from your dictionary, you should type translation\n"
                            "To stop command type /stop",

            "learn_words_from_list": "I will send you word from your learning list, you should type translation\n"
                            "To stop command type /stop",
        }
class MessageHandler:
    def __init__(self, dict):
        self.name_dict = dict
        self.lang = Language(dict)
        self.commands = Commands().commands
    
    #реализация команд, описанных в файле bot.py
    def stop_command(self, message):
        id = message.chat.id
        lang = self.lang
        if id in lang.learning_words:
            lang.learning_words.pop(id)
        if id in lang.adding_words:
            lang.adding_words.remove(id)
        if id in lang.deleting_words:
            lang.deleting_words.remove(id)
        if id in lang.learn_list:
            lang.learn_list.pop(id)
        if id in lang.adding_words_to_list:
            lang.adding_words_to_list.remove(id)
        if id in lang.deleting_words_from_list:
            lang.deleting_words_from_list.remove(id)

    def add_words_command(self, message):
        id = message.chat.id
        lang = self.lang
        lang.add_to_list(id, lang.adding_words)

    def to_dictionary(self, message):
        id = message.chat.id
        lang = self.lang
        lang.adding_words.remove(id)
        text = message.text
        return lang.add_words_from_text(id, text)
    
    def delete_words_command(self, message):
        id = message.chat.id
        lang = self.lang
        if lang.dict_is_empty(id):
            return False
        lang.add_to_list(id, lang.deleting_words)
        return True

    def from_dictionary(self, message):
        id = message.chat.id
        lang = self.lang
        lang.deleting_words.remove(id)
        text = message.text
        return lang.delete_words_from_text(id, text)

    def take_the_test(self, message):
        id = message.chat.id
        lang = self.lang
        if lang.dict_is_empty(id):
            return False
        lang.to_learning_words(id)
        return lang.send_word(id)
    
    def learn_words(self, message):
        id = message.chat.id
        lang = self.lang
        lang.to_learning_listwords(id)
    
    def check_word(self, message):
        id = message.chat.id
        text = message.text.strip()
        lang = self.lang
        if text == lang.learning_words[id]:
            return True
        return lang.learning_words[id]
    
    def print_dict(self, message):
        id = message.chat.id
        lang = self.lang
        if lang.dict_is_empty(id):
            return False
        with open(self.name_dict, 'r') as file:
            dictionary = json.load(file)
            dict_id = dictionary.get(str(id))
            display = ""
            for elem in dict_id:
                display = display + elem + ' - ' + dict_id[elem] + '\n'
            return display
        
    def get_new_eng_word(self, id):
        with open("Dictionaries/Dictionary.json", 'r') as file1:
            AppDict = json.load(file1)
            with open(self.name_dict, 'r') as file2:
                dictionary = json.load(file2)
                dict_id = dictionary.get(str(id))
                word = random.choice(list(AppDict.keys()))
                while word in list(dict_id.keys()):
                    word = random.choice(list(AppDict.keys()))
            return word, AppDict[word]
    