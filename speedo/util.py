from time import mktime
from datetime import datetime

# --- Common ---
def toUnixTime(time):
    """ Convert python datetime object to linux time """
    return mktime(time.timetuple())

def now():
    """ get current time in linux time format """
    return toUnixTime(datetime.now())

def partition(elements, criteria):
    """ perform in-place partition of a list to two parts:
            Left part: all elements that conforms the criteria
            Right part: all other elements
        @param elements: the list to be partitioned
        @param criteria: a predicator determining if an element
                         conforms the criteria.
        @returns: the index that all elements[:index] will be the
                  elements that conforms the criteria; all other
                  elements are in elements[index:]
    """
    begin = 0
    end = len(elements) - 1
    while begin < end:
        while begin < end and criteria(elements[begin]):
            begin += 1
        if begin >= end:
            break

        while begin < end and not criteria(elements[end]):
            end -= 1
        if begin >= end:
            break

        # swap
        elements[begin], elements[end] = elements[end], elements[begin]

    return begin

def tryParseInt(self, text, defaultValue = -1):
    try:
        return int(text)
    except Exception:
        return 0
