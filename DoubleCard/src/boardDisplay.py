import tkinter as tk
import tkinter.messagebox
from ValidRule import ValidRule
from gameBoard import gameBoard
from tkinter.constants import DISABLED, NORMAL
from tkinter import StringVar, IntVar
import re
import copy
from GameTree import GameTree
from MiniMax import MiniMax
import time

class BoardDisplay:
    maxStep=8
    maxCount=12
    colonm_left={'A':50,'B':100,'C':150,'D':200,'E':250,'F':300,'G':350,'H':400}
    colonm_right={'A':100,'B':150,'C':200,'D':250,'E':300,'F':350,'G':400,'H':450}
    row_left={'1':480,'2':440,'3':400,'4':360,'5':320,'6':280,'7':240,'8':200,'9':160,'10':120,'11':80,'12':40}
    row_right={'1':520,'2':480,'3':440,'4':400,'5':360,'6':320,'7':280,'8':240,'9':200,'10':160,'11':120,'12':80}
    count_dict={'color':maxCount,'dot':maxCount}
    step_dict={'color':maxStep,'dot':maxStep}
    preCard='0000'
       
    def locationParser(self,move,location):
        x1=location[0]
        y1=location[1:]
        x2=''
        y2=''
        
        if move=='01' or move=='03' or move=='05' or move=='07':
            y2=y1
            x2=chr(ord(x1)+1)
        else:
            x2=x1
            y2=str(int(y1)+1)
        
        return [x1,y1,x2,y2]
            
    def draw_dot(self,x1,y1,x2,y2,color):
        a1=x1+(x2-x1)/2-5
        b1=y1+(y2-y1)/2-5
        c1=x1+(x2-x1)/2+5 
        d1=y1+(y2-y1)/2+5   
        self.canvas.create_oval(a1,b1,c1,d1,fill=color)

    def remove_card(self,location):
        a1=self.colonm_left[location[0]]
        b1=self.row_left[location[1]]
        c1=self.colonm_right[location[0]]
        d1=self.row_right[location[1]]
        a2=self.colonm_left[location[2]]
        b2=self.row_left[location[3]]
        c2=self.colonm_right[location[2]]
        d2=self.row_right[location[3]]
        self.canvas.create_rectangle(a1,b1,c1,d1,fill='#F0F0F0')
        self.canvas.create_rectangle(a2,b2,c2,d2,fill='#F0F0F0')
        
    def draw_card(self,move,location):
        fir=''
        sec=''
        if move=='01' or move=='04':
            fir='1R'
            sec='0W'
        elif move=='02' or move=='03':
            fir='0W'
            sec='1R'
        elif move=='05' or move=='08':
            fir='0R'
            sec='1W'
        else:
            fir='1W'
            sec='0R'
        list=self.locationParser(move, location)
        
        a1=self.colonm_left[list[0]]
        b1=self.row_left[list[1]]
        c1=self.colonm_right[list[0]]
        d1=self.row_right[list[1]]
        a2=self.colonm_left[list[2]]
        b2=self.row_left[list[3]]
        c2=self.colonm_right[list[2]]
        d2=self.row_right[list[3]]
                            
        if fir=='1R':
            self.canvas.create_rectangle(a1,b1,c1,d1,fill='red')
            self.draw_dot(a1, b1, c1, d1, 'black')
            self.canvas.create_rectangle(a2,b2,c2,d2,fill='white')
            self.draw_dot(a2, b2, c2, d2, 'white')
        elif fir=='0W':
            self.canvas.create_rectangle(a1,b1,c1,d1,fill='white')
            self.draw_dot(a1, b1, c1, d1, 'white')
            self.canvas.create_rectangle(a2,b2,c2,d2,fill='red')
            self.draw_dot(a2, b2, c2, d2, 'black')
        elif fir=='0R':
            self.canvas.create_rectangle(a1,b1,c1,d1,fill='red')
            self.draw_dot(a1, b1, c1, d1, 'red')
            self.canvas.create_rectangle(a2,b2,c2,d2,fill='white')
            self.draw_dot(a2, b2, c2, d2, 'black')
        else:
            self.canvas.create_rectangle(a1,b1,c1,d1,fill='white')
            self.draw_dot(a1, b1, c1, d1, 'black')
            self.canvas.create_rectangle(a2,b2,c2,d2,fill='red')
            self.draw_dot(a2, b2, c2, d2, 'red')
        
        if move in ['01','03','05','07']:
                
            self.canvas.create_rectangle(a1+1,b1+1,c2-1,d2-1,outline="black",width=3)
        else:
            self.canvas.create_rectangle(a2+1,b2+1,c1-1,d1-1, outline="black",width=3)
            
    def recyclingParse(self,command):
        regex=re.compile("\D\d+")
        oldFir=''
        oldSec=''
        move_1=''
        location=''
        list=regex.findall(command)
        if len(list)!=3 :
            return ['wrong']
        elif len(list[1])<3: #A12B125D1, list[1]=B125 (B15-B125)
            return ['wrong']
        else:
            oldFir=list[0]
            oldSec=list[1][:-1] #from start to last one ,  oldSec=list[1][0:len(list[1])-1]
            move_1=list[1][-1]    #get last one,             move=list[1][len(list[1])-1]
            location=list[2]
            return [oldFir,oldSec,move_1,location]
            
    def AI_Move(self):
        start=time.time()
        self.winTime=0
        curBoard=copy.deepcopy(self.gb.board)
        curList=self.gb.card_list.copy()
#         print('preCard is: '+self.preCard)
        root=GameTree(curBoard,'0000',curList,self.preCard)
        curStep=40-(self.count_dict['color']+self.count_dict['dot']+self.step_dict['color']+self.step_dict['dot'])
        
        
        minimax=MiniMax(curBoard,curList,curStep,self.current_turn,self.isPuring,self.var_heuristic.get())
        
        minimax.generateTree(1,root,curStep)
        
        #sTime=time.time()
        command=minimax.miniMaxi(root).id
        #eTime=time.time()
        #print('minimax use time: '+str(eTime-sTime)+' (s)')
        if self.trace.get()==1:
            minimax.writeFile()

        self.var_command.set(command)
        self.isAI=True
        self.button_move()
        self.isAI=False
        if self.winTime!=0:
            end=self.winTime
            
        else:
            end=time.time()
        self.lable_time['text']='AI using time: '+"{:.2f}".format(end-start) 
        self.winTime=0           
    def card_Recycling(self):
        command=self.var_command.get().upper().replace(' ','')
        list=self.recyclingParse(command)
          
        actor=self.current_turn

        if list[0]=='wrong':
            tk.messagebox.showerror(title='error', message='invalid command ,please enter again')
        else:
            oldFir=list[0]
            oldSec=list[1]
            move_1=list[2]
            location=list[3]
            oldLocList=[oldFir[0],oldFir[1:],oldSec[0],oldSec[1:]]
            reply=self.rule.canRecycling(oldLocList,move_1,location, self.preCard,self.isAI)
            
            if 'success' in reply:
                oldFir=list[0]
                oldSec=list[1]
                move='0'+move_1
                location=list[3]
                locList=[list[0][0],list[0][1:],list[1][0],list[1][1:]]
                self.remove_card(locList)
                self.draw_card(move, location)
                preList=self.locationParser(move, location)
                self.preCard=preList[0]+preList[1]+preList[2]+preList[3]
                self.gb.recycling( oldLocList, move,location)
                self.gb.recycUpdate(oldLocList, move,location)
                
                self.cmd_list.insert(0,self.current_turn+' recycling move['+command+'] is success')
                
                if self.gb.ifWin(actor, location, move): 
                    self.winTime=time.time()                   
                    tk.messagebox.showinfo(title='win !', message='congradulations! '+actor+' is win!')
                    self.cmd_list.insert(0,actor+' is win! congradulations!')
                    self.game_over()
                else:
                    otherActor=''
                    if actor=='color':
                        otherActor='dot'
                    else:
                        otherActor='color'
                    if self.gb.ifWin(otherActor, location, move):
                        self.winTime=time.time()
                        tk.messagebox.showinfo(title='win !', message='congradulations! '+otherActor+' is win!')
                        self.cmd_list.insert(0,otherActor+' is win! congradulations!')
                        self.game_over()
                    else:
                        
                        self.boardUpdate(actor)
            
            else:
                tk.messagebox.showerror(message=reply)
                self.cmd_list.insert(0,'your recycling move['+command+"] is unsuccessfully")                                
              
        
    def card_move(self):
        command=self.var_command.get().upper().replace(' ','')
        move=command[0:2]
        location=command[2:]
        actor=self.current_turn
        reply=self.rule.canRegularMove(move, location,self.isAI)
        
        if "success" in reply: 
            code=self.gb.getCardCode(move, location)   
            self.preCard=code[0]+code[1]+code[2]+code[3]        
            self.draw_card(move, location)
            self.gb.regularMove(move, location)
            self.gb.updateMap(move, location)
            
            self.cmd_list.insert(0,self.current_turn+' regular move['+command+'] is success')
            
            if self.gb.ifWin(actor, location, move):
                self.winTime=time.time()
                tk.messagebox.showinfo(title='win !', message='congradulations! '+actor+' is win!')
                self.cmd_list.insert(0,actor+' is win! congradulations!')
                self.game_over()
            else:
                otherActor=''
                if actor=='color':
                    otherActor='dot'
                else:
                    otherActor='color'
                if self.gb.ifWin(otherActor, location, move):
                    self.winTime=time.time()
                    tk.messagebox.showinfo(title='win !', message='congradulations! '+otherActor+' is win!')
                    self.cmd_list.insert(0,otherActor+' is win! congradulations!')
                    self.game_over()
                else:
                    
                    self.boardUpdate(actor) 
                  
        else:
            tk.messagebox.showerror(message=reply)
            self.cmd_list.insert(0,'your regular move['+command+"] is unsuccessfully")
            
        
    def game_quit(self):
        self.window.destroy()
    
    def start(self):
        self.AI_turn='color'
        self.gb=gameBoard()
        self.isAI=False
        self.winTime=0
        self.rule=ValidRule(self.gb)
        choose=self.turn.get()
        self.draw_board()
        self.count_dict['color']=self.maxCount
        self.count_dict['dot']=self.maxCount
        self.step_dict['color']=self.maxStep
        self.step_dict['dot']=self.maxStep
        self.preCard=''
        ifPuring=self.puring.get()
        
        if choose ==0:
            self.lable_turn['text']='current turn: color'
            self.lable_turn['fg']='red'
            self.current_turn='color'
        else:
            self.lable_turn['text']='current turn: dot'
            self.lable_turn['fg']='blue'
            self.current_turn='dot'
        if ifPuring==0:
            self.isPuring=True
        else:
            self.isPuring=False
        
        self.isAuto=(self.auto.get()==1)
        self.isAIFirst=(self.AIFirst.get()==1 and self.isAuto)

       
                
        self.bt_color['state']=DISABLED
        self.bt_dot['state']=DISABLED
        self.bt_havePuring['state']=DISABLED
        self.bt_noPuring['state']=DISABLED

        self.bt_start['state']=DISABLED
        self.bt_move['state']=NORMAL
        self.entry_cmd['state']=NORMAL
        self.lable_count['text']='you have '+str(self.count_dict[self.current_turn])+' cards left'
        self.lable_count['fg']='red'  
        self.bat_button['state']=NORMAL  
        self.batch_cmd['state']=NORMAL
        self.entry_cmd.focus() #set cursor to input(entry_cmd)
        self.var_command.set('')  
        self.lable_remind['text']='regular mode'
        self.lable_remind['fg']='red'
        self.cmd_list.delete(0, self.cmd_list.size())
        self.check_Button['state']=NORMAL

        if self.isAuto:
            if self.isAIFirst:
                
                self.AI_turn=self.current_turn
                
            else:
                if self.current_turn=='color':
                    self.AI_turn='dot'
                else:
                    self.AI_turn='color'
                 
        else:
            self.AIFirst.set(0)
            self.isAIFirst=False

        self.bt_AIFirst['state']=DISABLED
        self.bt_auto['state']=DISABLED
        if self.isAuto:
            self.bat_button['state']=DISABLED
            
        if self.isAIFirst:
            self.AI_Move()
    def boardUpdate(self,actor):
        self.var_command.set('')
        if actor=='color':
            self.current_turn='dot'
            self.lable_turn['text']='current turn: dot'
            self.lable_turn['fg']='blue'            
        else:
            self.lable_turn['text']='current turn: color'
            self.lable_turn['fg']='red'
            self.current_turn='color'
        if self.count_dict['color']!=0 or self.count_dict['dot']!=0:
            self.count_dict[actor]=self.count_dict[actor]-1 
        if self.count_dict['color']==0 and self.count_dict['dot']==0:
            
            if self.step_dict['color']==self.maxStep and self.step_dict['dot']==self.maxStep:
                self.winTime=time.time()
                tk.messagebox.showinfo(message='recycling start!')
            self.step_dict[actor]=self.step_dict[actor]-1
            if self.step_dict['color']==0 and self.step_dict['dot']==0:
                self.winTime=time.time()
                tk.messagebox.showinfo(title='draw', message='no one win!')
                self.cmd_list.insert(0,'no one win!')
                self.game_over()
            self.lable_count['text']='you have '+str(self.step_dict[self.current_turn])+' steps left'
            self.lable_remind['text']='recycling mode'
        else:
                
            self.lable_count['text']='you have '+str(self.count_dict[self.current_turn])+' cards left'
            self.lable_count['fg']='red'
    
    def button_move(self):
        if self.count_dict['color']==0 and self.count_dict['dot']==0:
            self.card_Recycling()
        else:
            self.card_move()        
        if self.isAuto and self.AI_turn==self.current_turn and self.bt_move['state']==NORMAL:
            self.AI_Move()
            
    def key_Return(self,event):
        self.button_move()  
    
    def batch_move(self):
        cmd_text=self.batch_cmd.get('0.0', 'end').strip().upper()
        cmd_lines=cmd_text.splitlines()
        
        for cmd_str in cmd_lines:
            if cmd_str=='':
                continue
            if self.bt_move['state']==DISABLED:
                break
            self.var_command.set(cmd_str)
            self.button_move() 
              
                         
    def center_window(self,width,height):
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
        self.window.geometry(size)
    
    def game_over(self):
        self.var_command.set('')
        self.bt_color['state']=NORMAL
        self.bt_dot['state']=NORMAL
        self.bt_start['state']=NORMAL
        self.bt_havePuring['state']=NORMAL
        self.bt_noPuring['state']=NORMAL
        self.bt_Trace['state']=NORMAL
        self.bt_move['state']=DISABLED
        self.entry_cmd['state']=DISABLED
        self.bat_button['state']=DISABLED
        self.lable_turn['text']='please choose your role(color/dot)'
        self.lable_turn['fg']='red'
        self.lable_count['text']=''
        self.lable_remind['text']=''
        self.check_Button['state']=DISABLED
        self.bt_AIFirst['state']=NORMAL
        self.bt_auto['state']=NORMAL
        self.AIFirst.set(0)
        self.auto.set(0)
        self.trace.set(0)

        self.bt_naiveHeuristic['state']=NORMAL
        self.bt_heuristic1['state']=NORMAL
        self.bt_heuristic2['state']=NORMAL
        self.bat_button['state']=NORMAL
        self.lable_time['text']=''
        self.var_heuristic.set(1)
        
    def draw_board(self):
        self.canvas.create_rectangle(50,40,450,520,fill='#F0F0F0')
        for num in range(1,14):
            self.canvas.create_line(50,num*40,450,num*40)
            if num<=12:
                
                tk.Label(self.window,text=13-num).place(x=25,y=num*40+10)
        for num in range(1,10):
            self.canvas.create_line(num*50,40,num*50,520)
            if num<=8:
                
                tk.Label(self.window,text=chr(ord('A')+num-1)).place(x=num*50+15,y=530)
        
    def __init__(self):
        
        self.window=tk.Tk()
        self.canvas=tk.Canvas(self.window,height=700,width=1000)
        self.canvas.pack()        
        
        self.winTime=0
        self.window.title('welcome to play double card!')
        self.window.geometry('1000x700')
        self.center_window(1000, 700)
        self.window.maxsize(1000, 700)
        self.window.minsize(1000, 700)
        self.turn=IntVar()
        self.current_turn=''
        self.puring=IntVar()
        self.isPuring=True
        self.trace=IntVar()
        self.needTrace=False
        self.auto=IntVar()
        self.isAuto=False
        self.AIFirst=IntVar()
        self.isAIFirst=False
        self.var_heuristic=IntVar()
        self.var_heuristic.set(1)
        #put image here
        imagefile=tk.PhotoImage(file='cards.png')
        self.canvas.create_image(170+10*50,30,anchor='nw',image=imagefile)
        self.draw_board()
        tk.Label(self.window,text='command:').place(x=50,y=570)
        
        self.var_command=tk.StringVar()
        self.entry_cmd=tk.Entry(self.window,textvariable=self.var_command)
        self.entry_cmd.place(x=120,y=570)
        self.entry_cmd['state']=DISABLED
        self.entry_cmd.bind('<Return>',self.key_Return)
        
        self.bt_move=tk.Button(self.window,text='move',command=self.button_move)
        self.bt_move.place(x=300,y=600)
        self.bt_move['state']=DISABLED
        
        self.batch_cmd = tk.Text(self.window)
        self.batch_cmd.place(x=10*50-38,y=35,width=204,height=483)
        self.cmd_list=tk.Listbox(self.window)
        self.cmd_list.place(x=170+10*50,y=280,width=296,height=240)
        self.bat_button=tk.Button(self.window,text='bat move',command=self.batch_move)
        self.bat_button.place(x=462,y=540)
        self.bat_button['state']=DISABLED
        self.stop_button=tk.Button(self.window,text='stop game',command=self.game_over)
        self.stop_button.place(x=462,y=600)
        self.bt_quit=tk.Button(self.window,text='quit',command=self.game_quit)
        self.bt_quit.place(x=400,y=600)
        
        self.bt_start=tk.Button(self.window,text='start game',command=self.start)
        self.bt_start.place(x=300,y=650)
        self.bt_color=tk.Radiobutton(self.window,text='color player',variable=self.turn,value=0)
        self.bt_color.place(x=400,y=650)
        self.bt_dot=tk.Radiobutton(self.window,text='dot player',variable=self.turn,value=1)
        self.bt_dot.place(x=500,y=650)
        self.bt_noPuring=tk.Radiobutton(self.window,text='no puring',variable=self.puring,value=1)
        self.bt_noPuring.place(x=600,y=650)
        self.bt_havePuring=tk.Radiobutton(self.window,text='have puring',variable=self.puring,value=0)
        self.bt_havePuring.place(x=700,y=650)
        self.bt_Trace=tk.Checkbutton(self.window,text='trace',variable=self.trace,onvalue=1,offvalue=0)
        self.bt_Trace.place(x=700,y=600)
        self.bt_auto=tk.Checkbutton(self.window,text='auto mode',variable=self.auto,onvalue=1,offvalue=0)
        self.bt_auto.place(x=770,y=600)
        self.bt_AIFirst=tk.Checkbutton(self.window,text='AI first',variable=self.AIFirst,onvalue=1,offvalue=0)
        self.bt_AIFirst.place(x=860,y=600)
        self.lable_turn=tk.Label(self.window)
        self.lable_turn.place(x=50,y=610)
        self.lable_turn['text']='please choose your role(color/dot)'
        self.lable_turn['fg']='red'
        self.lable_count=tk.Label(self.window)
        self.lable_count.place(x=50,y=640)
        self.lable_remind=tk.Label(self.window)
        self.lable_remind.place(x=50,y=660)
        self.check_Button=tk.Button(self.window,text='AI Check',command=self.AI_Move)
        self.check_Button.place(x=550,y=600)
        self.check_Button['state']=DISABLED

        self.bt_naiveHeuristic=tk.Radiobutton(self.window,text='naive heuristic',variable=self.var_heuristic,value=0)
        self.bt_naiveHeuristic.place(x=660,y=570)
        self.bt_heuristic1=tk.Radiobutton(self.window,text='heuristic1',variable=self.var_heuristic,value=1)
        self.bt_heuristic1.place(x=790,y=570)
        self.bt_heuristic2=tk.Radiobutton(self.window,text='heuristic2',variable=self.var_heuristic,value=2)
        self.bt_heuristic2.place(x=890,y=570)
        self.lable_time=tk.Label(self.window)
        self.lable_time.place(x=170+10*50,y=530)
        self.lable_time['fg']='blue'
        self.window.mainloop() 
        
        

bd=BoardDisplay()           