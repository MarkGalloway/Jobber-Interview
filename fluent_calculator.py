"""
Fluent Calculator

The Kata is inspired by the "Calculating with Functions Kata for JavaScript" on codewars. The goal is to implement a simple calculator which uses fluent syntax:

Calc.new.one.plus.two            # Should return 3
Calc.new.five.minus.six          # Should return -1
Calc.new.seven.times.two         # Should return 14
Calc.new.nine.divided_by.three   # Should return 3

There are only four operations that are supported (plus, minus, times, divided_by) and 10 digits (zero, one, two, three, four, five, six, seven, eight, nine).
Each calculation consists of one operation only and will return an integer.
Note: This is not a string parsing problem. The calls above are a chain of methods. Some languages may require parenthesis in method calls. That is OK, but consider a different language what would support the above syntax if possible.

To run: python fluent_calculator.py
"""

NAME_TO_NUMBER = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

OPERATION_TO_FUNCTION = {
    'plus': lambda x, y: x + y,
    'minus': lambda x, y: x - y,
    'times': lambda x, y: x * y,
    'divided_by': lambda x, y: x / y,
}

ALLOWED_NUMBERS = NAME_TO_NUMBER.keys()
ALLOWED_OPERATIONS = OPERATION_TO_FUNCTION.keys()


class InvalidUseException(Exception):
    pass


class classproperty(property):
    """Custom decorator to wrap a class method to act like a property. This supports new `new` syntax with no brackets.
    Source: https://stackoverflow.com/a/13624858
    """
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


def calculator_property(wrapped_function):
    """Wraps the Calc methods to encapsulate error checking and calculator state evaluation"""
    @property
    def wrapper(self, *args, **kwargs):
        # Calculator should be chainable until exhausted
        result = self

        # Validate calculator usage order and methods
        if len(self.stack) in [0, 2] and wrapped_function.__name__ not in ALLOWED_NUMBERS:
            raise InvalidUseException('Invalid operation. Expected `Calc.new.number.operation.number`, where number is one of {}'.format(ALLOWED_NUMBERS))

        if len(self.stack) == 1 and wrapped_function.__name__ not in ALLOWED_OPERATIONS:
            raise InvalidUseException('Invalid operation. Expected `Calc.new.number.operation.number`, where operation is one of {}'.format(ALLOWED_OPERATIONS))

        # Delegate to class funtion
        wrapped_function(self, *args, **kwargs)

        # If the Calculator is read to evaluate it's state, lets do so
        if len(self.stack) == 3:
            left, operation, right = self.stack

            try:
                result = operation(left, right)
            except ZeroDivisionError:
                result = "Division by zero is undefined."

        return result

    return wrapper


class Calc(object):
    @classproperty
    def new(cls):
        return Calc()

    def __init__(self):
        self.stack = []

    @calculator_property
    def zero(self):
        self.stack.append(0)

    @calculator_property
    def one(self):
        self.stack.append(1)

    @calculator_property
    def two(self):
        self.stack.append(2)

    @calculator_property
    def three(self):
        self.stack.append(3)

    @calculator_property
    def four(self):
        self.stack.append(4)

    @calculator_property
    def five(self):
        self.stack.append(5)

    @calculator_property
    def six(self):
        self.stack.append(6)

    @calculator_property
    def seven(self):
        self.stack.append(7)

    @calculator_property
    def eight(self):
        self.stack.append(8)

    @calculator_property
    def nine(self):
        self.stack.append(9)

    @calculator_property
    def plus(self):
        self.stack.append(lambda x, y: x + y)

    @calculator_property
    def minus(self):
        self.stack.append(lambda x, y: x - y)

    @calculator_property
    def times(self):
        self.stack.append(lambda x, y: x * y)

    @calculator_property
    def divided_by(self):
        self.stack.append(lambda x, y: x / y)


def test_provided_cases():
    assert Calc.new.one.plus.two == 3
    assert Calc.new.five.minus.six == -1
    assert Calc.new.seven.times.two == 14
    assert Calc.new.nine.divided_by.three == 3


def test_all_valid_combinations():
    """Ensure all combinations of numbers and operations are valid"""
    for operation in ALLOWED_OPERATIONS:
        for left in ALLOWED_NUMBERS:
            for right in ALLOWED_NUMBERS:
                expression = 'Calc.new.{left}.{operation}.{right}'.format(left=left, operation=operation, right=right)
                result = eval(expression)

                if operation == 'divided_by' and right == 'zero':
                    assert result == "Division by zero is undefined."
                    continue

                assert result == OPERATION_TO_FUNCTION[operation](NAME_TO_NUMBER[left], NAME_TO_NUMBER[right])


def test_invalid_use():
    """Ensure invalid use is detected"""
    invalid_operations = [
        'Calc.new.plus.two.two',
        'Calc.new.two.two.plus',
    ]
    for operation in invalid_operations:
        try:
            eval(operation)
            assert False, "Failed to handle invalid argument"
        except InvalidUseException as e:
            assert str(e).startswith("Invalid operation")


if __name__ == '__main__':
    test_provided_cases()
    test_all_valid_combinations()
    test_invalid_use()
    print("All tests passed.")
