"""
PAWPRINTS-WEBSCRAPER

This project scrapes all petition data using the websocket all command from the RIT SG Pawprints Website.
It then formats and then preforms various queries, as well as graphing the data.

Author: Carter4242
https://github.com/Carter4242
"""


import format
import info
import load
import build
from sys import platform


def main() -> None:
    """
    Loads all scraping data into petitions list, then sorts in by a variety of methods.
    Calls several info functions and graphs data.
    Finally writes the formatted list and total sigs all time to a two separate files.

    :rtype: None
    """

    exitCode = 0
    print("Platform is: " + platform)
    if platform == "darwin":
        exitCode = 42
    

    petitions = load.scrapeAll()  # Load all data

    print("\nSorting...")
    petitions = info.sortPetitions(petitions, 'signatures')
    petitions = info.sortPetitions(petitions, 'response')
    petitions = info.sortPetitions(petitions, 'timestamp')
    latestPetitions = format.latestPetitions(petitions)

    # print("Most frequent author:", scraping_info.mostFrequentAuthor(petitions))
    # scraping_info.noResponseSixMonths(petitions)  # No response within six months > 200 sigs

    build.all(petitions)

    if exitCode != 42:  # Github Actions only
        build.latest(latestPetitions)
        build.alltime(petitions)
    else:
        print("")
        for i in range(8):
            print("ERROR: WILL NOT WRITE - RUNNING ON LOCAL")
        print("\n")

    exit(exitCode)



if __name__ == '__main__':
    main()
