from Helper import Helper

import copy
import re

class GameTree:
    moveFirDic={'01':'1R','02':'0W','03':'0W','04':'1R','05':'0R','06':'1W','07':'1W','08':'0R'}
    moveSecDic={'01':'0W','02':'1R','03':'1R','04':'0W','05':'1W','06':'0R','07':'0R','08':'1W'}
    
    
    def __init__(self,board,id,cardList,preCard):
        
        self.id=id  ## root's id is '0000' other  is the command from the parent
        self.parentNode=None
        self.curCardList=cardList ## card list should be the copy instance
        self.curBoard=board ## board should be the copy instance
        self.helper=Helper(self.curBoard,self.curCardList,preCard)
        self.childList=[] ## used to save all the child node
        self.isWin=False
        self.myValue=0  
        self.otherValue=0 
        self.preCard=preCard 
        self.isOtherWin=False
        
            
    def generateAllHorChildren(self):
        listHor=self.helper.findAllHorizontalCardLoc()
        for locStr in listHor:
            locList=self.decoding(locStr)
            for move in ['01','03','05','07']:

                locs=locStr.split(':')
                code=locs[0].split(',')[0]+locs[0].split(',')[1]+locs[1].split(',')[0]+locs[1].split(',')[1]

                newCardList=self.curCardList.copy() ## need different cardList
                newCardList.append(code)
                newBoard=copy.deepcopy(self.curBoard) ## need different board
                x1=locList[0]
                y1=locList[1]
                x2=locList[2]
                y2=locList[3]
                newBoard[x1][y1]=self.moveFirDic[move]
                newBoard[x2][y2]=self.moveSecDic[move]
                id=move+locs[0].split(',')[0]+locs[0].split(',')[1]

                newChild=GameTree(newBoard,id,newCardList,code) ## code is the id of preCard
                newChild.parentNode=self
                self.childList.append(newChild)
                
    def generateAllVerChildren(self):
        listVer=self.helper.findAllVerticalCardsLoc()
        for locStr in listVer:
            locList=self.decoding(locStr)
            for move in ['02','04','06','08']:
                
                locs=locStr.split(':')
                code=locs[0].split(',')[0]+locs[0].split(',')[1]+locs[1].split(',')[0]+locs[1].split(',')[1]

                newCardList=self.curCardList.copy()
                newCardList.append(code)
                newBoard=copy.deepcopy(self.curBoard)
                x1=locList[0]
                y1=locList[1]
                x2=locList[2]
                y2=locList[3]
                newBoard[x1][y1]=self.moveFirDic[move]
                newBoard[x2][y2]=self.moveSecDic[move]
                id=move+locs[0].split(',')[0]+locs[0].split(',')[1]

                newChild=GameTree(newBoard,id,newCardList,code) ## code is the id of preCard
                newChild.parentNode=self
                self.childList.append(newChild)
                    
    def generateAllRecyclingChildren(self):
        avaliableHor=self.helper.findAllAvaliableHorizontalCards()
        avaliableVer=self.helper.findAllAvaliableVerticalCards()  
        avaliableCards=avaliableHor+avaliableVer   
        hangOverList=self.curCardList.copy()  
        if self.preCard!='0000':
            
            hangOverList.remove(self.preCard) 
        
        for cards in avaliableCards:
            commandList=cards.split(':')
            Fir=commandList[0].split(',')
            Sec=commandList[1].split(',')
            code=Fir[0]+Fir[1]+Sec[0]+Sec[1]
            hangOverList.remove(code)
            locList=self.decoding(cards)
            curMove=commandList[2]
            x1=locList[0]
            y1=locList[1]
            x2=locList[2]
            y2=locList[3]
            newBoard=copy.deepcopy(self.curBoard)
            newBoard[x1][y1]='00'
            newBoard[x2][y2]='00'
            newCardList=self.curCardList.copy()
            newCardList.remove(code)
            newHelper=Helper(newBoard,newCardList,'0000')

            curCommand=curMove+commandList[0].split(',')[0]+commandList[0].split(',')[1]
            

            self.getRecyclingChildren(curCommand, newHelper)
        self.getHangoverRecyclingChildren(hangOverList)

    def getRecyclingChildren(self,curCommand,newHelper):
        recycHorList=newHelper.findAllHorizontalCardLoc()
        recycVerList=newHelper.findAllVerticalCardsLoc()
        
        for locStr in  recycHorList:
            locList=self.decoding(locStr)
            for move in ['01','03','05','07']:

                locs=locStr.split(':')
                code=locs[0].split(',')[0]+locs[0].split(',')[1]+locs[1].split(',')[0]+locs[1].split(',')[1]
                command=move+locs[0].split(',')[0]+locs[0].split(',')[1]
                if command==curCommand:
                    continue
                 
                newCardList=newHelper.cardList.copy() ## need different cardList
                newCardList.append(code)
                newBoard=copy.deepcopy(newHelper.board) ## need different board
                x1=locList[0]
                y1=locList[1]
                x2=locList[2]
                y2=locList[3]
                newBoard[x1][y1]=self.moveFirDic[move]
                newBoard[x2][y2]=self.moveSecDic[move]
                newId=self.moveCommandToCode(curCommand)+command[1:]
                    
                newChild=GameTree(newBoard,newId,newCardList,code) ## code is the id of preCard
                newChild.parentNode=self
                self.childList.append(newChild)
        for locStr in recycVerList:
            locList=self.decoding(locStr)
            for move in ['02','04','06','08']:
                
                locs=locStr.split(':')
                code=locs[0].split(',')[0]+locs[0].split(',')[1]+locs[1].split(',')[0]+locs[1].split(',')[1]
                command=move+locs[0].split(',')[0]+locs[0].split(',')[1]
                if command==curCommand:
                    continue
                newCardList=newHelper.cardList.copy()
                newCardList.append(code)
                newBoard=copy.deepcopy(newHelper.board)
                x1=locList[0]
                y1=locList[1]
                x2=locList[2]
                y2=locList[3]
                newBoard[x1][y1]=self.moveFirDic[move]
                newBoard[x2][y2]=self.moveSecDic[move]
                
                newId=self.moveCommandToCode(curCommand)+command[1:]
                    
                newChild=GameTree(newBoard,newId,newCardList,code) ## code is the id of preCard
                newChild.parentNode=self
                self.childList.append(newChild)    
    def getHangoverRecyclingChildren(self,cards):
        for card in cards:
            regex=re.compile('\D\d+')
            list=regex.findall(card)
            col1=list[0][0]
            row1=list[0][1:]
            col2=list[1][0]
            row2=list[1][1:]
            curMove=''
            x1=int(row1)-1
            y1=ord(col1)-65
            x2=int(row2)-1
            y2=ord(col2)-65
            value=self.curBoard[x1][y1]
            if col1!=col2:
                if value=='1R':
                    curMove='01'
                elif value=='0W':
                    curMove='03'
                elif value== '0R':
                    curMove='05'
                else:
                    curMove='07'
                for move in ['01','03','05','07']:
                    if move==curMove:
                        continue
                    newCardList=self.curCardList.copy()
                    newBoard=copy.deepcopy(self.curBoard)
                    newBoard[x1][y1]=self.moveFirDic[move]
                    newBoard[x2][y2]=self.moveSecDic[move]
                    newID=card+move[1:]+col1+row1
                    
                    child=GameTree(newBoard,newID,newCardList,card)
                    child.parentNode=self
                    self.childList.append(child)
                    
            else:
                if value=='0W':
                    curMove='02'
                elif value=='1R':
                    curMove='04'
                elif value=='1W':
                    curMove='06'
                else:
                    curMove='08'
                for move in ['02','04','06','08']:
                    if move==curMove:
                        continue
                    newCardList=self.curCardList.copy()
                    newBoard=copy.deepcopy(self.curBoard)
                    newBoard[x1][y1]=self.moveFirDic[move]
                    newBoard[x2][y2]=self.moveSecDic[move]
                    newID=card+move[1:]+col1+row1
                    
                    child=GameTree(newBoard,newID,newCardList,card)
                    child.parentNode=self
                    self.childList.append(child)    
                
                
    def moveCommandToCode(self,curCommand):
        move=curCommand[0:2]
        col1=curCommand[2]
        row1=curCommand[3:]
        col2=col1
        row2=row1
        if move in ['01','03','05','07']:
            col2=chr(ord(col1)+1)
        else:
            row2=str(int(row1)+1)
        return col1+row1+col2+row2
    def decoding(self,locStr):
        locs=locStr.split(':') 
        col1=locs[0].split(',')[0]
        row1=locs[0].split(',')[1]
        col2=locs[1].split(',')[0]
        row2=locs[1].split(',')[1]
        x1=int(row1)-1
        y1=ord(col1)-65
        x2=int(row2)-1
        y2=ord(col2)-65   
        return [x1,y1,x2,y2]

                
    def isLeaf(self):
        
        return self.childList==[]