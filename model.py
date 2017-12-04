from math import sqrt
import generator

# Функция возвращает корреляцую между двумя списками значений
def get_corr(x_list, y_list):
    avg_x = sum(x_list) / len(x_list)
    avg_y = sum(y_list) / len(y_list)
    sigma_x = 0
    for x in x_list:
        sigma_x += (x - avg_x) ** 2
    sigma_x = sqrt(sigma_x / len(x_list))
    sigma_y = 0
    for y in y_list:
        sigma_y += (y - avg_y) ** 2
    sigma_y = sqrt(sigma_y / len(y_list))
    p = 0
    for i in range(len(x_list)):
        p += ((x_list[i] - avg_x) / sigma_x) * ((y_list[i] - avg_y) / sigma_y)
    p /= (len(x_list))
    return p

class ServerModel():
    def __init__(self, T, L, Ms, Ds, Mt):
        self.T = T # время работы сервера
        self.L = L # длина очереди (LIFO)
        self.Ms = Ms # математическое ожидание времени выполнения задачи сервером
        self.Ds = Ds # дисперсия времени выполнения задачи сервером
        self.Mt = Mt # математическое ожидание времени поступления задачи в очередь
        self.Dt = 1.0 / (Mt * Mt) # дисперсия времени поступления задачи в очередь
    def run(self):
        system_time = 0  # системное время
        self.task_counter = 0  # счётчик поступивших задач
        self.task_time = generator.get_random_value_by_Piosson(1 / self.Mt)  # время поступления задач
        self.server_time = 0  # время работы сервера
        is_task_run = False  # флаг характеризующий событие работы сервера
        self.queue_tast_count = 0  # количество задач в очереди на определенный момент
        is_task_event = True  # флаг характеризующий событие поступления новой задачи
        self.queue_cnt = []  # список зафиксированных длин очередей
        self.time_task_list = []  # список сгенерированных времён прибытия задач
        self.time_server_list = []  # список сгенерированных времён обработки сервером задач
        self.busy_time_list = []  # список времён непрерыной работы сервера
        self.out_task_time_list = [] # список интервалов времени между выходящими заданиями
        busy_timer = 0  # время непрерывной работы сервера
        self.not_run_task_counter = 0  # количество не выполненных задач
        pred_server_time = 0 # предыдущее серверное время
        while system_time < self.T:
            if is_task_event:
                self.task_counter += 1
                if is_task_run:
                    if self.queue_tast_count != self.L:
                        self.queue_tast_count += 1
                    else:
                        self.not_run_task_counter += 1
                else:
                    is_task_run = True
                    value_G = generator.get_random_value_by_Gauss(self.Ms, self.Ds)
                    self.time_server_list.append(value_G)
                    server_time = self.task_time + value_G
                    busy_timer += value_G
                value_P = generator.get_random_value_by_Piosson(1 / self.Mt)
                self.time_task_list.append(value_P)
                self.task_time += value_P
                self.queue_cnt.append(self.queue_tast_count)
            else:
                if pred_server_time > 0:
                    self.out_task_time_list.append(server_time - pred_server_time)
                if self.queue_tast_count == 0:
                    is_task_run = False
                    pred_server_time = server_time
                    server_time = self.task_time
                    self.busy_time_list.append(busy_timer)
                    busy_timer = 0
                else:
                    self.queue_tast_count -= 1
                    value_G = generator.get_random_value_by_Gauss(self.Ms, self.Ds)
                    self.time_server_list.append(value_G)
                    pred_server_time = server_time
                    server_time += value_G
                    busy_timer += value_G
            is_task_event = True if self.task_time <= server_time else False
            system_time = min(self.task_time, server_time)

    # Средняя длина очереди
    def get_avg_task_queue(self):
        return sum(self.queue_cnt)/self.task_counter

    # Среднее время поступления задачи в очередь
    def get_avg_task_time(self):
        return sum(self.time_task_list) / len(self.time_task_list)

    # Среднее время обработки задачи сервером
    def get_avg_server_time(self):
        return sum(self.time_server_list) / len(self.time_server_list)

    # Загруженность сервера
    def get_server_load(self):
        return self.get_avg_server_time() / self.get_avg_task_time()

    # Вероятность того, что задача не будет добавлена в очередь
    def get_p_failure(self):
        return self.not_run_task_counter / self.task_counter

    # Автокорелляция интервалов времени между выходящими заданиями с указанным шагом сдвига
    def get_autocorr_by_runtime_task(self, step=1):
        displaced_task_list = self.out_task_time_list[step:]
        return get_corr(self.out_task_time_list[:len(displaced_task_list)], displaced_task_list)


    # Максимальное время непрерывной работы сервера
    def get_max_busy_server_time(self):
        return max(self.busy_time_list)

    # Среднее время непрерывной работы сервера
    def get_avg_busy_server_time(self):
        return sum(self.busy_time_list) / len(self.busy_time_list)

    # Результаты функции распределения вероятностей времени непрерывной занятости сервера
    def get_probability_func(self, N):
        h = self.get_max_busy_server_time() / N # интервал, попадание в который обеспечивает вычисление вероятности
        busy_time_list = sorted(self.busy_time_list)
        busy_time_count = len(busy_time_list)

        h_list = [] # список нижних границ интервалов
        probability_list = [] # список результатов функции распределения вероятностей
        h_counter = h # счётчик общего времени
        counter = 0

        for i in range(busy_time_count - 1):
            time = busy_time_list[i]
            if time > h_counter:
                h_list.append(h_counter - h)
                probability_list.append(counter / float(busy_time_count))
                h_counter += h
            if time < h_counter:
                counter += 1
        h_list.append(h_counter)
        probability_list.append(1)

        return h_list, probability_list

    # Результаты функции плотности распределения времени непрерывной занятости сервера
    def get_distribution_func(self, N):
        h = self.get_max_busy_server_time() / N  # интервал, попадание в который обеспечивает вычисление вероятности
        busy_time_list = sorted(self.busy_time_list)
        busy_time_count = len(busy_time_list)

        h_list = [] # список нижних границ интервалов
        distribution_list = [] # список результатов функции плотности распределения
        h_counter = h  # счётчик общего времени
        counter = 0

        for i in range(busy_time_count):
            time = busy_time_list[i]
            if time > h_counter:
                h_list.append(h_counter - h)
                distribution_list.append(counter / busy_time_count)
                h_counter += h
                counter = 1
            if time < h_counter:
                counter += 1
        if time < h_counter:
            h_list.append(h_counter - h)
        else:
            h_list.append(h_counter)
        distribution_list.append(counter / busy_time_count)

        return h_list, distribution_list
