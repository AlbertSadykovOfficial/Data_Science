"""

	Выяление скрытых переменных в наборе данных качества вина


	Метод главных компонент (PCA - Principal Components Analysis).

	Через метод главных компонент можно определить скрытые переменныев наборе
	данных с сохранение максимально возможной информации, анализировать кол-во 
	новых переменных,которые приносят наибольшую пользу посредством генерирования 
	и интрпретирования графика каменистой осыпи (scree plot). 

"""


"""

	Сбор данных и стандартизация переменных (Подготовка)

"""
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
import pylab as plt
from sklearn import preprocessing

# Подгруаем данные
url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
data = pd.read_csv(url, sep=";")

# Матрица свойств вина
X = data[[u'fixed acidity', u'volatile acidity', u'citric acid', u'residual sugar', u'chlorides',
					u'free sulfur dioxide', u'total sulfur dioxide', u'density', u'pH', u'sulphates', u'alcohol']]

# Вектор целевй переменной (субъективное качетство вина)
y = data.quality

# z = (x-m)/sigma, z - новое значение
X = preprocessing.StandardScaler().fit(X).transform(X)


"""
		
		Анализ главных компонент

		Демонстрация предельной величины информвции, которая может создавать каждая новая переменная.
		По графику:
			Первые переменные объясняют около 28% информации 
			Вторая - еще + 17%
			Третья - еще около 15%
				...
		
		Тут мы можем решить сколько скрытых переменнных нужно нам, но только после того как 
		будет понятно, что представляют из себя эти 5 переменных. 

"""

# Создание экземпляра класса анализа главных компонент
model = PCA()
results = model.fit(X) # Применение PCA к свобоным переменным для поиска возможности свертки их в меньшее кол-во переменных
Z = results.transform(X) # Результат преобразуется в массив
plt.plot(results.explained_variance_) # График дисперсии переменных - график каминистой осыпи.
plt.show()


# Вывод компонент PCA во фрейме данных pandas
# (Вычисление корреляции 11 исходных переменных с 5 сткрытми переменными)
#
# Полученные данные - строки описывают математическую корреляцию 
# Lv1 = (fixed acidity * 0.489314) + (volatile acidity * -2.238584) + ... + (alcohol * -0.113232)
print(pd.DataFrame(results.components_, 
							columns=list(
								[u'fixed acidity', u'volatile acidity', u'citric acid', u'residual sugar', u'chlorides',
								u'free sulfur dioxide', u'total sulfur dioxide', u'density', u'pH', u'sulphates', u'alcohol']
							)
						)
)


"""
	
	Сравнение точности исходного набора данных со скрыми переменными
			
			1) Прогнозирование качетсва вина до применения анализа главных компонент (по исхожным 11)
			2) Прогназирование качетсва вина с наращиванием количества главных компоенент

"""


from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import pylab as plt

""" Прогнозирование по исходным компонентам """

gnb = GaussianNB() # Выбор наивного классивифактора Байеса для оценки вероятностей нормального распределения
fit = gnb.fit(X, y) # Подгонка данных
predicted = fit.predict(X) # Прогнозирования для неизвесных данных
print(confusion_matrix(predicted,y)) # Изучение матрицы несоответсвий

# Подсчет правильно классифицированных случаев (по слежу матрицы)
# След - 897 правильных прогнозов из 1599
print(confusion_matrix(predicted,y).trace)


""" Прогнозирование по главным компонентам """

predicted_correct = [] # Массив правильно спрогнозированных наблюдений
for i in range(1, 10): # Переерем первые 10 оаруженных главных компонент
		model = PCA(n_components=i) # Создаем модель PCA с разным кол-вом компонентов (от 1 до 10)
		results = model.fit(X) 			# Подгонка модели PCA по x-переменным (показателям)
		Z = results.transform(X)		# Z - результат в форме матрицы
		fit = gnb.fit(Z,y)					# Применение наивного классификатора Байеса с Норм. распр
		predicted = fit.predict(Z)	# Прогнозирование с использованием подогнанной модели
		predicted_correct.append(confusion_matrix(predicted,y).trace()) # Добавляем правильно классифиц. модели
		print(predicted_correct) # Выводим массив для демонстрации увеличения правильно классифиц. знач. 

# Выводим график
# По графику видно, что всего с 3 скрытми компонентами классификатор лучше справляется,
# чем с 11 ихсодными 
# При этом добавление более 5 компонент уже не так влияет на результат как первые 5
plt.plot(predicted_correct)
plt.show()