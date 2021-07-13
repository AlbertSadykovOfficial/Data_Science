"""
	
	ПРЕОБРАЗОВАНИЕ ИЗОБРАЖЕНИЯ В ЧИСЛА

"""
# Импортируем БД цифр
from sklearn.datasets import load_digits
import pylab as pl

# Загружаем цифры
digits = load_digits()

# преобазовтаь изображение в оттенки серого
pl.gray()

# Вывести изобраение
pl.matshow(digits.images[0])
pl.show()

# вывести матрицу
print(digits.images[0])


"""
	
	ПОСТРОЕНИ МАТРИЦЫ НЕСООТВЕТСВИЙ ПО ДАННЫМ ИЗОБРАЖЕНИЯ

"""

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import pylab as plt

# Выбирем целевую переменную
y = digits.target

# Подготовка данных
# Преобразуем матрицу в вектор через reshape (этого требует классификатор Байеса)
n_samples = len(digits.images)
X = digits.images.reshape((n_samples, -1))
print(X)

# Разбиваем данные на тестовый и тренировочный наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
gnb = GaussianNB() # Выбор наивного классивифактора Байеса для оценки вероятностей нормального распределения
fit = gnb.fit(X_train, y_train) # Подгонка данных
predicted = fit.predict(X_test) # Прогнозирования по незнакомым данным

print(confusion_matrix(y_test, predicted)) # Создание матрицы несоответсвий


"""

	СРАВНЕНИЕ ПРОГНОЗОВ С РЕАЛЬНЫМИ ЧИСЛАМИ

	(Алгоритм распознавания числа на изображении)

"""

images_and_predictions = list(zip(digits.images, fit.predict(X))) # Сохранение матрицы изображения и прогноза в одном массиве
for index, (image, prediction) in enumerate(images_and_predictions[:6]): # перебор первых семи изображений
		plt.subplot(6, 3, index + 5) # Добавление доп поддиаграммы на сетке 6x3.
		plt.axis('off') # Не отображаем ось
		plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest') # Выводим изображение в оттенках серого
		plt.title('Prediction: %i' % prediction) # Выводим прогнозируемое значение в загловке изображения 
plt.show() # Выводим диаграмму, состаящую из 6 поддиаграмм