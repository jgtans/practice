import asyncio
import aiohttp
from abc import ABC, abstractmethod
import numpy as np  # для np.array_split, можно обойтись без numpy

# Базовый класс (без изменений)
class Model(ABC):
    @abstractmethod
    def download(self, categories):
        """Загружает данные по указанным категориям (синхронный вариант)"""
        pass

    @abstractmethod
    def to_dict(self, data):
        """Преобразует данные в словарь {id: product}"""
        pass

class Loader(Model):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.base_url = 'https://dummyjson.com/products/category/'

    # Синхронный метод (первое задание)
    def download(self, categories):
        import requests
        all_data = []
        for cat in categories:
            url = self.base_url + cat
            try:
                response = requests.get(url)
                response.raise_for_status()
                products = response.json().get('products', [])
                all_data.extend(products)
            except requests.RequestException as e:
                print(f"Ошибка загрузки категории '{cat}': {e}")
        return all_data

    #  Асинхронный метод (второе задание)
    async def download_async(self, categories):
        """
        Асинхронная загрузка всех категорий параллельно.
        Возвращает объединённый список продуктов.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_category(session, cat) for cat in categories]
            results = await asyncio.gather(*tasks)  # список списков продуктов (каждый список от одной категории)
            all_data = []
            for products in results:
                if products:  # при ошибке возвращаем пустой список
                    all_data.extend(products)
            return all_data

    async def _fetch_category(self, session, category):
        """Загружает одну категорию. В случае ошибки возвращает пустой список."""
        url = self.base_url + category
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get('products', [])
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Ошибка загрузки категории '{category}': {e}")
            return []

    # Пакетная обработка (задание повышенной сложности)
    async def download_batched(self, categories, batch_size=2):
        """
        Загружает категории пакетами (пакетная обработка).
        Внутри каждого пакета запросы выполняются параллельно.
        Пакеты обрабатываются последовательно, чтобы не перегружать сервер.
        """
        # Разделяем список категорий на пакеты
        # np.array_split или обычный код
        batches = self._split_into_batches(categories, batch_size)

        all_data = []
        async with aiohttp.ClientSession() as session:
            for batch in batches:
                tasks = [self._fetch_category(session, cat) for cat in batch]
                results = await asyncio.gather(*tasks)
                for products in results:
                    if products:
                        all_data.extend(products)
                # Пауза между пакетами(по желанию #):
                await asyncio.sleep(0.5)
        return all_data

    @staticmethod
    def _split_into_batches(lst, n):
        """Разделить список на подсписки длиной до n (без numpy)."""
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    # Общий метод to_dict (без правок)
    def to_dict(self, data):
        if not isinstance(data, list):
            return {}
        return {product['id']: product for product in data if 'id' in product}

# Пример использования
if __name__ == '__main__':
    loader = Loader()

    # Проверка синглтона
    loader2 = Loader()
    print(f"Синглтон работает: {loader is loader2}")

    # Синхронный запуск (для сравнения)
    # synch_data = loader.download(['beauty', 'smartphones'])
    # print(f"Синхронно загружено: {len(synch_data)}")

    # Асинхронный запуск (основной)
    async def run_async():
        data = await loader.download_async(['beauty', 'smartphones', 'laptops'])
        print(f"Асинхронно загружено продуктов: {len(data)}")
        products_dict = loader.to_dict(data)
        print(f"Словарь содержит {len(products_dict)} записей")
        for pid in list(products_dict.keys())[:3]:
            print(f"  Продукт {pid}: {products_dict[pid].get('title', 'Без названия')}")

    # Запускаем асинхронный код
    asyncio.run(run_async())

    # Пакетная обработка
    async def run_batched():
        data = await loader.download_batched(
            ['beauty', 'smartphones', 'laptops', 'fragrances', 'groceries'],
            batch_size=2
        )
        print(f"Пакетная загрузка: {len(data)} продуктов")

    asyncio.run(run_batched())