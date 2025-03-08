import random
import json

class Language:
    def __init__(self, name_dict):
        #списки состояний с id пользователей, чтобы понимать чьи команды и сообщения получает обработчик
        self.adding_words = []
        self.deleting_words = []
        self.adding_words_to_list = []
        self.deleting_words_from_list = []

        #списки с id пользователей и словом, которое он собирается изучать
        self.learning_words = {} 
        self.learn_list = {}
        self.learning_list = {} #список слов для изучения(временный), обнуляется после перехода из одного словаря в другой

        self.name_dict = name_dict #используемый словарь, определяет язык изучения

    #добавление id пользователей в списки/словари для отслеживания вызовов команд
    def add_to_list(self, id, A):
        if id not in A:
            A.append(id)

    def to_learning_words(self, id):
        if id in self.learning_words:
            return
        else:
            self.learning_words[id] = ""

    def to_learning_list(self, id):
        self.adding_words_to_list.append(id)
        if id in self.learning_list:
            return
        else:
            self.learning_list[id] = []

    #добавление слов в словарь/список
    def add_words_from_text(self, id, text):
        with open(self.name_dict, 'r') as file:
            try:
                dictionary = json.load(file)
            except:
                dictionary = {}
            dict_id = dictionary.get(str(id), {})
            lines = text.split('\n')
            for line in lines:
                try:
                    word, translation = line.split('-')
                except ValueError:
                    return False
                if translation.strip() == "":
                    return False
                dict_id[word.strip()] = translation.strip()
            dictionary[str(id)] = dict_id
            with open(self.name_dict, 'w') as file:
                json.dump(dictionary, file)
        return True
    
    def add_words_to_list(self, message):
        id = message.chat.id
        self.adding_words_to_list.remove(id)
        text = message.text.split("\n")
        with open(self.name_dict, 'r') as file:
            dictionary = json.load(file)
            dict_words = list(dictionary.get(str(id), {}).keys())
            f = False
            for word in text:
                word = word.strip()
                if word in dict_words and word not in self.learning_list[id]:
                    self.learning_list[id].append(word)
                    f = True
            return f
        
    #удаление слов из списка изучения
    def delete_words_from_list(self, message):
        id = message.chat.id
        self.deleting_words_from_list.remove(id)
        text = message.text.split(",")
        not_these_words = []
        for word in text:
            word = word.strip()
            if word in self.learning_list[id]:
                self.learning_list[id].remove(word)
            else:
                not_these_words.append(word)
        if len(not_these_words) == 0:
            return True
        else:
            return not_these_words #возвращает слова, которых нет в списке
        
    #получаем правильный перевод слов из списка изучения
    def translate(self, id, word):
        with open(self.name_dict, 'r') as file:
            dictionary = json.load(file)
            dict_id = dictionary.get(str(id))
            if word in list(dict_id.keys()):
                return dict_id[word]
            else:
                return word

    #проверяем словарь на пустоту
    def dict_is_empty(self, id):
        with open(self.name_dict, 'r') as file:
            try:
                dictionary = json.load(file)
            except:
                dictionary = {}
            dict_id = dictionary.get(str(id), {})
            if dict_id == {}:
                return True
            if len(dict_id.keys()) == 0:
                return True
            else:
                return False
            
    #удаляем слова из словаря
    def delete_words_from_text(self, id, text):
        with open(self.name_dict, 'r') as file:
            dictionary = json.load(file)
            dict_id = dictionary.get(str(id))
            words = text.split(',')
            not_these_words = []
            for word in words:
                try:
                    dict_id[word.strip()]
                    dict_id.pop(word.strip())
                except:
                    not_these_words.append(word.strip())
            dictionary[str(id)] = dict_id
            with open(self.name_dict, 'w') as file:
                json.dump(dictionary, file)
            if len(not_these_words) == 0:
                return True
            else:
                return not_these_words #возвращает слова, которых нет в словаре

    #отправка слова для проверки
    def send_word(self, id):
        with open(self.name_dict, 'r') as file:
            dictionary = json.load(file)
            dict_id = dictionary.get(str(id))
            word = random.choice(list(dict_id.keys()))
            if len(dict_id.keys()) != 1:
                while dict_id[word] == self.learning_words[id]:
                    word = random.choice(list(dict_id.keys()))
            self.learning_words[id] = dict_id[word]
            return word
        
    #получаем новое слово из англо-русского словаря
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
    
        