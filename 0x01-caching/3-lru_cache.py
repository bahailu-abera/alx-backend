#!/usr/bin/env python3
"""
LIFOCache module
"""
from collections import deque
BaseCaching = __import__('base_caching').BaseCaching


class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class List:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_front(self, value):
        new_node = Node(value)
        new_node.next = self.head

        if self.head is not None:
            self.head.prev = new_node

        else:
            self.tail = new_node

        self.head = new_node

    def insert_end(self, value):
        new_node = Node(value)
        new_node.prev = self.tail

        if self.tail is not None:
            self.tail.next = new_node

        else:
            self.head = new_node

        self.tail = new_node

    def pop_front(self):
        if self.head is None:
            return

        self.head = self.head.next

        if self.head is not None:
            self.head.prev = None

    def pop_back(self):
        if self.tail is None:
            return

        prev = self.tail.prev

        self.tail = prev

        if self.tail is not None:
            self.tail.next = None

    def front(self):
        return self.head

    def back(self):
        return self.tail

    def erase(self, node):
        if node is None:
            return

        prev = node.prev
        next = node.next

        if prev is not None:
            prev.next = next

        else:
            self.head = next

        if next is not None:
            next.prev = prev
        else:
            self.tail = prev


class LRUCache(BaseCaching):
    """
    LRU based caching system
    """
    def __init__(self):
        """
        Initialize
        """
        super().__init__()
        self.order = List()

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print("{}: {}".format(key, self.cache_data.get(key).data[1]))

    def put(self, key, item):
        """
        Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            node = self.cache_data[key]
            self.order.erase(node)

            self.order.insert_front((key, item))
            self.cache_data[key] = self.order.front()

            return

        if len(self.cache_data) == BaseCaching.MAX_ITEMS:
            lru = self.order.back()
            lru_key = lru.data[0]
            print("DISCARD: {}".format(lru_key))
            del self.cache_data[lru_key]
            self.order.pop_back()

        self.order.insert_front((key, item))
        self.cache_data[key] = self.order.front()

    def get(self, key):
        """
        Get an item by key
        """

        if key not in self.cache_data:
            return None

        node = self.cache_data[key]
        item = node.data[1]

        self.order.erase(node)

        self.order.insert_front((key, item))

        self.cache_data[key] = self.order.front()

        return item
