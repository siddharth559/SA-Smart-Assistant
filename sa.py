### coded by SIDDHARTH ACHARYA ###

'''
credits:
 Anthony Zhang for speech recognition
 DJ Oamen for plank and ball game
'''
####################################---------- imported libraries ---------#########################################
import os
import random
import time
import subprocess
import webbrowser
import sys
from wsgiref.util import request_uri

import requests
import json
import threading as th
import tkinter as tk
import sqlite3 as sq
from PIL import Image,ImageTk
import urllib.request as ur
from html.parser import HTMLParser
try:
    import speech_recognition as sr
    r=sr.Recognizer()
    import pyaudio
except:
    #print("kindly install python speech recognition, pyaudio\nfor the best use of the software")
    pass

import math
from bs4 import BeautifulSoup as beauty

######################################___platform specific stuff___#################################################
OSs={
    'darwin' : ('Mac','//'),
     'linux': ('Linux','//'),
     'win' : ('Windows','\\')
     }

OS_NAME = sys.platform
for i in OSs:
    if i in OS_NAME:
        OS_NAME,sepr = OSs[i][0],OSs[i][1]


#######################################################################################################################

db=sq.connect('SA.db')
try:
    test_=db.execute("select command from commands where srid=21")
except:
    db.execute("""create table commands(
srid int primary key,
command varchar(90) not null,
frequency int not null)
""")
    db.execute("""insert into commands values(1,"hello",0)""")   #inserting the basic commands available in SA, we can add more commands by edit.. command
    db.execute("""insert into commands values(2,"good morning",0)""")
    db.execute("""insert into commands values(3,"what is your name",0)""")
    db.execute("""insert into commands values(4,"what are you doing",0)""")
    db.execute("""insert into commands values(5,"what can you do",1)""")
    db.execute("""insert into commands values(6,"maths",0)""")
    db.execute("""insert into commands values(7,"games",1)""")
    db.execute("""insert into commands values(8,"play games",0)""")
    db.execute("""insert into commands values(9,"internet",0)""")
    db.execute("""insert into commands values(10,"open word",1)""")
    db.execute("""insert into commands values(11,"open powerpoint",0)""")
    db.execute("""insert into commands values(12,"open exel",0)""")
    db.execute("""insert into commands values(13,"open outlook",0)""")
    db.execute("""insert into commands values(14,"open notepad",0)""")
    db.execute("""insert into commands values(15,"open chrome",0)""")
    db.execute("""insert into commands values(16,"whatsup",0)""")
    db.execute("""insert into commands values(17,"what are you doing",0)""")
    db.execute("""insert into commands values(18,"where do you live",0)""")
    db.execute("""insert into commands values(19,"in which language are you written in",0)""")
    db.execute("""insert into commands values(20,"close",1)""")
    db.execute("""insert into commands values(21,"thanks",0)""")
    db.commit()
     #done
     
#############---------machine learning-------------------#########################
machience_learnt=db.execute("select command from commands order by frequency desc").fetchall()


def addbt(commd):
    fetching_lastind=db.execute("select max(srid) 'max' from commands")
    lastind=int(fetching_lastind.fetchall()[0][0])+1 
    try:
        abt_=db.execute("select frequency from commands where command='{}'".format(str(commd)))
        value=int(abt_.fetchall()[0][0])
        value+=1
        db.execute("update commands set frequency={} where command='{}'".format(value,str(commd)))
        db.commit()
    except:
        db.execute("insert into commands values({},'{}',0)".format(lastind,str(commd)))
        db.commit()


##################################################################################################################
try:
    test_=db.execute("select commtype from tb")
except:
    db.execute("""create table tb(
id int primary key,
comm varchar(90) not null,
commtype varchar(20) not null,
action varchar(90) not null)
""")
    db.execute("insert into tb values(0,'','','')")
def edit():
    edi=tk.Toplevel(root)
    editl1=tk.Label(edi, text="enter _new_ command")
    editl1.grid(row=1,column=1)
    editentry1=tk.Entry(edi)
    editentry1.grid(row=1,column=2)
    strval=tk.StringVar(edi)
    strval.set('tell')
    editl2=tk.Label(edi, text='TELL\n SA will only answer the command.\n Enter what to answer you for this command')
    editl2.grid(row=3,column=2)
    def changelab(val):
        if val=='tell':
            editl2.config(text='TELL\n SA will only answer the command\n enter what to anser you for this command')
        elif val=='open':
            editl2.config(text='In this SA will open any file for you\n enter the path in the entry box in the format ...\...\...\n for example C:\Windows\Python')
        elif val=='sa command':
            editl2.config(text="Use this if you want to replace any old command by a new one. \nWhen you enter the _new_  command the old command will execute\n for example if you enter 'hex' as _new_command and 'open chrome' as old command, then when you write hex in SA\n SA will open chrome")

    editmenu=tk.OptionMenu(edi, strval, *('tell','open','sa command'), command=changelab)
    editmenu.grid(row=2,column=1)
    editentry2=tk.Entry(edi)
    editentry2.grid(row=2,column=2)

    def done():
        edind=int(db.execute("select max(id) 'max' from tb").fetchall()[0][0])+1
        if strval.get() in ('tell','sa command'):
            db.execute("insert into tb values({},'{}','{}','{}')".format(edind,editentry1.get(),str(strval.get()),editentry2.get()))
            db.commit()
        elif strval.get() == 'open':
            disko=str(editentry2.get()).replace(sepr,'?')
            db.execute("insert into tb values({},'{}','{}','{}')".format(edind,editentry1.get(),str(strval.get()),disko))
            db.commit()
        edi.destroy()
        
    editbut=tk.Button(edi, text='DONE', command=done)
    editbut.grid(row=3,column=1)
    edi.mainloop()



################################################  search result learning  ##################################################################
try:
    test_=db.execute("select command from store")
except:
    db.execute("""create table store(
id int primary key,
command varchar(90) not null,
result varchar(100) not null)
""")
    db.execute("insert into store values(0,'','')")
    db.commit()
def storeinfo(commd,reslt):
    lind=int(db.execute("select max(id) 'max' from store").fetchall()[0][0])+1
    db.execute("insert into store values({},'{}','{}')".format(lind,str(commd),str(reslt).replace('\'','')))
    db.commit()
def delinfo(commd,reslt):
    lind=int(db.execute("select max(id) 'max' from store").fetchall()[0][0])
    minf,creq=int(db.execute("select min(frequency) 'min',command from commands").fetchall()[0][0]),db.execute("select min(frequency) 'min',command from commands").fetchall()[0][1]
    mind=int(db.execute("select min(id) 'min' from store").fetchall()[0][0])
    midf=((minf**2+lind**2)/2)**0.5
                       
       
                              
                                                            
    if lind == 5000:
        if (midf-minf)>(mind-midf):
            db.execute("delete from store where command = {}".format(creq))
        elif (midf-minf)<(mind-midf):
            db.execute("delete from store where id = {}".format(mind))
        elif (midf-minf)==(mind-midf):
            db.execute("delete from store where id = {}".format(mind))
        db.commit()
def checkinfo(commd):
    infot=db.execute("select command from store").fetchall()
    if commd in [jk[0] for jk in infot]:
        return 1
    else: return 0
def getresult(commd):
    infot=db.execute("select command, result from store").fetchall()
    for dist in infot:
        if dist[0]==commd:
            return dist[1]
    
##################################---initializing SA window---------#############################################
root=tk.Tk()
root.title("SA")
root.configure(background="white")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

WIDTH = int(screen_width//2.723404255319149)
HEIGHT = int(screen_height//1.7066666666666668+1) 

sw = int(screen_width) - int((WIDTH*1.0425531914893618)//1)
sh = int(screen_height) - int((HEIGHT*0.13333333333333333)//1)

to_be_subtracted = int(HEIGHT*0.9777777777777777) if OS_NAME == 'Windows' else 0

if OS_NAME!='Windows': sh -= HEIGHT  #UNIX SECURITY DOESN'T ALLOW PROGRAMS TO BE PLACED SO LOW IN THE SCREEN


root.geometry("{}x{}+{}+{}".format(WIDTH,HEIGHT-to_be_subtracted,sw,sh)) #470*450
root.columnconfigure(6, {'minsize':130})
root.withdraw()

    
###################################-----displaying rotating SA-----##############################################

mt1 = time.time() # for measuring time

rinit=tk.Toplevel(root)
rinit.overrideredirect(1)
rinit.geometry("+250+100".format(int(screen_width//5.12+1),int(screen_height//7.68)))
if OS_NAME == 'Windows' : 
    rinit.wm_attributes("-disabled", True)
    rinit.wm_attributes("-transparentcolor", "black")
rinit.wm_attributes('-topmost',1)
rlabel = tk.Label(rinit, bg='black')
rlabel.pack()
p_ath=sys.argv[0].split(sepr)
p_ath= p_ath[:-1]
p_ath+=['messenger']
p_ath=sepr.join(p_ath)
#s=[]
for i in range(0,72):
    if i<10:
        i='0'+str(i)
    SA_PH = tk.PhotoImage(file=p_ath+sepr+"graphics00{}.png".format(i))
    rlabel.configure(image = SA_PH)
    rinit.update()
    
rinit.destroy()  

root.deiconify()    #making the rootwindow appear
root.update()       #updating root window


root.attributes('-topmost',1)  #the root will always be at top


mt2 = time.time()

########################--the functions for making the window come out and go down(only transparent enabled in linux)--####################################
al=0.50 if OS_NAME=='Windows' else 1

root.wm_attributes('-alpha',al)
if OS_NAME != 'Linux':root.overrideredirect('True')
def check(RET_LIST=None):
    global an
    global sh
    an=root.geometry()
    a = an.split('x')
    a = [a[0]]+a[1].split('+')
    if RET_LIST:
        return a
    else:
        return a[3]
def actu():
    global al
    global an
    h_diff = 0.5/((HEIGHT*0.9777777777777777)//1)
    if OS_NAME == 'Windows':
        a=False        
        if int(check())<int((HEIGHT//1.6544117647058822)):  #272
            for i in range(0,int(HEIGHT*0.9777777777777777/5)):  ##440
                if i>=300:
                    a=True
                b=check(3)
                b[3]= str(int(b[3])+5)
                b[1]= str(int(b[1])-5)
                al=al-h_diff*5
                b = b[0]+'x'+b[1]+'+'+b[2]+'+'+b[3]
                root.wm_attributes('-alpha',al)
                root.geometry(b)
                root.update()
                
                if a==True:
                    time.sleep(0)
                if a==False:
                    time.sleep(0)
        else:
            for i in range(0,int(HEIGHT*0.9777777777777777/5)):
                if i>=300:
                    a=True
                b=check(3)
                b[3]= str(int(b[3])-5)
                b[1]= str(int(b[1])+5)
                al=al+h_diff*5
                b = b[0]+'x'+b[1]+'+'+b[2]+'+'+b[3]
                root.wm_attributes('-alpha',al)
                root.geometry(b)
                root.update()

                if a==True:
                    time.sleep(0)
                if a==False:
                    time.sleep(0)
            root.attributes('-topmost',1)
    else:
        sign_const = 1 if int(al*100) in range(22,28) else -1
        for i in range(0,int(1.5*HEIGHT*0.9777777777777777)//1):  ##440
            al = al + sign_const*h_diff
            root.wm_attributes('-alpha',al)
            root.update()
            time.sleep(0.001)
                    
    
cut=tk.Button(root, bg='red', fg='white',relief='flat', text="x", command=actu)
cut.grid(row=0, column=1)

#################################--initializing ml buttons---#######################################

S=tk.PhotoImage(file="sa.png")

mlframe=tk.Frame(root, bg='white')
mlframe.grid(row=1,column=0)

ml_frame=tk.Frame(mlframe,bg='white')
ml_frame.grid(row=1,column=0)

w=tk.Label(mlframe, text="Hello Coder !", bg="yellow", fg="grey", font="Times 20")
w.grid(row=2, column=0)

w1=tk.Label(mlframe,image=S,bg="white", anchor="center", relief="raised")
w1.grid(row=1, column=1)

# 4 buttons besides the image file of SA:
testb1=tk.Button(ml_frame, bg='white', fg='gray', relief='flat', text=machience_learnt[0][0], command=lambda: main(machience_learnt[0][0]))
testb1.grid(row=1, column=0)

testb2=tk.Button(ml_frame, bg='white', fg='gray', relief='flat', text=machience_learnt[1][0], command=lambda: main(machience_learnt[1][0]))
testb2.grid(row=2, column=0)

testb3=tk.Button(ml_frame, bg='white', fg='gray', relief='flat', text=machience_learnt[2][0], command=lambda: main(machience_learnt[2][0]))
testb3.grid(row=3, column=0)

testb4=tk.Button(ml_frame, bg='white', fg='gray', relief='flat', text=machience_learnt[3][0], command=lambda: main(machience_learnt[3][0]))
testb4.grid(row=4, column=0)
        

    

#-------------------------------initializng GUI other elements---------------------------------------------------------    

global n2
n1=tk.Label(mlframe, text="what can i do for you: ", relief="ridge").grid(row=2,column=1)

fr=tk.Frame(root, bg='white')
fr.grid(row=2,column=0)

n2=tk.Entry(fr,relief="ridge",bg='white', fg='black',font='Times', width = int(WIDTH//18.8)) #width=25
n2.grid(row=1,column=0,columnspan=2, stick = tk.W+tk.E)

L=tk.Label(root, text="", bg="yellow", fg="blue", width=int(WIDTH//9.791666666666666), wraplength=int(WIDTH//1.5666666666666667))#prime output label #width=48,wraplength=300
L.grid(row=4,column=0, columnspan=4, rowspan=6, sticky=tk.E+tk.W)

fistlabel=tk.Label(fr, text='', bg="blue", fg="white", width=int(WIDTH//18.8), wraplength=int(WIDTH//3.1333333333333333))  #width=25,wraplength=150
fistlabel.grid(row=2,column=6, columnspan=2, stick = tk.W)#blue coloured output label show what you entered


scr=tk.Scrollbar(root)# when meaning is searched
scc=tk.Scrollbar(root)# when google searched

T=tk.Text(root, width=int(WIDTH//9.4)+1, height=int(HEIGHT//37.5), yscrollcommand=scr.set, wrap='word')# when meaning is searched

C=tk.Canvas(root, bg='white', width=int(WIDTH//1.3428571428571427)+2, height=int(HEIGHT//2.5714285714285716)+1, yscrollcommand=scc.set)#when wikipedia/google searched or any file searched
scc.config(command=C.yview)
C.bind_all('<MouseWheel>', lambda event: C.yview_scroll(int(-1*(event.delta/120)), "units"))        
class but_g:   #google link buttons
    def __init__(self,frm,text,link,pic = None):
        self.text=text
        self.link=link
        self.pic = pic
        self.but_frame = tk.Frame(frm)
        self.but_frame.pack()
        self.b=tk.Button(self.but_frame,text=self.text,fg='gray',bg='white',command=self.comm,relief='flat',width=48,wraplength=288)
        self.b.pack(side = 'left')
        if pic!=None:
            self.pic_label = tk.Button(self.but_frame,image = self.pic)
            self.pic_label.pack(side='right')
    def comm(self):
        webbrowser.open(self.link)
    def edit_text(self,t = None, p =None):
        self.test = t
        self.pic = p 

class but:     #open sugesstions buttons
    def __init__(self,frm,text,link):
        self.text=text
        self.link=link
        self.link_ = self.link if '.lnk' not in self.link else self.link[:15]+'...'                 
        self.b=tk.Button(frm, text=self.text+'\n'+self.link_, fg='gray', bg='white', command=self.for_open, relief='flat', width=48, wraplength=288)
        self.b.pack()
    def for_open(self):
        if OS_NAME == 'Windows':os.startfile(self.link)                
        else: os.system('cd {}; gtk-launch {}'.format(start_menu_path[0],self.link))

class wiki_com: #for showing wikipedia data
    def __init__(self, frm, title_name, text_to_be_put, picture=None,const=None):
        self.frm=frm
        self.main_frame=tk.Frame(self.frm)
        self.main_frame.pack()
        self.child_fr=tk.Frame(self.main_frame)
        self.child_fr.grid(row=1,column=1)
        self.lab=tk.Label(self.child_fr, text=title_name,width=36, wraplength=288)
        self.but=tk.Button(self.child_fr, text='⯆',command=self.fun)
        self.lab.grid(row=1, column=1)
        self.but.grid(row=1,column =2)
        self.on=0
        self.text_to_be_put=text_to_be_put
        self.lab2=tk.Label(self.main_frame,text=self.text_to_be_put,width=46,wraplength=288)
        self.picture=picture
        if self.picture!=None:
            self.picture = Image.open(self.picture)
            self.picture = ImageTk.PhotoImage(self.picture)
        self.lab_image=tk.Label(self.main_frame,image=self.picture)
        if const:
            const='wiktionary'
        else:
            const='wikipedia'

        self.link_bt=tk.Button(self.main_frame, fg='blue', font='Times 12',relief='flat',text='open in {} website ⮩'.format(const), command=lambda: webbrowser.open('https://en.{}.org/wiki/'.format(const)+title_name.replace(' ','_')))
    def fun(self):
        if self.on==0:
            self.lab2.grid(row=3,column=1)
            self.lab_image.grid(row=2,column=1)
            self.link_bt.grid(row=4,column=1)
            self.but.config(text='⯅')
            self.on=1
            C.update()
            C.config(scrollregion=C.bbox('all'))
        else:
            self.lab2.grid_forget()
            self.lab_image.grid_forget()
            self.link_bt.grid_forget()
            self.on=0
            self.but.config(text='⯆')
            C.update()
            C.config(scrollregion=C.bbox('all'))

#---------------------------------speech reco function--------------------------------------------------------
def google_search(new_n):
    n2.delete(0,tk.END)
    new_n = new_n.replace(' ','+')
    url = f"https://www.google.com/search?source=hp&ei=D21vXovxGvzez7sPwPyquAQ&q="+str(new_n)  
    stri = ur.Request(url,headers={'User-Agent': 'chrome.exe'})
    req= ur.urlopen(stri) 

    soup=beauty(req.read(), 'html.parser') 

    results_ = {}

    gbar = soup.find(id='gbar')
    if gbar:
        gbar.clear()

    anchors = soup.findAll('a')


    for link in anchors:
        if link['href'].startswith('/url'):
            results_[link.get_text()]=link['href']

    
    C.grid(row=10,column=0)
    scc.grid(row=10,column=1,sticky=tk.N+tk.S)
    frame=tk.Frame(C, bg='yellow')

    rt=C.create_window(0,0,anchor=tk.N+tk.W,window=frame)
    def rstrp(n):
        t=n.find('&sa=')
        return n[:t]
    for i in results_:
        resd=results_[i].replace('/url?q=','').replace('/url?q=','')
        resi=rstrp(resd)
        but_g(frame,str(i),resi)##
        C.update()
        C.config(scrollregion=C.bbox('all'))
#________________________________________________________________________________________        
def speech():
    global r
    dy=0
    
    
    try:
        #import speech_recognition as sr
        #import pyaudio
        
        
        with sr.Microphone() as source:
    
            r.adjust_for_ambient_noise(source)
            w.configure(text='listening')
            root.update()
            
            audio = r.listen(source, timeout=3)
            
        dy=r.recognize_google(audio)
    except:
        mes=tk.Message(root, text="error\nsee if you have speech recognition installed\nsee if internet is on")
        mes.grid(row=11,column=16)
    w.configure(text="Hello Coder !")
    root.update()
    n2.delete(0,tk.END)
    main(dy)
    
            



################################# to be taken down in next version #########################################################
def handle_overline(n): #wrap function
#for handling excess caracters than width in label L
    to=list(n)
    if len(to)>50 and ('\n' not in to[0:52]):
        dec=0
        trav=0
        while trav<len(to):
            if trav-dec==50:
                dec=trav
                to.insert(trav,'\n')
            trav+=1
        else:
            n="".join(to)
    return n

##################################--------- for wikipedia ----------###########################################################

gl = []  #list of suggestions related to search

gsd = {}    #for multiple searches ( format = {title: {extract:, pic:}})
WAIT_TIME = 0.5   #defualts wait time
URL = "https://en.wikipedia.org/w/api.php"  #wikipedia api url
wiktionary = "https://en.wiktionary.org/w/api.php" #wiktionary api
S_e = requests.Session()   #requesting sessions

search_thread_flag = 1
to_be_searched_thread_flag = 1
searched = ''

Q_WORDS =  ['whereis','whatis','howis','whois',
            'where+is','what+is','how+is','who+is',
            'wheres','hows','whats','whos',"where's","how's","what's","who's"]


###########################__FUNCTIONS_wiki___#######################################

def api_call(p,mode=None):  #makes calls to the the wikipedia api
    if mode:
        r = S_e.get(url = wiktionary, params = p, timeout=15).json()
    else:
        r = S_e.get(url = URL, params = p, timeout=15).json()
    return r
#_________________________________________________________________________________

def wsearch(i):   #search a particular word(this searches the word in articles too)
    global gl
    PARAMS = {
    "action": "query",
    "format": "json",
    "list": "search",
    "srsearch": i,
    "srlimit": 10
    }
    ap = api_call(PARAMS)
    ap = [i['title'] for i in ap['query']['search']]
    
    gl = ap
#_________________________________________________________________________________

def open_search(i,mode=None):   #open search the word (this only matches title strings)
    global gl
    PARAMS = {
    "action": "opensearch",
    "namespace": "0",
    "search": i,
    "limit": 10,
    "format": "json"
    }
    
    ap = [i for i in api_call(PARAMS,mode)[1]]
    
    gl = ap
#__________________________________________________________________________________

    
def get_pic(i, photoname, thumb_size=None):   #getting thumbnail pictures
    global gsd
    PARAMS = {
    "action": "query",
    "format": "json",
    "titles": i,
    "prop": "pageimages",
    "pithumbsize":50 if thumb_size == None else thumb_size
    }
    ap = api_call(PARAMS)
    try:
        ap = [i for i in ap['query']['pages'].values()][0]['thumbnail']['source']
    except:
        ap = None
    try:
        gsd[i]
        gsd[i]['pic']='{}.png'.format(photoname) if ap!=None else None
    except:
        gsd[i]={}
        gsd[i]['pic'] = '{}.png'.format(photoname) if ap!=None else None

    #writing images in directory 
    if ap != None:
        img_url = ur.urlopen(ap)     
        data = img_url.read()
        filen='{}.png'.format(photoname) #images are mostly in jpg format
        wiki_img_file = open(filen, 'wb')
        wiki_img_file.write(data)
        wiki_img_file.close()



#___________________________________________________________________________________

def wget(i,mode=None):   #getting extracts
    PARAMS = {
    'action': 'query',
    'format':'json',
    'prop':'extracts',
    'exsentences':10,
    'exlimit':1,
    'titles':i,
    'explaintext':1,
    'formatversion':2
    }

    ap = api_call(PARAMS,mode)['query']['pages'][0]['extract']
    try:
        gsd[i] #check if i there is dict
        gsd[i]['extract']=ap
    except:
        gsd[i]={}
        gsd[i]['extract'] = ap
    
#____________________________________________________________________________________


def enter(entry,event = None):
    global gl
    global threads
    global gsd
    global searched

    gsd={} # to clear previous values

    #cont_var = 0
    #entry = n2.get()
    
    if entry.rstrip(' ').lower() == searched.lower(): #user was doing wiki open search before seeing results
        
        threads = []
        index = 0
        for i in gl[0:3]:
            threads.append([th.Thread(target = wget, args=(i,)),th.Thread(target = get_pic, args=(i,'thumb{}'.format(index+1)))])
            threads[index][0].start()
            threads[index][1].start()
            index += 1
        
            
            
    else:  #user didn't do a wiki open search before seeing results
        to_be_kept = []
        for i in gl:
            if (i.lower() in searched.lower()) or (searched.lower() in i.lower()):
                to_be_kept.append(i)           
        t2 = th.Thread(target = wsearch , args = (entry,))
        searched  = entry
        t2.start()
        t2.join()

        threads = []
        index = 0
        for i in gl[0:3]:
            threads.append([th.Thread(target = wget, args=(i,)),th.Thread(target = get_pic, args=(i,'thumb{}'.format(index+1)))])
            threads[index][0].start()
            threads[index][1].start()
            index += 1
        
        for i in gl:
            if i in to_be_kept: to_be_kept.pop(to_be_kept.index(i))
            
        gl = to_be_kept+gl
        

#root.bind('<Return>',enter)

class autocomplete:
    def __init__(self, frm,title_name,mode):
        #mode=None for wiki,1 for wiktionary, 2 for google/ddg
        self.frm=frm
        self.title_name=title_name
        self.mode=mode
        self.MAIN_BUTTON=tk.Button(self.frm,text=self.title_name,command=self.wiki_ped if (self.mode==None or self.mode==1) else lambda : google_search(self.title_name),width=46)
        self.MAIN_BUTTON.pack()
    def wiki_ped(self):
        global gsd
        gsd={}
        wget(self.title_name,self.mode)
        get_pic(self.title_name,'thumb1')
        C.delete('all')
        C.grid(row=10,column=0)
        scc.grid(row=10,column=1,sticky=tk.N+tk.S)
        self.frame_w=tk.Frame(C, bg='yellow') 
        
        multiplier=0 if self.mode==None else 1
        output=wiki_com(self.frame_w,self.title_name,gsd[self.title_name]['extract'][:500*(multiplier+1)],gsd[self.title_name]['pic'],self.mode)
        output.fun()
        
        rt=C.create_window(0,0,anchor=tk.N+tk.W,window=self.frame_w)

        C.update()
        root.update()
        C.config(scrollregion=C.bbox('all'))
    
   
def gett():
    global searched
    global to_be_searched_thread_flag
    global counter_var
    count_var = 0
    ag = ''
    counter_var=''
    
    while search_thread_flag == 1:
        
        cg = ag
        cg_mod = cg.replace(' ','+')
        for i in Q_WORDS:
            if i in cg_mod:
                cg_mod = cg_mod.replace(i , '')
                
        try:
            ag = n2.get()
        except: pass
        ag_mod = ag.lower().replace(' ','+')
        

        if (ag != '') and (len(ag)>2):
            truth = 0
            for i in Q_WORDS:
                if i in ag_mod:
                    ag = ag_mod.replace(i,'').replace('+',' ')
                    truth = 1
                    try:
                        if ag[0]==' ' and len(ag)==2: ag = ag[1:]
                    except IndexError:
                        pass
                    break
            else:
                if 'meaning+of' in ag_mod:
                    ag = ag_mod.replace('meaning+of','')
                    truth=2
            if to_be_searched_thread_flag==0:
                if counter_var.replace(' ','')!=ag.replace(' ',''):
                    to_be_searched_thread_flag=1
            
            if truth != 0:
                truth = None if truth==1 else 1
                if count_var == 10:
                    count_var = 0
                    
                    if ag.endswith(' '): ag = ag[:len(ag)-1]
                    
                    if ag != searched:
                        
                        
                        if to_be_searched_thread_flag==1:
                            t1 = th.Thread(target = open_search , args = (ag,truth))
                            searched = ag
                            t1.start()
                            t1.join()
                            #----------------------------------
                            C.delete('all')
                            L.config(text='')
                            C.grid(row=10,column=0)
                            scc.grid(row=10,column=1,sticky=tk.N+tk.S)
                            frame_w=tk.Frame(C, bg='yellow') 
                            
                            for i in gl:
                                autocomplete(frame_w,i,truth)
                            rt=C.create_window(0,0,anchor=tk.N+tk.W,window=frame_w)

                            C.update()
                            C.config(scrollregion=C.bbox('all'))
                            #----------------------------------------------

                elif (ag == cg) and (ag!= searched): #ag==cg that means writer didn't change what he/she had written and ag!=searched that means what writer wrote hasn't been searched
                    count_var+=1 #so this acts like a timer
            elif truth ==0:
                #google autocomplete
                link = 'http://suggestqueries.google.com/complete/search?'
                if ag!=searched:
                    if count_var==10:
                        count_var = 0
                        autocomplete_list = [ag]+S_e.get(url = link,params = {'client':'chrome','q':ag,'format':'json'}).json()[1]
                        if (n2.get() == ag) and (to_be_searched_thread_flag == 1 ):

                            
                            L.config(text='')
                            C.grid(row=10,column=0)
                            scc.grid(row=10,column=1,sticky=tk.N+tk.S)
                            if to_be_searched_thread_flag == 1 :
                                C.delete('all')
                                frame_w=tk.Frame(C, bg='yellow') 
                                for i in autocomplete_list:
                                    autocomplete(frame_w,i,2)                            
                                rt=C.create_window(0,0,anchor=tk.N+tk.W,window=frame_w)
                                C.update()
                                C.config(scrollregion=C.bbox('all'))
                            
                        searched = ag
                    elif (ag==cg) and (ag!=searched):
                        count_var+=1
                

        time.sleep(0.1)

           
entry_monitor = th.Thread(target=gett)

#def google_autocomplete():




################################################################################################################################

import any_file_searcher as afs
linux = ['/usr/share/applications/']
start_menu_path=[]
start_menu_progs={}



if OS_NAME=='Linux':
    start_menu_path = linux
    linux_apps = os.listdir(start_menu_path[0])
    for i in linux_apps:
        prog_name = i.split('.')
        start_menu_progs[prog_name[len(prog_name)-2]] = i #start_menu_path[0]+i


    

elif OS_NAME == 'Windows':
    win_9x = ['C:\\Windows\\Start Menu' , os.environ['USERPROFILE']+'\\Start Menu']
    win_nt_4 = [os.environ['USERPROFILE']+'\\Start Menu' , 'C:\\Windows\\Profiles\\All Users\\Start Menu']
    win_xp = [os.environ['USERPROFILE']+'\\Start Menu' , 'C:\\ProgramData\\Start Menu']
    win_mod = [os.environ['USERPROFILE']+'\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu' , 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu']

    wind_ver=sys.getwindowsversion()

    if wind_ver[3]!=2:
        start_menu_path=win_9x
    elif wind_ver[0]<=4:
        start_menu_path=win_nt_4
    elif wind_ver[0]==5:
        start_menu_path=win_xp
    elif wind_ver[0]>5:
        start_menu_path=win_mod

    start_menu_shorts= afs.bill('.lnk',start_menu_path[0])+afs.bill('.lnk',start_menu_path[1])
    
    for i in start_menu_shorts:
        start_menu_progs[i.split('\\')[-1].replace('.lnk','')] = i

################################################################################################################################

def main(n):  #main function of the software does everything
################################################################################
    global start_menu_progs
    global r
    global search_thread_flag
    global to_be_searched_thread_flag
    global counter_var
    ############################################################################
    #newbutton.grid_forget()
    #closebut.grid_forget()
    to_be_searched_thread_flag=0
    scr.grid_forget()
    scc.grid_forget()
    T.grid_forget()
    T.delete('1.0', tk.END)
    C.grid_forget() 
    L.config(text='')
    n=n.lower()
    fistlabel.configure(text=str(n))
    C.delete('all')
    n2.delete(0,tk.END)
    ############################################################################
    extraf=db.execute("select * from tb").fetchall()
    list_of_progs = db.execute("select * from tb where commtype='open'").fetchall()
    ############################################################################
    if ("voice") in n:
        try:
            with sr.Microphone() as source:
                q = r.listen(source)
                n=str(r.recognize_google(q))
                L.configure(text=n)
        except:
            L.configure(text="error\nsee if you have speech recognition installed\nsee if internet is on")
    if n==("hello") or n==("hi"):
        addbt(n)
        L['text']="hello"
    elif n=="edit..":
        addbt(n)
        edit()
    elif [i[1] for i in extraf].count(n)!=0:
        d=[i[1] for i in extraf].index(n)
        extraf2=[d[3] for d in extraf]
        if [z[2] for z in extraf][d]=="tell":
            caretext=handle_overline(extraf2[d])
            L.configure(text=caretext)
        elif [z[2] for z in extraf][d]=="sa command":
            main(extraf2[d])
        elif [z[2] for z in extraf][d]=="open":
            L.configure(text="opening...")
            if 'open' in n: os.startfile(str(extraf2[d]).replace('?','\\'))
            elif 'open' not in n: main('open '+n)
    elif n==("good morning"):
        addbt(n)
        L.configure(text="good morning")
    elif n==("what is your name") or n=="what's your name":
        addbt(n)
        L.configure(text="my name is sa assistant")
    elif n==("what are you") or n==("who are you"):
        addbt(n)
        L.configure(text="i am your personal assistant")
    elif n==("what can you do"):
        addbt(n)
        L['text']="let me give a gist\n1. I can talk with you\n2. open files for you\n3. do searches \n4. open websites \n5. do maths for you \n6. find word meanings \n7. can get you some inbuilt games"
    elif n==("maths"):
        addbt(n)
        L.configure(text="i can calculate the roots of quadratic equations\ndo summetions\n do integrations ")
        if OS_NAME == 'Windows':os.popen('.'+sepr+'calculator_SA.py')
        else: os.system('python3 calculator_SA.py')
    elif n == 'timer':
        addbt(n)
        L.configure(text='lets keep up with time')
        if OS_NAME == 'Windows':os.popen('.'+sepr+'timer_SA.py')
        else: os.system('python3 timer_SA.py')

    
    elif n==("games") or n==("i want to play games") or n==("Games") or n==("games ") or n==("Games "):
        addbt("games")
        gam=tk.Toplevel()
        L.configure(text="choose your game:\n1.tic tac toe\n2.space invaders\n3. plank and ball")
        
        def tictactoe():
            
            gam.destroy()
            game=tk.Toplevel()
            board = [[1,2,3],
                     [4,5,6],
                     [7,8,9]]

            bimg=tk.PhotoImage(file="but1.png")

            cross=tk.PhotoImage(file="cross.png")
            zero=tk.PhotoImage(file="zero.png")

            l1=tk.Label(game, image=zero)
            l1.grid(row=1, column=1)
            l2=tk.Label(game, image=zero)
            l2.grid(row=1, column=2)
            l3=tk.Label(game, image=zero)
            l3.grid(row=1, column=3)
            l4=tk.Label(game, image=zero)
            l4.grid(row=2, column=1)
            l5=tk.Label(game, image=zero)
            l5.grid(row=2, column=2)
            l6=tk.Label(game, image=zero)
            l6.grid(row=2, column=3)
            l7=tk.Label(game, image=zero)
            l7.grid(row=3, column=1)
            l8=tk.Label(game, image=zero)
            l8.grid(row=3, column=2)
            l9=tk.Label(game, image=zero)
            l9.grid(row=3, column=3)

            a=''
            def checkrow():
                global a
                for i in range(0,3):
                    if board[i][0]==board[i][1]and board[i][1]==board[i][2] and type(board[i][2])==str:
                        a=i
                        return True
                    
            b=''
            def checkcolumn():
                global b
                for i in range(0,3):
                    if board[0][i]==board[1][i] and board[1][i]==board[2][i] and type(board[2][i])==str:
                        b=i
                        return True

            def checkdiagonal():
                if board[0][0]==board[1][1] and board[1][1]==board[2][2] and type(board[1][1])==str:
                    return True
                if board[0][2]==board[1][1] and board[1][1]==board[2][0] and type(board[1][1])==str:
                    return True

            def check_computer():  #check if player can win or if computer can lose
                l=[]
                to_be_played=0
                for li in board:
                    if li.count('X')==2:
                        for li_ in li:
                            if type(li_)==int:
                                to_be_played=li_
                for i in range(0,3):
                    l+=[board[i][0]]
                    if l.count('X')==2:
                        for li_ in l:
                            if type(li_)==int:
                                to_be_played = li_
                l=[]
                for i in range(0,3):
                    l+=[board[i][1]]
                    if l.count('X')==2:
                        for li_ in l:
                            if type(li_)==int:
                                to_be_played = li_
                l=[]
                for i in range(0,3):
                    l+=[board[i][2]]
                    if l.count('X')==2:
                        for li_ in l:
                            if type(li_)==int:
                                to_be_played = li_
                l=[]
                for i in range(0,3):
                    for j in range(0,3):
                        if i==j:
                            l+=[board[i][j]]
                            if l.count('X')==2:
                                for li_ in l:
                                    if type(li_)==int:
                                        to_be_played = li_
                l=[board[0][2],board[1][1],board[2][0]]
                if l.count('X')==2:
                    for li_ in l:
                        if type(li_)==int:
                            to_be_played = li_
                return to_be_played
            #########################################################################
            def check_player():  #check if computer can win or if player can lose
                l=[]
                to_be_played=0
                for li in board:
                    if li.count('O')==2:
                        for li_ in li:
                            if type(li_)==int:
                                to_be_played=li_
                for i in range(0,3):
                    l+=[board[i][0]]
                    if l.count('O')==2:
                        for li_ in l:
                            if type(li_)==int:
                                to_be_played = li_
                l=[]
                for i in range(0,3):
                    l+=[board[i][1]]
                    if l.count('O')==2:
                        for li_ in l:
                            if type(li_)==int:
                                to_be_played = li_
                l=[]
                for i in range(0,3):
                    l+=[board[i][2]]
                    if l.count('O')==2:
                        for li_ in l:
                            if type(li_)==int:
                                to_be_played = li_
                l=[]
                for i in range(0,3):
                    for j in range(0,3):
                        if i==j:
                            l+=[board[i][j]]
                            if l.count('O')==2:
                                for li_ in l:
                                    if type(li_)==int:
                                        to_be_played = li_
                l=[board[0][2],board[1][1],board[2][0]]
                if l.count('O')==2:
                    for li_ in l:
                        if type(li_)==int:
                            to_be_played = li_
                return to_be_played

            ########################################################
                        
            gameover=tk.Label(game, text='', bg="white", fg="blue")
            gameover.grid(row=4,column=1)

                

            def show():
                global a
                global b
                if checkrow()==True:
                    if board[a][0]=="X" and board[a][1]=="X" and board[a][2]=="X":
                        gameover.configure(text='player wins')
                if checkcolumn()==True:
                    if board[0][b]=="X" and board[1][b]=="X" and board[2][b]=="X":
                        gameover.configure(text='player wins')
                if checkdiagonal()==True:
                    if board[0][0]==board[1][1]==board[2][2]=='X' or board[0][2]==board[1][1]==board[2][0]=='X':
                        gameover.configure(text='player wins')
                if check_player()!=0:
                    if check_player()==5:
                        but5.destroy()
                        board[1][1]="O"
                    elif check_player()==9:
                        but9.destroy()
                        board[2][2]="O"
                    elif check_player()==1:
                        but1.destroy()
                        board[0][0]="O"
                    elif check_player()==3:
                        but3.destroy()
                        board[0][2]="O"
                    elif check_player()==7:                
                        but7.destroy()
                        board[2][0]="O"
                    elif check_player()==2:
                        but2.destroy()
                        board[0][1]="O"
                    elif check_player()==8:
                        but8.destroy()
                        board[2][1]="O"
                    elif check_player()==4:
                        but4.destroy()
                        board[1][0]="O"
                    elif check_player()==6:
                        but6.destroy()
                        board[1][2]="O"
                elif check_computer()!=0:
                    if check_computer()==5:
                        but5.destroy()
                        board[1][1]="O"
                    elif check_computer()==9:
                        but9.destroy()
                        board[2][2]="O"
                    elif check_computer()==1:
                        but1.destroy()
                        board[0][0]="O"
                    elif check_computer()==3:
                        but3.destroy()
                        board[0][2]="O"
                    elif check_computer()==7:                
                        but7.destroy()
                        board[2][0]="O"
                    elif check_computer()==2:
                        but2.destroy()
                        board[0][1]="O"
                    elif check_computer()==8:
                        but8.destroy()
                        board[2][1]="O"
                    elif check_computer()==4:
                        but4.destroy()
                        board[1][0]="O"
                    elif check_computer()==6:
                        but6.destroy()
                        board[1][2]="O"
                    
                elif but5.winfo_exists()==1:
                    but5.destroy()
                    board[1][1]="O"
                elif but9.winfo_exists()==1:
                    but9.destroy()
                    board[2][2]="O"
                elif but1.winfo_exists()==1:
                    but1.destroy()
                    board[0][0]="O"
                elif but3.winfo_exists()==1:
                    but3.destroy()
                    board[0][2]="O"
                elif but7.winfo_exists()==1:                
                    but7.destroy()
                    board[2][0]="O"
                elif but2.winfo_exists()==1:
                    but2.destroy()
                    board[0][1]="O"
                elif but8.winfo_exists()==1:
                    but8.destroy()
                    board[2][1]="O"
                elif but4.winfo_exists()==1:
                    but4.destroy()
                    board[1][0]="O"
                elif but6.winfo_exists()==1:
                    but6.destroy()
                    board[1][2]="O"
                else:
                    gameover.configure(text="Game Over")

                if checkrow()==True:
                    if board[a][0]=="O" and board[a][1]=="O" and board[a][2]=="O":
                        gameover.configure(text='computer wins')
                if checkcolumn()==True:
                    if board[0][b]=="O" and board[1][b]=="O" and board[2][b]=="O":
                        gameover.configure(text='computer wins')
                if checkdiagonal()==True:
                    if board[0][2]==board[1][1]==board[2][0]=='O' or board[0][0]==board[1][1]==board[2][2]=='O':
                        gameover.configure(text='computer wins')
                check_computer()


            def act1():
                try:
                    but1.destroy()
                except:
                    pass
                board[0][0]="X"
                l1.configure(image=cross)
                show()
            def act2():
                try:
                    but2.destroy()
                except:
                    pass
                board[0][1]="X"
                l2.configure(image=cross)
                show()
            def act3():
                try:
                    but3.destroy()
                except:
                    pass
                board[0][2]="X"
                l3.configure(image=cross)
                show()
            def act4():
                try:
                    but4.destroy()
                except:
                    pass
                board[1][0]="X"
                l4.configure(image=cross)
                show()
            def act5():
                try:
                    but5.destroy()
                except:
                    pass
                board[1][1]="X"
                l5.configure(image=cross)
                show()
            def act6():
                try:
                    but6.destroy()
                except:
                    pass
                board[1][2]="X"
                l6.configure(image=cross)
                show()
            def act7():
                try:
                    but7.destroy()
                except:
                    pass
                board[2][0]="X"
                l7.configure(image=cross)
                show()
            def act8():
                try:
                    but8.destroy()
                except:
                    pass
                board[2][1]="X"
                l8.configure(image=cross)
                show()
            def act9():
                try:
                    but9.destroy()
                except:
                    pass
                board[2][2]="X"
                l9.configure(image=cross)
                show()

            but1=tk.Button(game, image=bimg, command=act1)
            but1.grid(row=1, column=1)

            but2=tk.Button(game, image=bimg, command=act2)
            but2.grid(row=1, column=2)

            but3=tk.Button(game, image=bimg, command=act3)
            but3.grid(row=1, column=3)

            but4=tk.Button(game, image=bimg, command=act4)
            but4.grid(row=2, column=1)

            but5=tk.Button(game, image=bimg, command=act5)
            but5.grid(row=2, column=2)

            but6=tk.Button(game, image=bimg, command=act6)
            but6.grid(row=2, column=3)

            but7=tk.Button(game, image=bimg, command=act7)
            but7.grid(row=3, column=1)

            but8=tk.Button(game, image=bimg, command=act8)
            but8.grid(row=3, column=2)

            but9=tk.Button(game, image=bimg, command=act9)
            but9.grid(row=3, column=3)
            game.mainloop()
            
        def ball_game():
            
            gam.destroy()
            class Ball:
                def __init__(self, canvas, paddle, color):
                    self.canvas = canvas
                    self.paddle = paddle
                    self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
                    starts = [-3, -2, -1, 1, 2, 3]
                    random.shuffle(starts)
                    self.x = starts[0]
                    self.y = -3
                    self.canvas_height = canvas.winfo_height()
                    self.canvas_width = canvas.winfo_width()
                    self.is_hitting_bottom = False
                    canvas.move(self.id, 245, 100)
                def draw(self):
                    self.canvas.move(self.id, self.x, self.y)
                    pos = self.canvas.coords(self.id)
                    if pos[1] <= 0:
                            self.y = 1
                    if pos[3] >= self.canvas_height:
                            # self.y = -1
                            self.is_hitting_bottom = True
                    if self.hit_top_paddle(pos) == True:
                            self.y = -3
                    if self.hit_bottom_paddle(pos) == True:
                            self.y = 1
                    if pos[0] <= 0:
                            self.x = 3

                    if pos[2] >= self.canvas_width:
                            self.x = -3

                def hit_top_paddle(self, pos):
                        paddle_pos = self.canvas.coords(self.paddle.id)
                        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                                if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                                        return True

                        return False

                def hit_bottom_paddle(self, pos):
                        paddle_pos = self.canvas.coords(self.paddle.id)
                        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                                if pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
                                        return True

                        return False

            class Paddle:
                def __init__(self, canvas, color):
                    self.canvas = canvas
                    self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)

                    self.x = 0
                    self.canvas_width = canvas.winfo_width()

                    canvas.move(self.id, 200, 300)

                    canvas.bind_all('<KeyPress-Left>', self.move_left)
                    canvas.bind_all('<KeyPress-Right>', self.move_right)

                def draw(self):
                    self.canvas.move(self.id, self.x, 0)

                    pos = self.canvas.coords(self.id)

                    if pos[0] <= 0:
                            self.x = 0

                    if pos[2] >= self.canvas_width:
                            self.x = 0

                def move_left(self, event):
                    self.x = -2

                def move_right(self, event):
                    self.x = 2

            ba = tk.Toplevel()
            ba.title('Game')
            canvas = tk.Canvas(ba, width=550, height=400, bd=0, highlightthickness=0)
            canvas.pack()
            ba.update()

            paddle = Paddle(canvas, 'white')
            ball = Ball(canvas, paddle, 'black')

            while 1:
                    if ball.is_hitting_bottom == False:
                            ball.draw()
                            paddle.draw()

                    ba.update_idletasks()
                    ba.update()
                    time.sleep(0.01)
        #################################################################################                    
        def space():
            gam.destroy()
            if OS_NAME == 'Windows': os.popen('turtlegame.py')
            else: os.system('python3 turtlegame.py')
        ##############################################################################                    
        tic=tk.PhotoImage(file="gameimg.png")
        ball=tk.PhotoImage(file="ball.png")
        spaceinv=tk.PhotoImage(file="spaceinv.png")
        tic_but=tk.Button(gam, image=tic, command=tictactoe)
        tic_but.pack()
        ball_but=tk.Button(gam, image=ball, command=ball_game)
        ball_but.pack()
        spaceinv_but=tk.Button(gam, image=spaceinv, command=space)
        spaceinv_but.pack()
        gam.mainloop()
    elif ("internet") in n:
        addbt(n)
        L.configure(text="lets see")
        net=tk.Tk()
        net.configure(bg="white")
        net.title=("web")
        l1=tk.Label(net, text="", fg="red", bg="yellow")
        l1.pack()
        l1.configure(text="do you wanna do a search\nor\nOpen a Website: ")
        W=tk.Entry(net)
        W.pack()
        def _internet():
            w=str(W.get())    
            if w==("search"):
                l1.configure(text="enter your search: ")
                M=tk.Entry(net)
                M.pack()
                def search():
                    m=str(M.get())
                    if " " in m:
                        m=m.replace(" ", "+")
                    webbrowser.open("www.google.com/search?ei=zzdwW4a6BMqFvQSsoK7QDw&q="+str(m)+"&oq="+str(m)+"&gs_l=psy-ab.3..0i131i67k1j0i67k1l2j0l7.9601.67276.0.67514.5.5.0.0.0.0.251.719.2-3.3.0..2..0...1.1.64.psy-ab..2.3.719...0i131k1.0.KeS3nnjIYqM")
                    net.destroy()
                inte1=tk.Button(net, text=">>", fg="blue", bg="white", command=search)
                inte1.pack()
            elif w==("open a website") or w==("Open a Website") or w==("website"):    
                l1.configure(text="enter the url of website: ")
                WEB=tk.Entry(net)
                WEB.pack()
                def website():
                    web=str(WEB.get())
                    webbrowser.open(web)
                    net.destroy()
                int2=tk.Button(net, text=">>", fg="blue", bg="white", command=website).pack()
        inte=tk.Button(net, text=">>", fg="blue", bg="white", command=_internet)
        inte.pack()
        net.mainloop()
    elif ("open") in n:
        addbt(n)
        n=n.replace('open ','')
        

        suggestions={}
        relevance_list=[]

        C.grid(row=10,column=0)
        scc.grid(row=10,column=1,sticky=tk.N+tk.S)
        frame=tk.Frame(C, bg='yellow')            

        rt=C.create_window(0,0,anchor=tk.N+tk.W,window=frame)

        for i in start_menu_progs:
            if n.lower() in i.lower():
                relevance_list.append(i)
                suggestions[i]=start_menu_progs[i]
            elif n[0:-1].lower() in i.lower():
                relevance_list.append(i)
                suggestions[i]=start_menu_progs[i]
            elif n[1:len(n)].lower() in i.lower():
                relevance_list.append(i)
                suggestions[i]=start_menu_progs[i]
                
        if len(relevance_list)==1:
            L.config(text = 'opening '+relevance_list[0])            
            if OS_NAME == 'Windows': os.startfile(start_menu_progs[relevance_list[0]])            
            else: os.system('cd {}; gtk-launch {}'.format(start_menu_path[0],start_menu_progs[relevance_list[0]]))
            relevance_list.clear()
            suggestions.clear()
                
                         
        elif len(relevance_list) == 0:
            
            d_list = [i[1] for i in list_of_progs]
            path_list=[i[3] for i in list_of_progs]
            
            for i in d_list:
                if n.lower() in i.lower():
                    suggestions[i] = path_list[d_list.index(i)]
                elif n.replace(' ','').lower() in i.replace(' ','').lower():
                    suggestions[i] = path_list[d_list.index(i)]
                elif n[0:-1].lower() in i.lower():
                    suggestions[i] = path_list[d_list.index(i)]
                elif n[1:-1].lower() in i.lower():
                    suggestions[i] = path_list[d_list.index(i)]


            for i in suggestions:
                if ' ' in i:
                    relevance_list.insert(0,i)
                else:
                    relevance_list.append(i)

        for i in relevance_list[::-1]:
            but(frame,str(i),suggestions[i])##
            C.update()
            C.config(scrollregion=C.bbox('all'))
        else:
            if len(relevance_list) > 1 :L.config(text='which one to open')
    
           #######################################################################################
    elif ("search") in n:
        addbt(n)
        if checkinfo(n)==1:
            L.configure(text=getresult(n)+"\n....Wikipedia")
        else:
            L.config(text = 'doing a google search')
            google_search(n)
            
    elif "whatsup" in n or "what's up" in n:
        addbt(n)
        L.configure(text="chilling dude :-)")
    elif n==("what are you doing"):
        addbt(n)
        L.configure(text="nothing much, just thinking about\nthe answers of small and big questions of life")
    elif n=="where do you live" or n=="where do u live":
        addbt(n)
        L.configure(text="In your P.C")
    elif n== "in which language are you written in":
        addbt(n)
        L.configure(text="Python !!!\ngood programming language, isn't it")
    elif ("stop") in n or "close" in n:
        addbt("close")
        L.configure(text="closing")
        search_thread_flag = 0
        to_be_searched_thread_flag=0
        db.close()
        root.destroy()
    elif "thanks" in n:
        addbt(n)
        L.configure(text="welcome;-)")
###################################################################################################################

    elif 'meaning' in n:
        addbt(n)
        n = n.replace('meaning of ','')
        wget(n,1)
        C.delete('all')
        C.grid(row=10,column=0)
        scc.grid(row=10,column=1,sticky=tk.N+tk.S)
        frame_w=tk.Frame(C, bg='yellow') 
        
        output_=wiki_com(frame_w,n,gsd[n]['extract'][:500*2],None,1)
        output_.fun()
        
        rt=C.create_window(0,0,anchor=tk.N+tk.W,window=frame_w)

        C.update()
        root.update()
        C.config(scrollregion=C.bbox('all'))
        
###################################################################################################################       
    else:
        if 'wh' in n:
            addbt(n)
            n2.insert(0,n)
            try:
                #os.remove('wiki_image.jpeg')
                os.remove('thumb1.png')
                os.remove('thumb2.png')
                os.remove('thumb3.png')
            except:
                pass
            truth_VALUE=0
            n=n.replace(' ','+')
            
            for i in Q_WORDS:
                if i in n:
                
                    truth_VALUE=1
                    n=n.replace(i,'').replace('+'," ")
                    
            
            if n.startswith(' '):
                n=n[1:]
            counter_var=n

            if truth_VALUE==1:
                truth_VALUE=0
                enter(n)
                for i in threads:
                    i[0].join()
                    i[1].join()
                
            
            C.grid(row=10,column=0)
            scc.grid(row=10,column=1,sticky=tk.N+tk.S)
            frame_wiki=tk.Frame(C, bg='yellow') 
            
            wiki_list=[]
            for i in gsd:
                wiki_list.append(wiki_com(frame_wiki,i,gsd[i]['extract'][:500],gsd[i]['pic']))
            for i in gl[3:]:
                autocomplete(frame_wiki,i,0)
            wiki_list[0].fun()
            rt=C.create_window(0,0,anchor=tk.N+tk.W,window=frame_wiki)

            C.update()
            root.update()
            C.config(scrollregion=C.bbox('all'))
            
            
            #except:
            #    L.configure(text="i don't understand\nTry using specific keyword or do a google search \nelse please check your connection \n if your net connection is proper then try suing specific keywords\nlike type new york city for searching new york")

        else:
            L.configure(text="I don't understand here are some search results")
            addbt(n)

            google_search(n)

            
    

            
            


###############################################################################################################################

def act(event=None):
    you=str(n2.get())
    main(you)
img=tk.PhotoImage(file="arrow.png")
img1=tk.PhotoImage(file="mic.png")
b=tk.Button(fr, image=img, bg="blue",relief="flat", command=act, width='15', height='13') #the arrow button
b.grid(row=1,column=4)
root.bind("<Return>", act) #binding enter key with the functions of arrow button
speechbut=tk.Button(fr, image=img1, bg="white",relief='flat', command=speech) #button for mic
speechbut.grid(row=1,column=5)


def parallellistner(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # to use another API key (if you have) , use `r.recognize_google(audio, key="<google speech recognition api key you have>")
        #instead of 'r.recognize_google(audio)'   [this is default api key and has limited words per day (about 50)]
        if recognizer.recognize_google(audio) in ("listen","listening",'list') :
            if int(check())>int((HEIGHT//1.6544117647058822)):
                actu()
                root.after(1,speech)
            else:
                root.after(1,speech)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass

try:
    r_par = sr.Recognizer()
    m_par = sr.Microphone()
    with m_par as source:
        r_par.adjust_for_ambient_noise(source)

    # started listening in the background 
    stop_listening = r_par.listen_in_background(m_par, parallellistner,3)
    # `stop_listening` is now a function that, when called, stops background listening
except:
    pass

entry_monitor.start()

root.mainloop()       

try:
    stop_listening(wait_for_stop=False)
except:
    pass

try:
    db.close()
except:
    pass




