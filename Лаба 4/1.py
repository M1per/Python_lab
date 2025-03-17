def fibonacci_closure():
    a, b = 0, 1  # Инициализация первых двух чисел Фибоначчи

    def next_fibonacci():
        nonlocal a, b  # Используем nonlocal для изменения переменных из внешней функции
        result = a
        a, b = b, a + b  # Обновляем значения a и b
        return result

    return next_fibonacci

# Декоратор, который будет выводить номер вызова и значение
def counter_decorator(func):
    count = 0

    def wrapper():
        nonlocal count
        count += 1
        result = func()
        print(f"Вызов №{count}: {result}")
        return result

    return wrapper

# Применяем декоратор к замыканию
fib = counter_decorator(fibonacci_closure())

# Выводим первые 10 чисел Фибоначчи
for x in range(10):
    fib()