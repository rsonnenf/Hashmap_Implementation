# Description: Implementation of a HashMap in two forms - separate chaining
# and via open addressing with quadratic probing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map. If key already exists in the
        hsah map, its value is replaced with the new value. If the key is
        not in the hash map, a new key/value pair is added.

        :param key: string representing the key of the key/value pair
        :param value: object associated with the key to be inserted.
        """

        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)

        # Get index
        index = self._hash_function(key) % self._capacity

        # Insert key/value if nothing is at the index
        if self._buckets[index] is None:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        # If something is already at that index
        else:
            j = 1
            quad_probe = index
            while self._buckets[quad_probe] is not None:
                # If item at this index is the key
                if self._buckets[quad_probe].key == key:
                    # If this was a tombstone, add key/value and increase size
                    if self._buckets[quad_probe].is_tombstone is True:
                        self._buckets[quad_probe] = HashEntry(key, value)
                        self._buckets[quad_probe].is_tombstone = False
                        self._size += 1
                    else:
                        # Do not increment size because just replacing value
                        self._buckets[quad_probe] = HashEntry(key, value)
                    return
                # Calculate next quadratic probe and increment j for next pass
                quad_probe = (index + j**2) % self._capacity
                j += 1

            # If we reach a quad_probe index that is not occupied, add and
            # increment size
            self._buckets[quad_probe] = HashEntry(key, value)
            self._size += 1



    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table while keeping
        existing key/value paris in the new hash map.

        :param new_capacity: int representing the new size of the hash map
        """
        if new_capacity <= self._size:
            return

        # Check if prime; if it is, use for new capacity
        if self._is_prime(new_capacity):
            resized_table = HashMap(new_capacity, self._hash_function)
            # If not prime, use next prime number
        else:
            resized_table = HashMap(self._next_prime(new_capacity),
                                    self._hash_function)
        # If new_capacity is 2, a prime number, set as capacity; was not
        # accounted for
        if new_capacity == 2:
            resized_table = HashMap(new_capacity, self._hash_function)
            resized_table._capacity = 2

        # Iterate through and add items
        for el in range(self._buckets.length()):
            if self._buckets[el] is not None:
                resized_table.put(self._buckets[el].key, self._buckets[
                    el].value)

        self._buckets = resized_table._buckets
        self._capacity = resized_table._capacity

    def table_load(self) -> float:
        """
        Returns current has table load factor.

        :return: float representing load factor
        """
        load_factor = self.get_size() / self._buckets.length()
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: int representing number of buckets in hash table
        """
        num_empty = self._capacity - self._size
        return num_empty

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. Returns None if the
        key is not in the hash map.

        :param key: str representing key for value to return

        :return: object associated with key
        """
        # Iterate through array
        for index in range(self._buckets.length()):
            # If there is an item at the index and it is not a tombstone
            if self._buckets[index] is not None:
                if self._buckets[index].key == key and self._buckets[
                    index].is_tombstone is False:
                    return self._buckets[index].value   # Return value
        return None



    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise returns False.

        :param key: str representing key being search for

        :return: bool representing whether key is in the hash map
        """
        for index in range(self._capacity):     # Iterate through array
            if self._buckets[index] is not None:    # If something is at index
                if self._buckets[index].key == key and \
                        self._buckets[index].is_tombstone is False:
                    return True # Return true if matches key and is not TS
        return False

    def remove(self, key: str) -> None:
        """
        Removes given key and its associated value from hash map. If key is
        not in the hash map, does nothing.

        :param key: string representing key/item pair to be removed.
        """

        for index in range(self._capacity): # Iterate through array
            if self._buckets[index] is not None:    # Something at index
                if self._buckets[index].key == key and self._buckets[index]\
                        .is_tombstone is False:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair in the hash map

        :return: DynamicArray containing tuples of key/value pairs in hash map
        """
        arr = DynamicArray()
        for index in range(self._buckets.length()): # Iterate through hash map
            if self._buckets[index] is not None and self._buckets[index]\
                    .is_tombstone is False: # Something at index, not TS
                # Append key and value tuple
                arr.append((self._buckets[index].key, self._buckets[
                    index].value))
        return arr

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying
        hash table capacity.
        """
        # Initialize new hashmap
        new_hash_table = HashMap(self._capacity, self._hash_function)
        # Associate properties of new_hash_table with self
        self._buckets = new_hash_table._buckets
        self._capacity = new_hash_table._capacity
        self._size = new_hash_table._size


    def __iter__(self):
        """
        Enables the hash map to iterate across itself
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based upon the current
        location of the iterator.
        """
        try:
            value = None
            # Skip over inactive items
            while value is None or value.is_tombstone == True:
                value = self._buckets[self.index] # Item at current index
                self.index += 1 # Increment index
        except DynamicArrayException:
            raise StopIteration
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
