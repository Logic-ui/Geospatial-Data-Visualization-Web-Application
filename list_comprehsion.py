
import time
mylist = [x for x in range(200000000)]
start = time.time()
even_list = [x for x in mylist if x%2==0]
end = time.time()
print(end-start)
start = time.time()
even_list2 = []
for x in mylist:
    if x%2==0:
        even_list2.append(x)
end = time.time()
print(end-start)
# print(even_list)
# print(even_list2)