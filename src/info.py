"""
PAWPRINTS-WEBSCRAPER

This module runs various queries on the full petitions list.
This includes sorting, checking for valid petitions not responded to and checking authors.

Author: Carter4242
https://github.com/Carter4242
"""


from dateutil.relativedelta import relativedelta
from datetime import datetime
from pytz import timezone


def mostFrequentAuthor(petitions: list) -> str:
    """
    Makes a list of just authors, then searches through list of just authors for the most frequent author.

    :param petitions: Full list of petitions
    :type petitions: list
    :return: The most prolific petition author
    :rtype: str
    """

    authors = []  # List of strings
    for i in petitions:
        authors.append(i.author)
    
    counter = 0  # Number of petitions an author has
    author = authors[0]  # Current author being checked
    for i in authors:
        curr_frequency = authors.count(i)  # Number of petitions an author has
        if(curr_frequency > counter):  # Only true if new author has more petitions
            counter = curr_frequency
            author = i
    return author


def sortPetitions(petitions: list, sortType: str) -> list:
    """
    Sort the petitions list by a sortType (from Petition dataclass). If failed return petition list.

    :param petitions: Full list of petitions
    :type petitions: list
    :param sortType: Method of sorting required
    :type sortType: str
    :return: Sorted list of petitions
    :rtype: list
    """

    if sortType == "timestamp":
        petitions.sort(key = lambda x: x.timestamp)
    else:
        try:
            petitions.sort(key = lambda x: getattr(x,sortType), reverse = True)
        except:
            print("SORT FAILED, sortType INVALID")
    return petitions


def noResponseSixMonths(petitions: list) -> list:
    """
    Generates the date sixMonthsAgo today.
    Checks every petition for it having no response, over 200 sigs and it being at least six months old.
    Adds each of those values to a list and returns the list.

    :param petitions: Full list of petitions
    :type petitions: list
    :return: List of petitions with no response, over 200 sigs, from at least six months ago.
    :rtype: list
    """
    
    tz = timezone('EST')
    now = datetime.now(tz).date()
    sixMonthsAgo = now - relativedelta(months=+6)
    
    noResponse = []
    for i in petitions:
        if i.response == False and i.signatures >= 200 and i.timestamp < sixMonthsAgo:
            noResponse.append(i)
    return noResponse
