from GameTree import GameTree
from Heuristic import Heuristic
import os
import sys
import random
class MiniMax:
    maxValue=sys.maxsize
    minValue=-maxValue
    maxDepth=3
    
    def __init__(self,board,cardList,curStep,player,needPuring,heuristicIndex):
        self.board=board
        self.cardList=cardList
        self.curStep=curStep
        self.heuristic=Heuristic(heuristicIndex)
        self.player=player
        self.needPuring=needPuring
        self.level3Number=0
        self.currentValue=0
        self.level2ValueList=[]
        self.maxChildCount=100
        self.heuristicIndex=heuristicIndex
        
    def generateTree(self,curDepth,gameTree,curStep):
        if curDepth>=self.maxDepth:
            return
        else:
            otherPlayer='color'
            if self.player=='color':
                otherPlayer='dot' 
            if curStep<24: ## regular part
                
                gameTree.generateAllHorChildren()
                gameTree.generateAllVerChildren()
                for child in gameTree.childList:
                    
                    [ifMeWin,myScore]=child.helper.ifWinForAI(self.player,child.id,self.curStep,self.heuristicIndex)
                    [ifOtherWin,otherScore]=child.helper.ifWinForAI(otherPlayer,child.id,self.curStep,self.heuristicIndex)
                    if ifMeWin:
                        child.isWin=True
                        child.myValue=myScore ## myValue is the win rate of my turn
                        if curDepth==1:
                            return
                        
                    
                    
                    if ifOtherWin:
                        child.otherValue=otherScore ## otherValue is the win rate of other turn
                        child.isOtherWin=True
                        
                    if not(ifMeWin or ifOtherWin):
                        child.myValue=myScore
                        child.otherValue=otherScore
                        self.generateTree(curDepth+1,child,curStep+1)
            else:
                gameTree.generateAllRecyclingChildren()
                noWinList=[]

                    
                
                for child in gameTree.childList:
                    
                    [ifMeWin,myScore]=child.helper.ifWinForAI(self.player,child.id,self.curStep,self.heuristicIndex)
                    [ifOtherWin,otherScore]=child.helper.ifWinForAI(otherPlayer,child.id,self.curStep,self.heuristicIndex)
                    if ifMeWin:
                        child.isWin=True
                        child.myValue=myScore ## myValue is the win rate of my turn
                        if curDepth==1:
                            return
                        
                    
                    if ifOtherWin:
                        child.otherValue=otherScore ## otherValue is the win rate of other turn
                        
                        child.isOtherWin=True
                    
                    if not(ifMeWin or ifOtherWin):    
                        child.myValue=myScore
                        child.otherValue=otherScore
                       
                        if curDepth==1:
                            noWinList.append(child)
                        else:
                            self.generateTree(curDepth+1,child,curStep+1)
                if curDepth==1:
                      
                    if len(noWinList)>self.maxChildCount:
                        random.seed()
                        noWinList=random.sample(noWinList,self.maxChildCount)
                 
                    for i in range(len(gameTree.childList)-1,-1,-1):
                        child=gameTree.childList[i]
                        if child.isWin or child.isOtherWin:
                            continue
                        elif child not in noWinList :
                            gameTree.childList.remove(child) 
                        else:
                            self.generateTree(curDepth+1,child,curStep+1)
    
    
    def maxi(self,gameTree,depth,player,alpha=minValue,beta=maxValue):
        if gameTree.isLeaf() or depth<=0:
            self.level3Number+=1
            return (self.heuristic.doHeuristic(gameTree,self.player,depth),None)
        else:
            path=None
            for child in gameTree.childList:
                if depth==self.maxDepth:
                    if child.isWin:
                        self.level2ValueList.append(child.myValue)
                        return (child.myValue,child)
                    else:
                        if child.isOtherWin:
                            continue
                score=self.mini(child, depth-1, player,alpha,beta)[0]
                score1=score
                if depth==self.maxDepth:
                    self.level2ValueList.append(score)

                if score>alpha:
                    alpha=score
                    path=child
                    #print('path '+child.id+' score '+str(score1)+' parent '+gameTree.id)
                if self.needPuring and beta<=alpha:
                    
                    break
                    
            return (alpha,path)
                    
    def mini(self,gameTree,depth,player,alpha=minValue,beta=maxValue): 
        if gameTree.isLeaf() or depth<=0:
            self.level3Number+=1
            
            return (self.heuristic.doHeuristic(gameTree,self.player,depth),None)
        else:
            path=None
            for child in gameTree.childList:
                if depth==self.maxDepth-1:
                    if child.isOtherWin:
                        return (-child.otherValue,child)
                score=self.maxi(child, depth-1, player,alpha,beta)[0]
                
                score1=score
                if depth==self.maxDepth:
                    self.level2ValueList.append(score)
               
                if score<beta:
                    beta=score
                    path=child
                    #print('path '+child.id+' child score '+str(score1)+' parent '+gameTree.id)
                if self.needPuring and beta<=alpha:
                    
                    break
                    
            return (beta,path)
    def miniMaxi(self,gameTree,depth=maxDepth):
#         
        (score,path)=self.maxi(gameTree, depth, self.player)
        #print('path: '+str(path.id)+' score: '+str(score))
        self.currentValue=score
        return path
    
    
    def writeFile(self):
        name='tracemm.txt'
        if self.needPuring:
            name='traceab.txt'
        base_dir=os.getcwd()
        file_name=os.path.join(base_dir,name)
        
        file_open=open(file_name,'a')
        file_open.write(str(self.level3Number)+'\n')
        file_open.write(str(self.currentValue)+'\n')
        file_open.write('\n')
        for line in self.level2ValueList:
            file_open.write(str(line)+'\n')
        file_open.write('\n')
        file_open.close()