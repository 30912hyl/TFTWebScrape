from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import time
#git init   git add main.py   git commit -m ""     git push origin master
noMatch = True
#Prints url of player if matches given unit and minimum playrate inputs
def findName(unit,url,min):
    html_text = requests.get(url).text

    count = 0
    count2 = 0
    playList = []
    
    soup = BeautifulSoup(html_text, 'lxml')
    tags = soup.find_all('td',class_="name")                #list of recent trend units/traits
    plays = soup.find_all('td',class_="plays")              #list of # of plays of units/traits

    for name in plays:                                      #list of unit plays
        if(count >= 10):
            playList.append(name.text)
        count+=1
        
    for name in tags:
        if(name.a is not None):                             #filter out traits
            champ = name.a.text.replace(' ','').strip()
            numberOfPlays = int(playList[count2-10])     
            #print(champ)
            #print(playList[count2-10])
            if(champ==unit and numberOfPlays>min):            #searches for given unit + >min # of plays
                print(champ+" is played "+str(numberOfPlays)+" times by: "+url)
                print()
                noMatch = False
            count2+=1    
    
#Compiles urls for every player present on leaderboard url
def players(url):
    playerList = []
    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, 'lxml')
    tags = soup.find_all('table',class_="table table-page-0 table-sort-tier")   
    tags2 = soup.find_all('table',class_="table table-page-1 table-sort-tier")  #for 1st page of a region
    tags = tags+tags2
    project_href = []
    
    for names in tags:
        project_href = [i['href'] for i in names.find_all('a', href=True)]   

    for name in project_href:
        if("https://lolchess.gg/profile/" in name):
            playerList.append(name)

    return playerList

#Flattens all nested lists from input
def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item
             
def main():
    t0 = time.time()

    #INITIALIZE PARAMETERS HERE
    champ = "Gnar"
    min = 5
    playerList = []
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=na'))
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=na&page=2'))
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=na&page=3'))
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=kr'))
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=kr&page=2'))
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=kr&page=3'))
    playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=euw'))
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=euw&page=2'))
    #playerList.append(players('https://lolchess.gg/leaderboards?mode=ranked&region=euw&page=3'))    
    
    playerList = list(flatten(playerList))    
    print("Summoners who play " + champ + ":")
    for player in playerList:
        findName(champ,player,min)

    if(noMatch):
        print("Sorry, no summoners match the search.")
    
    t1 = time.time() 
    print(f"{'%.2f'%(t1-t0)} seconds to analyze {len(playerList)} urls")
    

if __name__ == "__main__":
    main()