from requests_html import HTMLSession
import json
def upgrade_dictionary():
    s = HTMLSession()
    url = 'https://tuteng.ru/tutorial/32-anglo-russkij-slovar.html'
    response = s.get(url)
    response.html.render(wait=3, sleep=3)
    word_lists = response.html.find('li')
    dictionary = {}
    for i in word_lists:
        try:
           eng_word, rus_word = i.text.split(' n ')
           dictionary[eng_word] = rus_word
        except:
            continue
    with open("Dictionary.json", 'w') as file:
        json.dump(dictionary, file)
    return True
    



