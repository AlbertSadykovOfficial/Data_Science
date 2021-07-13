"""
		Контролируемое обучение

		Бейсовский классификатор - алгоритм разбиения наблюдений на классы:
				P(спам) - частота спама без учета слов.
				P(слова) - частота использовнаяия комбинации слов нзависмо от спама
				P(слова|спам) - частота использования слов в тренировочных сообщениях помеченныз как спам

				Тогда, вероятнсть того, что новое сообщение является спамом:

						P(спам|слова) = P(спам)P(спам|слова)/P(слова)

				P(B|A) = P(B)P(A|B)/P(A)
		

		МАТРИЦА НЕСООТВЕТСВИЙ - показатель точности работы модели.
			Главная диагональ - как часто прогнозируемое число совпадало спавильным
			Элементы i,j - сколько раз определялось значение j, когда на изображении было i
			
			Главная диагональ - след матрицы

			Пример:
				Просейшая модель 2x2 - Купит ли в сответствии смоделью человек пудинг или нет
				Главная диагональ - истиные значения
				Остальные значения - Ложные значения
				
				|___Да__|__Нет__|
				|	35(+) |  10   |
				|	15    | 40(+)	|

				Как видно: Модель правильно сработала в (35+40) = 75 случаях
									 При этом ошибки модель выдала в (15+10) = 25 случаях
				Итог: у модели 75/(25+75) = 75% процентов успеха

				Если сумма чисел главной диагонали намного больше, чем суммы чисел всех остальных
				значений, значит модель адекватна.

"""