import random

# Задание 1
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)

n = random.randint(3, 11)
print(f'\nЗадание 1: \nФакториал числа {n} - {factorial(n)}')

# Задание 2
def summ_list(m):
    sum = 0
    if len(m) == 0:
        return 0
    for i in m:
        sum += i
    return sum

m = [random.randint(1, 100) for _ in range(3)]
print(f'\nЗадание 2: \nСумма чисел {m} = {summ_list(m)}')

# Задание 3
def binary_search(arr, low, high, key):
    if high > low:
        mid = (high + low) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] > key:
            return binary_search(arr, low, mid - 1, key)
        else:
            return binary_search(arr, mid + 1, high, key)
    return -1

arr = []
for i in range(10):
    arr.append(random.randint(0, 50))
arr.sort()

num_key = random.randint(1, 10)
print(f'\nЗадание 3: \nОтсортированный список: {arr}')
print(f"Индекс числа {num_key}: {binary_search(arr, 0, 10, num_key)}")

# Задание 4

class Stack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return "Stack ПУСТ"
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return "Stack ПУСТ"
    def is_empty(self):
        return len(self.stack) == 0
    def size(self):
        return len(self.stack)

if __name__ == "__main__":
    stack = Stack()
    stack.push(7)
    stack.push(10)
    stack.push(True)
    stack.push(15)
    stack.push("list")
    stack.push(25)
    print(f'\nЗадание 4: \nТекущий стек: {stack.stack}')
    print(f'Удаляется элемент из вершины стека: {stack.pop()}')
    print("Верхний элемент стека:", stack.peek())
    print("Проверяем, пустой ли стек:", stack.is_empty())
    print("Размер стека:", stack.size())
    print("Текущий стек", stack.stack)















