"""
CMPS 6610  Problem Set 2
See problemset-02.pdf for details.
Yan Zhu
"""
import time
from tabulate import tabulate

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        # Make sure the parentheses are balanced in the return statement
        return 'decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec))
    


# some useful utility functions to manipulate bit vectors
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    mid = len(vec) // 2
    return (binary2int(vec[:mid]), binary2int(vec[mid:]))

def bit_shift(number, n):
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y
    
def quadratic_multiply(x, y):
    x_bits = x.binary_vec
    y_bits = y.binary_vec
    x_bits, y_bits = pad(x_bits, y_bits)
    product_result = ['0'] * (len(x_bits) + len(y_bits))

    for i in range(len(x_bits) - 1, -1, -1):
        if x_bits[i] == '1':
            shifted_y_bits = bit_shift(BinaryNumber(int(''.join(y_bits), 2)), len(x_bits) - 1 - i).binary_vec
            carry_over = 0

            for j in range(len(shifted_y_bits) - 1, -1, -1):
                position = j + len(product_result) - len(shifted_y_bits)
                total_sum = int(product_result[position]) + int(shifted_y_bits[j]) + carry_over

                if total_sum == 2:
                    product_result[position] = '0'
                    carry_over = 1
                elif total_sum == 3:
                    product_result[position] = '1'
                    carry_over = 1
                else:
                    product_result[position] = str(total_sum)
                    carry_over = 0

            if carry_over:
                product_result[position - 1] = str(int(product_result[position - 1]) + 1)

    return product_result


def subquadratic_multiply(x, y):
    x_bits = x.binary_vec
    y_bits = y.binary_vec
    x_bits, y_bits = pad(x_bits, y_bits)
    bit_length = len(x_bits)

    if bit_length == 2:
        x_value = int(''.join(x_bits), 2)
        y_value = int(''.join(y_bits), 2)
        product = x_value * y_value
        return list('{0:b}'.format(product))

    high_x, low_x = split_number(x_bits)
    high_y, low_y = split_number(y_bits)

    low_product = subquadratic_multiply(low_x, low_y)
    high_product = subquadratic_multiply(high_x, high_y)

    sum_x = BinaryNumber(high_x.decimal_val + low_x.decimal_val)
    sum_y = BinaryNumber(high_y.decimal_val + low_y.decimal_val)

    cross_product = subquadratic_multiply(sum_x, sum_y)

    cross_term = binary2int(cross_product).decimal_val - binary2int(high_product).decimal_val - binary2int(low_product).decimal_val
    if cross_term < 0:
        cross_term = 0

    cross_term_binary = list('{0:b}'.format(cross_term))

    shifted_high = bit_shift(binary2int(high_product), bit_length).binary_vec
    shifted_cross = bit_shift(binary2int(cross_term_binary), bit_length // 2).binary_vec

    final_result = binary2int(shifted_high).decimal_val + binary2int(shifted_cross).decimal_val + binary2int(low_product).decimal_val
    return list('{0:b}'.format(final_result))

def test_multiply():
    # Testing Karatsuba's subquadratic multiply

    assert binary2int(quadratic_multiply(BinaryNumber(2), BinaryNumber(2))).decimal_val == 2*2

    assert binary2int(quadratic_multiply(BinaryNumber(4), BinaryNumber(3))).decimal_val == 4*3
    assert binary2int(subquadratic_multiply(BinaryNumber(6), BinaryNumber(5))).decimal_val ==6*5
    assert binary2int(subquadratic_multiply(BinaryNumber(5), BinaryNumber(4))).decimal_val ==4*5
    print("Pass All!")



test_multiply()
    

def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    f(x,y)
    return (time.time() - start)*1000
def compare_multiply():
    res = []
    for n in [10,100,1000,10000,100000,1000000,10000000,100000000,1000000000,1000000000000000000000000]:
        qtime = time_multiply(BinaryNumber(n), BinaryNumber(n), quadratic_multiply)
        subqtime = time_multiply(BinaryNumber(n), BinaryNumber(n), subquadratic_multiply)        
        res.append((n, qtime, subqtime))
    print_results(res)


def print_results(results):
    print("\n")
    print(
        tabulate(
            results,
            headers=['n', 'quadratic', 'subquadratic'],
            floatfmt=".3f",
            tablefmt="github"
        )
    )

	
compare_multiply()
print("Although in theory, the time complexity of the Karatsuba algorithm is O(n^{\log_2 3}), while the traditional grade-school multiplication algorithm has a complexity of O(n^2), mathematically, the Karatsuba algorithm should be faster for large inputs. However, in practical applications, especially when implemented in Python, the Karatsuba algorithm does not exhibit a significant speed advantage due to Python’s inefficient handling of recursion. In fact, even for very large numbers (such as 10^{24}), it may still be slower than traditional grade-school multiplication.")
