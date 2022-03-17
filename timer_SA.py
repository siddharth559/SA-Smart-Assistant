import time
import tkinter as tk
import threading as thr
import playsound as pls
root=tk.Tk()
l1=tk.Label(root,text='hours').grid(row=1,column=1)
l2=tk.Label(root,text='minutes').grid(row=1,column=3)
l3=tk.Label(root,text='seconds').grid(row=1,column=5)
l4=tk.Label(root,text='')
l5=tk.Label(root,text='')
e1=tk.Entry(root)
e2=tk.Entry(root)
e3=tk.Entry(root)
e1.grid(row=1,column=2)
e2.grid(row=1,column=4)
e3.grid(row=1,column=6)
bt3=tk.Button(root, text='stop',command= lambda: (to_play.clear(),to_play.append(0)))

ps=0
rt=0
d=''
e=''
to_play=[0]
#print(to_play[0])
def Play_sound(n):
    global to_play
    if n==1:
        pls.playsound('timer_sound2.wav')
        Play_sound(to_play[0])

def timech():
    global c
    global d
    d-=1
    c=e-d-1
    l4.configure(text= ' time elapsed:  '+str(c//3600)+' hours '+str((c-c//3600*3600)//60)+' minutes '+str(c-c//60*60)+' seconds ')          
    root.update()


def commd():
    global ps
    global rt
    global e
    global d
    global to_play
    to_play[0]=0
    if ps==0 and rt==0:
        ps=1
        a=0 if e1.get() == '' else int(e1.get())        
        b=0 if e2.get() == '' else int(e2.get())
        c=0 if e3.get() == '' else int(e3.get())
        print(a,b,c)
        for i in a,b,c:
            if i >60:
                print('f')
                a=tk.Message(root,text='incorrect input')
                a.grid(row=2,column=5)
                break
        else:
            d=a*60*60 + b*60 + c if d == '' else d
            e=d if e=='' else e
            l4.grid(row=3,column=1)
            l5.grid(row=4,column=1)
            root.update()

            while d>=0 and rt==0 and ps==1:
                l5.configure(text='time remaining: '+str(d//3600)+' hours '+str((d-d//3600*3600)//60)+' minutes '+str(((d-d//60*60)))+' seconds ')
                root.after(1000,timech())#time.sleep(1)
            else:                
                
                if d <=0:
                    bt3.grid(row=2,column=7)
                    to_play[0]=1
                    ps=0
                    d=''
                    e=''
                    thr.Thread(target=Play_sound,args=(to_play[0],)).start()
        print(d,e)
    elif rt==1:
        d=e
    elif ps==1:
        ps=0
    
okb=tk.Button(root,text='ok',command=lambda: (okb.config(text='pause' if ps == 0 else 'resume'),commd()))
okb.grid(row=1,column=7)
root.mainloop()
to_play[0]=0
