def mainmenu():
    print("""
    \t\t\t\t\t\t MAIN MENU
    1. Start new game
    2. Load saved game
    3. View help
    4. Quit
    """)
    choicemain=input()
    while choicemain not in ['1','2','3','4']:
        print('Enter valid choice')
        choicemain=input()
    if choicemain=='1':
        genboard()
    elif choicemain=='2':
        loadgame()
    elif choicemain=='3':
        viewhelp()
        mainmenu()
    elif choicemain=='4':
        Quit()
    else:
        pass
def isValid(x,y,columns,rows):
    x,y,columns,rows=int(x),int(y),int(columns),int(rows)
    if 0<x<columns+1 and 0<y<rows+1:
        return 1
    else:return 0
def isValidInput(x):
    try:
        x=int(x)
        return 1
    except:
        return 0
def Neighbours(x,y,columns,rows):
    a=[]
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if i!=0 or j!=0:
                tempx=x+i
                tempy=y+j
                if isValid(tempx,tempy,columns,rows):
                    a.append((tempx,tempy))
    return a
def NumMine(x,y,columns,rows,BackEnd):
    n=0
    for i in Neighbours(x,y,columns,rows):
        tempx=i[0]-1
        tempy=i[1]-1
        if BackEnd[tempy][tempx]=='0':
            n+=1
    return n
def checkwin(FrontEnd,BackEnd):
    FrontCopy=FrontEnd
    rows=len(FrontEnd)
    columns=len(FrontEnd[0])
    for i in range(rows):
        for j in range(columns):
            if FrontEnd[i][j]=='| |':
                return 0
            elif FrontEnd[i][j]=='|^|' and BackEnd[i][j]=='1':
                return 0
    return 1
def PlayGame(FrontEnd,BackEnd):
    def DrawBoard(board=FrontEnd):
        rows=len(board)
        columns=len(board[0])
        print('\t',end='')
        for i in range(columns):
            i+=1
            j=str(i)
            if len(j)==1:
                j='0'+j
            j=' '+j+' '
            print(j,end=' ')
        print('\n'+'-'*(columns*3+(columns-1)*2+8))
        for row in range(rows):
            x=str(row+1)
            if len(x)==1:
                x='0'+x
            print(x,end='\t')
            for column in range(columns):
                print(board[row][column], end='  ')
            print('\n'+'-'*(columns*3+(columns-1)*2+8))
        return None
    print("Enter 'save' to save the game, 'quit' to quit the game and 'help' to view help")
    print("Enter the co-orddinates of tile to uncover/flag separated by comma. For example, '4,1' will uncover tile in 4th column and 1st row.")
    print("'#4,1' will flag the tile in 4th column and 1st row.")
    while True:
        DrawBoard()
        print('Enter the tile co-ordinates or special commands (save,help,quit):')
        gamecommand=input()
        if gamecommand.lower()=='save':
            savegame(BackEnd,FrontEnd)
        elif gamecommand.lower()=='quit':
            print('The game progress will be lost. Do you want to save the game? Y/N')
            x=input()
            while not x.lower().startswith('y') and not x.lower().startswith('n'):
                print('Enter Y/N')
                x=input()
            if x.lower().startswith('y'):
                savegame()
            elif x.lower().startswith('n'):
                mainmenu()
        elif gamecommand.lower()=='help':
            viewhelp()
        else:
            asdf=gamecommand.split(',')
            if asdf[0][0]=='#':
                flag=1
                asdf[0]=asdf[0][1:]
            else:
                flag=0
            if flag:
                FrontEnd[int(asdf[1])-1][int(asdf[0])-1]='|^|'
            else:
                if BackEnd[int(asdf[1])-1][int(asdf[0])-1]=='0':
                    print('There was a mine! You lost!')
                    break
                else:
                    FrontEnd[int(asdf[1])-1][int(asdf[0])-1]='|'+str(NumMine(int(asdf[0]),int(asdf[1]),len(FrontEnd[0]),len(FrontEnd),BackEnd))+'|'
            if checkwin(FrontEnd,BackEnd):
                print('Congrats! You won it!')
                break
    print('Do you want to play again? Y/N')
    PlayAgain=input()
    if PlayAgain.lower().startswith('y'):
        choice=True
    elif PlayAgain.lower().startswith('n'):
        choice=False
    else:
        while not PlayAgain.lower().startswith('y') or not PlayAgain.lower().startswith('n'):
            print('Enter valid reply. Y/N?')
            PlayAgain=input()
            if PlayAgain.lower().startswith('y'):
                choice=True
            elif PlayAgain.lower().startswith('n'):
                choice=False
    if choice==False:
        mainmenu()
    else:
        genboard()
def genboard():
    import random
    def crrangecheck(x):
        return 1 if 5 <= int(x) <= 10 else 0
    print('Enter size of the board')
    print('Number of columns (5-10):')
    columns=input()
    while not isValidInput(columns) or not crrangecheck(columns):
        if not isValidInput(columns):
            print('Enter an integer!')
            columns=input()
        else:
            print('Enter an integer between 5 and 10:')
            columns=input()
    print('Number of rows (5-10):')
    rows=input()
    while not isValidInput(rows) or not crrangecheck(rows):
        if not isValidInput(rows):
            print('Enter an integer!')
            rows=input()
        else:
            print('Enter an integer between 5 and 10:')
            rows=input()
    rows=int(rows)
    columns=int(columns)
    BackEnd=[]
    for i in range(rows):
        x=[]
        for j in range(columns):
            x.append(str(random.randint(0,1)))
        BackEnd.append(x)
    FrontEnd=[]
    for i in range(rows):
        x=[]
        for j in range(columns):
            m='| |'
            x.append(m)
        FrontEnd.append(x)
    PlayGame(FrontEnd=FrontEnd,BackEnd=BackEnd)
def savegame(BackEnd,FrontEnd):
    print('Enter User Name:')
    UserName=input()
    print('Enter Password:')
    Password=input()
    import pickle
    print('Warning: The current game will replace the previous game with this user name, if it already exists. Press Enter to continue.')
    gf=input()
    x=(Password,FrontEnd,BackEnd)
    pickle.dump(x,open(UserName,mode='wb'))
    print('Game Saved!')
    return None
def loadgame():
    print('Enter User Name')
    UserName=input()
    print('Enter Password')
    Password=input()
    import pickle
    while(True):
        try:
            x=pickle.load(open(UserName,mode='rb'))
            break
        except:
            print("Unable to load file. Make sure the user name is correct.")
            print('Enter User Name')
            UserName=input()
            print('Enter Password')
            Password=input()
    if Password==x[0]:
        PlayGame(FrontEnd=x[1],BackEnd=x[2])
    else:
        print('Wrong Password')
        loadgame()
def viewhelp():
    print("""
Minesweeper is a deceptively simple test of memory and reasoning. The goal: find the empty squares and avoid the mines.
Sounds easy, right?
The object:
    Find the empty squares while avoiding the mines. The faster you clear the board, the better your score.
    
How to play:
 - Uncover a mine, and the game ends
 - Uncover an empty square, and you keep playing
 - Uncover a number, and it tells you how many mines lay hidden in the eight surrounding squares—information you use to deduce which nearby squares are safe to click.
 - Enter the number of tile to uncover it
 - Enter the number of tile preceded by a '#' (hash, without quotes) to flag it
 - Enter 'quit' (without quotes) to quit the game (while playing)
 - Enter 'save' (without quotes) to save the game (while playing)
 - Enter 'help' (without quotes) to get the help (while playing)
 
Hints and tips:
 - Mark the mines: If you suspect a square conceals a mine, right-click it. This puts a flag on the square. (You can uncover it later if you want)
 - Study the patterns: If three squares in a row display 2-3-2, then you know three mines are probably lined up beside that row. If a square says 8, every surrounding square is mined.
 - Explore the unexplored: Not sure where to click next? Try clearing some unexplored territory. You're better off clicking in the middle of unmarked squares than in an area you suspect is mined.
""")
    return None
def Quit():
    print("Thanks for playing. Also don't forget to try Nim at 'http://pranjaljain.comeze.com/mygame.exe'")
    print('Press Enter to exit')
    x=input()
    quit()
    return None
mainmenu()
