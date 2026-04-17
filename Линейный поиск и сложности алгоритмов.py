import random
import timeit
import matplotlib.pyplot as plt

def linear_search(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return -1

# Создаем список из 100 случайных чисел
random_list = [random.randint(0, 100) for _ in range(100)]

# Тестирование поиска
test_values = [random.choice(random_list) for _ in range(3)]

for value in test_values:
    start_time = timeit.default_timer()
    index = linear_search(random_list, value)
    end_time = timeit.default_timer()

    print(f"Поиск значения {value}:")
    print(f"Индекс: {index}")
    print(f"Время выполнения: {end_time - start_time:.6f} секунд\n")

def measure_search_time(size):
    arr = [random.randint(0, 1000) for _ in range(size)]
    key = random.choice(arr)
    start = timeit.default_timer()
    linear_search(arr, key)
    end = timeit.default_timer()
    return end - start

# Измеряем время для разных размеров
sizes = [10, 100, 1000, 10000]
times = []

for size in sizes:
    time_taken = measure_search_time(size)
    times.append(time_taken)
    print(f"Размер списка: {size}, Время: {time_taken:.6f} секунд")

plt.figure(figsize=(10, 6))
plt.plot(sizes, times, marker='o', linestyle='-')
plt.title('Зависимость времени выполнения от размера списка')
plt.xlabel('Размер списка')
plt.ylabel('Время выполнения (секунды)')
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()

plt.show()

# Для поиска последнего элемента временная сложность возрастает до O(n), так как алгоритму приходится перебирать весь массив.
# Алгоритм имеет признаки итеративного подхода(используется цикл for, нет вызова самого себя),
# пространственная сложность варьируется в зависимости от расположения искомого элемента в массиве


