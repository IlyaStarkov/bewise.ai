import nltk
import pymorphy2


class Dialogue:

    def __init__(self, dataframe, dlg_id):
        self.data = dataframe
        self.dlg_id = dlg_id

    def get_manager_replicas(self):
        manager_replicas = self.data[(self.data['dlg_id'] == self.dlg_id)
                                     & (self.data['role'] == 'manager')]
        return list(manager_replicas['text'].values)


def get_greeting(corpus):
    greetings = ['доброе утро', 'добрый день',
                 'добрый вечер', 'здравствуйте',
                 'приветствую', 'приветствует']
    for i, token in enumerate(corpus[:10]):
        for phrase in greetings:
            if phrase in token:
                return corpus[i]


def first_letter_up(word):
    return word[0].upper()+word[1:]


def get_manager_name(corpus):
    morph = pymorphy2.MorphAnalyzer()
    patterns = ['меня', 'зовут', 'это']
    name = None
    identification = None
    for i, token in enumerate(corpus):
        for pattern in patterns:
            if pattern in token:
                for word in nltk.word_tokenize(token):
                    for p in morph.parse(word):
                        if 'Name' in p.tag and p.score > 0.5:
                            name = first_letter_up(word)
                            identification = corpus[i]
                            break
    return {'manager_name': name, 'identification': identification}


def find_word(normal_form, corpus):
    lemmatizer = pymorphy2.MorphAnalyzer()
    for i, token in enumerate(corpus[:12]):
        words = nltk.word_tokenize(token)
        for j, word in enumerate(words):
            if lemmatizer.parse(word)[0].normal_form == normal_form:
                return {'token_num': i, 'word_num': j}
    return None


def get_company_name(corpus):
    word_dict = find_word('компания', corpus)
    if not word_dict:
        return None
    token_num, word_num = word_dict['token_num'], word_dict['word_num']
    lemmatizer = pymorphy2.MorphAnalyzer()
    words = nltk.word_tokenize(corpus[token_num])
    company_name = [words[word_num + 1]]
    for i in range(word_num+2, len(words)):
        if not ('NOUN' in lemmatizer.parse(words[i])[0].tag):
            break
        company_name.append(words[i])
    return " ".join(company_name)


def get_farewell(corpus):
    farewells = ['до свидания', 'всего доброго', 'всего хорошего', 'до связи']

    for phrase in farewells:
        if phrase in corpus[-1].lower():
            return corpus[-1]

    for i, token in enumerate(corpus):
        for phrase in farewells:
            if phrase in token.lower():
                return corpus[i]
