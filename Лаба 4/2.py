def cache_decorator(func):
    cache = {}  # Словарь для кэширования результатов

    def wrapper(x):  # Принимаем только один аргумент
        if x in cache:  # Проверяем, есть ли результат в кэше
            print("Результат из кэша:")
            return cache[x]
        result = func(x)  # Вызываем функцию с аргументом x
        cache[x] = result  # Сохраняем результат в кэше
        print("Результат вычислен и закэширован:")
        return result

    return wrapper

def create_closure():
    @cache_decorator
    def cached_function(x):
        return x * x  # Пример вычисления

    return cached_function

# Создаем замыкание с кэширующей функцией
closure = create_closure()

# Вызываем функцию несколько раз
print(closure(2))  # Результат вычислен и закэширован: 4
print(closure(2))  # Результат из кэша: 4
print(closure(3))  # Результат вычислен и закэширован: 9
print(closure(3))  # Результат из кэша: 9