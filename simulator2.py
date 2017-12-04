import matplotlib.pyplot as plt
from model import ServerModel

if __name__ == "__main__":
    T = int(input("Введите время работы сервера: "))
    L = 9
    Mt = float(input("Введите мат. ожидание времени поступления задачи: "))
    Ms = float(input("Введите мат. ожидание времени выполнения задачи сервером: "))
    Ds = Ms / 4.0
    print("Ожидаемая дисперсия времени поступления задачи: ", Mt ** 2)
    print("Ожидаемая дисперсия времени выполнения задачи сервером задачи: ", Ds)
    server_load_list = [] # список загруженности сервера
    server_p_failurу = [] # список вероятностей отказа сервера
    print("Выполняется моделирование.")
    result_model = None
    while True:
        server_model = ServerModel(T, L, Ms, Ds, Mt)
        server_model.run()
        server_load = server_model.get_server_load()
        server_load_list.append(server_load)
        server_p_failurу.append(server_model.get_p_failure())
        # print(server_model.not_run_task_counter)
        if server_load < 1 and server_model.not_run_task_counter == 0:
            print("""Потенциальная оптимальная конфигурация: 
                    Загруженность сервера - {};
                    Мат. ожидание времени поступления задачи - {};
                    Мат. ожидание времени выполнения задачи сервером - {};""".format(round(server_load, 6), round(Mt, 6), round(Ms, 6)))
            print("Запуск тестирования конфигурации.")
            avg_load = 0
            avg_not_run_tasks = 0
            test_server_model = ServerModel(T, L, Ms, Ds, Mt)
            for i in range(100):
                test_server_model.run()
                avg_load += test_server_model.get_server_load()
                avg_not_run_tasks += test_server_model.not_run_task_counter
            avg_load /= 100.0
            avg_not_run_tasks /= 100.0
            print("Среднее время загруженности сервера - ", avg_load)
            if avg_load < 1 and int(avg_not_run_tasks) == 0:
                print("Данная конфигурация успешно прошла тестирование.")
                result_model = server_model
                break
            else:
                print("Данная конфигурация не прошла тестирование.")
            print()
        elif server_load > 1:
            Mt += 0.01
        else:
            Mt -= 0.01
    print("Полная информация о результате моделирования с оптимальной конфигурацией:")
    print("Время работы сервера - ", T)
    print("Количество поступивших задач - ", result_model.task_counter)
    print("Количество задач не попавших в очередь - ", result_model.not_run_task_counter)
    print("Загруженность сервера - ", round(server_load, 6))
    print("Среднее время поступления задачи - ", round(result_model.get_avg_task_time(), 6))
    print("Среднее время выполнения задачи сервером - ", round(result_model.get_avg_server_time(), 6))
    print("Средняя длина очереди - ", round(result_model.get_avg_task_queue(), 6))
    print("Среднее время непрерывной работы сервера - ", round(result_model.get_avg_busy_server_time(), 6))
    print("Максимальное время непрерывной работы сервера - ", round(result_model.get_max_busy_server_time(), 6))
    f = plt.figure("{}, {}, {}".format(T, Mt, Ms))

    corr_steps = [i for i in range(1, int(result_model.task_counter / 2))]
    corr_list = []
    for step in corr_steps:
        corr_list.append(result_model.get_autocorr_by_runtime_task(step))
    plt.plot(corr_steps, corr_list)
    plt.title('Автокорреляция времени между выполненными задачами')
    plt.ylabel('Корреляция')
    plt.xlabel('Шаг сдвига')
    plt.grid(True)
    plt.show()



    plt.figure("BtwTime"+str(Mt))
    plt.plot(result_model.out_task_time_list)
    plt.title('Время между выполненными задачами')
    plt.ylabel('Время')
    plt.xlabel('Номер')
    plt.grid(True)
    plt.show()

    plt.figure("TaskTime"+str(Mt))
    plt.plot(result_model.time_task_list)
    plt.title('Время поступления задачи в очередь')
    plt.ylabel('Время')
    plt.xlabel('Номер')
    plt.grid(True)
    plt.show()

    plt.figure("SertverTime"+str(Mt))
    plt.plot(result_model.time_server_list)
    plt.title('Время выполнения задачи на сервере')
    plt.ylabel('Время')
    plt.xlabel('Номер')
    plt.grid(True)
    plt.show()


    plt.figure("LoadToFail"+str(Mt))
    sorted_list = sorted(zip(server_load_list, server_p_failurу))
    server_load_list = [x for x,_ in sorted_list]
    server_p_failurу = [y for _, y in sorted_list]
    plt.plot(server_load_list, server_p_failurу)
    plt.title('Зависимость вероятности отказа сервера от загруженности')
    plt.xlabel('Загруженность сервера')
    plt.ylabel('Вероятность отказа')
    plt.grid(True)
    plt.show()

    plt.figure("Fprob"+str(Mt))
    plt.plot(*result_model.get_probability_func(result_model.task_counter / 3))
    plt.title('Функция распределения вероятностей')
    plt.xlabel('Время непрерывной работы сервера')
    plt.ylabel('Вероятность')
    plt.grid(True)
    plt.show()

    plt.figure("Fdistr"+str(Mt))
    plt.plot(*result_model.get_distribution_func(result_model.task_counter / 3))
    plt.title('Функция плотности распределения')
    plt.xlabel('Время непрерывной работы сервера')
    plt.ylabel('Вероятность')
    plt.grid(True)
    plt.show()

