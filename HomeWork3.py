import functools
import requests
import tracemalloc

from collections import OrderedDict


def cache(max_limit=64):
    """ Caches data """
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            # Блок анализа кэша, проверяем есть ли данные в кэше
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                deco._counter.update({cache_key: deco._counter.get(cache_key) + 1})
                return deco._cache[cache_key]
            result = f(*args, **kwargs)

            # Блок удаления при достижении лимита
            # Сортируем значение счетчика по возрастанию
            # Выбираем первый ключ и удаляем по нему данные из кэша и из счетчика
            if len(deco._cache) >= max_limit:
                list_of_items = list(deco._counter.items())
                list_of_items.sort(key=lambda i: i[1])
                deco._cache.pop(list_of_items[0][0])
                deco._counter.pop(list_of_items[0][0])

            deco._cache[cache_key] = result
            deco._counter[cache_key] = 1
            return result

        deco._cache = OrderedDict()
        deco._counter = {}
        return deco
    return internal


def memory_profiler(f):
    """ Get recent value of used memory """
    @functools.wraps(f)
    def memory_deco(*args, **kwargs):
        tracemalloc.start()
        result = f(*args, **kwargs)
        memory = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        print("Recent memory: ", round(memory[0]/1024, 2), "KiB")
        return result
    return memory_deco


@memory_profiler
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


if __name__ == '__main__':
    max_limit_of_cache = int(input('Enter maximum size of cache: '))
    fetch_url = cache(max_limit_of_cache)(fetch_url)

    fetch_url('https://google.com')
    fetch_url('https://google.com')
    fetch_url('https://ithillel.ua')
    fetch_url('https://dou.ua')
    fetch_url('https://ain.ua')
    fetch_url('https://google.com')
    fetch_url('https://youtube.com')
    fetch_url('https://ithillel.ua')
    fetch_url('https://google.com')
    fetch_url(url='https://reddit.com')
