import asyncio
import aiohttp
import requests
import concurrent.futures
from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def download(self, categories):
        pass

    @abstractmethod
    def to_dict(self, data):
        pass

class Loader(Model):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.base_url = 'https://dummyjson.com/products/category/'

    # Синхронный метод – загружает все категории последовательно (используется как базовая функция)
    def download(self, categories):
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

    # Асинхронный метод (из предыдущего задания)
    async def download_async(self, categories):
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_category(session, cat) for cat in categories]
            results = await asyncio.gather(*tasks)
            all_data = []
            for products in results:
                if products:
                    all_data.extend(products)
            return all_data

    async def _fetch_category(self, session, category):
        url = self.base_url + category
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get('products', [])
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Ошибка загрузки категории '{category}': {e}")
            return []

    # Пакетная асинхронная загрузка (из предыдущего задания)
    async def download_batched(self, categories, batch_size=2):
        batches = self._split_into_batches(categories, batch_size)
        all_data = []
        async with aiohttp.ClientSession() as session:
            for batch in batches:
                tasks = [self._fetch_category(session, cat) for cat in batch]
                results = await asyncio.gather(*tasks)
                for products in results:
                    if products:
                        all_data.extend(products)
                await asyncio.sleep(0.5)
        return all_data

    # НОВЫЙ МЕТОД – многопоточная загрузка с ThreadPoolExecutor
    def download_threadpool(self, categories, batch_size=2, max_workers=None):
        """
        Загружает данные по категориям, используя пул потоков.
        Категории разбиваются на пакеты размера batch_size, каждый пакет обрабатывается
        в отдельном потоке с помощью executor.map и метода download.
        """
        batches = self._split_into_batches(categories, batch_size)
        all_data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # executor.map применяет self.download к каждому пакету параллельно
            results = executor.map(self.download, batches)
            for result in results:
                all_data.extend(result)
        return all_data

    @staticmethod
    def _split_into_batches(lst, n):
        """Разделяет список на подсписки длиной не более n."""
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    def to_dict(self, data):
        if not isinstance(data, list):
            return {}
        return {product['id']: product for product in data if 'id' in product}

if __name__ == '__main__':
    loader = Loader()
    categories = ['beauty', 'smartphones', 'laptops', 'fragrances', 'groceries']

    # Многопоточная загрузка с пакетами по 2 категории
    data = loader.download_threadpool(categories, batch_size=2, max_workers=3)
    print(f"Загружено продуктов (многопоточно): {len(data)}")

    # Преобразование в словарь
    products_dict = loader.to_dict(data)
    print(f"Словарь содержит {len(products_dict)} записей")
    for pid in list(products_dict.keys())[:3]:
        print(f"  {pid}: {products_dict[pid].get('title', 'Без названия')}")
