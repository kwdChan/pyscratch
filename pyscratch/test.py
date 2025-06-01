from typing import Generator


def hello():
    yield 1

hello2 = hello()
print(isinstance(hello2, Generator))