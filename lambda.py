numbers = [2, 3, 8, 13, 16, 18, 23, 25, 34, 38, 45, 48, 50]

evenn = list(filter(lambda x: x % 2 == 0 and x > 10, numbers))

print("Even number is greater than 10:", evenn)

evenn1 = list(map(lambda x: x + 5, evenn))
print("Add 5 in even number list", evenn1)

odd = list(filter(lambda y: y % 2 == 1 and y > 20, numbers))

print("Odd number is greater than 20:", odd)

odd1 = list(map(lambda x: x - 3, odd))
print("subtract 3 in odd number list", odd1)
