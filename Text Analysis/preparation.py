import sqlite3
import nltk
import matplotlib.pyplot as plt
from collections import OrderedDict
import random

#----------------- ПОВТОРНАЯ ПОДГОТОВКА ДАННЫХ (ОЧИСТКА) -----------------#
"""

		Основные действия:
			1) Исключить гепаксы, бесполезные слова и символы
			2) Нам нужно выделить основу терминов для унификации и объединения слов одинакового написания
				(будем использовать Snowball (он привязывается к языку))
			3) Провести классификацию по Байесу и по Дереву принятия решений
			4) Натренировать классификатор
			5) Оценить точность разных етодов классификации


"""

# Загрузка используемых корпусов текстов
nltk.download('punkt')
nltk.download('stopwords')

conn = sqlite3.connect('reddit.db')
c = conn.cursor()

stopwords = nltk.corpus.stopwords.words('english')
stemmer = nltk.SnowballStemmer("english")

def wordStemmer(wordrow):
    stemmed = [stemmer.stem(word) for word in wordrow]
    return stemmed

def wordFilter(excluded,wordrow):
		filtered = [word for word in wordrow if word not in excluded]
		return filtered

def lowerCaseArray(wordrow):
		lowercased = [word.lower() for word in wordrow]
		return lowercased

# Массив мусорных значений
manual_stopwords = ['|',"'",',','.',')',',','(','m',"'m","n't",'e.g',"'ve",'s',
										'#','/','``',"'s","''",'!','r',']','=','[','s','&','%','*','...',
										'1','2','3','4','5','6','7','8','9','10','--',"''",';','-',':']

# Пересмотренная подготовка данных
def data_processing(sql,manual_stopwords):
		c.execute(sql)
		data = {'wordMatrix':[],'all_words':[]}
		interWordMatrix = []
		interWordList = []
		row = c.fetchone()
		while row is not None:
				tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')

				wordrow = tokenizer.tokenize(row[0]+" "+row[1])
				wordrow_lowercased = lowerCaseArray(wordrow)
				wordrow_nostopwords = wordFilter(stopwords,wordrow_lowercased)

				wordrow_nostopwords = wordFilter(manual_stopwords,wordrow_nostopwords)
				wordrow_stemmed = wordStemmer(wordrow_nostopwords)
				interWordList.extend(wordrow_stemmed)
				interWordMatrix.append(wordrow_stemmed)

				row = c.fetchone()

				wordfreqs = nltk.FreqDist(interWordList)
				hapaxes = wordfreqs.hapaxes()
				for wordvector in interWordMatrix:
								wordvector_nohapexes = wordFilter(hapaxes,wordvector)
								data['wordMatrix'].append(wordvector_nohapexes)
								data['all_words'].extend(wordvector_nohapexes)

				return data

subreddits = ['datascience', 'gameofthrones']
data = {}

# Выгрузим Категорию, Тему и содержимое
for subject in subreddits:
		data[subject] = data_processing(sql='''SELECT topicTitle,topicText,topicCategory FROM topics WHERE topicCategory = '''+ "'"+subject+"'", manual_stopwords=manual_stopwords)


wordfreqs_cat1 = nltk.FreqDist(data['datascience']['all_words'])
wordfreqs_cat2 = nltk.FreqDist(data['gameofthrones']['all_words'])

# Гепаксы - термины, которые встречаются 1 раз. - Мусор, они не нужны ждя модели
print(wordfreqs_cat1.hapaxes())
print(wordfreqs_cat2.hapaxes())

# Самые встречающиеся слова (топ 20)
print(wordfreqs_cat1.most_common(20))
print(wordfreqs_cat2.most_common(20))


# Размер Контрольной выборки 
holdoutLength  = 100

# Создани объединенного набора данных, 
# в котором каждое слово снабжается либо меткой "datascience", либо меткой "gameofthrones"
labeled_data1 = [(word,'datascience') for word in data['datascience']['wordMatrix'][holdoutLength:]]
labeled_data2 = [(word,'gameofthrones') for word in data['gameofthrones']['wordMatrix'][holdoutLength:]]
labeled_data = []
labeled_data.extend(labeled_data1)
labeled_data.extend(labeled_data2)

# Контрольная выборка состоит из непомеченных данных - из 2х подфорумов по 100 наблюдений из каждого набора.
# Метки хранятся в отдельном наборе данных
holdout_data = data['datascience']['wordMatrix'][:holdoutLength]
holdout_data.extend(data['gameofthrones']['wordMatrix'][:holdoutLength])
holdout_data_labels = ([('datascience') for _ in range(holdoutLength)] + [('gameofthrones') for _ in range(holdoutLength)])

# Создание списка всех уникальных терминов для посроения набора слов, необходимого для тренировки или оценки модели.
data['datascience']['all_words_dedup'] = list(OrderedDict.fromkeys(data['datascience']['all_words']))
data['gameofthrones']['all_words_dedup'] = list(OrderedDict.fromkeys(data['gameofthrones']['all_words']))
all_words = []
all_words.extend(data['datascience']['all_words_dedup'])
all_words.extend(data['gameofthrones']['all_words_dedup'])
all_words_dedup = list(OrderedDict.fromkeys(all_words))

# Преобразуем данные в формат набора слов
# Почему-то len(prepared_data) = 0, 
# из-за этого, видимо последующий код не работает
prepared_data = [({word: (word in x[0]) for word in all_words_dedup}, x[1]) for x in labeled_data]
prepared_holdout_data = [({word: (word in x[0]) for word in all_words_dedup}) for x in holdout_data]


# Случайно переставляем данные для тренировки
# Размер тренировочных данных - 75%
random.shuffle(prepared_data)
train_size = int(len(prepared_data) * 0.75)
train = prepared_data[:train_size]
test = prepared_data[train_size:]


#----------------- АНАЛИЗ ДАННЫХ (Не работает)-----------------#
"""

print(type(train), len(train))

# Классификация по Байесу
classifier = nltk.NaiveBayesClassifier.train(train)
nltk.classify.accuracy(classifier, test)
classified_data = classifier.classify_many(prepared_holdout_data)
cm = nltk.ConfusionMatrix(holdout_data_labels, classified_data)
print(cm)

print(classifier.show_most_informative_features(20))

# Классификация на базе дерева принятия решений:
classifier2 = nltk.DecisionTreeClassifier.train(train)
nltk.classify.accuracy(classifier2, test)
classified_data2 = classifier2.classify_many(prepared_holdout_data)
cm = nltk.ConfusionMatrix(holdout_data_labels, classified_data2)
print(cm)

"""