from __future__ import annotations # allows use of the class type inside the same class
from math import floor

class Vect:
    """ Stores two digits, allowing for operations """

    def __init__(self, *args) -> None:
        if len(args) == 1:
            if isinstance(args[0], Vect):
                self.x = args[0].x
                self.y = args[0].y
            elif isinstance(args[0], tuple) or isinstance(args[0], list):
                self.x = args[0][0]
                self.y = args[0][1]
            else: # Single integer
                self.x = args[0]
                self.y = args[0]
        
        elif len(args) == 2: # two parameters
            self.x = args[0]
            self.y = args[1]
        
        elif len(args) == 0: # zero parameters
            self.x = 0
            self.y = 0
        
        else:
            raise TypeError(f"Vect() takes 1 or 2 arguments, not {len(args)}")


    def copy(self) -> Vect:
        return Vect(self.x, self.y)
    

    def toTuple(self) -> tuple:
        return (self.x, self.y)
    
    
    def floor(self) -> Vect:
        return Vect(floor(self.x), floor(self.y))
    

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    

    def __add__(self, other: Vect | int | float) -> Vect:
        """ + by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x + other.x, self.y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x + other, self.y + other)
        else:
            raise TypeError(f"Cannot add Vect and {type(other)}")
    

    def __iadd__(self, other: Vect | int | float) -> Vect:
        """ += by a Vect or number """
        if isinstance(other, Vect):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
        else:
            raise TypeError(f"Cannot add Vect and {type(other)}")
        return self


    def __sub__(self, other: Vect | int | float) -> Vect:
        """ - by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x - other.x, self.y - other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x - other, self.y - other)
        else:
            raise TypeError(f"Cannot subtract Vect and {type(other)}")
        
    
    def __isub__(self, other: Vect | int | float) -> Vect:
        """ -= by a Vect or number """
        if isinstance(other, Vect):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
        else:
            raise TypeError(f"Cannot subtract Vect and {type(other)}")
        return self


    def __mul__(self, other: Vect | int | float) -> Vect:
        """ * by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x * other, self.y * other)
        else:
            raise TypeError(f"Cannot multiply Vect and {type(other)}")
    

    def __imul__(self, other: Vect | int | float) -> Vect:
        """ *= by a Vect or number """
        if isinstance(other, Vect):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
        else:
            raise TypeError(f"Cannot multiply Vect and {type(other)}")
        return self
    

    def __truediv__(self, other: Vect | int | float) -> Vect:
        """ / by a vector or a number """
        if isinstance(other, Vect):
            return Vect(self.x / other.x, self.y / other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x / other, self.y / other)
        else:
            raise TypeError(f"Cannot divide Vect and {type(other)}")
    

    def __itruediv__(self, other: Vect | int | float) -> Vect:
        """ /= by a Vect or number """
        if isinstance(other, Vect):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
        else:
            raise TypeError(f"Cannot divide Vect and {type(other)}")
        return self
        

    def __floordiv__(self, other: Vect | int | float) -> Vect:
        """ // by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x // other.x, self.y // other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x // other, self.y // other)
        else:
            raise TypeError(f"Cannot floor divide Vect and {type(other)}")
    

    def __ifloordiv__(self, other: Vect | int | float) -> Vect:
        """ //= by a Vect or number """
        if isinstance(other, Vect):
            self.x //= other.x
            self.y //= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x //= other
            self.y //= other
        else:
            raise TypeError(f"Cannot floor divide Vect and {type(other)}")
        return self
    

    def __eq__(self, other: Vect) -> bool:
        """ == overloading """
        if isinstance(other, Vect):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
    
    
    def __ne__(self, other: Vect) -> bool:
        """ != overloading """
        if isinstance(other, Vect):
            return self.x != other.x or self.y != other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
    

    def __lt__(self, other: Vect) -> bool:
        """ < overloading """
        if isinstance(other, Vect):
            return self.x < other.x and self.y < other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
        

    def __le__(self, other: Vect) -> bool:
        """ <= overloading """
        if isinstance(other, Vect):
            return self.x <= other.x and self.y <= other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
    

    def __gt__(self, other: Vect) -> bool:
        """ > overloading """
        if isinstance(other, Vect):
            return self.x > other.x and self.y > other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
        

    def __ge__(self, other: Vect) -> bool:
        """ >= overloading """
        if isinstance(other, Vect):
            return self.x >= other.x and self.y >= other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
        
    
    def __neg__(self) -> Vect:
        """ - overloading """
        return Vect(-self.x, -self.y)