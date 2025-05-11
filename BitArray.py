import random
from typing import Union,Iterable,Optional


class BitArray:
    def __init__(self, size_or_str, default_value=0):
        if isinstance(size_or_str, int):
            if size_or_str < 0:
                raise ValueError("Size must be a non-negative integer.")
            self.size = size_or_str
            self.byte_array = bytearray((self.size + 7) // 8)
            #only using setall method if default value is specified as 1 because byte array by default is initialised with 0s. 
            if default_value == 1:                       
                self.setall(1)
        
        elif isinstance(size_or_str, str):
            if not all(bit in '01' for bit in size_or_str):
                raise ValueError("Binary string can only contain '0' or '1'.")
            self.size = len(size_or_str)
            self.byte_array = bytearray((self.size + 7) // 8)
            for i, bit in enumerate(size_or_str):
                if bit == '1':
                    self[i] = 1
        
        elif isinstance(size_or_str, list) and all(isinstance(b, bool) for b in size_or_str):
            self.size = len(size_or_str)
            self.byte_array = bytearray((self.size + 7) // 8)
            for i, bit in enumerate(size_or_str):
                if bit:
                    self[i] = 1
        else:
            raise TypeError("Argument must be an integer(size), a binary string, or a list of booleans.")   
        
    #set item for some index with value i.e object[index]=value
    def __setitem__(self, index, value):
        if not (0 <= index < self.size):
            raise IndexError("Bit index out of range")
        if value not in (0, 1):
            raise ValueError("Bit value must be 0 or 1")
        byte_index = index // 8
        bit_index = index % 8
        if value:
            self.byte_array[byte_index] |= (1 << (7 - bit_index))
        else:
            self.byte_array[byte_index] &= ~(1 << (7 - bit_index))

    #get value at some index i.e object[index]
    def __getitem__(self, index):
        if isinstance(index, slice):
            return BitArray(str(self)[index]) 
        elif isinstance(index, int):
            if not (0 <= index < self.size):
                raise IndexError("Bit index out of range")
            byte_index = index // 8
            bit_index = index % 8
            return (self.byte_array[byte_index] >> (7 - bit_index)) & 1
        else:
            raise TypeError("Invalid index type")

    def __str__(self):
        return ''.join(str(self[i]) for i in range(self.size))

    #set all the value with some 0 or 1
    def setall(self, value):
        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        byte_value = 0xFF if value == 1 else 0x00
        self.byte_array[:] = bytes([byte_value]) * len(self.byte_array)

    #Removes and Return the value at the given index(default last)
    def pop(self, index=None):
        if self.size == 0:
            raise IndexError("Empty BitArray")

        if index is None:
            index = self.size - 1  

        if not (0 <= index < self.size):
            raise IndexError("Bit index out of range")
        
        removed_bit = self[index]

        for i in range(index, self.size - 1):
            self[i] = self[i + 1]

        self[self.size - 1]=0

        self.size -= 1  
        return removed_bit  
   
    #Removes the first occurence of the value and doesn't return anything
    def remove(self, value):
        if value not in (0, 1):
          raise ValueError("Value must be 0 or 1")
    
        for i in range(self.size):
           if self[i] == value:
           
                for j in range(i, self.size - 1):
                    self[j] = self[j + 1]  

                self[self.size - 1]=0

                self.size -= 1  
                return  

        raise ValueError(f"Bit {value} not found in BitArray")
    
    #Allows Deletion of an item from your object using Python's del keyboard i.e del object[index]
    def __delitem__(self, index):
        if not (0 <= index < self.size):
            raise IndexError("Bit index out of range")

        
        for i in range(index, self.size - 1):
            self[i] = self[i + 1]

        self[self.size - 1]=0

        self.size -= 1  

    #Append all items from other(iterable) to the end of the bitarray.
    def extend(self, other):

        if isinstance(other, BitArray):
            bit_string = str(other)  

        elif isinstance(other, str) and all(bit in '01' for bit in other):
            bit_string = other  

        elif isinstance(other, list) and all(isinstance(b, bool) for b in other):
            bit_string = ''.join('1' if b else '0' for b in other)

        else:
            raise TypeError("Argument must be a BitArray, a binary string, or a list of booleans.")
    
        old_size = self.size
        new_size = old_size + len(bit_string)
        if (new_size + 7) // 8 > len(self.byte_array):
            self.byte_array.extend(bytearray((new_size + 7) // 8 - len(self.byte_array)))

        self.size = new_size  

        for i, bit in enumerate(bit_string):
            if bit == '1':
                self[old_size + i] = 1

    #Insert value into Bit Array before index.
    def insert(self, value, index):
        if not (0 <= index <= self.size):
            raise IndexError("Index out of range")
        if value not in (0, 1):
            raise ValueError("Bit value must be 0 or 1")
        
        self.size += 1

        for i in range(self.size - 1, index, -1):
            self[i] = self[i - 1]
    
        self[index] = value

    #Invert all bits in bitarray (in-place).      
    def invert(self):
        for i in range(len(self.byte_array)):  
            self.byte_array[i] ^= 0xFF  # XOR with 0xFF 

        excess_bits = (len(self.byte_array) * 8) - self.size
        if excess_bits > 0:
            self.byte_array[-1] &= (0xFF << excess_bits) & 0xFF   # shifts it left by excess_bits, pushing 0s into the right and Applies the mask to the last byte using bitwise AND, clearing the excess bits.

    #Reverse all bits in bitarray (in-place).
    def reverse(self):
        for i in range(self.size // 2):
            j = self.size - 1 - i
            self[i], self[j] = self[j], self[i]

    #Return iterator over indices where sub_bitarray is found, such that sub_bitarray is contained within [start:stop]
    def search(self, pattern):
        if not pattern or not all(bit in "01" for bit in pattern):
            raise ValueError("Pattern must be a non-empty binary string containing only '0' and '1'.")
    
        pattern_length = len(pattern)
        bit_string = str(self)  
    
        return bit_string.find(pattern) 
    
    #Number of occurrences of value bitarray within [start:stop:step].
    def count(self, pattern):
        if self.size ==0:
            return 0 
        
        bit_string = str(self)  
        count = 0
        start = 0
        pattern_length = len(pattern)

        while True:
            start = bit_string.find(pattern, start)
            if start == -1:
                break
            count += 1
            start += pattern_length  #To skip past the matched pattern to avoid overlaps 

        return count

    #Enables use of the & operator (bitwise AND) between two BitArray objects.
    def __and__(self, other):

        if not isinstance(other, BitArray):
            raise TypeError("Bitwise AND is only supported between BitArray instances")

        min_size = min(self.size, other.size)
        result = BitArray(min_size)

        min_bytes = (min_size + 7) // 8
        for i in range(min_bytes):
            result.byte_array[i] = self.byte_array[i] & other.byte_array[i]

        # Handle excess bits in the last byte (if any)
        excess_bits = (8 * min_bytes) - min_size
        if excess_bits:
            mask = 0xFF << excess_bits & 0xFF
            result.byte_array[-1] &= mask

        return result
    
    #Enables use of the | operator (bitwise OR) between two BitArray objects.
    def __or__(self, other):
        if not isinstance(other, BitArray):
            raise TypeError("Bitwise OR is only supported between BitArray instances")

        min_size = min(self.size, other.size)
        result = BitArray(min_size)

        min_bytes = (min_size + 7) // 8
        for i in range(min_bytes):
            result.byte_array[i] = self.byte_array[i] | other.byte_array[i]

        # Mask excess bits in the last byte (if any)
        excess_bits = (8 * min_bytes) - min_size
        if excess_bits:
            mask = 0xFF << excess_bits & 0xFF
            result.byte_array[-1] &= mask

        return result
    
    #Enables use of the ^ operator (bitwise XOR) between two BitArray objects.
    def __xor__(self, other):
        if not isinstance(other, BitArray):
            raise TypeError("Bitwise XOR is only supported between BitArray instances")

        min_size = min(self.size, other.size)
        result = BitArray(min_size)

        min_bytes = (min_size + 7) // 8
        for i in range(min_bytes):
            result.byte_array[i] = self.byte_array[i] ^ other.byte_array[i]

        # Mask out excess bits in the last byte
        excess_bits = (8 * min_bytes) - min_size
        if excess_bits:
            mask = 0xFF << excess_bits & 0xFF
            result.byte_array[-1] &= mask

        return result
    
    #Enables use of the ~ operator (bitwise NOT) on BitArray objects.
    def __invert__(self):
        result = BitArray(self.size)
        for i in range(len(self.byte_array)):
            result.byte_array[i] = self.byte_array[i] ^ 0xFF

        excess_bits = (len(result.byte_array) * 8) - self.size
        if excess_bits:
            result.byte_array[-1] &= (0xFF << excess_bits) & 0xFF

        return result
    
    #Return the bit array as a string of '0' and '1'.
    def to01(self):
        return ''.join("1" if self[i] else "0" for i in range(self.size))

    #Return the bitarray buffer in bytes (pad bits are set to zero).
    def tobytes(self):
        """Returns the bit array as bytes."""
        return bytes(self.byte_array)

    #Allows Bit array to be loaded from Byte data
    def frombytes(self, byte_data):

        if isinstance(byte_data, (bytes, bytearray)):
            self.byte_array = bytearray(byte_data)

        elif isinstance(byte_data, (list, tuple)) and all(isinstance(b, int) and 0 <= b <= 255 for b in byte_data):
            self.byte_array = bytearray(byte_data)

        else:
            raise TypeError("frombytes() expects bytes, bytearray, or a list/tuple of integers 0–255.")

        self.size = len(self.byte_array) * 8

    #
    def rotate(self, n):

        if self.size == 0:
            return  
        
        n = n % self.size  

        if n > 0:  
            rotated_bits = [self[i] for i in range(self.size - n, self.size)] + [self[i] for i in range(self.size - n)]
        elif n < 0:  
            n = abs(n)
            rotated_bits = [self[i] for i in range(n, self.size)] + [self[i] for i in range(n)]
        else:
            return  

        
        for i, bit in enumerate(rotated_bits):
            self[i] = bit

    #Add zeros to the end of the bitarray, such that the length will be a multiple of 8, and return the number of bits added [0..7].
    def fill(self):
        extra_bits = (8 - (self.size % 8)) % 8  
        self.extend("0" * extra_bits)  
    
    #Return Bit Array representation of a positive integer
    def inttoba(value, length=None):
        if value < 0:
            raise ValueError("Only non-negative integers are supported.")
        
        binary_str = bin(value)[2:]             #[2:] strips off the '0b'
        
        if length is not None:
            if length < len(binary_str):
                raise ValueError("Length is too small to fit the integer.")
            
            binary_str = binary_str.zfill(length)  
        
        return BitArray(binary_str)  

    #Return Integer representation of a Bit Array
    def batoint(self):
        """Convert the BitArray to an integer."""
        return int(self.to01(), 2)          #Converts a binary string(base 2) to an Integer
    
    #Return a random BitArray of a given size
    def rrandom(size):
        
        if size < 0:
            raise ValueError("Size must be a non-negative integer.")

        random_bits = ''.join(str(random.randint(0, 1)) for _ in range(size))
        return BitArray(random_bits)

    #Return True if Bit Array is Pallindrom else False
    def is_palindromic(self):
        return str(self) == str(self)[::-1]
    
    #Sort the Bit Array
    def sort(self):
        if self.size == 0:
            return

        sorted_bits = sorted(self.to01())  
        for i, bit in enumerate(sorted_bits):
            self[i] = int(bit)

    #Returns 1 if the number of 1s in the bit array is odd, otherwise returns 0.
    def parity(self):
        return self.count("1") % 2       

    #Returns True if the bit array represents a power of two, else False.
    def is_power_of_two(self):
        num = self.ba2int()  
        return num > 0 and (num & (num - 1)) == 0     
    
    #Returns the number of bits in Bit Array
    def __len__(self) -> int:
        return self.size

    #Compare two bit arrays for equality
    def __eq__(self, other: object) -> bool:

        if not isinstance(other, BitArray):
            return False
        return self.size == other.size and self.byte_array == other.byte_array

    #Bit iterator i.e To make BitArray class compatible with iteration
    def __iter__(self) -> Iterable[int]:
        #Iterate over each bit in the bit array
        for i in range(self.size):
            yield self[i]

    #Check if the given bit value exists
    def __contains__(self, value: int) -> bool:
        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        return any(bit == value for bit in self)

    #Left shift the bit array by n positions (zeros added at end).
    def __lshift__(self, n: int) -> 'BitArray':
        if n < 0:
            raise ValueError("Shift amount must be non-negative")
        result = BitArray(self.size)
        for i in range(max(0, self.size - n)):
            result[i] = self[i + n]
        return result

    # 6.Right shift the bit array by n positions (zeros added at beginning).
    def __rshift__(self, n: int) -> 'BitArray':

        if n < 0:
            raise ValueError("Shift amount must be non-negative")
        result = BitArray(self.size)
        for i in range(n, self.size):
            result[i] = self[i - n]
        return result

    #Concatenate two bit arrays.
    def __add__(self, other: 'BitArray') -> 'BitArray':
        if not isinstance(other, BitArray):
            raise TypeError("Can only concatenate with another BitArray")
        result = BitArray(self.size + other.size)
        for i in range(self.size):
            result[i] = self[i]
        for i in range(other.size):
            result[self.size + i] = other[i]
        return result

    #Repeat the bit array n times.
    def __mul__(self, n: int) -> 'BitArray':
        if n <= 0:
            return BitArray(0)
        result = BitArray(self.size * n)
        for i in range(n):
            for j in range(self.size):
                result[i*self.size + j] = self[j]
        return result

    #Check if all bits are 1 i.e Return True if all bits are 1.
    def all(self) -> bool:
        return all(bit == 1 for bit in self)

    #Check if any bit is 1 i.e Return True if any bit is 1.
    def any(self) -> bool:
        return any(bit == 1 for bit in self)

    #Return a deep copy of the bit array.
    def copy(self) -> 'BitArray':
        new_ba = BitArray(self.size)
        new_ba.byte_array = self.byte_array.copy()
        return new_ba

    #Reset i.e Remove all bits (set size to 0).
    def clear(self) -> None:
        self.size = 0
        self.byte_array = bytearray()

    #Return first index of value between start and stop.
    def index(self, value: int, start: int = 0, stop: Optional[int] = None) -> int:
        
        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        stop = self.size if stop is None else stop
        for i in range(start, min(stop, self.size)):
            if self[i] == value:
                return i
        raise ValueError(f"{value} not found in BitArray")

    #Convert to hexadecimal string (padded to full bytes) and return it
    def to_hex(self) -> str:
        
        if self.size == 0:
            return ""
        # Calculate needed bytes (round up)
        num_bytes = (self.size + 7) // 8
        # Get the bytes representation
        byte_str = bytes(self.byte_array[:num_bytes])
        
        return byte_str.hex()

    #Create BitArray from hexadecimal string. (class method)
    @classmethod
    def from_hex(cls, hex_str: str) -> 'BitArray':
        try:
            byte_data = bytes.fromhex(hex_str)
        except ValueError as e:
            raise ValueError("Invalid hexadecimal string") from e
        ba = cls(0)             #creates a temporary empty BitArray object using cls
        ba.byte_array = bytearray(byte_data)
        ba.size = len(byte_data) * 8
        return ba

    #Alias for to01  Returns binary string representation.
    def to_bin(self) -> str:
        return self.to01()

    #Alias for string constructor Create from binary string.
    @classmethod
    def from_bin(cls, bin_str: str) -> 'BitArray':
        return cls(bin_str)

    #Resize the bit array, filling new bits with value (0 or 1).
    def resize(self, new_size: int, value: int = 0) -> None:
        if new_size < 0:
            raise ValueError("Size must be non-negative")
        if value not in (0, 1):
            raise ValueError("Fill value must be 0 or 1")
        
        old_size = self.size
        self.size = new_size
        needed_bytes = (new_size + 7) // 8
        
        # Resize byte array if needed
        if needed_bytes > len(self.byte_array):
            self.byte_array.extend(bytearray(needed_bytes - len(self.byte_array)))
        
        # Set new bits if growing
        if new_size > old_size:
            for i in range(old_size, new_size):
                self[i] = value

    #Count 1 bits i.e Count the number of 1 bits (alias for count('1')).
    def count_ones(self) -> int:
        return self.count("1")

    #Count 0 bits i.e Count the number of 0 bits (alias for count('0')).
    def count_zeros(self) -> int:
        return self.count("0")

    #Find first occurrence of value (0 or 1).
    def find_first(self, value: int) -> int:
        return self.index(value)

    #Find last occurrence of value (0 or 1)
    def find_last(self, value: int) -> int:
        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1")
        for i in range(self.size - 1, -1, -1):
            if self[i] == value:
                return i
        raise ValueError(f"{value} not found in BitArray")

    #Return a slice as a new BitArray (similar to __getitem__ with slice).
    def slice(self, start: Optional[int] = None, stop: Optional[int] = None, step: Optional[int] = None) -> 'BitArray':
        return self.__getitem__(slice(start, stop, step))

    #Replace occurrences of old pattern with new pattern and Returns new BitArray with replacements.
    def replace(self, old: str, new: str) -> 'BitArray':
        
        if not all(c in '01' for c in old) or not all(c in '01' for c in new):
            raise ValueError("Patterns must only contain 0 and 1")
        str_rep = self.to01().replace(old, new)
        return BitArray(str_rep)

    #Check if bit array starts with the given binary prefix.
    def startswith(self, prefix: str) -> bool:
        
        if not all(c in '01' for c in prefix):
            raise ValueError("Prefix must only contain 0 and 1")
        return self.to01().startswith(prefix)

    #Check if bit array ends with the given binary suffix.
    def endswith(self, suffix: str) -> bool:

        if not all(c in '01' for c in suffix):
            raise ValueError("Suffix must only contain 0 and 1")
        return self.to01().endswith(suffix)
