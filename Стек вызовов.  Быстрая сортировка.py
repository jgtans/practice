import random
import timeit
import matplotlib.pyplot as plt

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Анализ стека для n = 5
print("Вычисление fibonacci(5):")
result = fibonacci(5)
print(f"Результат: {result}")

# fibonacci(5) → вызывает:
#     fibonacci(4) → вызывает:
#         fibonacci(3) → вызывает:
#             fibonacci(2) → вызывает:
#                 fibonacci(1) → возвращает 1
#                 fibonacci(0) → возвращает 0
#             fibonacci(1) → возвращает 1
#         fibonacci(2) → вызывает:
#             fibonacci(1) → возвращает 1
#             fibonacci(0) → возвращает 0
#     fibonacci(3) → вызывает:
#         fibonacci(2) → вызывает:
#             fibonacci(1) → возвращает 1
#             fibonacci(0) → возвращает 0
#         fibonacci(1) → возвращает 1

def max_divide_conquer(arr):
    if len(arr) == 1:
        return arr[0]

    mid = len(arr) // 2
    left_max = max_divide_conquer(arr[:mid])
    right_max = max_divide_conquer(arr[mid:])

    return max(left_max, right_max)

# Пример использования
arr = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Максимальный элемент: {max_divide_conquer(arr)}")

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Пример использования
arr = [3,6,8,10,1,4,7]
print(f"Исходный массив: {arr}")
print(f"Отсортированный массив: {quicksort(arr)}")

# Функция быстрой сортировки (QuickSort)
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Функция для сортировки вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Измерение времени выполнения
def measure_time(sort_func, arr):
    start = timeit.default_timer()
    sort_func(arr.copy())  # Используем копию массива
    end = timeit.default_timer()
    return end - start

# Тестирование и сравнение
sizes = [10, 100, 1000, 10000]  # Расширили диапазон размеров
quicksort_times = []
insertion_times = []

for size in sizes:
    test_arr = [random.randint(0, 1000) for _ in range(size)]

    # Измеряем время для QuickSort
    q_time = measure_time(quicksort, test_arr)
    # Измеряем время для Insertion Sort
    i_time = measure_time(insertion_sort, test_arr)

    quicksort_times.append(q_time)
    insertion_times.append(i_time)

    print(f"Размер списка: {size}")
    print(f"Quicksort: {q_time:.6f} сек")
    print(f"Insertion sort: {i_time:.6f} сек")
    print(f"Ускорение Quicksort: {i_time / q_time:.2f} раз\n")

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(sizes, quicksort_times, marker='o', label='Quicksort', color='blue')
plt.plot(sizes, insertion_times, marker='x', label='Insertion Sort', color='red')

plt.title('Сравнение производительности сортировок')
plt.xlabel('Размер массива')
plt.ylabel('Время выполнения (секунды)')
plt.xscale('log')  # Логарифмическая шкала для лучшей визуализации
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
