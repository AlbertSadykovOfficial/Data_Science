"""

	Построение рекомендательной системы

	Допустим есть кинотеатр, у кинотеатра есть БД, 
	в которой указан пользоватль и фильмы которые он смотрел.
	Кинотеатр хочет построить рекомендательную систему для
	своих поситителей.

	Приемы которые будут использованы:
		1) Создание битовых строк
		2) Определение хэш-функций
		3) Добавить индексацию в таблицу для ускорения работы.

	1) Битовая строка - сжатая версия содеримого стобцов.
		 У нас есть пользователь и информация о том какой он фильм смотрел.
		 Есть таблица:
					Фильм_1 | Фильм_2 | ... | Фильм_32
		 User1	 1				 0			...			 1
		 User2	 0				 0			...			 1

		 Из таблицы видно, что можно "не возиться" с названиями фильмов,
		 а заменить их на бинарные значения (смотрел не смотрел - 1 и 0)

		 Тогда каждый пользователь будет представляться бинарным 32-значным
		 числом. По этому числу и можно будет делать выводы.

		 Конечно, бездумно сравнивать этот можно сказать хаотичный набор битов
		 бесмысленно, поэтому нужо задать метрики. Метрики нужны, чтобы выделить
		 группу. К примеру Фильмы № 5, 10 и 18 могут быть одного класса (ужастиками), 
		 поэтому есть смысл их рассматривать как флаг.
		 Можно выбрать несколько таких флагов и уже по ним проводить анализ и 
		 выстраивать рекомендации. 
		 К примеру можно здать 3 метрики: фильмы про автомобили, путешествия и выживания.

		 Примем тот факт, что мы выбрали какие-то 3 метрики и хотим по ним составить рекомендации.
		 Мы составим новую таблицу по фильмам из флагов. Так, у каждого пользователя будет 
		 статистика вида: 
				101 000 111, где 
				1-смотрел фильм из флага, 
				0 - не смотрел

			Дальше можно поступить следующим образом:
			1) 	Стоит посмотреть есть ли люди схожие по флагам (3м фильмам), если такие есть,
					то, наверное, можно предположить, что у них есть какие-то схожие интересы.
					Допустим, мы выберем одного клиента(X) для которого нужно составить рекомендации,
					так, мы выберем для рекомендации тех людей, у которых совпадают с нашим клиентом(X)
					хоть какие-то флаги. (Понятно, что их может и не быть)
			2)  Далее следует из тех отобранных людей, у кого интересы схожи с нашим клиентом(X),
					выбрать наиболее подходящих. Мы не зря переводили фильмы в 0 и 1, далее нам поможет
					Метрика под названием - расстояние Хемминга. Чем расстояние Хэмминга меньше, тем
					более схожи вкусы 2х человек.
						Пример:
							Исхожные данные:
														Флаг_1 | Флаг_2 | Флаг_3
								Клиент (X)		110			011				000
								Человек 1			010			001				010
								Человек 2			111			101				111

							Клиент(X) + Человек 1. Расстояние: 1+1+1 = 3 (3 Несовпадения)
							Клиент(X) + Человек 2. Расстояние: 1+2+3 = 6 (6 Несовпадений)

							Итог: Человек 1 лучше подходит как основа для рекомендаций Клиенту(X) 
			3) 	Сортируем отобранных людей по возрастанию расстояния Хэмминга
			4)	Берем нужно кол-во людей наиболее близких к клиенту(X) (с меньшим расстоянием Хэмминга)
			5)	Далее мы можем убрать фильмы, которые смотрел клиент(X), 
					затем применить комнду XOR к фильмам наиболее близких к нему людей,
					тогда 1 покажут те фильмы, которые клиенту(X) следует посмотреть.

			Расстояние Хэмминга.
					Расстояние Хэмминга показывает степень различия 2х строк и определяется как 
					кол-во различающихся символов в строках. Для двочных данных для определения расстояния
					подойдет команда XOR(^):									
					
					1^1 = 0 |-> Смотрели один и тот же фильм -> есть логика, что у них одинаковые интересы
					0^0 = 0 |-> (Поэтому расстояние между ними 0)
					1^0 = 1	|-> 1й смотрел этот фильм, 2й нет-> есть логика, что есть различие в интересах
					0^1 = 1	|-> (Поэтому расстояние 1 - как бы отдаление)
	

"""