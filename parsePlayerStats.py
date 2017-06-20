import requests
from bs4 import BeautifulSoup
from bs4 import Comment


def main():
    player1Stats = []  # holds all of the stats for player 1 in the order that the user typed them in
    player2Stats = []  # holds all of the stats for player 2 in the order that the user typed them in

    player1FirstName = getPlayerFirstName()  # gets the first player's first name
    player1LastName = getPlayerLastName()  # gets the first player's last name

    player2FirstName = getPlayerFirstName()  # gets the second player's first name
    player2LastName = getPlayerLastName()  # gets the second player's last name

    url1 = getURL(player1FirstName, player1LastName)  # crafts the basketball-reference url for player 1
    url2 = getURL(player2FirstName, player2LastName)  # crafts the basketball-reference url for player 2

    player1FullName = player1FirstName + " " + player1LastName  # generates the full name for player 1
    player2FullName = player2FirstName + " " + player2LastName  # generates the full name for player 2

    player1CollegeExp = getCollegeExp(player1FullName)  # finds out whether player 1 went to college or not
    player2CollegeExp = getCollegeExp(player2FullName)  # finds out whether player 2 went to college or not

    listOfStats = getStatsToCompare()  # gets the stats that the user wants to use to compare the two players

    player1Stats = getInfo(url1, player1CollegeExp, listOfStats)  # gets the stats for player 1
    player2Stats = getInfo(url2, player2CollegeExp, listOfStats)  # gets the stats for palyer 2

    player1Stats, player2Stats = compareStats(player1Stats, player2Stats, listOfStats)  # compares the stats

    player1FullName = padStringsWithWhitespace(player1FullName, 20)  # pads player 1's name with white space
    player2FullName = padStringsWithWhitespace(player2FullName, 20)  # pads player 2's name with white space
    player1Stats, player2Stats = padStats(player1Stats, player2Stats)  # pads all stats with white space

    print(padStringsWithWhitespace("Player Name", 30), player1FullName.title(), player2FullName.title())
    printResults(player1Stats, player2Stats, listOfStats)  # prints the stats in a table format


#
# Gets  and returns a player's first name by prompting the user
#
# @return: playerFirstName - the player's first name
def getPlayerFirstName():
    playerFirstName = input("Enter a current player's firstname:")  # asks for player's first name
    playerFirstName = playerFirstName.lower()  # makes the input all lowercase letters
    return playerFirstName


#
# Gets and returns a player's last name by prompting the user
#
# @return: playerLastName - the player's last name
def getPlayerLastName():
    playerLastName = input("Enter the player's lastname:")  # asks for player's last name
    playerLastName = playerLastName.lower()  # makes the input all lowercase letters
    return playerLastName


#
# Prompts the user for which stats they would like to use to compare the two players
#
# @return: listOfStats - a list of the stats entered in the order they were entered
def getStatsToCompare():
    print("Available stats for comparison: ortg, drtg, ts, usgrtg, ws, obpm, dbpm, bpm, +/-per100, sfd")
    strOfStats = input("Enter the stats you want to compare from the list above, each separated by a space "
                       "(please type them in the order they appear in the list):")
    listOfStats = strOfStats.split(" ")
    return listOfStats


#
# Gets and returns the Basketball-Reference(BBallRef) URL for a given player
#
# @param: playerFirstName - the player's first name, playerLastName - the player's last name
# @return: the BBallRef URL for the player
def getURL(playerFirstName, playerLastName):
    baseUrl = 'http://www.basketball-reference.com/players/'
    url = baseUrl + playerLastName[:1] + "/" + playerLastName[:5] + playerFirstName[:2] + "01.html"
    return url


#
# Returns whether a given player went to college or not
#
# @param: playerName - the player's full name
# @return 1 if the player skipped college, 0 if the palyer went to college
def getCollegeExp(playerName):
    collegeExp = 0
    # this is a list of the players that have skipped college
    skipped_college = ["Reggie Harding", "Darryl Dawkins", "Bill Willoughby", "Kevin Garnett", "Kobe Bryant",
                       "Jermaine O'Neal", "Tracy McGrady", "Al Harrington", "Rashard Lewis", "Korleone Young",
                       "Jonathan Bender", "Leon Smith", "Darius Miles", "DeShawn Stevenson", "Kwame Brown",
                       "Tyson Chandler", "Eddy Curry", "DeSagana Diop", "Amar'e Stoudemire", "LeBron James",
                       "Travis Outlaw", "Ndudi Ebi", "Kendrick Perkins", "James Lang", "Dwight Howard",
                       "Shaun Livingston", "Robert Swift", "Sebastian Telfair", "Al Jefferson", "Josh Smith",
                       "J. R. Smith", "Dorell Wright", "Martell Webster", "Andrew Bynum", "Gerald Green",
                       "C. J. Miles", "	Monta Ellis", "Louis Williams", "Andray Blatche", "Amir Johnson",
                       "Thon Maker"]

    for player in skipped_college:
        if playerName.lower() == player.lower():  # check if the player is in the list of players that skipped college
            collegeExp = 1

    return collegeExp


#
# Gets and returns all of the stats that were specified for a given player
#
# @param: url - the player's BBallRef URL, collegeExp - whether the skipped college or not,
#                                        listOfStats - the list to get for the given player
# @return: a list of the stats gathered for the given player
def getInfo(url, collegeExp, listOfStats):
    stats = []  # list to put the stats into
    # gets the beautiful soup object and the comments in the html of the BBallRef page for the player
    beautifulSoupObject, comments = getSoup(url)
    adv, per100Poss, pbp = getTables(comments)  # gets the advanced, per 100 possessions, and play by play tables

    # all the stats start with a value of -1000 which represents a dummy value that is not possible
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

    experience = getExperience(beautifulSoupObject, collegeExp)  # gets the NBA players total career years

    for stat in listOfStats:  # for each stat that was requested
        if stat == 'ortg':
            offensiveRating = getOffRtg(per100Poss, experience)  # gets the offensive rating for this player
            stats.append(offensiveRating)
        elif stat == 'drtg':
            defensiveRating = getDefRtg(per100Poss, experience)  # gets the defensive rating for this player
            stats.append(defensiveRating)
        elif stat == 'ts':
            trueShootingPct = getTS(adv, experience)  # gets the true shooting percentage for this player
            stats.append(trueShootingPct)
        elif stat == 'usgrtg':
            usageRate = getUsgRate(adv, experience)  # gets the usage rate for this player
            stats.append(usageRate)
        elif stat == 'ws':
            winShares = getWS(adv, experience)  # gets the win shares for this player
            stats.append(winShares)
        elif stat == 'obpm':
            offensiveBoxPlusMinus = getOBPM(adv, experience)  # gets the offensive box plus minus for this player
            stats.append(offensiveBoxPlusMinus)
        elif stat == 'dbpm':
            defensiveBoxPlusMinus = getDBPM(adv, experience)  # gets the defensive box plus minus for this player
            stats.append(defensiveBoxPlusMinus)
        elif stat == 'bpm':
            offensiveBoxPlusMinus = getOBPM(adv, experience)
            defensiveBoxPlusMinus = getDBPM(adv, experience)
            # gets the box plus minus for this player
            boxPlusMinus = offensiveBoxPlusMinus + defensiveBoxPlusMinus  # the bpm is obpm + dbpm
            stats.append(boxPlusMinus)
        elif stat == '+/-per100':
            # gets the on court plus minus per 100 possessions for this player
            onCourtPlusMinusPer100 = getOnCourtPlusMinusPer100(pbp, experience)
            stats.append(onCourtPlusMinusPer100)
        elif stat == 'sfd':
            sfDrawn = getSFDrawn(pbp, experience)  # gets the shooting fouls drawn for this player
            stats.append(sfDrawn)

    return stats


#
# Gets and returns the per 100 possessions, advanced, and play by play tables for a player given the players BBallRef
# page's html comments. The comments hold these tables
#
# @param: comments - the comments from the BBallRef page of the player
# @return: adv - the advanced stats table, per100poss - the per 100 possessions table,
#                           pbp - the play by play table
def getTables(comments):
    per100Poss = BeautifulSoup(comments[24], "lxml")
    adv = BeautifulSoup(comments[28], "lxml")
    pbp = BeautifulSoup(comments[30], "lxml")
    return adv, per100Poss, pbp


#
# Gets and returns the beautiful soup object and the comments for a given player
#
# @param: url - the URL for the player's BBallRef page
# @return: beautifulSoupObject - the beautiful soup object, comments - the comments for this player
def getSoup(url):
    sourcecode = requests.get(url)  # connect to the webpage
    plaintext = sourcecode.text  # get a plain text version
    beautifulSoupObject = BeautifulSoup(plaintext, "html.parser")  # this object is an html parser
    beautifulSoupObject.prettify()  # makes the html more readable
    comments = beautifulSoupObject.findAll(text=lambda text: isinstance(text, Comment))  # gets all html comments
    return beautifulSoupObject, comments


#
# Gets and returns player's NBA experience in years
#
# @param: beautifulSoupObject - the beautiful soup object, collegeExp - whether the player skipped college or not
# @return: exp - the player's NBA experience
def getExperience(beautifulSoupObject, collegeExp):
    # 11 if college, 10 if no college, exp_college is = to 1 if they skipped college
    experience = beautifulSoupObject.findAll('p')[11 - collegeExp].getText()
    exp = str(experience)
    exp = "".join(exp.split())  # generates the experience string
    exp = exp[11:]
    exp = exp[:(len(exp) - 5)]
    exp = int(exp)  # turns the experience string to a number
    return exp


#
# Gets and returns the offensive rating for the given player
#
# @param: per100poss - the per 100 possessions table, expNum - given player's NBA experience
# @return: offensiveRating - the offensive rating for the given player
def getOffRtg(per100Poss, expNum):
    offRtg = per100Poss.findAll('td', attrs={"data-stat": "off_rtg"})[expNum - 1]  # gets the td for offensive rating
    offRtgList = []
    for char in offRtg:
        offRtgList.append(str(char))  # adds the offensive rating to a list
    offRtgStr = ''.join(offRtgList)  # turns that list to a string
    offensiveRating = float(offRtgStr)  # turns that string to a number
    return offensiveRating


#
# Gets and returns the defensive rating for the given player
#
# @param: per100poss - the per 100 possessions table, expNum - given player's NBA experience
# @return: defensiveRating - the defensive rating for the given player
def getDefRtg(per100Poss, expNum):
    defRtg = per100Poss.findAll('td', attrs={"data-stat": "def_rtg"})[expNum - 1]  # gets the td for defensive rating
    defRtgList = []
    for char in defRtg:
        defRtgList.append(str(char))  # adds the defensive rating to a list
    defRtgStr = ''.join(defRtgList)  # turns that list to a string
    defensiveRating = float(defRtgStr)  # turns that string to a number
    return defensiveRating


#
# Gets and returns the true shooting percentage for the given player
#
# @param: adv - the advanced table, expNum - given player's NBA experience
# @return: trueShootingPct - the true shooting percentage for the given player
def getTS(adv, expNum):
    ts = adv.findAll('td', attrs={"data-stat": "ts_pct"})[expNum - 1]  # gets the td for true shooting percentage
    tsList = []
    for char in ts:
        tsList.append(str(char))  # adds the true shooting percentage to a list
    tsStr = ''.join(tsList)  # turns that list to a string
    trueShootingPct = float(tsStr)  # turns that string to a number
    return trueShootingPct


#
# Gets and returns the usage rate for the given player
#
# @param: adv - the advanced table, expNum - given player's NBA experience
# @return: usageRate - the usage rate for the given player
def getUsgRate(adv, expNum):
    usageRate = adv.findAll('td', attrs={"data-stat": "usg_pct"})[expNum - 1]  # gets the td for usage rate
    usageRateList = []
    for char in usageRate:
        usageRateList.append(str(char))  # adds the usage rate to a list
    usageRateStr = ''.join(usageRateList)  # turns that list to a string
    usageRate = float(usageRateStr)  # turns that string to a number
    return usageRate


#
# Gets and returns the win shares for the given player
#
# @param: adv - the advanced table, expNum - given player's NBA experience
# @return: winShares - the win shares for the given player
def getWS(adv, expNum):
    ws = adv.findAll('td', attrs={"data-stat": "ws"})[expNum - 1]  # gets the td for win shares
    wsList = []
    for char in ws:
        wsList.append(str(char))  # adds the win shares to a list
    wsStr = ''.join(wsList)  # turns that list to a string
    winShares = float(wsStr)  # turns that string to a number
    return winShares


#
# Gets and returns the offensive box plus minus for the given player
#
# @param: adv - the advanced table, expNum - given player's NBA experience
# @return: offensiveBoxPlusMinus - the offensive box plus minus for the given player
def getOBPM(adv, expNum):
    obpm = adv.findAll('td', attrs={"data-stat": "obpm"})[expNum - 1]  # gets the td for offensive box plus minus
    obpmList = []
    for char in obpm:
        obpmList.append(str(char))  # adds the offensive box plus minus to a list
    obpmStr = ''.join(obpmList)  # turns that list to a string
    offensiveBoxPlusMinus = float(obpmStr)  # turns that string to a number
    return offensiveBoxPlusMinus


#
# Gets and returns the defensive box plus minus for the given player
#
# @param: adv - the advanced table, expNum - given player's NBA experience
# @return: defensiveBoxPlusMinus - the defensive box plus minus for the given player
def getDBPM(adv, expNum):
    dbpm = adv.findAll('td', attrs={"data-stat": "dbpm"})[expNum - 1]  # gets the td for defensive box plus minus
    dbpmList = []
    for char in dbpm:
        dbpmList.append(str(char))  # adds the defensive box plus minus to a list
    dbpmStr = ''.join(dbpmList)  # turns that list to a string
    defensiveBoxPlusMinus = float(dbpmStr)  # turns that string to a number
    return defensiveBoxPlusMinus


#
# Calculates and returns the box plus minus for the given player
#
# @param: obpm - the offensive box plus minus for the given player,
#                           dbpm - the defensive box plus minus for the given player
# @return: bpm - the box plus minus for the given player
def getBPM(obpm, dbpm):
    bpm = obpm + dbpm  # box plus minus is the total of the offensive box plus minus and the defensive box plus minus
    return bpm


#
# Gets and returns the on court plus minus per 100 possessions for the given player
#
# @param: pbp - the play by play table, expNum - given player's NBA experience
# @return: onCourtPlusMinusPer100 - the on court plus minus per 100 possessions for the given player
def getOnCourtPlusMinusPer100(pbp, expNum):
    # gets the td for on court plus minus per 100 possessions
    ocpmPer100 = pbp.findAll('td', attrs={"data-stat": "plus_minus_on"})[expNum - 1]
    ocpmPer100List = []
    for char in ocpmPer100:
        ocpmPer100List.append(str(char))  # adds the on court plus minus per 100 possessions to a list
    ocpmPer100Str = ''.join(ocpmPer100List)  # turns that list to a string
    onCourtPlusMinusPer100 = float(ocpmPer100Str)  # turns that string to a number
    return onCourtPlusMinusPer100


#
# Gets and returns the shooting fouls drawn for the given player
#
# @param: pbp - the play by play table, expNum - given player's NBA experience
# @return: shootingFoulsDrawn - the shooting fouls drawn for the given player
def getSFDrawn(pbp, expNum):
    # gets the td for shooting fouls drawn
    sfDrawn = pbp.findAll('td', attrs={"data-stat": "drawn_shooting"})[expNum - 1]
    sfDrawnList = []
    for char in sfDrawn:
        sfDrawnList.append(str(char))  # adds the shooting fouls drawn to a list
    sfDrawnStr = ''.join(sfDrawnList)  # turns that list to a string
    shootingFoulsDrawn = float(sfDrawnStr)  # turns that string to a number
    return shootingFoulsDrawn


#
# Compares the stats for both players and returns the stats in a formatted string which indicates
# which player is ahead in that category
#
# @param: player1Stats - list of the stats for player 1, player2Stats - list of the stats for player 2,
#               listOfStats - list of the stats to compare in the order they are listed in both playerStat lists
# @return: retListPlayer1 - formatted stats for player 1, retListPLayer2 - formatted stats for player 2
def compareStats(player1Stats, player2Stats, listOfStats):
    retListPlayer1 = []  # container for return list for player 1
    retListPlayer2 = []  # container for return list for player 2
    for stat1, stat2, statName in zip(player1Stats, player2Stats, listOfStats):
        if statName == 'drtg' or statName == 'usgrtg':  # for these stats, the lower the number, the better
            temp1, temp2 = compareTwoStatsLow(stat1, stat2)  # compare the two stats
            # appends the formatted stats to the appropriate player's return list
            retListPlayer1.append(temp1)
            retListPlayer2.append(temp2)
        else :
            temp1, temp2 = compareTwoStatsHigh(stat1, stat2)  # for all other stats, the higher the number, the better
            # appends the formatted stats to the appropriate player's return list
            retListPlayer1.append(temp1)
            retListPlayer2.append(temp2)
    return retListPlayer1, retListPlayer2


#
# Compares two stats based on which one is higher and formats them appropriately
#
# @param: stat1Num - the first stat to compare, stat2Num - the second stat to compare
# @return: stat1 - the formatted version of stat1, stat2 - the formatted version of stat2
def compareTwoStatsHigh(stat1Num, stat2Num):
    stat1 = str(stat1Num)
    stat2 = str(stat2Num)
    if stat1Num > stat2Num:  # compares the two stats
        stat1 = "-->" + stat1  # if stat1 was higher, format it with an arrow
        stat2 = "" + stat2
    else:
        stat1 = "" + stat1
        stat2 = "-->" + stat2  # if stat2 was higher, format it with an arrow
    return stat1, stat2


#
# Compares two stats based on which one is lower and formats them appropriately
#
# @param: stat1Num - the first stat to compare, stat2Num - the second stat to compare
# @return: stat1 - the formatted version of stat1, stat2 - the formatted version of stat2
def compareTwoStatsLow(stat1Num, stat2Num):
    stat1 = str(stat1Num)
    stat2 = str(stat2Num)
    if stat1Num < stat2Num:  # compares the two stats
        stat1 = "-->" + stat1  # if stat1 was lower, format it with an arrow
        stat2 = "" + stat2
    else:
        stat1 = "" + stat1
        stat2 = "-->" + stat2  # if stat2 was lower, format it with an arrow
    return stat1, stat2

#
# Pads all stats with white space such that each stat is 20 characters long
#
# @param: player1Stats - the list containing all of player 1's stats,
#                   player2Stats - the list containing all of player 2's stats
# @return: retStatsPlayer1 - formatted list of player 1's stats, retStatsPlayer2 - formatted list of player 2's stats
def padStats(player1Stats, player2Stats):
    retStatsPlayer1 = []  # container for return list for player 1
    retStatsPlayer2 = []  # container for return list for player 2
    for stat1, stat2 in zip(player1Stats, player2Stats):
        # pads each stat with white space
        stat1 = padStringsWithWhitespace(stat1, 20)
        stat2 = padStringsWithWhitespace(stat2, 20)
        # append each stat to the appropriate return list
        retStatsPlayer1.append(stat1)
        retStatsPlayer2.append(stat2)
    return retStatsPlayer1, retStatsPlayer2


#
# Pads a given string with a given amount of padding
#
# @param: string - the string to pad, padding - the amount of padding to put on the string
# @return: string - the padded string
def padStringsWithWhitespace(string, padding):
    while len(string) < padding:
        string = " " + string  # pad the string until the total length reaches the amount passed into for padding
    return string


#
# Prints the result of the comparison of the two players onto the terminal
#
# @param: player1Stats - the list containing stats for player 1, player2Stats - the list containing stats for player 2,
#                     listOfStats - the list of stats to display in the order they appear in each playerStats list
def printResults(player1Stats, player2Stats, listOfStats):
    # prints all of the information to the console with a nice table like format
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
