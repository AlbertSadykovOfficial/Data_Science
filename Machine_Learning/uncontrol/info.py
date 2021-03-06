"""
		Некотролируемое обучение

			Тогда, когда человек не учавсвует в процессе обучения

			Методологии:
				1) Изучение распределенных данных и выявление закономерностей
				2) Анализ и послежующий прогноз на его основе

			
			Выделенрие упрощенной скрытой структуры из данных.

				Часть переменных может быть доступны сразу - наблюдаемые,
				часть переменных может быть выведена только логически - скрытые переменные.

				Пример: Впервые встретились с человеком и вам показалось, что вы ему не понравились,
				но, возможно, вчера у него сбили кота и сегодня он не в настроении, поэтому вам так
				и показалось - это и есть скрытая переменная.
				
				Выведение скрытых переменных на основании фактического набора очень полезно, так как:
					1) Скрытые переменная может заменить несколько текущих переменных
					2) Меньше переменных - легче работать с набором
					3) Таки переменные являются более информативными, чем обычные.
"""