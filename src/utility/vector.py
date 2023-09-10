class Vect:
    """ Stores two digits, allowing for operations """

    def __init__(self, *args):
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
        
        else:
            raise TypeError(f"Vect() takes 1 or 2 arguments, not {len(args)}")


    def copy(self):
        return Vect(self.x, self.y)
    

    def __str__(self):
        return f"({self.x}, {self.y})"
    

    def __add__(self, other):
        """ + by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x + other.x, self.y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x + other, self.y + other)
        else:
            raise TypeError(f"Cannot add Vect and {type(other)}")
    

    def __iadd__(self, other):
        """ += by a Vect or number """
        if isinstance(other, Vect):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
        else:
            raise TypeError(f"Cannot add Vect and {type(other)}")


    def __sub__(self, other):
        """ - by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x - other.x, self.y - other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x - other, self.y - other)
        else:
            raise TypeError(f"Cannot subtract Vect and {type(other)}")
        
    
    def __isub__(self, other):
        """ -= by a Vect or number """
        if isinstance(other, Vect):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
        else:
            raise TypeError(f"Cannot subtract Vect and {type(other)}")


    def __mul__(self, other):
        """ * by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x * other.x, self.y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x * other, self.y * other)
        else:
            raise TypeError(f"Cannot multiply Vect and {type(other)}")
    

    def __imul__(self, other):
        """ *= by a Vect or number """
        if isinstance(other, Vect):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
        else:
            raise TypeError(f"Cannot multiply Vect and {type(other)}")
    

    def __truediv__(self, other):
        """ / by a vector or a number """
        if isinstance(other, Vect):
            return Vect(self.x / other.x, self.y / other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x / other, self.y / other)
        else:
            raise TypeError(f"Cannot divide Vect and {type(other)}")
    

    def __itruediv__(self, other):
        """ /= by a Vect or number """
        if isinstance(other, Vect):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
        else:
            raise TypeError(f"Cannot divide Vect and {type(other)}")
        

    def __floordiv__(self, other):
        """ // by a Vect or number """
        if isinstance(other, Vect):
            return Vect(self.x // other.x, self.y // other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vect(self.x // other, self.y // other)
        else:
            raise TypeError(f"Cannot floor divide Vect and {type(other)}")
    

    def __ifloordiv__(self, other):
        """ //= by a Vect or number """
        if isinstance(other, Vect):
            self.x //= other.x
            self.y //= other.y
        elif isinstance(other, int) or isinstance(other, float):
            self.x //= other
            self.y //= other
        else:
            raise TypeError(f"Cannot floor divide Vect and {type(other)}")
    

    def __eq__(self, other):
        """ == overloading """
        if isinstance(other, Vect):
            return self.x == other.x and self.y == other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
    
    
    def __ne__(self, other):
        """ != overloading """
        if isinstance(other, Vect):
            return self.x != other.x or self.y != other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
    

    def __lt__(self, other):
        """ < overloading """
        if isinstance(other, Vect):
            return self.x < other.x and self.y < other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
        

    def __le__(self, other):
        """ <= overloading """
        if isinstance(other, Vect):
            return self.x <= other.x and self.y <= other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
    

    def __gt__(self, other):
        """ > overloading """
        if isinstance(other, Vect):
            return self.x > other.x and self.y > other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
        

    def __ge__(self, other):
        """ >= overloading """
        if isinstance(other, Vect):
            return self.x >= other.x and self.y >= other.y
        else:
            raise TypeError(f"Cannot compare Vect and {type(other)}")
        
    