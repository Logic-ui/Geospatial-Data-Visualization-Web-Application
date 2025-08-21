class Test:
    def class_method(self):
        print("This is a tree")


def monkey_function():
    print("Flask is a python framework")


Test.class_method = monkey_function
Test.class_method()