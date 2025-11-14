from collections import OrderedDict

class LRUCache:
    def __init__(self, limit):
        self.limit = limit
        self.cache = OrderedDict()

    def put(self, key, value):
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.limit:
                self.cache.popitem(last=False)
            self.cache[key] = value

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]


def main():
    cache = LRUCache(3)
    print(cache.put("a", 1))
    print(cache.put("b", 2))
    print(cache.get("a"))
    print(cache.put("c", 3))
    print(cache.get("b"))
    print(cache.put("d", 4))
    print(cache.get("a"))
    print(cache.get("c"))
    print(cache.get("d"))

if __name__ == "__main__":
    main()

