Delay Differential Equation Solver with Discontinuity Handling
This project implements a method for solving delay differential equations (DDEs) with a constant step size, taking into account the presence of discontinuity points.

📌 Description (на русском)
Метод решения дифференциальных уравнений с запаздывающим аргументом с постоянным шагом и учитывающий точки разрыва.

Параметры:
f : function
Функция, задающая дифференциальное уравнение.

h : function
Функция "истории" дифференциального уравнения.

delays : List[function]
Список функций запаздывания.

t0 : float
Начальная точка интегрирования.

tn : float
Конечная точка интегрирования.

steps : int
Количество шагов.

break_pointers : list
Список начальных точек разрыва и соответствующих значений функции.

Возвращает:
Список элементов вида [t0, u0, h, k_list] для вычисления значений решения на интервале [t0, tn].

📁 Structure
bash
Копировать
Редактировать
name.py            # Main implementation of the solver
README.md          # This file
🚀 Usage
python
Копировать
Редактировать
from name import your_function  # Заменить на реальное имя функции

t0 = 0
tn = 3


def history(t):
    if t == 0: return 1
    return 0


def f(t, nu):
    return nu[0] ** ((1 + 2 * t) ** 2)


def delay(t):
    return t / ((1 + 2 * t) ** 2)


result = combine_method(history = history, f = f, delays = [delay],t0 = t0, tn = tn, steps =  512, break_pointers = [])
