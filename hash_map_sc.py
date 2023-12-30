# Description: Implementation of a HashMap using separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates key/value pair in the hash map. If the key already exists,
        its associated value is replaced with the new value. Otherwise,
        a new key/value pair is added.

        :param key: string representing the key of the key/value pair
        :param value: object associated with the key to be inserted
        """
        if self.table_load() >= 1.0:
            self.resize_table(self.get_capacity()*2)

        # Get index
        index = self._hash_function(key) % self._capacity
        # Obtain the bucket at the index
        bucket = self._buckets[index]

        # If bucket contains nothing, add key
        if bucket.length() == 0:
            bucket.insert(key, value)
            self._size += 1
        else:  # If bucket contains list items, iterate for key
            for node in bucket:
                if node.key == key:     # Change value if key exists
                    node.value = value
                    return
            bucket.insert(key, value)   # If key not in linked list, add node
            self._size += 1

        return



    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of the internal hash table while keeping existing
        key/value pairs in the new hash map.

        :param new_capacity: integer representing the new capacity of the
        hash table.
        """

        if new_capacity < 1:
            return

        if new_capacity >= 1:
            # Check if prime; if it is, use for new capacity
            if self._is_prime(new_capacity):
                resized_table = HashMap(new_capacity, self._hash_function)

            else:
                # If not prime, use next prime number
                resized_table = HashMap(self._next_prime(new_capacity),
                                        self._hash_function)
        # If new_capacity is 2, a prime number, set as capacity; was not
        # accounted for
        if new_capacity == 2:
            resized_table = HashMap(new_capacity, self._hash_function)
            resized_table._capacity = 2

        for index in range(self._capacity):
            # If bucket contains nodes, put key & value in resized table
            if self._buckets[index] is not None:
                for node in self._buckets[index]:
                    resized_table.put(node.key, node.value)
        self._buckets = resized_table._buckets
        self._capacity = resized_table._capacity



    def table_load(self) -> float:
        """
        Returns current hash table load factor.

        :return: float representing hash table load factor.
        """
        load_factor = self.get_size()/self._buckets.length()
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: int representing number of buckets in hash table
        """
        num_empty = 0
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                num_empty += 1
        return num_empty

    def get(self, key: str):
        """
        Returns the value associated with the given key. If the key is not
        in the hash map, returns None.

        :param key: string representing the key for which the value will be
        returned
        """
        # Get index
        index = self._hash_function(key) % self._capacity
        # Obtain the bucket at the index
        bucket = self._buckets[index]

        # Iterate through linked list at index and obtain value of node if
        # present
        for node in bucket:
            if node.key == key:
                return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if key is in the hash map, otherwise returns False

        :param key: string representing key being searched for in hash map

        :return: boolean representing whether key is in hash map
        """
        # If empty hash map
        if self._size == 0:
            return False

        # Get index
        index = self._hash_function(key) % self._capacity
        # Obtain the bucket at the index
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                return True
        return False


    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.

        :param key: string representing key for which its value will be removed
        """

        # Get index
        index = self._hash_function(key) % self._capacity
        # Obtain the bucket at the index
        bucket = self._buckets[index]

        for node in bucket:
            if node.key == key:
                bucket.remove(key)
                self._size -= 1




    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a
        key/value pair stored in the hash map.

        :return: DynamicArray containing tuples of key/value pairs stored in
        the hash map.
        """

        new_array = DynamicArray()
        # Iterate through each item and obtain corresponding key/value pair
        # before adding to new_array
        for index in range(self._capacity):
            for bucket in self._buckets[index]:
                new_array.append((bucket.key, bucket.value))
        return new_array


    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying
        hash table capacity.
        """
        # Obtain old capacity
        table_capacity = self._capacity

        # Initialize new hash table
        new_hash_table = HashMap(table_capacity, self._hash_function)
        # Set new_hash_table values for hash table at issue
        self._buckets = new_hash_table._buckets
        self._size = new_hash_table._size
        self._capacity = new_hash_table._capacity



def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives a dynamic array and returns a tuple containing 1) dynamic array
    comprising the mode (mostly occurring) value of the given array, and (2)
    an integer representing the highest frequency of occurrence for the mode
    value.

    :param da: DynamicArray to for which mode will be obtained

    :return: tuple of a DynamicArray containing the mode and integer
    representing the highest frequency of occurrence for the mode.
    """

    map = HashMap()
    mode_list = DynamicArray()
    # Put items in da in map, with a value representing number of times
    # value has occurred.
    for index in range(da.length()):
        if map.contains_key(da[index]) is False:
            map.put(da[index], 1)
        else:
            map.put(da[index], map.get(da[index]) + 1)

    # Create new array containing keys and associated frequencies. Find
    # highest frequency.
    frequency = 0
    frequency_list = map.get_keys_and_values()
    # If iterated frequency is higher than current frequency, make new
    # frequency
    for index in range(frequency_list.length()):
        if frequency < frequency_list[index][1]:
            frequency = frequency_list[index][1]

    # Iterate through frequency array, and if associate frequency equals
    # designated highest frequency, add to list
    for index in range(frequency_list.length()):
        if frequency_list[index][1] == frequency:
            mode_list.append(frequency_list[index][0])

    return mode_list, frequency





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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
