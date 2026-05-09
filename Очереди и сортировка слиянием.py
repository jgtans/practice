import random
import timeit
import matplotlib.pyplot as plt

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Добавить элемент в конец очереди"""
        self.items.append(item)

    def dequeue(self):
        """Удалить и вернуть первый элемент очереди"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.items.pop(0)

    def is_empty(self):
        """Проверить, пуста ли очередь"""
        return len(self.items) == 0

    def peek(self):
        """Посмотреть первый элемент без удаления"""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self.items[0]

    def size(self):
        """Получить размер очереди"""
        return len(self.items)

class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

def process_tasks(tasks):
    task_queue = Queue()
    current_time = 0

    # Добавляем задачи в очередь
    for task in tasks:
        task_queue.enqueue(task)

    print("Обработка задач:")
    while not task_queue.is_empty():
        current_task = task_queue.dequeue()
        current_time += current_task.duration
        print(f"Задача {current_task.name} завершена в момент времени {current_time}")

# Пример использования
tasks = [
    Task("Задача 1", 5),
    Task("Задача 2", 3),
    Task("Задача 3", 8),
    Task("Задача 4", 2)
]

process_tasks(tasks)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Разделение массива
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # Рекурсивная сортировка
    left = merge_sort(left)
    right = merge_sort(right)

    # Слияние
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Добавление оставшихся элементов
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Пример использования
arr = [38, 27, 43, 3, 9, 82, 10]
print("Исходный массив:", arr)
print("Отсортированный массив:", merge_sort(arr))

# Функция пузырьковой сортировки
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Функция сортировки слиянием
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Функция измерения времени
def measure_time(sort_func, arr):
    start = timeit.default_timer()
    sort_func(arr.copy())  # Используем копию массива
    end = timeit.default_timer()
    return end - start

# Тестирование
sizes = [10, 100, 1000]
merge_sort_times = []
bubble_sort_times = []

for size in sizes:
    test_arr = [random.randint(0, 1000) for _ in range(size)]

    m_time = measure_time(merge_sort, test_arr)
    b_time = measure_time(bubble_sort, test_arr)

    merge_sort_times.append(m_time)
    bubble_sort_times.append(b_time)

    print(f"Размер списка: {size}")
    print(f"Сортировка слиянием: {m_time:.6f} сек")
    print(f"Пузырьковая сортировка: {b_time:.6f} сек")
    print(f"Ускорение: {b_time / m_time:.2f} раз\n")

# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(sizes, merge_sort_times, marker='o', label='Сортировка слиянием', color='blue')
plt.plot(sizes, bubble_sort_times, marker='x', label='Пузырьковая сортировка', color='red')

plt.title('Сравнение производительности сортировок')
plt.xlabel('Размер массива')
plt.ylabel('Время выполнения (секунды)')
plt.xscale('log')  # Логарифмическая шкала для лучшей визуализации
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()



