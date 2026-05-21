"""
Приложение для управления виртуальным магазином (корзиной покупок)
с возможностью сортировки товаров различными алгоритмами.
"""

import copy

# =========================== Модуль товаров ===========================

class Product:
    """Класс для представления товара в каталоге/корзине."""
    def __init__(self, name, category, price, weight, description=""):
        self.name = name
        self.category = category
        self.price = float(price)      # цена в рублях
        self.weight = float(weight)    # вес в кг
        self.description = description

    def __str__(self):
        # Краткое строковое представление для отображения в списке
        return f"{self.name} ({self.category}) | Цена: {self.price} руб. | Вес: {self.weight} кг | {self.description[:30]}..."

    def __repr__(self):
        return self.__str__()


class Catalog:
    """Хранилище всех доступных товаров."""
    def __init__(self):
        self.products = []  # список объектов Product

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, name):
        """Удаление товара по имени (для простоты)."""
        self.products = [p for p in self.products if p.name != name]

    def edit_product(self, name, **kwargs):
        """Редактирование характеристик товара по имени."""
        for p in self.products:
            if p.name == name:
                if 'name' in kwargs:
                    p.name = kwargs['name']
                if 'category' in kwargs:
                    p.category = kwargs['category']
                if 'price' in kwargs:
                    p.price = float(kwargs['price'])
                if 'weight' in kwargs:
                    p.weight = float(kwargs['weight'])
                if 'description' in kwargs:
                    p.description = kwargs['description']
                return True
        return False

    def find_product(self, name):
        """Поиск товара по имени."""
        for p in self.products:
            if p.name == name:
                return p
        return None

    def list_products(self):
        """Показать все товары каталога."""
        for i, p in enumerate(self.products, start=1):
            print(f"{i}. {p}")


# =========================== Модуль корзины ===========================

class Cart:
    """Корзина покупок (список товаров)."""
    def __init__(self):
        self.items = []  # список объектов Product

    def add_item(self, product):
        self.items.append(product)

    def remove_item(self, index):
        """Удаление по индексу (1-based)."""
        if 1 <= index <= len(self.items):
            del self.items[index-1]
            return True
        return False

    def clear(self):
        self.items.clear()

    def total_cost(self):
        """Суммарная стоимость всех товаров в корзине."""
        return sum(item.price for item in self.items)

    def total_weight(self):
        """Суммарный вес (может пригодиться)."""
        return sum(item.weight for item in self.items)

    def display(self):
        """Отображает содержимое корзины с нумерацией."""
        if not self.items:
            print("Корзина пуста.")
            return
        print("\nТовары в корзине:")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item}")
        print(f"Итого: {self.total_cost()} руб. | Общий вес: {self.total_weight():.2f} кг")

    def __len__(self):
        return len(self.items)


# =========================== Модуль сортировки ===========================

class SortingAlgorithms:
    """
    Статические методы для реализации различных алгоритмов сортировки.
    Каждый алгоритм получает список товаров и ключ сортировки (функция),
    возвращает новый отсортированный список (не изменяя исходный).
    """

    @staticmethod
    def bubble_sort(items, key_func, reverse=False):
        """
        Пузырьковая сортировка (Bubble Sort).
        Для демонстрации промежуточных этапов печатает состояние.
        """
        arr = items[:]  # копируем
        n = len(arr)
        for i in range(n-1):
            swapped = False
            for j in range(n-1-i):
                # Сравнение с учётом порядка (reverse)
                if (key_func(arr[j]) > key_func(arr[j+1])) ^ reverse:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swapped = True
            # Для визуализации выводим промежуточное состояние
            print(f"  Bubble step {i+1}: {[p.name for p in arr]}")
            if not swapped:
                break
        return arr

    @staticmethod
    def insertion_sort(items, key_func, reverse=False):
        """Сортировка вставками (Insertion Sort)."""
        arr = items[:]
        for i in range(1, len(arr)):
            current = arr[i]
            j = i - 1
            # Сдвигаем элементы, пока не найдём место для вставки
            while j >= 0 and ((key_func(current) < key_func(arr[j])) ^ reverse):
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = current
            print(f"  Insertion step {i}: {[p.name for p in arr]}")
        return arr

    @staticmethod
    def quick_sort(items, key_func, reverse=False):
        """Быстрая сортировка (Quick Sort) — рекурсивная."""
        arr = items[:]
        def _quick(arr, low, high):
            if low < high:
                p = _partition(arr, low, high)
                _quick(arr, low, p-1)
                _quick(arr, p+1, high)
                # Выводим промежуточное состояние (не часто, но для демонстрации)
                print(f"  Quick partition on [{low},{high}]: {[p.name for p in arr]}")
        def _partition(arr, low, high):
            pivot_val = key_func(arr[high])
            pivot_idx = low
            for i in range(low, high):
                if (key_func(arr[i]) <= pivot_val) ^ reverse:
                    arr[i], arr[pivot_idx] = arr[pivot_idx], arr[i]
                    pivot_idx += 1
            arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
            return pivot_idx
        _quick(arr, 0, len(arr)-1)
        return arr

    @staticmethod
    def merge_sort(items, key_func, reverse=False):
        """Сортировка слиянием (Merge Sort)."""
        arr = items[:]
        def _merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if (key_func(left[i]) <= key_func(right[j])) ^ reverse:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        def _msort(lst):
            if len(lst) <= 1:
                return lst
            mid = len(lst)//2
            left = _msort(lst[:mid])
            right = _msort(lst[mid:])
            merged = _merge(left, right)
            print(f"  Merge: {[p.name for p in merged]}")
            return merged
        return _msort(arr)


# =========================== Пользовательский интерфейс ===========================

class ShopUI:
    """Текстовый интерфейс для взаимодействия с пользователем."""
    def __init__(self):
        self.catalog = Catalog()
        self.cart = Cart()
        self.sorting = SortingAlgorithms()
        self._init_catalog()  # заполняем каталог тестовыми данными

    def _init_catalog(self):
        """Заполнение каталога несколькими товарами для демонстрации."""
        products_data = [
            ("Ноутбук", "Электроника", 55000, 2.5, "Игровой ноутбук"),
            ("Мышь", "Электроника", 1200, 0.15, "Беспроводная"),
            ("Книга", "Книги", 800, 0.5, "Фантастика"),
            ("Футболка", "Одежда", 1500, 0.2, "Хлопок"),
            ("Часы", "Аксессуары", 5000, 0.1, "Смарт-часы"),
            ("Наушники", "Электроника", 3000, 0.3, "Bluetooth"),
            ("Рюкзак", "Аксессуары", 3500, 1.2, "Водонепроницаемый"),
        ]
        for name, cat, price, weight, desc in products_data:
            self.catalog.add_product(Product(name, cat, price, weight, desc))

    def display_main_menu(self):
        print("\n" + "="*50)
        print("       ВИРТУАЛЬНЫЙ МАГАЗИН - УПРАВЛЕНИЕ КОРЗИНОЙ")
        print("="*50)
        print("1. Показать каталог товаров")
        print("2. Добавить товар в корзину (по имени)")
        print("3. Удалить товар из корзины (по номеру)")
        print("4. Показать корзину")
        print("5. Сортировать товары в корзине")
        print("6. Подсчитать итоговую стоимость корзины")
        print("7. Очистить корзину")
        print("8. Выйти")
        print("="*50)

    def show_catalog(self):
        print("\n--- КАТАЛОГ ТОВАРОВ ---")
        self.catalog.list_products()
        print("----------------------")

    def add_to_cart(self):
        name = input("Введите название товара для добавления: ").strip()
        product = self.catalog.find_product(name)
        if product:
            self.cart.add_item(product)
            print(f"Товар '{name}' добавлен в корзину.")
        else:
            print("Товар не найден в каталоге.")

    def remove_from_cart(self):
        if not self.cart.items:
            print("Корзина пуста.")
            return
        self.cart.display()
        try:
            idx = int(input("Введите номер товара для удаления: "))
            if self.cart.remove_item(idx):
                print("Товар удалён.")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Введите число.")

    def show_cart(self):
        self.cart.display()

    def sort_cart(self):
        """Организует выбор алгоритма сортировки, ключа и направления."""
        if len(self.cart) < 2:
            print("В корзине недостаточно товаров для сортировки (нужно хотя бы 2).")
            return

        print("\n--- СОРТИРОВКА КОРЗИНЫ ---")
        # Выбор критерия
        print("Критерий сортировки:")
        print("1. По цене")
        print("2. По весу")
        print("3. По категории (по алфавиту)")
        crit_choice = input("Ваш выбор (1-3): ").strip()
        if crit_choice == '1':
            key_func = lambda p: p.price
            crit_name = "цене"
        elif crit_choice == '2':
            key_func = lambda p: p.weight
            crit_name = "весу"
        elif crit_choice == '3':
            key_func = lambda p: p.category.lower()
            crit_name = "категории"
        else:
            print("Неверный выбор.")
            return

        # Выбор порядка
        print("\nПорядок сортировки:")
        print("1. По возрастанию")
        print("2. По убыванию")
        order_choice = input("Ваш выбор (1-2): ").strip()
        reverse = (order_choice == '2')
        order_name = "убыванию" if reverse else "возрастанию"

        # Выбор алгоритма
        print("\nАлгоритм сортировки:")
        print("1. Пузырьковая (Bubble Sort)")
        print("2. Вставками (Insertion Sort)")
        print("3. Быстрая (Quick Sort)")
        print("4. Слиянием (Merge Sort)")
        algo_choice = input("Ваш выбор (1-4): ").strip()

        # Копируем исходные товары для вывода промежуточных этапов
        original_items = self.cart.items[:]
        print(f"\nНачальный список (до сортировки): {[p.name for p in original_items]}")
        print(f"Сортируем по {crit_name}, {order_name} с помощью ", end='')

        # Применяем выбранный алгоритм
        if algo_choice == '1':
            print("Пузырьковой сортировки:\n")
            sorted_items = self.sorting.bubble_sort(original_items, key_func, reverse)
        elif algo_choice == '2':
            print("Сортировки вставками:\n")
            sorted_items = self.sorting.insertion_sort(original_items, key_func, reverse)
        elif algo_choice == '3':
            print("Быстрой сортировки:\n")
            sorted_items = self.sorting.quick_sort(original_items, key_func, reverse)
        elif algo_choice == '4':
            print("Сортировки слиянием:\n")
            sorted_items = self.sorting.merge_sort(original_items, key_func, reverse)
        else:
            print("Неверный выбор алгоритма.")
            return

        # Обновляем корзину
        self.cart.items = sorted_items
        print("\nИТОГОВЫЙ ОТСОРТИРОВАННЫЙ СПИСОК:")
        self.cart.display()

    def total_cost(self):
        """Подсчёт общей стоимости с опциональной скидкой/налогом."""
        total = self.cart.total_cost()
        print(f"\nОбщая стоимость товаров в корзине: {total} руб.")
        # Дополнительная опция: скидка/налог
        choice = input("Применить скидку/налог? (y/n): ").lower()
        if choice == 'y':
            try:
                discount = float(input("Введите процент скидки (0-100): "))
                tax = float(input("Введите процент налога (0-100): "))
                after_discount = total * (1 - discount/100)
                final = after_discount * (1 + tax/100)
                print(f"Скидка {discount}%: {total} -> {after_discount:.2f} руб.")
                print(f"Налог {tax}%: {after_discount:.2f} -> {final:.2f} руб.")
                print(f"ИТОГО К ОПЛАТЕ: {final:.2f} руб.")
            except:
                print("Ошибка ввода.")
        else:
            print("Спасибо за покупку!")

    def run(self):
        """Главный цикл приложения."""
        while True:
            self.display_main_menu()
            choice = input("Выберите действие (1-8): ").strip()
            if choice == '1':
                self.show_catalog()
            elif choice == '2':
                self.add_to_cart()
            elif choice == '3':
                self.remove_from_cart()
            elif choice == '4':
                self.show_cart()
            elif choice == '5':
                self.sort_cart()
            elif choice == '6':
                self.total_cost()
            elif choice == '7':
                self.cart.clear()
                print("Корзина очищена.")
            elif choice == '8':
                print("До свидания!")
                break
            else:
                print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    app = ShopUI()
    app.run()