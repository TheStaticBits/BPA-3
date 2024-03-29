from __future__ import annotations

import pygame
from math import floor, sqrt, atan2, cos, sin


class Vect:
    """ Stores two digits/vars, allowing for operations """

    def __init__(self, *args) -> None:
        if len(args) == 1:
            if type(args[0]) is Vect:
                self.x = args[0].x
                self.y = args[0].y
            elif type(args[0]) is tuple or type(args[0]) is list:
                self.x = args[0][0]
                self.y = args[0][1]
            else:  # Single integer
                self.x = args[0]
                self.y = args[0]

        elif len(args) == 2:  # two parameters
            self.x = args[0]
            self.y = args[1]

        elif len(args) == 0:  # zero parameters
            self.x = 0
            self.y = 0

        else:
            raise TypeError(f"Vect() takes 1 or 2 arguments, not {len(args)}")

    def copy(self) -> Vect:
        return Vect(self.x, self.y)

    def toTuple(self) -> tuple:
        return (self.x, self.y)

    def round(self) -> Vect:
        return Vect(round(self.x), round(self.y))

    def floor(self) -> Vect:
        return Vect(floor(self.x), floor(self.y))

    def clamp(self, minVect: Vect, maxVect: Vect) -> None:
        """ Locks the vector between two vectors """
        self.clampX(minVect.x, maxVect.x)
        self.clampY(minVect.y, maxVect.y)

    def clampX(self, minX: float, maxX: float) -> None:
        """ Locks the x component between two numbers """
        self.x = min(max(self.x, minX), maxX)

    def clampY(self, minY: float, maxY: float) -> None:
        """ Locks the y component between two numbers """
        self.y = min(max(self.y, minY), maxY)

    def dist(self, other: Vect) -> float:
        """ Returns distance using pythagorean theorem """
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle(self, other: Vect) -> float:
        """ Returns the angle in radians between two points """
        return atan2(other.y - self.y, other.x - self.x)

    @staticmethod
    def toRect(pos: Vect, size: Vect) -> pygame.Rect:
        return pygame.Rect(pos.x, pos.y, size.x, size.y)

    @staticmethod
    def angleMove(angle: float) -> Vect:
        """ Returns a vector from an angle """
        return Vect(cos(angle), sin(angle))

    def getSigns(self) -> Vect:
        """ Returns a vector with the signs of each component """
        return Vect(
            1 if self.x > 0 else -1 if self.x < 0 else 0,
            1 if self.y > 0 else -1 if self.y < 0 else 0
        )

    def signsMatch(self, other: Vect) -> bool:
        """ Returns if the signs of the components match """
        return self.getSigns() == other.getSigns()

    def forEach(self, func: callable,
                vectParams: tuple[Vect] = (),
                otherParams: tuple = ()) -> Vect:
        """ Applies a function to each component of the vector,
            with additional parameters passed in via lists for x and y """

        # Create lists of the params for
        # each axis of the vector
        paramsX: list = []
        paramsY: list = []

        for vect in vectParams:
            paramsX.append(vect.x)
            paramsY.append(vect.y)

        # Apply function callback to each axis of the vector
        # using the * spread operator for the parameters
        return Vect(
            func(self.x, *paramsX, *otherParams),
            func(self.y, *paramsY, *otherParams)
        )

    # Getters and setters for when using a string to get the x or y component

    def get(self, dir: str) -> any:
        """ Gets the x or y component of the vector """
        if dir == "x":
            return self.x
        elif dir == "y":
            return self.y

    def add(self, dir: str, value: any) -> any:
        """ Adds to the x or y component of the vector """
        if dir == "x":
            self.x += value
        elif dir == "y":
            self.y += value

    def set(self, dir: str, value: any) -> any:
        """ Sets the x or y component of the vector """
        if dir == "x":
            self.x = value
        elif dir == "y":
            self.y = value

    # A whole ton of boilerplate for overloading operators

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: Vect | int | float) -> Vect:
        """ + by a Vect or number """
        if type(other) is Vect:
            return Vect(self.x + other.x, self.y + other.y)
        elif type(other) is int or type(other) is float:
            return Vect(self.x + other, self.y + other)
        else:
            raise TypeError(f"Cannot add Vect and {type(other)}")

    def __iadd__(self, other: Vect | int | float) -> Vect:
        """ += by a Vect or number """
        if type(other) is Vect:
            self.x += other.x
            self.y += other.y
        elif type(other) is int or type(other) is float:
            self.x += other
            self.y += other
        else:
            raise TypeError(f"Cannot add Vect and {type(other)}")
        return self

    def __sub__(self, other: Vect | int | float) -> Vect:
        """ - by a Vect or number """
        if type(other) is Vect:
            return Vect(self.x - other.x, self.y - other.y)
        elif type(other) is int or type(other) is float:
            return Vect(self.x - other, self.y - other)
        else:
            raise TypeError(f"Cannot subtract Vect and {type(other)}")

    def __isub__(self, other: Vect | int | float) -> Vect:
        """ -= by a Vect or number """
        if type(other) is Vect:
            self.x -= other.x
            self.y -= other.y
        elif type(other) is int or type(other) is float:
            self.x -= other
            self.y -= other
        else:
            raise TypeError(f"Cannot subtract Vect and {type(other)}")
        return self

    def __mul__(self, other: Vect | int | float) -> Vect:
        """ * by a Vect or number """
        if type(other) is Vect:
            return Vect(self.x * other.x, self.y * other.y)
        elif type(other) is int or type(other) is float:
            return Vect(self.x * other, self.y * other)
        else:
            raise TypeError(f"Cannot multiply Vect and {type(other)}")

    def __imul__(self, other: Vect | int | float) -> Vect:
        """ *= by a Vect or number """
        if type(other) is Vect:
            self.x *= other.x
            self.y *= other.y
        elif type(other) is int or type(other) is float:
            self.x *= other
            self.y *= other
        else:
            raise TypeError(f"Cannot multiply Vect and {type(other)}")
        return self

    def __truediv__(self, other: Vect | int | float) -> Vect:
        """ / by a vector or a number """
        if type(other) is Vect:
            return Vect(self.x / other.x, self.y / other.y)
        elif type(other) is int or type(other) is float:
            return Vect(self.x / other, self.y / other)
        else:
            raise TypeError(f"Cannot divide Vect and {type(other)}")

    def __itruediv__(self, other: Vect | int | float) -> Vect:
        """ /= by a Vect or number """
        if type(other) is Vect:
            self.x /= other.x
            self.y /= other.y
        elif type(other) is int or type(other) is float:
            self.x /= other
            self.y /= other
        else:
            raise TypeError(f"Cannot divide Vect and {type(other)}")
        return self

    def __floordiv__(self, other: Vect | int | float) -> Vect:
        """ // by a Vect or number """
        if type(other) is Vect:
            return Vect(self.x // other.x, self.y // other.y)
        elif type(other) is int or type(other) is float:
            return Vect(self.x // other, self.y // other)
        else:
            raise TypeError(f"Cannot floor divide Vect and {type(other)}")

    def __ifloordiv__(self, other: Vect | int | float) -> Vect:
        """ //= by a Vect or number """
        if type(other) is Vect:
            self.x //= other.x
            self.y //= other.y
        elif type(other) is int or type(other) is float:
            self.x //= other
            self.y //= other
        else:
            raise TypeError(f"Cannot floor divide Vect and {type(other)}")
        return self

    def __eq__(self, other: Vect) -> bool:
        """ == overloading """
        if type(other) is Vect:
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")

    def __ne__(self, other: Vect) -> bool:
        """ != overloading """
        if type(other) is Vect:
            return self.x != other.x or self.y != other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")

    def __lt__(self, other: Vect) -> bool:
        """ < overloading """
        if type(other) is Vect:
            return self.x < other.x and self.y < other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")

    def __le__(self, other: Vect) -> bool:
        """ <= overloading """
        if type(other) is Vect:
            return self.x <= other.x and self.y <= other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")

    def __gt__(self, other: Vect) -> bool:
        """ > overloading """
        if type(other) is Vect:
            return self.x > other.x and self.y > other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")

    def __ge__(self, other: Vect) -> bool:
        """ >= overloading """
        if type(other) is Vect:
            return self.x >= other.x and self.y >= other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")

    def __neg__(self) -> Vect:
        """ - overloading """
        return Vect(-self.x, -self.y)
