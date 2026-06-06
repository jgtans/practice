import requests
from abc import ABC, abstractmethod

# Базовый абстрактный класс
class Model(ABC):

    @abstractmethod
    def download(self, categories):
        """Загружает данные по указанным категориям"""
        pass

    @abstractmethod
    def to_dict(self, data):
        """Преобразует данные в словарь"""
        pass

# Наследник, реализующий синглтон
class Loader(Model):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Базовый URL для продуктов DummyJSON
        self.base_url = 'https://dummyjson.com/products/category/'

    def download(self, categories):
        """
        Загружает данные по указанным категориям.
        categories: список строк с названиями категорий
        возвращает список словарей с данными
        """
        all_data = []
        for cat in categories:
            url = self.base_url + cat
            try:
                response = requests.get(url)
                response.raise_for_status()  # выбросит исключение при ошибке HTTP
                data = response.json()
                # DummyJSON возвращает объект с ключом 'products'
                products = data.get('products', [])
                all_data.extend(products)
            except requests.RequestException as e:
                print(f"Ошибка загрузки категории '{cat}': {e}")
        return all_data

    def to_dict(self, data):
        """
        Преобразует данные (список продуктов) в словарь, где ключ - id продукта.
        """
        if not isinstance(data, list):
            return {}
        result = {}
        for product in data:
            # предполагаем, что у каждого продукта есть поле 'id'
            product_id = product.get('id')
            if product_id:
                result[product_id] = product
        return result

# Проверка работы
if __name__ == '__main__':
    # Создаём два экземпляра Loader – они будут одним и тем же объектом (синглтон)
    loader1 = Loader()
    loader2 = Loader()

    print(f"loader1 is loader2: {loader1 is loader2}")  # True

    # Загружаем данные по категориям
    categories = ["beauty", "smartphones"]
    raw_data = loader1.download(categories)
    print(f"Загружено продуктов: {len(raw_data)}")

    # Преобразуем в словарь
    dict_data = loader1.to_dict(raw_data)
    print(f"Словарь содержит {len(dict_data)} записей")

    # Выведем пару примеров
    for pid in list(dict_data.keys())[:3]:
        print(f"Продукт {pid}: {dict_data[pid].get('title', 'Без названия')}")






