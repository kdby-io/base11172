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
    result = ''
    for char in page:
        result += chr(char+44032)
    print(result)

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