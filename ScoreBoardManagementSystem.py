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
        self.strikeRate = 0.0
        self.runBat = 0
        self.ballUsed = 0
        self.fours = 0
        self.sixes = 0
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
        self.currentBattingList=[battingTeam.playersListOfObject[0],battingTeam.playersListOfObject[1]]
        self.striker=battingTeam.playersListOfObject[0]
        self.currentBowler=None
        self.currentOverStatus=[]
        self.allOversStatus=[]
    def show_score_board(self):
        print(f"*{self.currentBattingList[0].playerName} - {self.currentBattingList[0].runBat}({self.currentBattingList[0].ballUsed})",end="\t")
        print(f"{self.currentBattingList[1].playerName} - {self.currentBattingList[1].runBat}({self.currentBattingList[1].ballUsed})")
        print(f"{self.battingTeam.teamName[:3].upper()} | {self.totalRun}-{self.totalWickets}")
        print(f"Overs: {self.totalOver}.{self.currentBall}")
        if self.currentBowler is not None:
            print(f"{self.currentBowler.playerName} - {self.currentBowler.runBowl}/{self.currentBowler.wicketsTaken}")
    def set_bowler(self,bowlerObj):
        self.currentBowler=bowlerObj
    def bowl(self,status):
        self.totalRun+=status
        self.striker.runBat+=status
        self.striker.ballUsed+=1
        self.currentBowler.runBowl+=status
        self.currentBowler.ballsBowled+=1
        self.currentBall+=1
        
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
    print("Choose bowler: ")
    for i,val in enumerate(bowlingTeamObj.playersListOfObject):
        print(f"{i+1}. {val.playerName}")
    bowlerIndex = int(input("Enter bowler index: "))
    bowlerIndex-=1
    bowlerObj = bowlingTeamObj.playersListOfObject[bowlerIndex]
    firstInnings.set_bowler(bowlerObj)
    print("\n")
    firstInnings.bowl(6)
    firstInnings.show_score_board()
    break
