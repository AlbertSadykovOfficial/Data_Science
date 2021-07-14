"""
		Онлайновый алгоритм - парцептрон.

		Принцип парцептрона - использовать кадр и забыть, что экономит память 
		Парцептрон предназначен для бинарной классификации - (0 или 1), (да или нет).

"""

import numpy as np

class parceptron():
		def __init__(self, X,y, threshold=0.5, learning_rate=0.1, max_epochs=10):
				self.threshold = threshold						# Точка отсечения  - решает какой прогноз будет - 0 или 1 ()часто 0.5
				self.learning_rate = learning_rate		# Скорость обучения - поправка при каждом набюдении
				self.X = X
				self.y = y
				self.max_epochs = max_epochs					# Эпоха - 1 прогон по всем данным (10 прогнв до остановки)

		# Функция назначения веса
		# У нас 2 варианта изначального веса:
		#		1) Либо вес равен 0
		#		2) Либо вес расположен в диапазоне (от 0  до 0.05) 
		def initialize(self, init_type='zeros'):
				if init_type == 'random':
						self.weights = np.random.rand(len(self.X[0]))*0.05
				if init_type == 'zeros':
						self.weights = np.zeros(len(self.X[0]))

		# Функция тренировки
		def train(self):
				epoch = 0
				# Формальный бесконечный цикл (прервется либо при схождении, либо при достижении макс. кол-ва эпох)
				while True:
						error_count = 0 # Для каждой эпохи выставяем 0 ошибок, чтобы оперделить сходимость (при 0 ошибок)
						epoch += 1
						# Меняем веса, испольуя лишь 1 наблюдение за раз
						for (X,y) in zip(self.X, self.y):
								error_count += self.train_observation(X,y,error_count)
						
						if error_count == 0:
								print("training successful")
								break
						if epoch >= self.max_epochs:
								print("reached maximum epochs, no perfect prediction")
								break

		# Функция корректирования весов по формуле
		#  w = aex
		#  w - Величина изменения веса
		#  a - скорость обучения
		#  x - i-e значение во входном векторе
		def train_observation(self, X,y, error_count):
				result = np.dot(X, self.weights) > self.threshold  # Строим прогноз для текущего значения (0 или 1)
				error = y - result 																 # Реальное значения (y) тоже равно 0 или 1.
																													 # Если прогноз ошибочен мы получаем 1 или -1
				if error != 0:																		 # Если прогноз ошибочен - его нужно отрегулирвать
						error_count += 1															 # Костатируем факт ошибки
						for index, value in enumerate(X):							 # Для каждой свободной переменной во входном векторе X 
								self.weights[index] += self.learning_rate * error * value # Регулируем ее вес в соответсвии со знаком ошибки
				return error_count

		# Прогноз
		# Свободные переменные (X) умножаются на соотвествующие веса (умножение реалтзовано в np.dot)
		# Результат сравниваетс с порогом (у нас он 0.5)
		# Результат данного сравнения определяетпрогноз - 0 или 1.
		def predict(self, X):
				return int(np.dot(X, self.weights) > self.threshold)

# X - Матрица данных (свобожные переменные)
# y - Вектор целевых значений 
X = [(1,0,0), (1,1,0), (1,1,1), (1,1,1), (1,0,1), (1,0,1)]
y = [1,1,0,0,1,1]

p = parceptron(X,y)
p.initialize() 						# Инициализация весов свободных переменных
p.train()									# Модель прошла тренировку. Будет тренироваться, 
													# пока не будет ошибок или не кончатся эпохи
# Проверяем что теперь спрогнозирует парцептрон с др. знач. свободн. переме
print(p.predict((1,1,1))) # Результат: 0
print(p.predict((1,0,1))) # Результат: 1
