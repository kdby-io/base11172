from base11172 import Base11172
import cProfile
import random


def withBase11172():
    BASE = 11172    # number of Korean Unicode
    MAX_CHAR = 40   # number of chars per line
    MAX_LINE = 40   # number of lines per page
    MAX_PAGE = 410  # number of pages per book

    LENGTH_OF_BOOK = MAX_CHAR*MAX_LINE*MAX_PAGE # length of book
    LENGTH_OF_PAGE = MAX_CHAR*MAX_LINE          # length of page

    book = Base11172([random.randrange(BASE) for _ in range(LENGTH_OF_BOOK)], 1)

    page_num = 200  # which page do you want to read?

    page = book[page_num*LENGTH_OF_PAGE:(page_num+1)*LENGTH_OF_PAGE]
    result = [chr(char+44032) for char in page]
    print(''.join(result))


def withoutBase11172():
    BASE = 11172    # number of Korean Unicode
    MAX_CHAR = 40   # number of chars per line
    MAX_LINE = 40   # number of lines per page
    MAX_PAGE = 410  # number of pages per book

    NUMBER_OF_BOOK = BASE**(MAX_CHAR*MAX_LINE*MAX_PAGE) # number of possible books
    NUMBER_OF_PAGE = BASE**(MAX_CHAR*MAX_LINE)          # number of possible pages

    book = random.randrange(NUMBER_OF_BOOK)  # which book do you want to read?
    page_num = 200                              # which page do you want to read?

    divisor = NUMBER_OF_PAGE**page_num
    book //= divisor        # cut off front pages
    book %= (divisor**2)  # cut off behind pages
    result = ''
    for _ in range(MAX_CHAR*MAX_LINE):
        book, char = divmod(book, BASE)
        result += chr(char+44032)
    print(result)


if __name__ == "__main__":
    print(" [*] Start withBase11172()")
    cProfile.run("withBase11172()")
    print(" [*] Finish withBase11172()")

    print(" [*] Start withoutBase11172()")
    cProfile.run("withoutBase11172()")
    print(" [*] Finish withoutBase11172()")

    # arithmetic
    # a = Base11172([1,2,3,4,5], 1)
    # b = Base11172([1,2], 1)
    # print(a*b, 12345*12)
    # a = Base11172([5, 4, 3, 2, 1], -1)
    # b = Base11172([9, 9, 9], 1)
    # print(a//b, a%b, divmod(-54321, 999))
    # a = Base11172([5, 4, 3, 2, 1], 1)
    # b = Base11172([9, 9, 9], -1)
    # print(a//b, a%b, divmod(54321, -999))
    # x = Base11172([1, 0, 2, 8], 1)
    # print(x*b)
    #
    # c = Base11172([1, 2, 3, 2, 1], 1)
    # d = Base11172([1, 1], 1)
    # print(c//d, c%d, divmod(12321, 11))
    #
    # e = Base11172([7, 7, 7, 7, 7], 1)
    # f = Base11172([9, 9], 1)
    # print(e//f, e%f, divmod(77777, 99))
    # print(a+b)
    # print(a == (a+b)-b)
    # print(a*b)
    # print(b*a)
