import requests
from bs4 import BeautifulSoup
from bs4 import Comment


def main():
    player1Stats = []
    player2Stats = []

    player1FirstName = getPlayerFirstName()
    player1LastName = getPlayerLastName()

    player2FirstName = getPlayerFirstName()
    player2LastName = getPlayerLastName()

    url1 = getURL(player1FirstName, player1LastName)
    url2 = getURL(player2FirstName, player2LastName)

    player1FullName = player1FirstName + " " + player1LastName
    player2FullName = player2FirstName + " " + player2LastName

    player1CollegeExp = getCollegeExp(player1FullName)
    player2CollegeExp = getCollegeExp(player2FullName)

    listOfStats = getStatsToCompare()

    player1Stats = getInfo(url1, player1CollegeExp, listOfStats)
    player2Stats = getInfo(url2, player2CollegeExp, listOfStats)

    player1Stats, player2Stats = compareStats(player1Stats, player2Stats, listOfStats)

    player1FullName = padStringsWithWhitespace(player1FullName, 20)
    player2FullName = padStringsWithWhitespace(player2FullName, 20)
    player1Stats, player2Stats = padStats(player1Stats, player2Stats)

    print(padStringsWithWhitespace("Player Name", 30), player1FullName.title(), player2FullName.title())
    printResults(player1Stats, player2Stats, listOfStats)


def getPlayerFirstName():
    playerFirstName = input("Enter a player's firstname:")
    playerFirstName = playerFirstName.lower()
    return playerFirstName


def getPlayerLastName():
    playerLastName = input("Enter the player's lastname:")
    playerLastName = playerLastName.lower()
    return playerLastName


def getStatsToCompare():
    print("available stats for comparison: ")
    print("ortg, drtg, ts, usgrtg, ws, obpm, dbpm, bpm, +/-per100, sfd")
    strOfStats = input("Enter the stats you want to compare from the list above, each separated by a space "
                       "(please type them in the order they appear in the list):")
    listOfStats = strOfStats.split(" ")
    return listOfStats


def getURL(playerFirstName, playerLastName):
    baseUrl = 'http://www.basketball-reference.com/players/'
    url = baseUrl + playerLastName[:1] + "/" + playerLastName[:5] + playerFirstName[:2] + "01.html"
    return url


def getCollegeExp(playerName):
    skipped_college = ["Reggie Harding", "Darryl Dawkins", "Bill Willoughby", "Kevin Garnett", "Kobe Bryant",
                       "Jermaine O'Neal", "Tracy McGrady", "Al Harrington", "Rashard Lewis", "Korleone Young",
                       "Jonathan Bender", "Leon Smith", "Darius Miles", "DeShawn Stevenson", "Kwame Brown",
                       "Tyson Chandler", "Eddy Curry", "DeSagana Diop", "Amar'e Stoudemire", "LeBron James",
                       "Travis Outlaw", "Ndudi Ebi", "Kendrick Perkins", "James Lang", "Dwight Howard",
                       "Shaun Livingston", "Robert Swift", "Sebastian Telfair", "Al Jefferson", "Josh Smith",
                       "J. R. Smith", "Dorell Wright", "Martell Webster", "Andrew Bynum", "Gerald Green",
                       "C. J. Miles", "	Monta Ellis", "Louis Williams", "Andray Blatche", "Amir Johnson",
                       "Thon Maker"]
    collegeExp = 0

    for player in skipped_college:
        if playerName.lower() == player.lower():
            collegeExp = 1

    return collegeExp


def getInfo(url, collegeExp, listOfStats):
    stats = []
    beautifulSoupObject, comments = getSoup(url)
    adv, per100Poss, pbp = getTables(comments)
    offensiveRating = -1000.0
    defensiveRating = -1000.0
    trueShootingPct = -1000.0
    usageRate = -1000.0
    winShares = -1000.0
    offensiveBoxPlusMinus = -1000.0
    defensiveBoxPlusMinus = -1000.0
    boxPlusMinus = -1000.0
    onCourtPlusMinusPer100 = -1000.0
    sfDrawn = -1000.0

    experience = getExperience(beautifulSoupObject, collegeExp)

    for stat in listOfStats:
        if stat == 'ortg':
            offensiveRating = getOffRtg(per100Poss, experience)
            stats.append(offensiveRating)
        elif stat == 'drtg':
            defensiveRating = getDefRtg(per100Poss, experience)
            stats.append(defensiveRating)
        elif stat == 'ts':
            trueShootingPct = getTS(adv, experience)
            stats.append(trueShootingPct)
        elif stat == 'usgrtg':
            usageRate = getUsgRate(adv, experience)
            stats.append(usageRate)
        elif stat == 'ws':
            winShares = getWS(adv, experience)
            stats.append(winShares)
        elif stat == 'obpm':
            offensiveBoxPlusMinus = getOBPM(adv, experience)
            stats.append(offensiveBoxPlusMinus)
        elif stat == 'dbpm':
            defensiveBoxPlusMinus = getDBPM(adv, experience)
            stats.append(defensiveBoxPlusMinus)
        elif stat == 'bpm':
            offensiveBoxPlusMinus = getOBPM(adv, experience)
            defensiveBoxPlusMinus = getDBPM(adv, experience)
            boxPlusMinus = offensiveBoxPlusMinus + defensiveBoxPlusMinus
            stats.append(boxPlusMinus)
        elif stat == '+/-per100':
            onCourtPlusMinusPer100 = getOnCourtPlusMinusPer100(pbp, experience)
            stats.append(onCourtPlusMinusPer100)
        elif stat == 'sfd':
            sfDrawn = getSFDrawn(pbp, experience)
            stats.append(sfDrawn)

    return stats


def getTables(comments):
    per100Poss = BeautifulSoup(comments[24], "lxml")
    adv = BeautifulSoup(comments[28], "lxml")
    pbp = BeautifulSoup(comments[30], "lxml")
    return adv, per100Poss, pbp


def getSoup(url):
    sourcecode = requests.get(url)
    plaintext = sourcecode.text
    beautifulSoupObject = BeautifulSoup(plaintext, "html.parser")
    beautifulSoupObject.prettify()
    comments = beautifulSoupObject.findAll(text=lambda text: isinstance(text, Comment))
    return beautifulSoupObject, comments


def getExperience(beautifulSoupObject, collegeExp):
    # 11 if college, 10 if no college, exp_college is = to 1 if they skipped college
    experience = beautifulSoupObject.findAll('p')[11 - collegeExp].getText()
    exp = str(experience)
    exp = "".join(exp.split())
    exp = exp[11:]
    exp = exp[:(len(exp) - 5)]
    exp = int(exp)
    return exp


def getOffRtg(per100Poss, expNum):
    offRtg = per100Poss.findAll('td', attrs={"data-stat": "off_rtg"})[expNum - 1]
    offRtgList = []
    for char in offRtg:
        offRtgList.append(str(char))
    offRtgStr = ''.join(offRtgList)
    offensiveRating = float(offRtgStr)
    return offensiveRating


def getDefRtg(per100Poss, expNum):
    defRtg = per100Poss.findAll('td', attrs={"data-stat": "def_rtg"})[expNum - 1]
    defRtgList = []
    for char in defRtg:
        defRtgList.append(str(char))
    defRtgStr = ''.join(defRtgList)
    defensiveRating = float(defRtgStr)
    return defensiveRating


def getTS(adv, expNum):
    ts = adv.findAll('td', attrs={"data-stat": "ts_pct"})[expNum - 1]
    tsList = []
    for char in ts:
        tsList.append(str(char))
    tsStr = ''.join(tsList)
    trueShootingPct = float(tsStr)
    return trueShootingPct


def getUsgRate(adv, expNum):
    usageRate = adv.findAll('td', attrs={"data-stat": "usg_pct"})[expNum - 1]
    usageRateList = []
    for char in usageRate:
        usageRateList.append(str(char))
    usageRateStr = ''.join(usageRateList)
    usageRate = float(usageRateStr)
    return usageRate


def getWS(adv, expNum):
    ws = adv.findAll('td', attrs={"data-stat": "ws"})[expNum - 1]
    wsList = []
    for char in ws:
        wsList.append(str(char))
    wsStr = ''.join(wsList)
    winShares = float(wsStr)
    return winShares


def getOBPM(adv, expNum):
    obpm = adv.findAll('td', attrs={"data-stat": "obpm"})[expNum - 1]
    obpmList = []
    for char in obpm:
        obpmList.append(str(char))
    obpmStr = ''.join(obpmList)
    offensiveBoxPlusMinusNum = float(obpmStr)
    return offensiveBoxPlusMinusNum


def getDBPM(adv, expNum):
    dbpm = adv.findAll('td', attrs={"data-stat": "dbpm"})[expNum - 1]
    dbpmList = []
    for char in dbpm:
        dbpmList.append(str(char))
    dbpmStr = ''.join(dbpmList)
    defensiveBoxPlusMinusNum = float(dbpmStr)
    return defensiveBoxPlusMinusNum


def getBPM(obpm, dbpm):
    bpm = obpm + dbpm
    return bpm


def getOnCourtPlusMinusPer100(pbp, expNum):
    ocpmPer100 = pbp.findAll('td', attrs={"data-stat": "plus_minus_on"})[expNum - 1]
    ocpmPer100List = []
    for char in ocpmPer100:
        ocpmPer100List.append(str(char))
    ocpmPer100Str = ''.join(ocpmPer100List)
    ocpmPer100Num = float(ocpmPer100Str)
    return ocpmPer100Num


def getSFDrawn(pbp, expNum):
    sfDrawn = pbp.findAll('td', attrs={"data-stat": "drawn_shooting"})[expNum - 1]
    sfDrawnList = []
    for char in sfDrawn:
        sfDrawnList.append(str(char))
    sfDrawnStr = ''.join(sfDrawnList)
    sfDrawnNum = float(sfDrawnStr)
    return sfDrawnNum


def compareStats(player1Stats, player2Stats, listOfStats):
    retListPlayer1 = []
    retListPlayer2 = []
    for stat1, stat2, statName in zip(player1Stats, player2Stats, listOfStats):
        if statName == 'drtg' or statName == 'usgrtg':
            temp1, temp2 = compareTwoStatsLow(stat1, stat2)
            retListPlayer1.append(temp1)
            retListPlayer2.append(temp2)
        else :
            temp1, temp2 = compareTwoStatsHigh(stat1, stat2)
            retListPlayer1.append(temp1)
            retListPlayer2.append(temp2)
    return retListPlayer1, retListPlayer2


def compareTwoStatsHigh(stat1Num, stat2Num):
    stat1 = str(stat1Num)
    stat2 = str(stat2Num)
    if stat1Num > stat2Num:
        stat1 = "-->" + stat1
        stat2 = "" + stat2
    else:
        stat1 = "" + stat1
        stat2 = "-->" + stat2
    return stat1, stat2


def compareTwoStatsLow(stat1Num, stat2Num):
    stat1 = str(stat1Num)
    stat2 = str(stat2Num)
    if stat1Num < stat2Num:
        stat1 = "-->" + stat1
        stat2 = "" + stat2
    else:
        stat1 = "" + stat1
        stat2 = "-->" + stat2
    return stat1, stat2


def padStats(player1Stats, player2Stats):
    retStatsPlayer1 = []
    retStatsPlayer2 = []
    for stat1, stat2 in zip(player1Stats, player2Stats):
        stat1 = padStringsWithWhitespace(stat1, 20)
        stat2 = padStringsWithWhitespace(stat2, 20)
        retStatsPlayer1.append(stat1)
        retStatsPlayer2.append(stat2)
    return retStatsPlayer1, retStatsPlayer2


def padStringsWithWhitespace(string, padding):
    while len(string) < padding:
        string = " " + string
    return string


def printResults(player1Stats, player2Stats, listOfStats):
    for stat1, stat2, statName in zip(player1Stats, player2Stats, listOfStats):
        if statName == 'ortg':
            print(padStringsWithWhitespace("Offensive Rating", 30), stat1, stat2)
        if statName == 'drtg':
            print(padStringsWithWhitespace("Defensive Rating", 30), stat1, stat2)
        if statName == 'ts':
            print(padStringsWithWhitespace("True Shooting %", 30), stat1, stat2)
        if statName == 'usgrtg':
            print(padStringsWithWhitespace("Usage Rate %", 30), stat1, stat2)
        if statName == 'ws':
            print(padStringsWithWhitespace("Win Shares", 30), stat1, stat2)
        if statName == 'obpm':
            print(padStringsWithWhitespace("Offensive Box Plus Minus", 30), stat1, stat2)
        if statName == 'dbpm':
            print(padStringsWithWhitespace("Defensive Box Plus Minus", 30), stat1, stat2)
        if statName == 'bpm':
            print(padStringsWithWhitespace("Box Plus Minus", 30), stat1, stat2)
        if statName == '+/-per100':
            print(padStringsWithWhitespace("On-court Plus Minus Per 100", 30), stat1, stat2)
        if statName == 'sfd':
            print(padStringsWithWhitespace("Shooting Fouls Drawn", 30), stat1, stat2)

main()
