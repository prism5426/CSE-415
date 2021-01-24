import math
import re


def is_multiple_of_9(n):
    """Return True if n is a multiple of 9; False otherwise."""
    return n % 9 == 0


def next_prime(m):
    """Return the first prime number p that is greater than m.
    You might wish to define a helper function for this.
    You may assume m is a positive integer."""
    while not is_prime(m + 1):
        m = m + 1
    return m + 1


def is_prime(n):
    for x in range(2, n // 2 + 1):
        if n % x == 0:
            return False
    return True


def quadratic_roots(a, b, c):
    """Return the roots of a quadratic equation (real cases only).
    Return results in tuple-of-floats form, e.g., (-7.0, 3.0)
    Return "complex" if real roots do not exist."""
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return 'complex'
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root2 = (-b - math.sqrt(discriminant)) / (2 * a)
        result = tuple((float(root2), float(root1)))
        return result


def perfect_shuffle(even_list):
    """Assume even_list is a list of an even number of elements.
    Return a new list that is the perfect-shuffle of the input.
    For example, [0, 1, 2, 3, 4, 5, 6, 7] => [0, 4, 1, 5, 2, 6, 3, 7]"""
    result = []
    first_half = even_list[:len(even_list) // 2]
    second_half = even_list[len(even_list) // 2:]
    for x in range(len(first_half)):
        result.append(first_half[x])
        result.append(second_half[x])

    return result


def triples_list(input_list):
    """Assume a list of numbers is input. Using a list comprehension,
    return a new list in which each input element has been multiplied
    by 3."""
    result = [3 * x for x in input_list]
    return result


def double_consonants(text):
    """Return a new version of text, with all the consonants doubled.
    For example:  "The *BIG BAD* wolf!" => "TThhe *BBIGG BBADD* wwollff!"
    For this exercise assume the consonants are all letters OTHER
    THAN A,E,I,O, and U (and a,e,i,o, and u).
    Maintain the case of the characters."""
    pattern = re.compile(r'[^aeiouAEIOU\W]')
    matches = pattern.findall(text)

    result = ''
    for char in text:
        result += char
        if char in matches:
            result += char

    return result


def count_words(text):
    """Return a dictionary having the words in the text as keys,
    and the numbers of occurrences of the words as values.
    Assume a word is a substring of letters and digits and the characters
    '-', '+', '*', '/', '@', '#', '%', and "'" separated by whitespace,
    newlines, and/or punctuation (characters like . , ; ! ? & ( ) [ ]  ).
    Convert all the letters to lower-case before the counting."""
    text = text.lower()
    pattern = re.compile(r'\s|\.|,|;|!|\?|&|\(|\)|\[|]|\n|:|_|\\|=|>|<|"|`|\||\^|\{|\}|~|\$')
    # pattern = re.compile(r'\s|\n')
    word_list = re.split(pattern, text)

    # create result dictionary
    dic = {}
    for word in word_list:
        dic[word] = 0

    for word in word_list:
        dic[word] += 1

    if '' in dic:
        del dic['']

    return dic


def make_cubic_evaluator(a, b, c, d):
    """When called with 4 numbers, returns a function of one variable (x)
    that evaluates the cubic polynomial
    a x^3 + b x^2 + c x + d.
    For this exercise Your function definition for make_cubic_evaluator
    should contain a lambda expression."""
    return lambda x: a * x ** 3 + b * x ** 2 + c * x + d


class Polygon:
    """Polygon class."""

    def __init__(self, n_sides, lengths=None, angles=None):
        self.n_sides = n_sides
        self.lengths = lengths
        self.angles = angles

    def is_rectangle(self):
        if self.n_sides is 4:  # has 4 sides
            if self.angles is None:
                return None
            for angle in self.angles:
                if angle != 90:
                    return False
            return True

        return False

    def is_rhombus(self):
        if self.n_sides is 4:  # has 4 sides
            if self.lengths is None:
                return None
            else:
                return all(length == self.lengths[0] for length in self.lengths)

        return False

    def is_square(self):
        if self.n_sides is 4:  # has 4 sides
            if self.angles is None and self.lengths is None:
                return None
            elif self.angles is None and self.lengths is not None:
                if all(length == self.lengths[0] for length in self.lengths):
                    return None
                else:
                    return False
            elif self.angles is not None and self.lengths is not None:
                l = all(length == self.lengths[0] for length in self.lengths)
                a = all(angle == 90 for angle in self.angles)
                return l and a
            elif self.angles is not None and self.lengths is None:
                if all(angle == 90 for angle in self.angles):
                    return None
                else:
                    return False
        else:
            return False

    def is_regular_hexagon(self):
        if self.n_sides == 6:
            if self.angles is None and self.lengths is None:
                return None
            elif self.angles is None and self.lengths is not None:
                if any(length != self.lengths[0] for length in self.lengths):
                    return False
                else:
                    return None
            elif self.angles is not None:
                if self.lengths is None and all(angle == 120 for angle in self.angles):
                    return None
                else:
                    return all(angle == 120 for angle in self.angles)

        return False

    def is_isosceles_triangle(self):
        if self.n_sides == 3:
            if self.angles is None and self.lengths is None:
                return None
            if self.lengths is not None and any(self.lengths.count(length) > 1 for length in self.lengths):
                return True
            if self.angles is not None and any(self.angles.count(angle) > 1 for angle in self.angles):
                return True
        return False

    def is_equilateral_triangle(self):
        if self.n_sides == 3:
            if self.angles is None and self.lengths is None:
                return None
            if self.lengths is not None and any(self.lengths.count(length) == 3 for length in self.lengths):
                return True
            if self.angles is not None and any(self.angles.count(angle) == 3 for angle in self.angles):
                return True
        return False

    def is_scalene_triangle(self):
        if self.n_sides == 3:
            if self.lengths is None and self.angles is None:
                return None
            if self.lengths is not None and all(self.lengths.count(length) == 1 for length in self.lengths):
                return True
            if self.angles is not None and all(self.angles.count(angle) == 1 for angle in self.angles):
                return True

        return False
