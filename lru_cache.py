
class QueryAPI:
    def __init__(self, memory_cache, reverse_index_cluster):
        self.memory_cache = memory_cache
        self.reverse_index_cluster = reverse_index_cluster

    def parse_query(self, query):
        """
        Normalize the query.
        - remove markup
        - tokenize
        - normalize case
        - typo handling
        """
        return query.lower().strip()

    def process_query(self, query):
        parsed_query = self.parse_query(query)

        results = self.memory_cache.get(parsed_query)
        if results:
            return results 

        results = self.reverse_index_cluster.process_search(parsed_query)
        self.memory_cache.set(parsed_query, results)

        return results

# -----------------------------
# Doubly Linked List Node
# -----------------------------
class Node:
    def __init__(self, query, results):
        self.query = query
        self.results = results
        self.prev = None
        self.next = None


# Doubly Linked List

class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def move_to_front(self, node):
        if node == self.head:
            return

        self._remove(node)
        self.append_to_front(node)

    def append_to_front(self, node):
        node.prev = None
        node.next = self.head

        if self.head:
            self.head.prev = node #part 1 of appending to the front

        self.head = node

        if self.tail is None:
            self.tail = node

    def remove_from_tail(self):
        if self.tail is None:  #part 2 of detaching the tail part
            return None

        old_tail = self.tail
        self._remove(old_tail)
        return old_tail

    def _remove(self, node):

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev



# LRU Cache
class Cache:

    def __init__(self, max_size):
        self.max_size = max_size
        self.lookup = {}
        self.list = DoublyLinkedList()

    def get(self, query):
        node = self.lookup.get(query)

        if node is None:
            return None

        self.list.move_to_front(node)
        return node.results

    def set(self, query, results):

        node = self.lookup.get(query)

        if node:
            node.results = results
            self.list.move_to_front(node)
            return

        if len(self.lookup) >= self.max_size:
            tail = self.list.remove_from_tail()
            if tail:
                del self.lookup[tail.query]

        new_node = Node(query, results)
        self.list.append_to_front(new_node)
        self.lookup[query] = new_node
