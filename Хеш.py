class HashTable:
    def __init__(self, size=5):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.load_factor_threshold = 0.7  # Пороговое значение для resize
        self.count = 0  # Количество элементов

    def _hash_function(self, key):
        """Простая хеш-функция"""
        return hash(key) % self.size

    def insert(self, key, value):
        """Вставка элемента"""
        index = self._hash_function(key)
        # Проверяем, не существует ли уже такой ключ
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value  # Обновляем значение
                return
        self.table[index].append([key, value])
        self.count += 1
        # Проверяем необходимость resize
        if self.count / self.size >= self.load_factor_threshold:
            self.resize()

    def search(self, key):
        """Поиск элемента"""
        index = self._hash_function(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None  # Элемент не найден

    def delete(self, key):
        """Удаление элемента"""
        index = self._hash_function(key)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                self.count -= 1
                return True
        return False  # Элемент не найден

    def resize(self):
        """Увеличение размера хеш-таблицы"""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0  # Обнуляем счетчик

        # Перехешируем все элементы
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def __str__(self):
        return str(self.table)

# Создаем хеш-таблицу с начальным размером 5
hash_table = HashTable(5)

# Добавляем 10 элементов
for i in range(10):
    key = f"key_{i}"
    value = f"value_{i}"
    print(f"Вставка: {key} -> {value}")
    hash_table.insert(key, value)
    print(f"Текущая таблица: {hash_table}")
    print(f"Размер: {hash_table.size}\n")

# Тестирование поиска
print("Тестирование поиска:")
for i in range(10):
    key = f"key_{i}"
    print(f"Поиск {key}: {hash_table.search(key)}")

# Тестирование удаления
print("\nТестирование удаления:")
for i in range(5):
    key = f"key_{i}"
    print(f"Удаление {key}: {hash_table.delete(key)}")
    print(f"Текущая таблица: {hash_table}")

# Проверка работы после удаления
print("\nПроверка оставшихся элементов:")
for i in range(5, 10):
    key = f"key_{i}"
    print(f"Поиск {key}: {hash_table.search(key)}")

def simple_hash(string):
    """
    Простая хеш-функция: сумма ASCII-кодов всех символов строки
    """
    hash_value = 0
    for char in string:
        hash_value += ord(char)  # ord() возвращает ASCII-код символа
    return hash_value

# Пример использования
print(simple_hash("hello"))  # Выведет сумму ASCII-кодов букв h, e, l, l, o


class HashDictionary:
    def __init__(self):
        self.storage = {}

    def add(self, key, value):
        """
        Добавление элемента в словарь
        """
        hash_key = simple_hash(key)
        self.storage[hash_key] = value

    def search(self, key):
        """
        Поиск значения по ключу
        """
        hash_key = simple_hash(key)
        return self.storage.get(hash_key, None)

    def __str__(self):
        return str(self.storage)


# Пример использования
hash_dict = HashDictionary()

# Добавление элементов
hash_dict.add("apple", "фрукт")
hash_dict.add("banana", "фрукт")
hash_dict.add("carrot", "овощ")

print("Словарь после добавления элементов:")
print(hash_dict)

# Поиск элементов
print("\nПоиск элементов:")
print(f"Значение для 'apple': {hash_dict.search('apple')}")
print(f"Значение для 'banana': {hash_dict.search('banana')}")
print(f"Значение для 'carrot': {hash_dict.search('carrot')}")
print(f"Значение для 'potato': {hash_dict.search('potato')}")  # Не существует
