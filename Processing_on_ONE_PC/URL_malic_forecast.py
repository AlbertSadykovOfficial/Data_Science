"""
	
	Прогнозирование вредоносных URL-адресов.

		Дано:
			1) Данные за 120 дней, каждое наблюдение - 3 200 000 показателей.
				 При этом  1 - сайт вредоносный
				 				  -1 - сайт нормальный
			2) Библиотека Scikit-learn

		Цель:
			Можно ли доверять некоторым адресам или нет.
			Научиться работать с большим объемом данных, не помещающимся в ОЗУ.

"""

import tarfile
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.datasets import load_svmlight_file
import numpy as np

# Скачать архив можно по ссылкке:
# http://www.sysnet.ucsd.edu/projects/url/#datasets
uri = r"D:\url_svmlight.tar.gz"
tar = tarfile.open(uri, "r:gz")

max_obs = 0
max_vars = 0
i = 0
split = 5

for tarinfo in tar:
		print("extracting %s,f size %s" % (tarinfo.name, tarinfo.size))
		if tarinfo.isfile():
				f = tar.extractfile(tarinfo.name)
				X,y = load_svmlight_file(f)
				max_vars = np.maximum(max_vars, X.shape[0])
				max_obs = np.maximum(max_obs, X.shape[1])
		if i > split:
				break
		i += 1
print("max X = %s, max y demension = %s" % (max_obs, max_vars))
