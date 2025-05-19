import inspect
from typing import List



six_step_c = [
    0,
    2 / 5,
    16 / 51,
    8 / 17,
    19 / 20,
    1
]

six_step_a = [
    [0],
    [lambda tetta: tetta],
    [lambda tetta: tetta - (tetta ** 2) * (5 / 4), lambda tetta: (tetta ** 2) * (5 / 4), lambda tetta: 0],
    [lambda tetta: 2 / 17, lambda tetta: 0, lambda tetta: 6 / 17],
    [lambda tetta: tetta - (tetta ** 2) * (85 / 32) + (tetta ** 3) * (289 / 128),
     lambda tetta: 0,
     lambda tetta: (tetta ** 2) * (153 / 32) - (tetta ** 3) * (867 / 128),
     lambda tetta: -(tetta ** 2) * (17 / 8) + (tetta ** 3) * (289 / 64)],
    [lambda tetta: tetta - (tetta ** 2) * (483 / 304) + (tetta ** 3) * (85 / 114),
     lambda tetta: 0,
     lambda tetta: 0,
     lambda tetta: (tetta ** 2) * (5491 / 2608) - (tetta ** 3) * (1445 / 978),
     lambda tetta: -(tetta ** 2) * (1600 / 3097) + (tetta ** 3) * (6800 / 9291)]
]

six_step_b = [
    lambda tetta: tetta - (tetta ** 2) * (635 / 304) + (tetta ** 3) * (823 / 456) - (tetta ** 4) * (85 / 152),
    lambda tetta: 0,
    lambda tetta: 0,
    lambda tetta: (tetta ** 2) * (93347 / 23472) - (tetta ** 3) * (63869 / 11736) + (tetta ** 4) * (24565 / 11736),
    lambda tetta: -(tetta ** 2) * (32000 / 3097) + (tetta ** 3) * (200000 / 9291) - (tetta ** 4) * (34000 / 3097),
    lambda tetta: (tetta ** 2) * (76 / 9) - (tetta ** 3) * (161 / 9) + (tetta ** 4) * (85 / 9)
]



def binary_search_last(arr: List[list], target: float):
    """
        Выполняет модифицированный бинарный поиск, чтобы найти последний индекс элемента,
        у которого первое значение в подсписке меньше заданного значения target.

        Параметры:
        arr : List[list]
            Отсортированный список элементов вида [t0, u0, h, [k1,k2,k3,k4,k5,k6]] .
            Предполагается, что arr[i][0] упорядочены по возрастанию.
        target : float
            Целевое значение, с которым сравниваются первые элементы подсписков.

        Возвращает:
        int
            Индекс последнего элемента, в который попадает наш target.
            Если такого элемента нет, возвращает -1."""

    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid][0] < target:
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result


# вычисления значения nu из прошлого
def past_nu(my_list, delay_dot, break_point, index_of_delay, history):
    """
            Определяет значение функции в точке из прошлого с помощью этапного интерполянта или же с помощью истории.

            Параметры:
            my_list : List[list]
            Отсортированный список элементов вида [t0, u0, h, [k1,k2,k3,k4,k5,k6]] .
            Предполагается, что arr[i][0] упорядочены по возрастанию.
            delay_dot : float
                точка запаздывания.

            break_point : List[ * ] * -
            элемент вида [точка разрыва, указатель ветви (-1 левая, 1 правая), точка из которой попали в точку разрыва, индекс функции запаздывания]

            index_of_delay: Integer - индекс текущего запаздывания

            Возвращает:
            float
                Значение функции в точке """

    # определяем в какой интервал попадает точка запаздывания
    index = binary_search_last(my_list, delay_dot)
    if delay_dot == 0:

        pass
    element = None

    # если на текущем шаге нет точек разрыва или точки разрыва есть, но другой функции запаздывания, то вычисляем значение стандартно
    if break_point == [] or not any(sublist[3] == index_of_delay for sublist in break_point):

        # если не нашлось интервала, значит точка запаздывания попала в историю
        if index == -1:
            return history(delay_dot)

        # хранит t0 u0 k_list интервала в который попала наша точка запаздывания
        element = my_list[index]

    # если для вычисления значения точки запаздывания необходимо учесть ветку по которой она вычисляется
    else:

        """
        left хранит в себе точки разрыва при попадани в интервал которых мы должны брать левую ветку
        right хранит в себе точки разрыва при попадани в интервал которых мы должны брать правую ветку
        """
        left = []
        right = []

        # находим эти точки
        for pair in break_point:
            if pair[3] == index_of_delay:
                if pair[1] == 1:
                    right = pair
                else:
                    left = pair

        """
        если index -1 значит наша точка запаздывания попала в историю 
        и мы берем значение из истории, кроме случая когда нам надо учитывать точку разрыва,
         которая лежит на стыке истории и нашего интерполнята
        """
        if index == -1:
            if right != []:

                if my_list[0][0] == right[0]:
                    element = my_list[0]
                else:
                    return history(delay_dot)
            else:

                return history(delay_dot)


        # если попали не в историю
        else:
            if left != []:
                # строим решение по левой ветке
                if my_list[index][0] == left[0]:
                    if index - 1 < 0: return history(delay_dot)
                    element = my_list[index - 1]

            if right != []:
                # строим решение по правой ветке
                if my_list[index + 1][0] == right[0]:
                    element = my_list[index + 1]
                else:

                    element = my_list[index]
            # если нет точек разрыва которые надо учитывать то просто берем тот интервал в который попали
            if element is None:
                element = my_list[index]

    tn = element[0]
    nu = element[1]
    h = element[2]
    k_list = element[3]

    # при подсчете глобальной погрешности тк последний элемент имеет вид [tn, u0,[]]
    if k_list == []: return nu

    tetta = (delay_dot - tn) / h

    return nu + h * (
            six_step_b[0](tetta) * k_list[0] + six_step_b[3](tetta) * k_list[3] + six_step_b[4](tetta) * k_list[4] +
            six_step_b[5](tetta) * k_list[5])


def call_function(f, t=None, y=None, nu=None):
    """
        Универсальный вызов функции с передачей только тех аргументов, которые она действительно принимает.

        Параметры:
        f : function
            Функция, которую необходимо вызвать. Может принимать любые комбинации аргументов: t, y, nu.
        t : любой тип (по умолчанию None)
            Значение аргумента t, если он требуется вызываемой функции.
        y : любой тип (по умолчанию None)
            Значение аргумента y, если он требуется вызываемой функции.
        nu : любой тип (по умолчанию None)
            Значение аргумента nu, если он требуется вызываемой функции.

        Возвращает:
        Результат выполнения функции f с корректно подобранными аргументами.

        Примечание:
        Функция предназначена сделать предоставление входных данных универсальным """

    # Получаем список параметров функции
    sig = inspect.signature(f)
    params = sig.parameters

    # Формируем аргументы, которые нужны функции
    args = []
    for param in params:
        if param == "t":
            args.append(t)
        elif param == "y":
            args.append(y)
        elif param == "nu":
            args.append(nu)

    # Вызываем функцию с правильными аргументами
    return f(*args)


def combine_method(history,f, delays: List, t0: float, tn: float, steps: float, break_pointers: List):
    """
        Метод решения дифференциальных уравнений с запаздывающим аргументом с потстоянным шагом и учитывающий точки разрыва.

        Параметры:
        f : function
            Функция с  дифф уравнением

        h: function
            Функция "истории" дифф уравнения

        delays : List[function] function - функции запаздывания
            содержит функции запаздывания уравнения

        t0 : Float
            начальная точка
        tn : Float
            конечная точка
        steps : Integer
            кол-во шагов
        break_pointers: список начальных тчоек разрыва и значений функции в них
        Возвращает:
        Список элементов вида [t0,u0,h,k_list] для расчета значения решения  в инетрвале [t0,tn]

        """

    # добавляем начальную точку в точки разрыва

    break_points = []
    for i in break_pointers:
        break_points.append(i[0])


    package_t_u_k = []
    # длина шага
    h = (tn - t0) / steps

    """добавляем первый элемент,  который содержит начальную точку этого шага,
     значение в начальной точке и длину шага с которым вычислется интерполянт"""

    # новая часть высчитываем значение в нчальной точке если там точка разрыва то берем знач точки разырва если нет то из истории
    if any(point[0] == t0 for point in break_pointers):
        for point in break_pointers:
            if point[0] == t0:
                u0 = point[1]
    else:
        u0 = history(t0)
    #

    package_t_u_k.append([t0, u0, h, []])

    # хранит точки разрыва которые нужно учитывать на текущем шаге
    break_point = []

    while t0 < tn:

        if t0 + h > tn:
            h = tn - t0

        k_list = package_t_u_k[-1][3]

        # вычисляем коэффициенты k
        for i in range(0, 6):
            # print(t0)
            t1 = t0 + six_step_c[i] * h

            # вычисляем Yi
            y = package_t_u_k[-1][1] + h * sum(
                ki * six_step_a[i][index](six_step_c[i]) for index, ki in enumerate(k_list))

            # вычисляем nu_i адаптировано под случай нескольких запаздываний
            nu_i = []
            # храним точки у которых оверлепинг на 4 этапе
            delay_dot_with_overlap_on_4_stage = []
            # идем по списку delays и смотрим куда попадют точки
            for j, delay in enumerate(
                    delays):

                delay_dot = call_function(delay, t1, y)

                if delay_dot <= t0:  # no overlapping
                    # вычисляем значение с помощью этапного интерполянта в который попадает точка

                    nu_i.append(past_nu(package_t_u_k,
                                        delay_dot,
                                        break_point,
                                        j, history))
                else:

                    tetta = (delay_dot - t0) / h
                    nu_i.append(package_t_u_k[-1][1])
                    if i == 3:  # overlapping 4 step

                        nu_i[j] += h * sum(ki * six_step_a[i - 1][index](tetta) for index, ki in enumerate(k_list))
                        delay_dot_with_overlap_on_4_stage.append(j)


                    else:
                        nu_i[j] += h * sum(ki * six_step_a[i][index](tetta) for index, ki in enumerate(k_list))

            # если были точки с overlapping на 4 этапе
            if delay_dot_with_overlap_on_4_stage != []:
                y = package_t_u_k[-1][1]
                y += h * sum(ki * six_step_a[i - 1][index](six_step_c[3]) for index, ki in enumerate(k_list))

                k_4 = call_function(f, t1, y, nu_i)

                y = package_t_u_k[-1][1] + h * sum(
                    ki * six_step_a[i + 1][index](six_step_c[3]) for index, ki in enumerate(k_list)) + h * k_4 * \
                    six_step_a[4][3](six_step_c[3])
                # пересчитываем значения точек с overlappingом
                for jj in delay_dot_with_overlap_on_4_stage:
                    nu_i[jj] = package_t_u_k[-1][1] + h * sum(
                        ki * six_step_a[i + 1][index](tetta) for index, ki in enumerate(k_list)) + h * k_4 * \
                               six_step_a[4][3](tetta)

            k = call_function(f, t1, y, nu_i)

            package_t_u_k[-1][3].append(k)

        # хранит только новые точки разрыва которые определим на текущем шаге
        new_break_point = []
        """начинаем поиск точек разрыва в том случае, когда в break_point нет точек разрыва с -1 то есть,
         так как если есть точки с -1, значит это точки
         , которые мы определили на прошлой итерации и на этой итерации нам остается только завершить шаг,
          заканчивающийся в этой точке """

        if not any(sublist[1] == -1 for sublist in break_point):

            # определяем значения на концах текущего шага
            tetta_0 = 0
            u_0 = package_t_u_k[-1][1] + h * sum(ki * six_step_b[index](tetta_0) for index, ki in enumerate(k_list))

            tetta_1 = 1
            u_1 = package_t_u_k[-1][1] + h * sum(ki * six_step_b[index](tetta_1) for index, ki in enumerate(k_list))

            # перебираем известные точки разрыва
            for point in break_points:

                # перебираем функции запаздывания по индексам по самим функциям одновременно
                for jj, delay in enumerate(delays):

                    """вот это условие я добавил, чтобы избежать проблемы, когда мы находим точек запаздывания,
                    но ее точное значение остается справа и  из-за этого
                    на следующем шаге мы снова ее находим, разница между такими "клонами" 10^-12 поэтому это не дает большой погрешности"""
                    # то есть если мы рассматриваем точку запаздывания с функцией запаздывания и у нас уже сохранена эта точка с этим запаздыванием то мы пропускаем эту точку
                    if break_point != [] and any(
                            len(item) > 3 and item[3] == jj and item[0] == point for item in break_point):
                        continue
                    # условие определения точки разрыва в интервале

                    if (point - call_function(delay, t0, u_0)) * (point - call_function(delay, t0 + h, u_1)) <= 0:


                        a = t0
                        b = t0 + h
                        for _ in range(3):
                            tetta_a = (a - t0) / h
                            u_a = package_t_u_k[-1][1] + h * sum(
                                ki * six_step_b[index](tetta_a) for index, ki in enumerate(k_list))
                            tetta_b = (b - t0) / h
                            u_b = package_t_u_k[-1][1] + h * sum(
                                ki * six_step_b[index](tetta_b) for index, ki in enumerate(k_list))

                            if a == b:
                                x = a
                                break

                            x = a - (point - call_function(delay, a, u_a)) * (b - a) / (
                                    (point - call_function(delay, b, u_b)) - (point - call_function(delay, a, u_a)))

                            tetta_x = (x - t0) / h
                            u_x = package_t_u_k[-1][1] + h * sum(
                                ki * six_step_b[index](tetta_x) for index, ki in enumerate(k_list))

                            if (point - call_function(delay, a, u_a)) * (point - call_function(delay, x, u_x)) < 0:
                                b = x
                            else:
                                a = x

                        """если нет брейк поинтов добавляем найденный если есть
                         проверяем если точка левее то удаляем все имеющиеся и вставляем эту,
                         если правее не добавляем , если это та же точка но  у другого запаздывания добавляем"""
                        if not new_break_point:
                            new_break_point.append([point, -1, x, jj])
                        elif x < new_break_point[0][2]:
                            new_break_point.clear()
                            new_break_point.append([point, -1, x, jj])
                        elif x == new_break_point[0][2]:
                            new_break_point.append([point, -1, x, jj])

        if not new_break_point:  # если нет новых точек разрыва внутри шага то считаем шаг
            if any(sublist[1] == -1 for sublist in
                   break_point):  # условие на случай когда мы досчитываем шаг до точки разрыва, то есть в break_point есть точка с -1

                indexis = []  # определеяем индексы точек разрыва с -1
                for jjj, sublist in enumerate(break_point):
                    if sublist[1] == -1:
                        indexis.append(jjj)

                tetta = (break_point[indexis[0]][2] - t0) / h

                nu_ans = package_t_u_k[-1][1] + h * sum(
                    ki * six_step_b[index](tetta) for index, ki in enumerate(k_list))

                # досчитываю шаг до точки разрыва
                t0 = break_point[indexis[0]][2]
                package_t_u_k[-1][2] = h
                package_t_u_k.append([t0, nu_ans, h, []])

                """удаляем использованные точки разрыва а в тех точках которые указывали на левую ветку меняем -1 на 1
                 тк на следующем шаге нам нужно будет брать правую ветку при попаднии в интервал точки разрыва"""
                for jjj in range(len(break_point) - 1, -1, -1):
                    if break_point[jjj][1] == 1:
                        del break_point[jjj]
                    elif break_point[jjj][1] == -1:
                        break_point[jjj][1] = 1  # меняем -1 на 1

                continue

            else:  # если нет точек разрыва с -1
                # вычисляем значение на конце шага
                nu_ans = package_t_u_k[-1][1] + h * sum(ki * six_step_b[index](1) for index, ki in enumerate(k_list))
                t0 += h
                package_t_u_k[-1][2] = h
                package_t_u_k.append([t0, nu_ans, h, []])

                """удаляем брейк поинты тк они уже отработали,
                 здесь только точки с 1 то есть они указывали на правую ветку 
                 и на следуюещм шаге они нам будут уже неактуальны"""
                break_point = []

        else:
            """если на этом шаге нашли новые точки разрыва,
             то добавляем их к уже имеющимся,
              там лежат точки с 1 (то есть указывают на правую ветку) или не лежат вовсе"""
            break_point.extend(new_break_point)

            """удаляем вычисленные коэффиценты K тк они будут пересчитаны,
             это как раз тот момент что я изменил, я не засчитываю шаг с текущими K, а пересчитываю их"""
            package_t_u_k[-1][-1] = []
            break_points.append(new_break_point[0][2])
            new_break_point = []

    return package_t_u_k
