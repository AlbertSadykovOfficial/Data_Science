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