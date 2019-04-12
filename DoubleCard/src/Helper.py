import re
class Helper:
    horMoveDic={'1R':'01','0W':'03','0R':'05','1W':'07'} ##only focus on the first part
    verMoveDic={'0W':'02','1R':'04','1W':'06','0R':'08'}
    maxValue=999999999
    minValue=-maxValue
    def __init__(self,board,cardList,preCard):
        self.board=board
        self.cardList=cardList
        self.preCard=preCard
    def upperRow(self): ## find the first row which is all empty from the bottom
        
        for i in range(0,12):
            isEmpty=True
            for j in range(0,8):
                if self.board[i][j]!='00':
                    isEmpty=False
                    break
            if isEmpty:
                return i
                
        return 12
    
    
    def lowerRow(self): ## find the first row which is all full from the up
        
        for i in range(11,-1,-1):
            notEmpty=True
            for j in range(0,8):
                if self.board[i][j]=='00':
                    notEmpty=False
                    break
            if notEmpty:
                return i
        return -1
    def findAllHorizontalCardLoc(self): ## add all horizontal loction in form of "0,1:0,2"
        lower=self.lowerRow()
        upper=self.upperRow()
        list=[]

        if upper==12 and lower==11: ## all full
            return list    
        elif lower==-1 and upper==0: ## all empty
            i=upper
            for j in range(0,7):
    
                loc=self.encoding(i, j,i,j+1)
                list.append(loc)
                
                
        else:
            for i in range(lower+1,min(upper+1,12)):
                for j in range(0,7):
                    if self.board[i][j]=='00' and self.board[i][j+1]=='00':
                        if i==0:
                            loc=self.encoding(i, j,i,j+1)
                            list.append(loc)
                        elif self.board[i-1][j]!='00' and self.board[i-1][j+1]!='00':
                            loc=self.encoding(i, j,i,j+1)
                            list.append(loc)
                        else:
                            continue
        return list
                                   
    def encoding(self,row1,col1,row2,col2):
        return  chr(col1+65)+','+str(row1+1)+':'+chr(col2+65)+','+str(row2+1)            
    def regularEncoding(self,row,col):
        return chr(col+65)+str(row+1)
    def findAllVerticalCardsLoc(self):
        lower=self.lowerRow()
        upper=self.upperRow()
        list=[]
        
        if upper==12 and lower==11: ## all full
            return list    
        if lower==-1 and upper==0: ## all empty
            i=upper
            for j in range(0,8):
                loc=self.encoding(i, j,i+1,j)
                list.append(loc)
        else:
            for i in range(lower+1,min(upper+1,11)):
                for j in range(0,8):
                    if self.board[i][j]=='00':
                        if i==0:
                            loc=self.encoding(i, j,i+1,j)
                            list.append(loc)
                        elif self.board[i-1][j]!='00':
                            loc=self.encoding(i, j,i+1,j)
                            list.append(loc)
                        else:
                            continue
        return list
    def getMove(self,x1,y1,x2,y2):
        move=self.board[x1][y1]
        if y2==y1+1:
            
            return self.horMoveDic[move]
        else:
            return self.verMoveDic[move]
    def getCodeStr(self,x1,y1,x2,y2):
        return chr(y1+65)+str(x1+1)+chr(y2+65)+str(x2+1)        
    def findAllAvaliableHorizontalCards(self):
        lower=self.lowerRow()
        upper=self.upperRow()
        list=[]
         
        if upper==12 and lower==11:
            i=upper-1
            for j in range(0,7):
                code=self.getCodeStr(i, j, i, j+1)
                if code==self.preCard:
                    continue
                if code in self.cardList:
                    loc=self.encoding(i, j, i, j+1)
                    move=self.getMove(i, j, i, j+1)   
                    list.append(loc+':'+move)  
        elif lower==-1 and upper==0:
            return list

                    
        else:
            for i in range(lower,upper):
                for j in range(0,7):
                    code=self.getCodeStr(i, j, i, j+1)
                    if code==self.preCard:
                        continue
                    if code in self.cardList:
                        if i==11 or (self.board[i+1][j]=='00' and self.board[i+1][j+1]=='00'):
                            loc=self.encoding(i, j, i, j+1)
                            move=self.getMove(i, j, i, j+1)   
                            list.append(loc+':'+move)
        return list                           
    def findAllAvaliableVerticalCards(self):
        lower=self.lowerRow()
        upper=self.upperRow()
        list=[]
         
        if upper==12 and lower==11:
            i=upper-2
            for j in range(0,8):
                code=self.getCodeStr(i, j, i+1, j)
                if code==self.preCard:
                    continue
                if code in self.cardList:
                    loc=self.encoding(i, j, i, j+1)
                    move=self.getMove(i, j, i, j+1)   
                    list.append(loc+':'+move)  
        elif lower==-1 and upper==0:
            return list

                    
        else:
            for i in range(lower,upper-1):
                for j in range(0,8):
                    code=self.getCodeStr(i, j, i+1, j)
                    if code==self.preCard:
                        
                        continue
                    if code in self.cardList:
                        if i==10 or self.board[i+2][j]=='00' :
                            loc=self.encoding(i, j, i+1, j)
                            move=self.getMove(i, j, i+1, j)   
                            list.append(loc+':'+move)
        return list                           
    def winCheckForAI(self,index,x,y,curStep,heuristicIndex):
        sumCount=0
        count=1 # search horizontal line
        check=self.board[x][y] #0W, 1R etc
        check=check[index]     #color or dot value
        spaceCount=0
        gapCount=0
        
        for i in range(y+1,8):    # right search
            if self.board[x][i]=='00':
                if i+1<8 and (self.board[x][i+1])[index]==check:
                    gapCount+=1
                break           
            if (self.board[x][i])[index]==check: 
                count=count+1
                
                if i+1<8 and self.board[x][i+1]=='00':
                    spaceCount+=1
                if count==4:
                    return [True,self.maxValue]                
            else:
                if curStep>=24 and i+1<8 and (self.board[x][i+1])[index]==check: # recycling part
                    gapCount+=1
                
                break
        #count=1 right search+left search = horizontal search
        for i in range(y-1,-1,-1):  # left search
            if self.board[x][i]=='00':
                if i-1>=0 and (self.board[x][i-1])[index]==check:
                    gapCount+=1
                break
            if (self.board[x][i])[index]==check:
                count=count+1 
                if i-1>=0 and self.board[x][i-1]=='00':
                    spaceCount+=1               
                if count==4:
                    return [True,self.maxValue]
            else:
                if curStep>=24 and i-1>=0 and (self.board[x][i-1])[index]==check:
                    gapCount+=1
                
                break
        if heuristicIndex==1:
            
            sumCount+=(10**(count))*(spaceCount+gapCount)
        else:
            sumCount+=count+spaceCount+gapCount
        spaceCount=0
        gapCount=0
        
        count=1 #repeat search other line (vertical line)
        for i in range(x+1,12): # up search
            if self.board[i][y]=='00':
                
                break
            if (self.board[i][y])[index]== check:
                count=count+1
                if i+1<12 and self.board[i+1][y]=='00':
                    spaceCount+=1
                if count==4:
                    return [True,self.maxValue]                
            else:
                if curStep>=24 and i+1<12 and (self.board[i+1][y])[index]==check:
                    gapCount+=1
                
                break
        # count=1 up search+down search = vertical search       
        for i in range(x-1,-1,-1): # down search
            if self.board[i][y]=='00':
#                 if i-1>=0 and (self.board[i-1][y])[index]==check:
#                     spaceCount+=1
                break
            if (self.board[i][y])[index]== check:
                count=count+1
#                 if i-1>=0 and self.board[i-1][y]=='00':
#                     spaceCount+=1
                if count==4:
                    return [True,self.maxValue]
            else:
                if curStep>=24 and i-1>=0 and (self.board[i-1][y])[index]==check:
                    gapCount+=1
                
                break
        if heuristicIndex==1:
            sumCount+=(10**(count))*(spaceCount+gapCount)
        else:
            sumCount+=count+spaceCount+gapCount
        spaceCount=0
        gapCount=0
        
        count=1 #repeat search other line
        for i,j in zip(range(x+1,12),range(y+1,8)): # right-up search
            if self.board[i][j]=='00':
                if i+1<12 and j+1<8 and (self.board[i+1][j+1])[index]==check:
                    gapCount+=1
                break            
            if (self.board[i][j])[index]== check:
                count=count+1
                if i+1<12 and j+1<8 and self.board[i+1][j+1]=='00':
                    spaceCount+=1
                    
                if count==4:
                    return [True,self.maxValue]
            else:
                if curStep>=24 and i+1<12 and j+1<8 and (self.board[i+1][j+1])[index]==check:
                    gapCount+=1

                break
        #count=1 right-up search+ left-down search=right-up obliquely search
        for i,j in zip(range(x-1,-1,-1),range(y-1,-1,-1)): #left-down search
            if self.board[i][j]=='00':
                if i-1>=0 and j-1>=0 and (self.board[i-1][j-1])[index]==check:
                    gapCount+=1
                break
            if (self.board[i][j])[index]== check:
                count=count+1
                if i-1>=0 and j-1>=0 and self.board[i-1][j-1]=='00':
                    spaceCount+=1
                if count==4:
                    return [True,self.maxValue]
            else:
                if curStep>=24 and i-1>=0 and j-1>=0 and (self.board[i-1][j-1])[index]==check:
                    gapCount+=1

                break 
        if heuristicIndex==1:
            sumCount+=(10**(count))*(spaceCount+gapCount)
        else:
            sumCount+=count+spaceCount+gapCount
        spaceCount=0    
        gapCount=0
        
        count=1 #repeat search other line   
        for i,j in zip(range(x+1,12),range(y-1,-1,-1)): # left-up search
            if self.board[i][j]=='00':
                if i+1<12 and j-1>=0 and (self.board[i+1][j-1])[index]==check:
                    gapCount+=1
                break
            if (self.board[i][j])[index]== check:
                count=count+1
                if i+1<12 and j-1>=0 and self.board[i+1][j-1]=='00':
                    spaceCount+=1
                if count==4:
                    return [True,self.maxValue]
            else:
                if curStep>=24 and i+1<12 and j-1>=0 and (self.board[i+1][j-1])[index]==check:
                    gapCount+=1
                
                break 
        # count=1 left-up search+ right-down search=right-down obliquely search 
        for i,j in zip(range(x-1,-1,-1),range(y+1,8)): # right-down search
            if self.board[i][j]=='00':
                if i-1>=0 and j+1<8 and (self.board[i-1][j+1])[index]==check:
                    gapCount+=1
                break
            if (self.board[i][j])[index]== check:
                count=count+1
                if i-1>=0 and j+1<8 and self.board[i-1][j+1]=='00':
                    spaceCount+=1
                if count==4:
                    return [True,self.maxValue]
            else:
                if curStep>=24 and i-1>=0 and j+1<8 and (self.board[i-1][j+1])[index]==check:
                    gapCount+=1

                break
        if heuristicIndex==1:    
            sumCount+=(10**(count))*(spaceCount+gapCount)
        else:
            sumCount+=count+spaceCount+gapCount
        return [False,sumCount]
        
    def ifWinForAI(self,actor,id,curStep,heursticIndex):
        index=0
        if actor=='color':
            index=1
        move=''
        location=''
        if len(id)<=5:
            move=id[0:2]
            location=id[2:]
        else:
            regex=re.compile('\D\d+')
            commandList=regex.findall(id)
            
            move='0'+commandList[1][-1]
            location=commandList[2]
            
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
        [win1,value1]=self.winCheckForAI(index, x1, y1,curStep,heursticIndex)
        [win2,value2]=self.winCheckForAI(index, x2, y2,curStep,heursticIndex)
        if win1 or win2:
            return [True,self.maxValue]
        else:
            return [False,value1+value2]            