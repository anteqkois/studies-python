# ZADANIE 1

# a
def mySrednia(*args):
    liczby = [float(x) for x in args if str(x).replace('.', '', 1).isdigit()]
    return sum(liczby) / len(liczby) if liczby else 0

print("Zadanie 1a:", mySrednia(3, "5", "a", 7.5, "12.3"))

# b
from math import prod

def mySredniaTup(*args):
    n = len(args)
    if n == 0:
        return (0, 0, 0)
    
    harmoniczna = n / sum(1/x for x in args)
    geometryczna = prod(args) ** (1/n)
    arytmetyczna = sum(args) / n
    
    return (harmoniczna, geometryczna, arytmetyczna)

print("Zadanie 1b:", mySredniaTup(2, 4, 8))

# c
def wykladnik(k):
    n = 0
    while 2 ** n <= k:
        n += 1
    return n

print("Zadanie 1c:", wykladnik(20))

# ZADANIE 2

# a
tuples = [(3, 'c'), (1, 'a'), (2, 'b')]

sorted_by_first = sorted(tuples, key=lambda x: x[0])
sorted_by_second = sorted(tuples, key=lambda x: x[1])

print("Zadanie 2a (po pierwszym elemencie):", sorted_by_first)
print("Zadanie 2a (po drugim elemencie):", sorted_by_second)

# b
lista_slownikow = [
    {'producent': 'Nokia', 'model': 216, 'kolor': 'Czarny'},
    {'producent': 'Mi Max', 'model': 2, 'kolor': 'Złoty'},
    {'producent': 'Samsung', 'model': 7, 'kolor': 'Niebieski'}
]

sorted_dict = sorted(lista_slownikow, key=lambda x: (x['model'], x['kolor']))
print("Zadanie 2b:", sorted_dict)

# c
starts_with = lambda text, letter: text.startswith(letter)
print("Zadanie 2c:", starts_with("Hello", "H"))

# d
from datetime import datetime

date_lambda = lambda: datetime.now().strftime("%Y-%m-%d")
print("Zadanie 2d:", date_lambda())

# e
is_number = lambda x: x.isdigit()
print("Zadanie 2e ('123'):", is_number("123"))
print("Zadanie 2e ('12a'):", is_number("12a"))

# ZADANIE 3

# a
from itertools import accumulate

lst = ['a', 'b', 'c', 'd', 'e', 'f']
lst_res = list(accumulate(lst))
print("Zadanie 3a:", lst_res)

# b
nums = [5, 3, 6, 2, 1, 9, 1]
max_list = list(accumulate(nums, max))
print("Zadanie 3b:", max_list)

# c
def wypisz_imiona():
    names = input("Podaj imiona, oddzielone spacją: ").split()
    for index, name in enumerate(names, 1):
        print(f"Zadanie 3c: {index}. {name}")

# wypisz_imiona()  # Odkomentuj do testowania interaktywnego

# d
def potegi_dwojki(n):
    for i in range(n + 1):
        yield 1 << i

print("Zadanie 3d:", list(potegi_dwojki(5)))

# e
def cyfry_liczby(n):
    for digit in str(n):
        yield int(digit)

gen = cyfry_liczby(12345)
print("Zadanie 3e (kolejne cyfry):", list(gen))

# f
def tylko_parzyste(generator):
    for num in generator:
        if num % 2 == 0:
            yield num

gen = tylko_parzyste(range(10))
print("Zadanie 3f:", list(gen))

# g
words = ["level", "hello", "radar", "world"]
palindromes = list(map(lambda x: x == x[::-1], words))
print("Zadanie 3g:", palindromes)

# h
palindromes = list(map(str.upper, filter(lambda x: x == x[::-1], words)))
print("Zadanie 3h:", palindromes)

# i
from itertools import groupby

data = [("Klasa A", 11), ("Klasa A", 12), ("Klasa A", 5), 
        ("Klasa B", 3), ("Klasa B", 15), ("Klasa B", 10), ("Klasa B", 2)]

data.sort(key=lambda x: x[0])
grouped = {k: sum(v for _, v in g) for k, g in groupby(data, key=lambda x: x[0])}
print("Zadanie 3i:", grouped)

# j
numbers = [1, 2, 3, 4, 5, 6]
letters = ['a', 'b', 'c', 'd', 'e', 'f']

pairs = list(zip(numbers, letters))
print("Zadanie 3j:", pairs)
