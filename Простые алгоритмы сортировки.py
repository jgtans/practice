def bubble_sort(arr):
    """
    Сортировка списка методом пузырька
    """
    n = len(arr)
    for i in range(n):
        # Флаг для оптимизации
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                # Меняем элементы местами
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # Если обменов не было, массив уже отсортирован
        if not swapped:
            break
    return arr

def selection_sort(arr):
    """
    Сортировка списка методом выбора
    """
    n = len(arr)
    for i in range(n):
        # Ищем минимальный элемент
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Меняем найденный минимальный элемент с первым
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    """
    Сортировка списка методом вставок
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        # Перемещаем элементы больше key
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


import random
import timeit
import matplotlib.pyplot as plt


def measure_sort_time(sort_func, arr):
    start = timeit.default_timer()
    sort_func(arr.copy())  # Используем копию, чтобы не сортировать исходный массив
    end = timeit.default_timer()
    return end - start


# Тестирование
sizes = [100, 200, 500, 1000, 2000]
bubble_times = []
selection_times = []
insertion_times = []

for size in sizes:
    test_list = [random.randint(0, 1000) for _ in range(size)]

    bubble_time = measure_sort_time(bubble_sort, test_list)
    selection_time = measure_sort_time(selection_sort, test_list)
    insertion_time = measure_sort_time(insertion_sort, test_list)

    bubble_times.append(bubble_time)
    selection_times.append(selection_time)
    insertion_times.append(insertion_time)

    print(f"Размер списка: {size}")
    print(f"Сортировка пузырьком: {bubble_time:.6f} сек")
    print(f"Сортировка выбором: {selection_time:.6f} сек")
    print(f"Сортировка вставками: {insertion_time:.6f} сек\n")

plt.figure(figsize=(12, 6))

plt.plot(sizes, bubble_times, marker='o', label='Сортировка пузырьком', color='red')
plt.plot(sizes, selection_times, marker='s', label='Сортировка выбором', color='blue')
plt.plot(sizes, insertion_times, marker='x', label='Сортировка вставками', color='green')

plt.title('Сравнение времени сортировки')
plt.xlabel('Размер списка')
plt.ylabel('Время выполнения (секунды)')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Все три алгоритма имеют временную сложность O(n2), а пространственная О(1)