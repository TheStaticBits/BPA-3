from __future__ import annotations


class AdvDict:
    """ Advanced Dictionary.
        Adds features such as +, -, *, /, etc. to dictionaries. """

    def __init__(self, pyDict: dict) -> None:
        self.pyDict = pyDict

    def getPyDict(self) -> dict: return self.pyDict
    def copy(self) -> AdvDict: return AdvDict(self.pyDict.copy())

    def __getitem__(self, key: any) -> any:
        """ Gets the value of the given key """
        return self.pyDict[key]

    def __setitem__(self, key: any, value: any) -> None:
        """ Sets the value of the given key """
        self.pyDict[key] = value

    # Operator overloading

    def __str__(self) -> str:
        return str(self.pyDict)

    def __add__(self, other: AdvDict | int | float) -> AdvDict:
        """ + overloading """
        copy = self.copy()

        if isinstance(other, AdvDict):  # Add two AdvDicts
            for key in other.getPyDict():
                copy[key] += other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in other.getPyDict():
                copy[key] += other

        else:
            raise TypeError(f"Cannot add AdvDict and {type(other)}")

        return copy

    def __iadd__(self, other: AdvDict | int | float) -> AdvDict:
        """ += overloading """
        if isinstance(other, AdvDict):
            for key in other.getPyDict():
                self.pyDict[key] += other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in other.getPyDict():
                self.pyDict[key] += other

        else:
            raise TypeError(f"Cannot add AdvDict and {type(other)}")

        return self

    def __sub__(self, other: AdvDict | int | float) -> AdvDict:
        """ - overloading """
        if isinstance(other, AdvDict):
            for key in other.getPyDict():
                self.pyDict[key] -= other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in other.getPyDict():
                self.pyDict[key] -= other

        else:
            raise TypeError(f"Cannot subtract AdvDict and {type(other)}")

        return self

    def __isub__(self, other: AdvDict | int | float) -> AdvDict:
        """ -= overloading """
        if isinstance(other, AdvDict):
            for key in other.getPyDict():
                self.pyDict[key] -= other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in other.getPyDict():
                self.pyDict[key] -= other

        else:
            raise TypeError(f"Cannot subtract AdvDict and {type(other)}")

        return self

    def __mul__(self, other: AdvDict | int | float) -> AdvDict:
        """ * overloading """
        copy = self.copy()

        if isinstance(other, AdvDict):
            for key in other.getPyDict():
                copy[key] *= other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in self.pyDict:
                copy[key] *= other

        else:
            raise TypeError(f"Cannot multiply AdvDict and {type(other)}")

        return copy

    def __imul__(self, other: AdvDict | int | float) -> AdvDict:
        """ *= overloading """
        if isinstance(other, AdvDict):
            for key in other.getPyDict():
                self.pyDict[key] *= other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in self.pyDict:
                self.pyDict[key] *= other

        else:
            raise TypeError(f"Cannot multiply AdvDict and {type(other)}")

        return self

    def __truediv__(self, other: AdvDict | int | float) -> AdvDict:
        """ / overloading """
        copy = self.copy()

        if isinstance(other, AdvDict):
            for key in other.getPyDict():
                copy[key] /= other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in self.pyDict:
                copy[key] /= other

        else:
            raise TypeError(f"Cannot divide AdvDict and {type(other)}")

        return copy

    def __itruediv__(self, other: AdvDict | int | float) -> AdvDict:
        """ /= overloading """
        if isinstance(other, AdvDict):
            for key in other.getPyDict():
                self.pyDict[key] /= other[key]

        elif isinstance(other, int) or isinstance(other, float):
            for key in self.pyDict:
                self.pyDict[key] /= other

        else:
            raise TypeError(f"Cannot divide AdvDict and {type(other)}")

        return self
