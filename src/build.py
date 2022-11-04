"""
PAWPRINTS-WEBSCRAPER

This module handles the writing to files of the full petitions list and the daily total signatures.

Author: Carter4242
https://github.com/Carter4242
"""

from dateutil.relativedelta import relativedelta
from datetime import datetime
from pytz import timezone
import graphing
import os  # Getting file names from folders, renaming files


def all(petitions: list) -> None:
    """
    Writes the full list of petitions into a newly created file, each petition on a new line.
    Filename is - YYYY-MM-DD HR:MM:SS:DECMAL

    :param petitions: Full list of petitions
    :type petitions: list
    :rtype: None
    """

    tz = timezone('EST')
    now = datetime.now(tz)

    # YYYY-MM-DD HR:MM:SS:DECMAL
    filename = "output/" + str(now) + " - Length: " + str(len(petitions)) + ".txt"

    print("\nOpening "+filename)
    with open(filename, 'a') as f:  # Appending
        print("Writing to " + filename)
        for i in petitions:
            f.write(str(i))
            f.write("\n")  # There will be one extra line at end of file.

    print(filename +" written\n")

    graphing.Graphs(petitions)



def alltime(petitions: list) -> None:
    """
    Gets the last line of signatureTotals.txt
    Splits it into date [(YYYY-MM-DD), totalSigs)] then checks if the day isn't today.
    If so finds the totalSigs for all time by reading entire petitions list.
    Writes total sigs to the end of the file in the form - YYYY-MM-DD totalSigs) - Including the space.

    :param petitions: Full list of petitions
    :type petitions: list
    :rtype: None
    """

    tz = timezone('EST')
    now = datetime.now(tz).date()

    lastLine = ""
    with open('dailySignatures/signatureTotals.txt', 'r') as f:  # Reading contents
        for line in f:
            lastLine = line  # Will end with this as the actual last line.

    lastLine = lastLine.split()  # Split by the one space character.

    if lastLine[0] != str(now):  # Is the day NOT today?
        print("Writing today's total sigs\n")
        totalSigs = 0
        for p in petitions:
            totalSigs += p.signatures
        
        with open('dailySignatures/signatureTotals.txt', 'a') as f:  # Appending
            f.write('\n')
            f.write(str(now) + ' ' + str(totalSigs))
    
    graphing.buildAllTimeGraph()  # Graph


def latest(petitionsLatest: list):
    """
    Handles the calling of the graph function for individual petitions, as well as storing petition signature data.

    For every petition in the not expired petitions, if it doesn't have an existing storage file create one.
    Then write 'yesterdays-date 0' and 'todays-date currentSigs'.
    If the file already exists append 'todays-date currentSigs' to it's storage file.
    The style for the storage is 'expiry-date petition-id.txt'
    Update the currentFiles which is a list of all files in the petitions/current folder.
    Then for every current file in the current folder, graph it, then if it has expired move it to the expired folder.

    :param petitionsLatest: All not expired petitions
    :type petitionsLatest: list
    """

    tz = timezone('EST')
    now = datetime.now(tz).date()  # Date object (so just year month and day, no time)
    print("\n\nToday is hopefully:\n", now)
    currentFolder = os.getcwd()+"/petitions/current"  # Location of currentFolder within the entire filesystem
    expiredFolder = os.getcwd()+"/petitions/expired"  # Location of expiredFolder within the entire filesystem
    currentFiles = os.listdir(currentFolder) # List of names of every file in currentFolder

    for p in petitionsLatest:
        pFilename = str(p.expires) + " " + str(p.id) + ".txt"
        filename = 'petitions/current/'+ pFilename
        if pFilename not in currentFiles:
            first = (now - relativedelta(days=+1))
            with open(filename, 'w') as f:
                f.write(first.strftime('%m/%d') + " 0\n")
                f.write(now.strftime('%m/%d') + " " + str(p.signatures))
        else:
            with open(filename, 'a') as f:
                f.write("\n" + now.strftime('%m/%d') + " " + str(p.signatures))

    currentFiles = os.listdir(currentFolder)  # Update the list with the newly created files

    for f in currentFiles:
        filename = 'petitions/current/'+ f
        graphing.buildPetitionGraph(filename)  # Newly expired petitions get graphed one last time as well
        fileDate = f.split()[0]
        pExpire = datetime.strptime(fileDate, '%Y-%m-%d').date()
        if pExpire < now:  # Getting rid of now expired folders
            currentLocation = currentFolder + "/" + f
            newLocation = expiredFolder + "/" + f
            os.rename(currentLocation, newLocation)