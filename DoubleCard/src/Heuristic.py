import GameTree
class Heuristic:
    
    def __init__(self,heuristicIndex):
        self.heuristicIndex=heuristicIndex
    def doHeuristic(self,gameTree,player,depth):
        if self.heuristicIndex==0:
            return self.naiveHeuristic(gameTree,player)

        else:
            return self.heuristic(gameTree,depth)
              

        
    def heuristic(self,gameTree,depth):
        if self.heuristicIndex==1:
            return 1.2*gameTree.myValue-gameTree.otherValue+depth
        else:
                
            return gameTree.myValue-gameTree.otherValue*1.2+depth
     
                    
                    
                    
    

    
    def naiveHeuristic(self,gameTree,player):
        curBoard=gameTree.curBoard
        whiteO=0
        whiteX=0
        redX=0
        redO=0
        isChange=False
        for i in range(0,12):
            isChange=False
            for j in range(0,8):
                
                key=curBoard[i][j]
                if key=='00':
                    continue
                else:
                    isChange=True
                    if key=='0W':
                        whiteO+=i*10+j+1
                    elif key=='1W':
                        whiteX+=i*10+j+1
                    elif key=='1R':
                        redX+=i*10+j+1
                    else:
                        redO+=i*10+j+1
            if not isChange:
                break
        res=whiteO+3*whiteX-2*redX-1.5*redO
        
        if player=='dot':
            return -res
        else:
                 
            return  res 
        
 