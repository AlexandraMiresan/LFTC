
class HashTable:
    def __init__(self, capacity=101):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0
        self.next_position = 0

    def hash_function(self, key):
        """Compute a hash index without using Python's hash table."""
        category, value = key
        text = category + ":" + value

        hash_value = 0
        for char in text:
            hash_value = (
                hash_value * 31 + ord(char)
            ) % self.capacity

        return hash_value

    def insert(self, category, value):
        """Insert a symbol if it does not already exist."""
        key = (category, value)
        index = self.hash_function(key)

        # Search the bucket for an existing symbol.
        for entry in self.buckets[index]:
            if entry["key"] == key:
                return entry["position"]

        # Assign a unique symbol-table position.
        position = self.next_position
        self.next_position += 1

        self.buckets[index].append({
            "key": key,
            "position": position
        })

        self.size += 1
        return position

    def search(self, category, value):
        """Return the symbol-table position, or None."""
        key = (category, value)
        index = self.hash_function(key)

        for entry in self.buckets[index]:
            if entry["key"] == key:
                return entry["position"]

        return None

    def items(self):
        """Return all symbols with their assigned positions."""
        result = []

        for bucket in self.buckets:
            for entry in bucket:
                result.append((
                    entry["key"],
                    entry["position"]
                ))

        return result
