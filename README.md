# Hashmap_Implementation
Hashmap Implementation utilizing chaining and open addressing.


## Table of Contents
1. [Overview](#Overview)
2. [Chaining](#Chaining)
3. [Open-Addressing](#Open-Addressing)
4. [Reflection](#Reflection)

## Overview
In this project, I implemented a Hashmap in two forms--separate chaining and open-addressing--using Python 3. The Hashmaps were created without using Python's built-in methods or data structures.

## Chaining
### Specification

The Hash table is stored in a dynamic array. In the event of a collision, chaining is utilized via a singly-linked list. Under this structure, key/value pairs are stored in linked list nodes.

### Implementation
* **put(self, key: str, value: object) -> None:** This method updates key/value pair in the hash map. If the key already exists, its associated value is replaced with the new value. Otherwise, a new key/value pair is added. The hash table is resized to double its current capacity when this method is called if the load size is equal to or greater than 1.0.

* **resize_table(self, new_capacity: int) -> None:** This method changes the capacity of the internal hash table while keeping existing key/value pairs in the new hash map. The method first checks if the new capacity is prime, and if it is not, uses the next prime number. Once the appropriate new capacity is determined, the method iterates through each bucket in the old hash table and adds the key/value pairs to the new hash table. The method then assigns the buckets in the new hash table and the new capacity to the old hash table.

* **table_load(self) -> float**: This method returns the current hash table load factor.

*  **empty_buckets(self) -> int**: This method returns the number of empty buckets that are in the hash table.

* **get(self, key: str) -> object**: This method returns the value associated with the given key.

* **contains_key(self, key: str) -> bool**: This method returns True if the entered key is present in the hash map. Otherwise, the method returns False.

* **remove(self, key: str) -> None**: This method removes the entered key and its associated value from the hash map. If the key is not contained in the hash map, however, the method does nothing.

* **get_keys_and_values(self) -> DynamicArray** This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.

* **clear(self) -> None**: This method clears the contents of the hash map without changing the underlying hash table capacity.

* **find_mode(da: DynamicArray) -> tuple\[DynamicArray, int]**: This method receives a dynamic array and returns a tuple that contains (1) a dynamic array comprising the mode (or mostly occurring) value of the given array and (2) an integer representing the highest frequency of occurrence for the mode value.

## Open-Addressing
### Specification
A dynamic array stores the hash table and uses open addressing in the event of a collision inside the dynamic array.

### Implementation
* **put(self, key: str, value: object) -> None**: This method updates a key/value pair in the hash map. If the entered key already exists in the hash map, its value is replaced with the new value. If, however, the key is not in the hash map, a new key/value pair is added. The method first checks to see if the table load factor is greater than or equal to 0.5. If so, the table is resized to double the current capacity of the table.

* **resize_table(self, new_capacity: int) -> None**: This method changes the capacity of the internal hash table while keeping existing key/value pairs in the new hash map. The method checks to see if the new capacity is prime, and if not, uses the next prime number. Once the new capacity is determined, the method iterates through the old hash table and puts each of the key/value pairs into the newly sized hash map. Then, the method reassigns the revised buckets and the new capacity to the old hash map.

* **table_load(self) -> float**: This method returns the current hash table load factor.

* **empty_buckets(self) -> int**: This method returns the number of empty buckets in the hash table.

* **get(self, key: str) -> object**: This method returns the value associated with the given key. However, if the key is not in the hash map, the method returns None.

* **contains_key(self, key: str) -> bool**: This method returns True if the given key is in the hash map; otherwise, it returns False.

* **remove(self, key: str) -> None**:  This method removes given key and its associated value from hash map. If the key is not in the hash map, it does nothing.

* **get_keys_and_values(self) -> DynamicArray**: This method returns a dynamic array where each index contains a tuple of a key/value pair in the hash map.

* **clear(self) -> None**: This method clears the contents of the hash map without changing the underlying hash table capacity.

* **__iter__(self)**: This method enables the hash map to iterate across itself.

* **__next__(self)**: This method returns the next item in the hash map, based upon the current location of the iterator.

## Reflection
This project was my first exposure to hash map implementation. This project reinforced my understanding that hash map collisions can be resolved in such ways as chaining and open addressing. Open addressing, in turn, can utilize various probing methods to handle collisions, such as linear or quadratic probing. This project could be improved by implementing quadratic probing, instead of iterating through the hash map. This is especially so since quadratic probing reduces the likelihood of too many elements clustering together. For purposes of open addressing, tombstones can be used to allow searches for a particular object to continue, while still simulating an "empty" space. Using a low load factor allows for the avoidance of collisions, but because a load factor that is too low might lead to poor usage of space, a balance must be struck to make the most efficient use of space while avoiding collisions.
