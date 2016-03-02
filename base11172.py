# base11172.py
import itertools
from enum import IntEnum
# import numpy as np

# BASE = 11172
# dt = np.dtype('i2')


class Sign(IntEnum):
    Positive = 1
    Zero = 0
    Negative = -1


class Base11172:
    BASE = 11172

    @classmethod
    def base(cls, base):
        cls.BASE = base
        return cls.BASE

    def __init__(self, data, sign=0):
        sign = Sign(sign)

        if isinstance(data, int):
            assert -self.BASE < data < self.BASE
            sign = 1 if data > 0 else 0 if data == 0 else -1
            # data = np.array([abs(data)], dtype=dt)
            data = [abs(data)]
        elif isinstance(data, list):
            for x in data:
                assert -self.BASE < x < self.BASE
            assert sign != 0
            # data = np.array(data[::-1], dtype=dt)
            data = data[::-1]
        else:
            assert False

        # Properties
        self.data, self.sign = data, sign
        self.clear_zero()

    # Represent
    def __repr__(self):
        if self.sign == 1:
            return '+' + str(self.data[::-1])
        elif self.sign == 0:
            return '0'
        else:   # self.sign == -1:
            return '-' + str(self.data[::-1])

    def __str__(self):
        if self.sign == 1:
            return '+' + str(self.data[::-1])
        elif self.sign == 0:
            return '0'
        else:   # self.sign == -1:
            return '-' + str(self.data[::-1])

    # Index & Slice
    def __len__(self):
        return len(self.data)

    def __getitem__(self, degree):
        return self.data[degree]

    def __setitem__(self, degree, coefficient):
        self.data[degree] = coefficient

    def __delitem__(self, degree):
        # self.data = np.delete(self.data, degree)
        del self.data[degree]

    # Shifting
    def __lshift__(self, move):
        # return Base11172(np.append(self.data[::-1], [0]*move), self.sign)
        return Base11172(self.data[::-1] + [0]*move, self.sign)

    def __rshift__(self, move):
        if len(self) <= move:
            return Base11172(0)
        return Base11172(self.data[:move-1:-1], self.sign)

    # Comparison operators
    def __cmp__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # Same object
        if id(self) == id(other):
            return 0

        # Different sign
        if self.sign > other.sign:
            return 1
        elif self.sign < other.sign:
            return -1
        # Same sign
        else:
            if self.sign == 1:
                return self.compare_data(other)
            elif self.sign == 0:
                return 0
            else:   # self.sign == -1
                return self.compare_data(other)*-1

    def __eq__(self, other):
        compare = self.__cmp__(other)
        if compare == 0:
            return True
        return False

    def __ne__(self, other):
        compare = self.__cmp__(other)
        if compare != 0:
            return True
        return False

    def __lt__(self, other):
        compare = self.__cmp__(other)
        if compare < 0:
            return True
        return False

    def __gt__(self, other):
        compare = self.__cmp__(other)
        if compare > 0:
            return True
        return False

    def __le__(self, other):
        compare = self.__cmp__(other)
        if compare <= 0:
            return True
        return False

    def __ge__(self, other):
        compare = self.__cmp__(other)
        if compare >= 0:
            return True
        return False

    def compare_data(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        if id(self) == id(other):
            return 0

        # different length
        if len(self) > len(other):
            return 1
        elif len(self) < len(other):
            return -1
        # Same length
        else:
            for i in range(len(self)-1, -1, -1):
                if self.data[i] > other.data[i]:
                    return 1
                elif self.data[i] < other.data[i]:
                    return -1
            return 0

    # Unary operators
    def __pos__(self):
        return Base11172(self.data[::-1], self.sign)

    def __neg__(self):
        if self.sign == 0:
            Base11172(0)
        return Base11172(self.data[::-1], self.sign*-1)

    def __abs__(self):
        return Base11172(self.data[::-1], 1)

    # Normal arithmetic operators
    def __add__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # One of both is Zero
        if self.sign == 0:
            return other
        elif other.sign == 0:
            return self

        # Different sign means subtract
        if self.sign != other.sign:
            data = self.sub_data(other)
            if self.compare_data(other) == 1:
                sign = self.sign
            else:   # self.compare_data(other) == -1
                sign = other.sign

        else:   # Self.sign == Other.sign
            data = self.add_data(other)
            sign = self.sign
        return Base11172(data, sign)

    def add_data(self, other):
        size = max(len(self), len(other))
        # data = np.array([0]*(size + 1), dtype=dt)
        data = [0]*(size + 1)
        carry = 0
        for i, (a, b) in enumerate(itertools.zip_longest(*(self.data, other.data), fillvalue=0)):
            carry, data[i] = divmod(a + b + carry, self.BASE)
        data[-1] = carry
        return data[::-1]

    def __sub__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # One of both is Zero
        if self.sign == 0:
            return -other
        elif other.sign == 0:
            return self

        if self.sign != other.sign:
            data = self.add_data(other)
            if self.compare_data(other) == 1:
                sign = self.sign
            else:   # self.compare_data(other) == -1
                sign = other.sign

        else:   # Self.sign == Other.sign
            if self.compare_data(other) < 0:
                data = other.sub_data(self)
                sign = -1
            else:
                data = self.sub_data(other)
                sign = self.sign
        return Base11172(data, sign)

    def sub_data(self, other):
        size = max(len(self), len(other))
        # data = np.array([0]*(size + 1), dtype=dt)
        data = [0]*(size + 1)
        carry = 0
        for i, (a, b) in enumerate(itertools.zip_longest(*(self.data, other.data), fillvalue=0)):
            carry, data[i] = divmod(a - b + carry, self.BASE)
        data[-1] = carry
        return data[::-1]

    def __mul__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other, 0)

        # One of both is Zero
        if self.sign == 0 or other.sign == 0:
            return 0
        if self.sign == other.sign:
            sign = 1
        else:
            sign = -1

        data = self.mul_data(other)
        return Base11172(data, sign)

    def mul_data(self, other):
        temps = []
        for i, x in enumerate(other.data):
            # tmp = np.array([0]*(i + 1 + len(self)), dtype=dt)
            tmp = [0]*(i + 1 + len(self))
            carry = 0
            for j, y in enumerate(self.data):
                carry, tmp[i+j] = divmod(x*y + carry, self.BASE)
            tmp[-1] = carry
            if tmp[-1] == 0:
                # tmp = np.delete(tmp, -1)
                del tmp[-1]
            temps.append(tmp)

        size = len(self) + len(other)
        # data = np.array([0]*size, dtype=dt)
        data = [0]*size
        carry = 0
        for i, x in enumerate(itertools.zip_longest(*temps, fillvalue=0)):
            carry, data[i] = divmod(sum(x) + carry, self.BASE)
        if data[-1] == 0:
            data[-1] = carry
        return data[::-1]

    def __floordiv__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # One of both is Zero
        if self.sign == 0:
            return 0
        elif other.sign == 0:
            raise ZeroDivisionError
        elif self.sign != other.sign:
            sign = -1
        else:
            sign = 1

        quotient_data, remind_data = self.floordiv_data(other)
        quotient = Base11172(quotient_data, sign)
        # if np.all(remind_data != 0):
        if remind_data[0] != 0:
            if sign == -1:
                quotient -= 1
        return quotient

    def __mod__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # One of both is Zero
        if self.sign == 0:
            return 0
        elif other.sign == 0:
            raise ZeroDivisionError
        elif other.sign == -1:
            sign = -1
        else:
            sign = 1

        remind_data = self.floordiv_data(other)[1]
        if self.sign == -1 or other.sign == -1:
            # remind_data = np.subtract(np.array([BASE-1], dtype=dt), remind_data)
            remind_data = [(self.BASE - 1) - x for x in remind_data]
        remind = Base11172(remind_data, sign)
        return remind

    def __divmod__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)

        # set quotient sign
        if self.sign == 0:
            quotient = Base11172(0)
            remind = Base11172(0)
            return quotient, remind
        elif other.sign == 0:
            raise ZeroDivisionError
        elif self.sign != other.sign:
            quotient_sign = -1
        else:
            quotient_sign = 1

        # set remind sign
        if other.sign == -1:
            remind_sign = -1
        else:
            remind_sign = 1

        quotient_data, remind_data = self.floordiv_data(other)
        if self.sign == -1 or other.sign == -1:
            # remind_data = np.subtract(np.array([BASE-1], dtype=dt), remind_data)
            remind_data = [(self.BASE - 1) - x for x in remind_data]

        quotient = Base11172(quotient_data, quotient_sign)
        remind = Base11172(remind_data, remind_sign)

        # if np.all(remind_data != 0):
        if remind_data[0] != 0:
            if quotient_sign == -1:
                quotient -= 1

        return quotient, remind

    def floordiv_data(self, other):
        if self.compare_data(other) == 0:
            # quotient, remind = np.array([1], dtype=dt), np.array([0], dtype=dt)
            quotient, remind = [1], [0]
        elif self.compare_data(other) == -1:
            # quotient, remind = np.array([0], dtype=dt), self.data
            quotient, remind = [0], self.data
        else:   # self.compare_data(other) == 1
            # dividend, divisor, quotient = self, other, np.array([], dtype=dt)
            dividend, divisor, quotient = self, other, []

            pointer = len(dividend) - 1
            sub_dividend = []
            while pointer >= 0:
                # sub_dividend = Base11172(np.append(sub_dividend[::-1], [dividend[pointer]]), 1)
                sub_dividend = Base11172(sub_dividend[::-1] + [dividend[pointer]], 1)

                while sub_dividend.compare_data(divisor) != 1:
                    # quotient = np.insert(quotient, 0, np.array([0], dtype=dt))
                    quotient.insert(0, 0)
                    pointer -= 1
                    if pointer < 0:
                        break
                    # sub_dividend.data = np.insert(sub_dividend.data, 0, dividend[pointer])
                    sub_dividend.data.insert(0, dividend[pointer])

                sub_quotient = 0
                while sub_dividend.compare_data(divisor) >= 0:
                    sub_quotient += 1
                    sub_dividend = Base11172(sub_dividend.sub_data(divisor), 1)

                if pointer >= 0:
                    # quotient = np.insert(quotient, 0, sub_quotient)
                    quotient.insert(0, sub_quotient[:])
                    pointer -= 1

            # remind is sub_dividend
            remind = sub_dividend.data
        return quotient[::-1], remind[::-1]

    # Reflected arithmetic operators
    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)
        return other - self

    def __rmul__(self, other):
        return self * other

    def __rfloordiv__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)
        return other // self

    def __rmod__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)
        return other % self

    def __rdivmod__(self, other):
        if not isinstance(other, Base11172):
            other = Base11172(other)
        return divmod(other, self)

    def clear_zero(self):
        for i in range(len(self)-1, -1, -1):
                if i != 0 and self.data[i] == 0:
                    del self[i]
                else:
                    break


if __name__ == '__main__':
    pass
