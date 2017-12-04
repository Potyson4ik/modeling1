from math import cos, pi, sqrt, log
import random

# получение экспоненциально распределенного случайного чисела
def get_random_value_by_Piosson(lambda_):
    rand = random.Random()
    value = - log(1 - rand.random()) / lambda_
    return value

# получение нормально распределенного случайного числа
def get_random_value_by_Gauss(lambda_, sigma):
    result = _method_by_Muller_cos()
    while result < 0:
        result = _method_by_Muller_cos() * sigma + lambda_
    return result

# метод Мюллера для получения нормальных чисел
def _method_by_Muller_cos():
    rand = random.Random()
    return sqrt(-2 * log(rand.random())) * cos(2 * pi * rand.random())