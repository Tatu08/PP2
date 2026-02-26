from typing import Iterator, Iterable, Generator

def countdown(n: int) -> Generator[int, None, None]:
    while n >= 0:
        yield n
        n -= 1

def even_numbers(limit: int) -> Generator[int, None, None]:
    for x in range(0, limit + 1):
        if x % 2 == 0:
            yield x

def fibonacci(n: int) -> Generator[int, None, None]:
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

class SquaresIterator:
    def __init__(self, n: int):
        self.n = n
        self.i = 0

    def __iter__(self) -> "SquaresIterator":
        return self

    def __next__(self) -> int:
        if self.i >= self.n:
            raise StopIteration
        val = self.i * self.i
        self.i += 1
        return val

def take(iterable: Iterable, k: int):
    result = []
    it = iter(iterable)
    for _ in range(k):
        try:
            result.append(next(it))
        except StopIteration:
            break
    return result

if __name__ == "__main__":
    print("countdown(5):", list(countdown(5)))
    print("even_numbers(10):", list(even_numbers(10)))
    print("fibonacci(10):", list(fibonacci(10)))

    sq = SquaresIterator(6)
    print("SquaresIterator(6):", list(sq))

    print("take(fibonacci(100), 7):", take(fibonacci(100), 7))