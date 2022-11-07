import random

from more_itertools import first


class T2Cup:
    allTeams = []
    def entry_team(self,teamObj):
        self.allTeams.append(teamObj)
        
class Team(T2Cup):
    def __init__(self,name) -> None:
        self.teamName = name
        self.playersListOfObject = []
        super().entry_team(self)
    def entry_player(self,player): ## player is a type of Player Object
        self.playersListOfObject.append(player)
    def __repr__(self) -> str:
        return f"From Object. Team Name: {self.teamName}"

class Player:
    def __init__(self,name,teamObj) -> None:
        self.playerName = name
        ## Batsman
        self.strikeRate = 0.0
        self.runBat = 0
        self.ballUsed = 0
        self.fours = 0
        self.sixes = 0
        ## Bowler
        self.runBowl = 0
        self.wicketsTaken = 0
        self.ballsBowled = 0
        teamObj.playersListOfObject.append(self)
    def __repr__(self) -> str:
        return f"From Player Object Name: {self.playerName}"

class Innings:
    def __init__(self,team1,team2,battingTeam,bowlingTeam,) -> None:
        self.teamOneObj=team1
        self.teamTwoObj=team2
        self.battingTeam=battingTeam
        self.bowlingTeam=bowlingTeam
        self.totalRun=0
        self.totalWickets=0
        self.totalOver=0
        self.currentBall=0
        self.currentBatsmanOrder=2
        self.currentBattingList=[battingTeam.playersListOfObject[0],battingTeam.playersListOfObject[1]]
        self.striker=battingTeam.playersListOfObject[0]
        self.currentBowler=None
        self.currentOverStatus=[]
        self.allOversStatus=[] ## list of list
        self.target = None 
    def show_score_board(self):
        print(f"*{self.currentBattingList[0].playerName} - {self.currentBattingList[0].runBat}({self.currentBattingList[0].ballUsed})",end="\t")
        print(f"{self.currentBattingList[1].playerName} - {self.currentBattingList[1].runBat}({self.currentBattingList[1].ballUsed})")
        print(f"{self.battingTeam.teamName[:3].upper()} | {self.totalRun}-{self.totalWickets}")
        print(f"Overs: {self.totalOver}.{self.currentBall}")
        if self.currentBowler is not None:
            print(f"{self.currentBowler.playerName} - {self.currentBowler.runBowl}/{self.currentBowler.wicketsTaken}")
        if self.currentBall>0:
            print("Current Over- ",end="")
            for i in self.currentOverStatus:
                print(i,end=" ")
            print("\n")
        if self.currentBall==0 and self.totalOver>0:
            print("Last Over- ",end="")
            for i in self.allOversStatus[len(self.allOversStatus)-1]:
                print(i,end=" ")
            print("\n")
        if self.target is not None:
            print(f"Target - {self.target}")
            print(f"Need {self.target-self.totalRun} runs in {12-(self.totalOver*6 + self.currentBall)} balls.")
    def set_bowler(self,bowlerObj):
        self.currentBowler=bowlerObj
    def bowl(self,status):
        run=0
        extraRun=0
        isNoball = False
        isWide = False 
        willStrikeChange = False 
        isWicketDown=False
        
        if status[0]>='0' and status[0]<='9':
            run=int(status)
            if run%2==1:
                willStrikeChange=True 
        else:
            if status[0]=='W' and len(status)==1:
                isWicketDown=True
            elif status[0]=='N':
                isNoball = True
                extraRun=1
                run=int(status[1])
                if run%2==1:
                    willStrikeChange=True
            elif status[0]=='W':
                isWide=True
                extraRun=1+int(status[1])
                if int(status[1])%2==1:
                    willStrikeChange=True 
        self.totalRun+=run+extraRun
        if self.target is not None:
            if self.totalRun >= self.target:
                return "end"
        self.striker.runBat+=run
        if run==4:
            self.striker.fours+=1
        if run==6:
            self.striker.sixes+=1
        if isWide==False:
            self.striker.ballUsed+=1
        self.currentBowler.runBowl+=run+extraRun
        
        self.currentOverStatus.append(status)
        if isWide==False and isNoball==False:
            self.currentBowler.ballsBowled+=1
            self.currentBall+=1
            # over complete
            if self.currentBall == 6:
                self.currentBall=0
                self.totalOver+=1
                willStrikeChange=True
                self.allOversStatus.append(self.currentOverStatus)
                self.currentOverStatus=[]
        if isWicketDown==True:
            if self.totalWickets==1:
                return "end"
            print()
            print(f"{self.striker.playerName}\t{self.striker.runBat}/{self.striker.ballUsed}")
            print(f"Strike rate - {self.striker.runBat*100/self.striker.ballUsed}")
            print(f"4's-{self.striker.fours}\t6's-{self.striker.sixes}")
            print()
            # New batsman
            self.currentBattingList[0]=self.battingTeam.playersListOfObject[self.currentBatsmanOrder]
            self.currentBatsmanOrder+=1
            self.striker=self.currentBattingList[0]
            self.totalWickets+=1
            self.currentBowler.wicketsTaken+=1
        if willStrikeChange==True:
            self.currentBattingList[0],self.currentBattingList[1] = self.currentBattingList[1],self.currentBattingList[0]
            self.striker=self.currentBattingList[0]
        return ""
        
            
        
cup=T2Cup()
bangladesh = Team("Bangladesh")
india = Team("India")
tamim = Player("Tamim Iqbal",bangladesh)
shakib = Player("Shakib Al Hasan",bangladesh)
mustafiz = Player("Mustafizur Rahman",bangladesh)
kohli = Player("Virat Kohli",india)
rohit = Player("Rohit Sharma",india)
bumra = Player("Bumra",india)

while True:
    print("Select teams to be played")
    for i,val in enumerate(cup.allTeams):
        print(f"{i+1}. {val.teamName}")
    teamOneIndex,teamTwoIndex = map(int,input("Enter two team indexes: ").split(" "))
    teamOneIndex-=1
    teamTwoIndex-=1
    teamOneObj = cup.allTeams[teamOneIndex]
    teamTwoObj = cup.allTeams[teamTwoIndex]
    tossWin = random.choice([teamOneIndex,teamTwoIndex])
    print(f"{cup.allTeams[tossWin].teamName} wins toss")
    if tossWin==teamOneIndex:
        tossLose = teamTwoIndex
    else:
        tossLose = teamOneIndex
    rand = random.choice([0,1])
    if rand == 0:
        ## Winner Team Choose Bowling
        print(f"{cup.allTeams[tossWin].teamName} choose bowling")
        battingTeamObj = cup.allTeams[tossLose]
        bowlingTeamObj = cup.allTeams[tossWin]
    else:
        ## Winner Team Choose Batting
        print(f"{cup.allTeams[tossWin].teamName} choose batting")
        battingTeamObj = cup.allTeams[tossWin]
        bowlingTeamObj = cup.allTeams[tossLose]
    firstInnings = Innings(teamOneObj,teamTwoObj,battingTeamObj,bowlingTeamObj)
    firstInnings.show_score_board()
    over=0
    while over<2:
        off=False
        print("Choose bowler: ")
        for i,val in enumerate(bowlingTeamObj.playersListOfObject):
            print(f"{i+1}. {val.playerName}")
        bowlerIndex = int(input("Enter bowler index: "))
        bowlerIndex-=1
        bowlerObj = bowlingTeamObj.playersListOfObject[bowlerIndex]
        firstInnings.set_bowler(bowlerObj)
        print("\n")
        
        while True:
            status = input("Enter status: ")
            rcv = firstInnings.bowl(status)
            if rcv=="end":
                off=True
                break
            firstInnings.show_score_board()
            if (firstInnings.totalOver*6 + firstInnings.currentBall)%6==0:
                break
        over+=1
        if off==True:
            break
    print(f"Target is {firstInnings.totalRun+1}")
    battingTeamObj,bowlingTeamObj = bowlingTeamObj,battingTeamObj
    secondInnings = Innings(teamOneObj,teamTwoObj,battingTeamObj,bowlingTeamObj)
    secondInnings.target=firstInnings.totalRun+1
    over=0
    
    # seconf innings
    while over<2:
        off = False
        print("Choose bowler: ")
        for i,val in enumerate(bowlingTeamObj.playersListOfObject):
            print(f"{i+1}. {val.playerName}")
        bowlerIndex = int(input("Enter bowler index: "))
        bowlerIndex-=1
        bowlerObj = bowlingTeamObj.playersListOfObject[bowlerIndex]
        secondInnings.set_bowler(bowlerObj)
        print("\n")
        
        while True:
            status = input("Enter status: ")
            rcv = secondInnings.bowl(status)
            if rcv == "end":
                off=True
                break
            secondInnings.show_score_board()
            if (secondInnings.totalOver*6 + secondInnings.currentBall)%6==0:
                break
        over+=1
        if off==True:
            break
    if secondInnings.totalRun >= secondInnings.target:
        print(f"{secondInnings.battingTeam.teamName} wins")
    else:
        print(f"{secondInnings.bowlingTeam.teamName} wins")
    break

