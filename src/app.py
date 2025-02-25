a = 12
b = 45


def foo():
    global b
    b = 53
    print(a)

foo()
print(b)