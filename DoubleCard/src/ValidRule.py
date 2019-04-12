from gameBoard import gameBoard

class ValidRule:
    move_list=['01','02','03','04','05','06','07','08']
    row_list=['1','2','3','4','5','6','7','8','9','10','11','12']
    colunm_list=['A','B','C','D','E','F','G','H']
    def __init__(self,gameBoard):
        self.gb=gameBoard
            
    def canRegularMove(self,move,location,isAI):
        
        command=move+location
        if isAI:
            return "your move "+command+" is success!"
        if move not in self.move_list:
            return "invalid move enter, please enter again"
        elif location[0] not in self.colunm_list:
            return "invalid column enter,please enter again"
        elif location[1:] not in self.row_list:
            return "invalid row enter ,please enter again "
        elif self.gb.alreadyInBoard(move, location):
            
            return "there is card in that place, please enter again"
        elif self.isOutBound(move, location):
            return "your move is out of bound, please enter again"
        elif not self.gb.isLegal(location, move):
            return "your move "+command+" is illegal,please enter again"
        else:
            return "your move "+command+" is success!"

    def isOutBound(self,move,location):
        if move=='01' or move=='03' or move=='05' or move=='07':
            if location[0]=='H':
                return True
            else:
                return False
        else:
            if location[1:]=='12':
                return True
            else:
                return False
    
    def canRecycling(self,oldLocList, move_1,location,preCard,isAI):
        newCommand=move_1+location
        move = '0'+move_1
        if isAI:
            return "your move "+newCommand+" is success!"
        if  move not in self.move_list:
            return"invalid move enter, please enter again"
        elif oldLocList[0] not in self.colunm_list or oldLocList[2] not in self.colunm_list or location[0] not in self.colunm_list:
            return "invalid column enter,please enter again"
        elif oldLocList[1] not in self.row_list or oldLocList[3] not in self.row_list or location[1:] not in self.row_list:
            return "invalid row enter,please enter again"
        elif self.isOutBound(move, location):
            return "your move is out of bound, please enter again"
        elif oldLocList[0]+oldLocList[1]+oldLocList[2]+oldLocList[3] not in self.gb.card_list:
            return "there isn't card here, please enter again"
        
        msg=self.isLegalRecycling(oldLocList, move_1,location, preCard)
        if 'valid' not in msg:
            return msg
        elif not self.gb.isLegal(location, move):
            return "your move"+newCommand+" is illegal, please enter again"        
        else:
            return "your move "+newCommand+" is success!"
        
    def canRemove(self,oldLocList):
        oldList=self.gb.getNumLoc(oldLocList)
        if oldLocList[1]==oldLocList[3]:
            
            if oldList[1]<11 and (self.gb.board[oldList[1]+1][oldList[0]]!='00' or self.gb.board[oldList[3]+1][oldList[2]]!='00'):
                return False
            else:
                return True
        else:
            if oldList[3]<11 and self.gb.board[oldList[3]+1][oldList[2]]!='00':
                return False
            else:
                return True

    def isBoardNotEmpty(self,location):
        strLoc=str(int(location[1:])-1)+str(ord(location[0])-65)
        
        if strLoc in self.gb.loc_list:
            return True
        else:
            return False
            
    def isHangOver(self,oldLocList,newLocList):
        oldList=self.gb.getNumLoc(oldLocList)   
        newList=self.gb.getNumLoc(newLocList)  

        if newList[1]==0:
            return False
        else:
            if newList[0] in [oldList[0],oldList[2]] or newList[2] in [oldList[0],oldList[2]]:                
#                 if newList[1]-1 in [oldList[1],oldList[3]] or newList[3]-1 in [oldList[1],oldList[3]]:
                return True # new card is hand over with old card
            elif  newLocList[1]==newLocList[3]:
                
                if self.gb.board[newList[1]-1][newList[0]]=='00' or self.gb.board[newList[3]-1][newList[2]]=='00':
                    return True
                else:
                    False
            else:
                if self.gb.board[newList[1]-1][newList[0]]=='00':
                    return True
                else:                    
                    return False

    def isPortionOverEmpty(self,removedCell,newLocList): # check the part which is not hang over that if above the empty cell
        if newLocList[1]=='1':
            return False
        else:
            if newLocList[0]==newLocList[2]: #vertical card
                if removedCell==newLocList[0]+str(int(newLocList[1])-1) or self.gb.board[int(newLocList[1])-2][ord(newLocList[0])-65]=='00':
                    return True
                else:
                    return False           
            elif newLocList[1]==newLocList[3]: #horizontal card
                if removedCell==newLocList[0]+str(int(newLocList[1])-1) or self.gb.board[int(newLocList[1])-2][ord(newLocList[0])-65]=='00':
                    return True
                elif removedCell==newLocList[2]+str(int(newLocList[3])-1) or self.gb.board[int(newLocList[3])-2][ord(newLocList[2])-65]=='00':
                    return True
                else:
                    return False           
            else:
                return False           
                
           
    def isLegalRecycling(self,oldLocList,move_1,newLoc,preCard):
        move='0'+move_1
        newLocList=self.gb.getCardCode(move, newLoc)
        removeCell1 = oldLocList[0]+oldLocList[1]
        removeCell2 = oldLocList[2]+oldLocList[3]
        putCell1 = newLocList[0]+newLocList[1] 
        putCell2 = newLocList[2]+newLocList[3]
        
        if removeCell1+removeCell2==preCard:
            return "you can't move the card that just move, please enter again"
        else:            
            if putCell1 in [removeCell1,removeCell2] and putCell2 in [removeCell1,removeCell2]: #same place                
                ox1=int(oldLocList[1])-1
                oy1=ord(oldLocList[0])-65
                ox2=int(oldLocList[3])-1
                oy2=ord(oldLocList[2])-65
                oldFir=self.gb.board[ox1][oy1]
                oldSec=self.gb.board[ox2][oy2]
             
                newCardValue=self.gb.getCardValue(move)
                if oldFir==newCardValue[0] and oldSec==newCardValue[1]: 
                    return "you can't place the card to the same place, please enter again"
                else:
                    return "recycling valid!"                    
            elif putCell1 in [removeCell1,removeCell2]: #overlap
                if self.isBoardNotEmpty(putCell2):                    
                    return "there is card here,you can't put the card here, please enter again"
                else:
                    if not self.canRemove(oldLocList):
                        return "you can't remove this card, please enter again"

                    removedCell = removeCell1 if putCell1==removeCell2 else removeCell2                    
                    if self.isPortionOverEmpty(removedCell,newLocList):
                        return "your enter can't over the empty cell, please again"
                    else:
                        return "recycling valid!"
            elif putCell2 in [removeCell1,removeCell2]: #overlap
                if self.isBoardNotEmpty(putCell1):                    
                    return "there is card here,you can't put the card here, please enter again"
                else:
                    if not self.canRemove(oldLocList):
                        return "you can't remove this card, please enter again"

                    removedCell = removeCell1 if putCell2==removeCell2 else removeCell2
                    if self.isPortionOverEmpty(removedCell,newLocList):
                        return "your enter can't over the empty cell, please again"
                    else:
                        return "recycling valid!"            
            else: #not overlap
                if self.isBoardNotEmpty(putCell1) or self.isBoardNotEmpty(putCell2):                    
                    return "there is card here,you can't put the card here, please enter again"
                else:
                    if not self.canRemove(oldLocList):
                        return "you can't remove this card, please enter again"                    
                    elif self.isHangOver(oldLocList, newLocList):
                        return "your enter can't over the empty cell, please again"
                    else:                         
                        return "recycling valid!" 
                    