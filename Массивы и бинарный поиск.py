import random
import timeit
import matplotlib.pyplot as plt

# Бинарный поиск
def binary_search(arr, key):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Тестирование
random_arr = sorted([random.randint(0,1000) for _ in range(0, 100)])
test_values = [random.choice(random_arr) for _ in range(3)]

for value in test_values:
    index = binary_search(random_arr, value)
    print(f"Поиск индекса элемента - {value}: {index}")

# Линейный поиск
def linear_search(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1

# Измеряем время выполнения
def measure_time(search_func, arr, key):
    start = timeit.default_timer()
    search_func(arr, key)
    end = timeit.default_timer()
    return end - start

# Сравнение времени выполнения
import random
import timeit
import matplotlib.pyplot as plt


# Линейный поиск
def linear_search(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1


# Бинарный поиск
def binary_search(arr, key):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# Функция измерения времени
def measure_time(search_func, arr, key):
    start = timeit.default_timer()
    search_func(arr, key)
    end = timeit.default_timer()
    return end - start


# Сравнение времени выполнения
sizes = [100, 1000, 10000, 100000]
binary_times = []
linear_times = []

for size in sizes:
    arr = sorted([random.randint(0, 1000) for _ in range(size)])
    key = random.choice(arr)

    binary_time = measure_time(binary_search, arr, key)
    linear_time = measure_time(linear_search, arr, key)

    binary_times.append(binary_time)
    linear_times.append(linear_time)

    advantage = linear_time / binary_time

    print(f"Размер списка: {size}")
    print(f"Бинарный поиск: {binary_time:.6f} сек")
    print(f"Линейный поиск: {linear_time:.6f} сек")
    print(f"Преимущество бинарного поиска: {advantage:.2f} раз\n")

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(sizes, binary_times, marker='o', label='Бинарный поиск', color='blue')
plt.plot(sizes, linear_times, marker='x', label='Линейный поиск', color='red')

plt.title('Сравнение времени выполнения поиска')
plt.xlabel('Размер списка')
plt.ylabel('Время выполнения (секунды)')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Временная сложность от О(lof n) до О(1) в лучшем случае.
# Пространственная сложность в итеративной версии O(1), в рекурсивной версии из-за стека вызовов O(log n) .












