import sqlite3
import nltk
import matplotlib.pyplot as plt
from collections import OrderedDict
import random

# Загрузка используемых корпусов текстов
nltk.download('punkt')
nltk.download('stopwords')

conn = sqlite3.connect('reddit.db')
c = conn.cursor()


#----------------- ПОДГОТОВКА ДАННЫХ ПЕРЕД ИСПОЛЬЗОВАНИЕМ (Выявление выбросов) -----------------#

"""
		Основные действия:
			1) Привести данные к единообразному виду (в нижний регистр)
			2) Исключить бесполезные слова (по типу - я, мы), вводные конструкции 
			3) Построить частоту использования слов
			4) Выявить гепаксы
			5) Посмотреть наиболее часто встречающиеся слова
			6) Выявить бесполезные слова и символы, которые еще не исключили

			ПОСЛЕ выявления пунктов 4 и 6, следует очистить ненужны данные,
			это реализовано в файле preparation.py

"""


# Исключаем слова по типу (i, me), которые не несут информации 
stopwords = nltk.corpus.stopwords.words('english')
print(stopwords)

def wordFilter(excluded,wordrow):
		filtered = [word for word in wordrow if word not in excluded]
		return filtered

def lowerCaseArray(wordrow):
		lowercased = [word.lower() for word in wordrow]
		return lowercased

def data_processing(sql):
		c.execute(sql)
		data = {'wordMatrix': [], 'all_words':[]}
		row = c.fetchone()
		while row is not None:
			# row[0] - название
			# row[1] - текст темы
			# Пробразуем их в 1 блок
			wordrow = nltk.tokenize.word_tokenize(row[0]+" "+row[1])
			wordrow_lowercased = lowerCaseArray(wordrow)
			wordrow_nostopwords = wordFilter(stopwords, wordrow_lowercased)
			data['all_words'].extend(wordrow_nostopwords)
			data['wordMatrix'].append(wordrow_nostopwords) # Матрица, состоящая из векторов слов
			row = c.fetchone() # Получаем новый документ из БД sqlite
		return data

subreddits = ['datascience', 'gameofthrones']
data = {}

# Выгрузим Категорию, Тему и содержимое
for subject in subreddits:
	data[subject] = data_processing(sql='''SELECT topicTitle, topicText, topicCategory FROM topics WHERE topicCategory=''' + "'"+subject+"'")

# Выводим все слова, которые встречаются в подкатегории datascience
print(data['datascience']['wordMatrix'][0])


#----------------- ИССЛЕДОВАНИЕ ДАННЫХ -----------------#

# Построим графики частоты слов
wordfreqs_cat1 = nltk.FreqDist(data['datascience']['all_words'])
plt.hist(wordfreqs_cat1.values(), bins = range(10))
plt.show()
wordfreqs_cat2 = nltk.FreqDist(data['gameofthrones']['all_words'])
plt.hist(wordfreqs_cat2.values(), bins = range(10))
plt.show()

# Гепаксы - термины, которые встречаются 1 раз. - Мусор, они не нужны ждя модели
print(wordfreqs_cat1.hapaxes())
print(wordfreqs_cat2.hapaxes())

# Самые встречающиеся слова (топ 20)
# Можно заметить, что туда входит много знаков препинания и односимвольных терминов
print(wordfreqs_cat1.most_common(20))
print(wordfreqs_cat2.most_common(20))