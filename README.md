# BitArray - Efficient Bit Array Implementation in Python

A Python implementation of a bit array data structure with comprehensive functionality for efficient bit-level operations.

## Features

-  **Efficient storage** using bytearrays (8 bits per byte)
-  **Multiple initialization options**: size, binary string, boolean list, hex string
-  **Bitwise operations**: AND, OR, XOR, NOT, shifts
-  **Sequence operations**: indexing, slicing, concatenation, repetition
-  **Comprehensive bit manipulation**: set/get, insert/remove, rotate/reverse
-  **Conversions**: to/from integers, bytes, hex strings, binary strings
-  **Search operations**: find patterns, count occurrences
-  **Mathematical utilities**: parity, power-of-two detection
-  **Utility methods**: sort, fill, resize, clear


## Installation

Simply include the `BitArray.py` file in your project:

```python
from BitArray import BitArray
```

## Basic Usage
```python
# Empty bit array of size 10
ba1 = BitArray(10)

# From binary string
ba2 = BitArray("10101100")

# From boolean list
ba3 = BitArray([True, False, True, True])

# From integer (with optional length)
ba4 = BitArray.inttoba(42, length=8)  # '00101010'
```
## Basic Operations
```python
# Set and get bits
ba = BitArray(8)
ba[3] = 1        # Set bit at index 3
bit = ba[3]      # Get bit (returns 1)

# Bitwise operations
ba1 = BitArray("1010")
ba2 = BitArray("1100")
result_and = ba1 & ba2  # "1000"
result_or = ba1 | ba2   # "1110"

# Concatenation
combined = ba1 + ba2  # "10101100"
```
## Advanced Operations
```python
# Conversion
ba = BitArray("1101")
as_int = ba.ba2int()  # 13
as_hex = ba.to_hex()  # '0d'

# Searching
ba = BitArray("101010101")
index = ba.search("101")  # 0
count = ba.count("101")   # 3

# Rotation
ba = BitArray("100110")
ba.rotate(2)  # becomes "101001"
```

## API Reference

### Core Operations
- **Bit Access**:
  - `__getitem__` - Get bit at index
  - `__setitem__` - Set bit at index
- **Bitwise Operations**:
  - `__and__` - Bitwise AND
  - `__or__` - Bitwise OR
  - `__xor__` - Bitwise XOR
  - `__invert__` - Bitwise NOT
- **Bit Shifts**:
  - `__lshift__` - Left shift
  - `__rshift__` - Right shift

### Conversion Methods
- **Binary String**:
  - `to01()` - Return as '01' string
  - `to_bin()` - Alias for to01()
- **Byte Conversion**:
  - `tobytes()` - Convert to bytes
  - `frombytes()` - Create from bytes
- **Hex String**:
  - `to_hex()` - Convert to hex string
  - `from_hex()` - Create from hex string
- **Integer Conversion**:
  - `ba2int()` - Convert to integer
  - `inttoba()` - Create from integer

### Utility Methods
- `rotate(n)` - Rotate bits by n positions
- `reverse()` - Reverse bit order
- `sort()` - Sort bits (0s first)
- `fill()` - Pad with 0s to full bytes
- `resize(new_size)` - Resize bit array

### Search/Count Operations
- `search(pattern)` - Find first occurrence of pattern
- `count(pattern)` - Count occurrences of pattern
- `find_first(value)` - Find first 0 or 1
- `find_last(value)` - Find last 0 or 1

## Contributing
Contributions are welcome! Please reach us for any improvements.
