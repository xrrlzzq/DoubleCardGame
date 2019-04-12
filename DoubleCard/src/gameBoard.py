class gameBoard:
    board=[]
    
    def __init__(self):
        self.board=[['00' for i in range(8)] for j in range(12)]
        self.card_list=[] 
        self.loc_list=[]
    def updateCard(self,move,location):
        x1=location[0]
        x2=location[1:]
        x3=''
        x4=''
        if move=='01' or move=='03' or move=='05' or move=='07':
            x3=chr(ord(x1)+1)
            x4=x2
        else:
            x3=x1
            x4=str(int(x2)+1)
        
        self.card_list.append(x1+x2+x3+x4)

    def updateLocation(self,move,location):
        list=self.parser(move, location)
        self.loc_list.append(str(list[0])+str(list[1]))
        self.loc_list.append(str(list[2])+str(list[3]))

    def updateMap(self,move,location):
        self.updateCard(move, location)
        self.updateLocation(move, location)

    def regularMove(self,move,location):    # r=red 1=solid dot w=white 0=hollow dot
        if move=='01':
            self.board[int(location[1:])-1][ord(location[0])-65]='1R'
            self.board[int(location[1:])-1][ord(location[0])-65+1]='0W'
            
        elif move== '02':
            self.board[int(location[1:])-1][ord(location[0])-65]='0W'
            self.board[int(location[1:])][ord(location[0])-65]='1R'
        elif move=='03':
            self.board[int(location[1:])-1][ord(location[0])-65]='0W'
            self.board[int(location[1:])-1][ord(location[0])-65+1]='1R'
        elif move=='04':
            self.board[int(location[1:])-1][ord(location[0])-65]='1R'
            self.board[int(location[1:])][ord(location[0])-65]='0W'
        elif move=='05':
            self.board[int(location[1:])-1][ord(location[0])-65]='0R'
            self.board[int(location[1:])-1][ord(location[0])-65+1]='1W'
        elif move=='06':
            self.board[int(location[1:])-1][ord(location[0])-65]='1W'
            self.board[int(location[1:])][ord(location[0])-65]='0R'
        elif move=='07':
            self.board[int(location[1:])-1][ord(location[0])-65]='1W'
            self.board[int(location[1:])-1][ord(location[0])-65+1]='0R'
        else:
            self.board[int(location[1:])-1][ord(location[0])-65]='0R'
            self.board[int(location[1:])][ord(location[0])-65]='1W'
            
    
    def isLegal(self,location,move):
        if location[1:]=='1':
            return True
        else:
            str=self.parser(move, location)
            x1=str[0]
            y1=str[1]
            x2=str[2]
            y2=str[3]
            if move=='01' or move=='03' or move=='05' or move=='07':
                if self.board[x1-1][y1]!='00' and self.board[x2-1][y2]!='00' :
                    return True
                else:
                    return False
            else:
                if self.board[x1-1][y1]!='00':
                    return True
                else:
                    return False
                
    def alreadyInBoard(self,move,location):
        list=self.parser(move, location)
        fir=str(list[0])+str(list[1])
        sec=str(list[2])+str(list[3])
        if fir not in self.loc_list and sec not in self.loc_list:
            return False
        else:
            return True

    def parser(self,move,location):
        x1=int(location[1:])-1
        y1=ord(location[0])-65
        x2=0
        y2=0
        if move=='01' or move=='03' or move=='05' or move=='07':
            x2=x1
            y2=y1+1
        else:
            x2=x1+1
            y2=y1
        return [x1,y1,x2,y2]
            

    def recycling(self,oldLocList,move,location):
        y1=ord(oldLocList[0])-65
        x1=int(oldLocList[1])-1
        y2=ord(oldLocList[2])-65
        x2=int(oldLocList[3])-1
        self.board[x1][y1]='00'
        self.board[x2][y2]='00'
       
        self.regularMove(move, location)    
    def recycUpdate(self,oldLocList,move,location):
        self.card_list.remove(''.join(oldLocList))
            
        y1=ord(oldLocList[0])-65
        x1=int(oldLocList[1])-1
        y2=ord(oldLocList[2])-65
        x2=int(oldLocList[3])-1
        self.loc_list.remove(str(x1)+str(y1))
        self.loc_list.remove(str(x2)+str(y2))
        self.updateMap(move, location)
        
 
    def winCheck(self,index,x,y):
        count=1 # search horizontal line
        check=self.board[x][y] #0W, 1R etc
        check=check[index]     #color or dot value
        
        for i in range(y+1,8):    # right search
            if self.board[x][i]=='00':
                break;            
            if (self.board[x][i])[index]==check: 
                count=count+1
                if count==4:
                    return True                
            else:
                break
        #count=1 right search+left search = horizontal search
        for i in range(y-1,-1,-1):  # left search
            if self.board[x][i]=='00':
                break
            if (self.board[x][i])[index]==check:
                count=count+1                
                if count==4:
                    return True
            else:
                break
        
        count=1 #repeat search other line (vertical line)
        for i in range(x+1,12): # up search
            if self.board[i][y]=='00':
                break
            if (self.board[i][y])[index]== check:
                count=count+1
                if count==4:
                    return True                
            else:
                break
        # count=1 up search+down search = vertical search       
        for i in range(x-1,-1,-1): # down search
            if self.board[i][y]=='00':
                break
            if (self.board[i][y])[index]== check:
                count=count+1
                if count==4:
                    return True
            else:
                break
        
        count=1 #repeat search other line
        for i,j in zip(range(x+1,12),range(y+1,8)): # right-up search
            if self.board[i][j]=='00':
                break            
            if (self.board[i][j])[index]== check:
                count=count+1
                if count==4:
                    return True
            else:
                break
        #count=1 right-up search+ left-down search=right-up obliquely search
        for i,j in zip(range(x-1,-1,-1),range(y-1,-1,-1)): #left-down search
            if self.board[i][j]=='00':
                break
            if (self.board[i][j])[index]== check:
                count=count+1
                if count==4:
                    return True
            else:
                break 
            
        count=1 #repeat search other line   
        for i,j in zip(range(x+1,12),range(y-1,-1,-1)): # left-up search
            if self.board[i][j]=='00':
                break
            if (self.board[i][j])[index]== check:
                count=count+1
                if count==4:
                    return True
            else:
                break 
        # count=1 left-up search+ right-down search=right-down obliquely search 
        for i,j in zip(range(x-1,-1,-1),range(y+1,8)): # right-down search
            if self.board[i][j]=='00':
                break
            if (self.board[i][j])[index]== check:
                count=count+1
                if count==4:
                    return True
            else:
                break
        
        return False
        
    def ifWin(self,actor,location,move):
        index=0
        if actor=='color':
            index=1
        if move=='01' or move=='03' or move=='05' or move=='07':
            x1=int(location[1:])-1
            y1=ord(location[0])-65
            x2=x1
            y2=y1+1
        else:
            x1=int(location[1:])-1
            y1=ord(location[0])-65
            x2=x1+1
            y2=y1
        
        if self.winCheck(index, x1, y1) or self.winCheck(index, x2, y2):
            return True
        else:
            return False

    def getCardValue(self,move):
        fir=''
        sec=''
        if move=='01' or move=='04':
            fir='1R'
            sec='0W'
        elif move=='02'or move=='03':
            fir='0W'
            sec='1R'
        elif move=='05' or move=='08':
            fir='0R'
            sec='1W'
        else:
            fir='1W'
            sec='0R'
        return [fir,sec]

    def getCardCode(self,move,location):
        x1=location[0]
        y1=location[1:]
        x2=''
        y2=''
        if move=='01' or move=='03' or move=='05' or move=='07':
            x2=chr(ord(x1)+1)
            y2=y1
        else:
            x2=x1
            y2=str(int(y1)+1)
        return [x1,y1,x2,y2]
                                     
    def getNumLoc(self,locList):# transfer [A,1,B,1] into [0,0,1,0]
        x1=ord(locList[0])-65
        y1=int(locList[1])-1
        x2=ord(locList[2])-65
        y2=int(locList[3])-1
        return [x1,y1,x2,y2]
    