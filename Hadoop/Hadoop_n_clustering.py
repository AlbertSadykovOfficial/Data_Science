"""

	Hadoop - инфраструктура для работы с кластерами.

	Базовая структура Hoadoop состоит из следующих компонентов:
		1) Распределенная файловая система (HDFS)
		2) MapReduce (Технология распределенного программтрования)
		3) Система управления ресурсами кастеров (YARN)
		+ инфраструктура, образовавшаяся вокруг:
			- Hive - БД
			- Imapla - ускорение работы Hive (Вплоть до 100 раз)
			- Qlik - инструмен бизнес-аналитики (средства предаставления информации).ы


	MapReduce:
		
		Данный алгоритм плохо подходит для интерактивного анализа, потому что данные записыаются
		на диск между этапами вычилсения, что существенно снижает скорость.
		ПОЭТОМУ для data science этот алгоритм не очень подходит. 

		Алгоритм следующий:
			1) Разбить данные
			2) Параллельно обработать разбитые данные иотобразить их (mapper)
			3) 
					3.1 Читаем значения из файла (цвета)
					3.2 Выводим отдельно для каждого цвета файл с количеством его вхождений 
							(отображаем ключ на значение)
			4) Сортируем ключи для обработки данных
			5) Суммируем кол-во вхождений каждого цвета и для каждого цвета 
				 выводим 1 файл с общим кол-вом вхождений (Reduce)
			6) Все ключи собираются в 1 файл.

	Spark:
		
		Чтобы решить проблемы MaPReduce, а именно - низкую скорость, 
		был придуман Spark.

		Spark - инфраструктура кластерных вычислений, схожая с MapReduce,
		но при этом Spark не занимается ни хранением файлов, ни управления ресурсами.
		Для этого Spark обращается к HDFS, YARN или Apacehe Mesos.

		Spark создает "общую оперативную память" для кмпьютеров кластера,
		что позволяет разным рабочим процессам использовать общие переменные,
		что снимает необходимость записи промежуточных результатов на диск.
		Это и повышает скорость и является основным преимуществом для data science.



"""