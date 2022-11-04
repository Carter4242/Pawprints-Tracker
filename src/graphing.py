"""
PAWPRINTS-WEBSCRAPER

This module handles the creation of graphs using the petitions data.

Author: Carter4242
https://github.com/Carter4242
"""


from format import Petition  # Dataclass for type hint
import matplotlib.pyplot as plt  # Graphing
import os  # Getting file names


def Graphs(petitions: list) -> None:
    """
    Bit of a mess right now, will sort out later.

    :param petitions: Full list of petitions
    :type petitions: list
    :rtype: None
    """

    xValues = []

    if (petitions[0].timestamp.year != petitions[-1].timestamp.year):
        for m in range(petitions[0].timestamp.month, 13):
            dateStr = str(m) + r"/" + str(petitions[0].timestamp.year)
            xValues.append(dateStr)

        if ((petitions[0].timestamp.year+1) != petitions[-1].timestamp.year):
            for y in range(petitions[0].timestamp.year+1,petitions[-1].timestamp.year):
                for m in range(1,13):
                    dateStr = str(m) + r"/" + str(y)
                    xValues.append(dateStr)

        for m in range(1, petitions[-1].timestamp.month+1):
            dateStr = str(m) + r"/" + str(petitions[-1].timestamp.year)
            xValues.append(dateStr)

    else:
        for m in range(petitions[0].timestamp.month, petitions[-1].timestamp.month+1):
                dateStr = str(m) + r"/" + str(petitions[-1].timestamp.year)
                xValues.append(dateStr)
    

    yearMonthsList = []
    for p in petitions:
        dateStr = str(p.timestamp.month) + r"/" + str(p.timestamp.year)
        yearMonthsList.append(dateStr)

    yValuesIgnored, yValuesResponded, yValuesSigsOverCharged, yValuesSigsOverNotCharged = [], [], [], []
    lIgnored, lResponded, lSigsOverCharged, lSigsNotOverCharged = 0, 0, 0, 0
    lCountUp = -1
    lCountDown = 0
    for x in xValues:
        countPetitions = yearMonthsList.count(x)
        lCountDown = countPetitions
        lCountUp += countPetitions
        for i in range(lCountDown):
            if petitions[lCountUp-i].response == False:
                if petitions[lCountUp-i].signatures >= 200:
                    if petitions[lCountUp-i].charged:
                        lSigsOverCharged += 1
                    else:
                        lSigsNotOverCharged += 1
                else:
                    lIgnored += 1
            else:
                lResponded += 1

        yValuesIgnored.append(lIgnored)
        yValuesResponded.append(lResponded)
        yValuesSigsOverCharged.append(lSigsOverCharged)
        yValuesSigsOverNotCharged.append(lSigsNotOverCharged)
        lIgnored, lResponded, lSigsOverCharged, lSigsNotOverCharged = 0, 0, 0, 0
    
    xRespondedList = []
    for i in range(len(yValuesSigsOverCharged)):
        xRespondedList.append(yValuesSigsOverCharged[i] + yValuesSigsOverNotCharged[i])

    xIgnoreList = []
    for i in range(len(yValuesSigsOverCharged)):
        xIgnoreList.append(yValuesSigsOverCharged[i] + yValuesResponded[i] + yValuesSigsOverNotCharged[i])


    print("\nGraphing Detailed")
    plt.figure(figsize=(12, 9), dpi=80)
    plt.bar(xValues, yValuesSigsOverNotCharged, 0.8, color = ['#FF0000'], label='Not Responded ≥ 200 Signatures + Not Charged')
    plt.bar(xValues, yValuesSigsOverCharged, 0.8, bottom=yValuesSigsOverNotCharged, color = ['#FF8000'], label='Not Responded ≥ 200 Signatures + Charged')
    plt.bar(xValues, yValuesResponded, 0.8, bottom=xRespondedList, color = ['#00E600'], label='Responded')
    plt.bar(xValues, yValuesIgnored, 0.8, bottom=xIgnoreList, color = ['#4E2C2C'], label='Not Responded < 200 Signatures')

    plt.ylabel("Petitions")
    plt.legend()

    plt.xticks(fontsize=8)
    plt.xticks(rotation = 90)

    plt.margins(0.005, tight=True)
    plt.tight_layout(pad=0.5)

    plt.savefig('graphsFull/BarGraph_Detailed.svg')
    plt.close()


    yValuesSigsOver = []
    for i in range(len(yValuesSigsOverCharged)):
        yValuesSigsOver.append(yValuesSigsOverCharged[i] + yValuesSigsOverNotCharged[i])

    print("Graphing Regular\n")
    plt.figure(figsize=(12, 9), dpi=80)
    plt.bar(xValues, yValuesSigsOver, 0.8, color = ['#FF0000'], label='Not Responded ≥ 200 Signatures')
    plt.bar(xValues, yValuesResponded, 0.8, bottom=yValuesSigsOver, color = ['#00E600'], label='Responded')
    plt.bar(xValues, yValuesIgnored, 0.8, bottom=xIgnoreList, color = ['#4E2C2C'], label='Not Responded < 200 Signatures')

    plt.ylabel("Petitions")
    plt.legend()

    plt.xticks(fontsize=8)
    plt.xticks(rotation = 90)

    plt.margins(0.005, tight=True)
    plt.tight_layout(pad=0.5)

    plt.savefig('graphsFull/BarGraph_Regular.svg')
    plt.close()


    tagsDict = {}
    for x in xValues:
        tagsDict[x] = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    for i in range(len(yearMonthsList)):
        for t in petitions[i].tags:
            tagsDict[yearMonthsList[i]][t.id] += 1

    tagsList = ['Technology', 'Academics', 'Parking_Transportation', 'Other', 'Dining', 'Sustainability', 'Facilities', 'Housing', 'Public_Safety', 'Campus_Life', 'Governance', 'Clubs_Organizations', 'Deaf_Advocacy']
    for i in range(13):
        print('Graphing ' + tagsList[i])
        yValues = []
        for x in xValues:
            yValues.append(tagsDict[x][i])
        plt.figure(figsize=(12, 9), dpi=80)
        plt.bar(xValues, yValues, 0.8, color = ['#4E2C2C'])
        plt.ylabel("Petitions")
        plt.axis.TickLabelFormat = '%d'
        plt.xticks(fontsize=8)
        plt.xticks(rotation = 90)
        plt.margins(0.005, tight=True)
        plt.tight_layout(pad=0.5)
        plt.savefig('graphsFull/BarGraph_' + tagsList[i] + '.svg')
        plt.close()

    print("\nGraphing Total Petitions\n")

    totalPetitionsY = []
    TotalPetitions = 0
    for i in range(len(xValues)):
        TotalPetitions += (yValuesSigsOver[i] + yValuesResponded[i] + yValuesIgnored[i])
        totalPetitionsY.append(TotalPetitions)

    plt.figure(figsize=(12, 9), dpi=80)
    plt.plot(xValues, totalPetitionsY, "-o")
    plt.ylabel("Petitions")
    plt.axis.TickLabelFormat = '%d'
    plt.xticks(fontsize=8)
    plt.xticks(rotation = 90)
    plt.margins(0.005, tight=True)
    plt.tight_layout(pad=0.5)
    plt.savefig('graphsFull/LineGraph_totalPetitions.svg')
    plt.close()
    

def buildAllTimeGraph() -> None:
    """
    Bit of a mess right now, will sort out later.

    :param petitions: Full list of petitions
    :type petitions: list
    :rtype: None
    """

    print("Graphing Total Signatures\n")

    startingTotal = 0
    with open('dailySignatures/signatureTotals.txt', 'r') as f:
        startingTotal = int(f.readline().split()[1])
    
    totalSigsY = []
    datesX = []
    with open('dailySignatures/signatureTotals.txt', 'r') as f:
        for line in f:
            data = line.split()
            datesX.append(data[0])
            totalSigsY.append(int(data[1])-startingTotal)
    plt.figure(figsize=(12, 9), dpi=80)
    plt.plot(datesX, totalSigsY, "-o")
    plt.ylabel("Signatures")
    plt.axis.TickLabelFormat = '%d'
    plt.xticks(fontsize=8)
    plt.xticks(rotation = 90)
    plt.margins(0.005, tight=True)
    plt.tight_layout(pad=0.5)
    plt.savefig('graphsFull/LineGraph_totalSigs.svg')
    plt.close()


def buildPetitionGraph(filename: str) -> None:
    """
    Builds individual petition graphs.
    For every line of the file the first item is the date/xValue and the second value is the numSigs/yValue.
    Creates graph from those values in location graphsSingle/Petition-ID.svg

    :param filename: filename in the form 'YYYY-MM-DD Petition-ID'
    :type filename: str
    """

    datesX = []
    sigsY = []
    dataAndID = filename.split()
    print("Graphing", dataAndID[1])
    with open(filename, 'r') as f:
        for line in f:
            l = line.split()
            datesX.append(l[0])
            sigsY.append(int(l[1]))
    
    plt.figure(figsize=(12, 9), dpi=80)
    plt.plot(datesX, sigsY, "-o")
    plt.ylabel("Signatures")
    plt.axis.TickLabelFormat = '%d'
    plt.xticks(fontsize=8)
    plt.xticks(rotation = 90)
    plt.margins(0.005, tight=True)
    plt.tight_layout(pad=0.5)
    plt.savefig('graphsSingle/' + str(dataAndID[1][:-4]) + '.svg')
    plt.close()
