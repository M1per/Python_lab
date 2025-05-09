# Лабораторная работа №4


# Задание 1
*Условие задания:* 

Замыкание реализующее последовательность Фибоначчи используя декоратор.


*Ход решения:* 

*Замыкание для последовательность Фибоначи:*

Создаю функцию fibonacci_closure, которая инициализирует первые два числа последовательности Фибоначчи: a = 0 и b = 1.
Внутри этой функции определяю вложенную функцию next_fibonacci, которая возвращает текущее значение a и обновляет значения a и b для следующего вызова.
Использую nonlocal, чтобы изменять переменные a и b из внешней функции.
Функция fibonacci_closure возвращает функцию next_fibonacci, которая при каждом вызове будет возвращать следующее число Фибоначчи.


*Декоратор:*

Создаю декоратор counter_decorator, который принимает функцию func в качестве аргумента.
Внутри декоратора создаю переменную count, которая будет отслеживать количество вызовов функции.
Определяю вложенную функцию wrapper, которая увеличивает счетчик count, вызывает функцию func и выводит номер вызова и результат.
Декоратор возвращает функцию wrapper.

*Создание и использование замыкания и декоратора:*

Создается замыкание fibonacci_closure(), которое возвращает функцию next_fibonacci.
Затем эта функция передается в декоратор counter_decorator, который возвращает обернутую версию функции next_fibonacci с добавленным счетчиком вызовов.
Результат сохраняется в переменную fib


*Результат работы кода:* 

![image](https://github.com/user-attachments/assets/42939443-bde5-4552-aa9b-7b7a8889ad3e)




# Задание 2 

*Условие задания:* 

Декоратор для кэширования результатов выполнения функций используя декоратор.


*Ход решения:* 

*Декоратор для кэширования:*

Создаю функцию cache_decorator, которая принимает функцию func в качестве аргумента.
Внутри декоратора создаю словарь cache, который будет хранить результаты вычислений.
Определяю вложенную функцию wrapper, которая принимает один аргумент x.
Внутри wrapper проверяю, есть ли результат для аргумента x в кэше. Если результат есть, выводится сообщение "Результат из кэша:" и возвращает значение из кэша.
Если результата нет в кэше, вызывается функцию func(x), сохраняется результат в кэше и выводится сообщение "Результат вычислен и закэширован:".
Декоратор возвращает функцию wrapper.

*Замыкание с кэширующей функцией:*

Создаю функцию create_closure, которая определяет вложенную функцию cached_function.
Применю декоратор cache_decorator к функции cached_function, чтобы добавить функциональность кэширования.
Функция cached_function выполняет вычисление (Я привел простой пример возведения в квадрат).
Функция create_closure возвращает замыкание cached_function
Создаю экземпляр замыкания, вызывая функцию create_closure.
Результат сохраняется в переменную closure


 *Резултат работы кода:* 

![image](https://github.com/user-attachments/assets/40931ed8-bf8c-47e0-9f3b-91a5cc0e10c0)



# Список источников:

1.  [Декораторы Python: пошаговое руководство](https://habr.com/ru/companies/otus/articles/727590/)
2.  [Замыкания и Декораторы](https://pyhub.ru/python-advanced/lecture-10-33-71/)
3.  [Кэширование функций в Python](https://myrusakov.ru/python-function-memoization.html)
