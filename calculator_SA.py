import tkinter as tk
import math as m
from pynput.keyboard import Controller as p

mat=tk.Tk()

def matfun(form,n,val):
    if form==2:
        if n in [m.atan,m.acos,m.asin]:
            return m.degrees(n(val))
        else:
            return n(m.radians(val))
    else:
        return n(val)

form='rad'
def deg_rad():
    global form
    if form=='deg':
        form='rad'
    else:
        form='deg'
    print(form)

formbut=tk.Button(text=form,width=20,bg='#ff0800',fg='white',font='Times 20 bold',command=lambda: (deg_rad(), formbut.config(text=form)))
formbut.pack()

t=tk.Text(mat, font='Times 20 bold', height=4, width=30,fg='#ff0800')
t.pack()
t.focus()
e=tk.Entry(mat, font='Times 20',width=30)
e.pack()

def main_funct():
    global form
    v=1
    if form=='deg':
        v=2
    e.delete(first=0,last=tk.END)
    req=t.get( '1.0' , tk.END )
    diction={
    'log(':'m.log(',
    'log₁₀(':'m.log10(',
    '^':'**',
    'sin⁻(':'matfun({},m.asin,'.format(v),
    'cos⁻(':'matfun({},m.acos,'.format(v),
    'tan⁻(':'matfun({},m.atan,'.format(v),
    'sin(':'matfun({},m.sin,'.format(v),    
    'cos(':'matfun({},m.cos,'.format(v),    
    'tan(':'matfun({},m.tan,'.format(v),    
    'pi':'m.pi',
    'e':'m.e',
    'factorial(':'m.factorial(',
    'sqrt(':'m.sqrt('}
    
    old_req = req
    for j in range(len(req)):
        if '0'<=req[j]<='9':
            if ('a'<=req[j+1]<='z') or (req[j+1]=='('):
                req = req[:j+1]+'*'+req[j+1:]
        if req[j]== ')':
            if (req[j+1] == '(') or ('0'<=req[j+1]<='9') or ('a'<=req[j+1]<='z'):
                req = req[:j+1]+'*'+req[j+1:]
    if old_req!=req:
        t.delete('1.0',tk.END)
        t.insert('1.0',req)
    
    for i in diction:
        if i in req:
            req=req.replace(i,diction[i])
                
    e.insert( 0 , eval(req))
    
b=tk.Button(mat,text='OK',font='Times 15 bold',width=35, bg='white', fg='#ff0800',relief='flat',command=main_funct)
b.pack()

c=tk.Button(mat,text='C',font='Times 15 bold',width=35, bg='white', fg='#ff0800',relief='flat',command=lambda: ( e.delete(first=0,last=tk.END) , t.delete('1.0',tk.END)))
c.pack()

frm=tk.Frame(mat)
frm.pack()


class but:
    def __init__(self,n,r,c,m=0): # m is what the but actually enters in the Text box(it may be different than what is there in the but)
        self.n=n  #this is what shows up on the button
        self.r=r  #grid row
        self.c=c  #grid column
        self.m=m
        self.b=tk.Button(frm,text=self.n,font='Times 25',relief='flat',command=self.com)
        self.b.grid(row=self.r,column=self.c)
    def com(self):
        if self.m!=0:
            self.n=self.m

        keyb=p()
        keyb.type(str(self.n))
        #t.insert(tk.END,self.n)

num=0
for i in range(1,4):
    for j in range(1,5):
        if num>9:
            break
        but(num,i,j)
        num+=1
    
but('+',3,3)
but('-',3,4)
but('*',4,1)
but('/',4,2)
but(')',4,3)
but('(',4,4)
but('ln',1,5,'log(')
but('^',1,6)
but('sin',2,5,'sin(')
but('sin⁻',2,6,'sin⁻(')
but('cos',3,5,'cos(')
but('cos⁻',3,6,'cos⁻(')
but('tan',4,5,'tan(')
but('tan⁻',4,6,'tan⁻(')
but('π',5,1,'pi')
but('e',5,2)
but('log₁₀',5,3,'log₁₀(')
but('!',5,4,'factorial(')
but('logₐ',5,5,'log(,a')
but('√',5,6,'sqrt(')

f=tk.Frame(mat)
f.pack(side='right')

#---for integrations and summations-----
class topl:
    def __init__(self,opt):
        self.toplevel=tk.Toplevel(mat)

        self.opt=opt

        self.pict=tk.PhotoImage(file=('sigma.png','integ.PNG')[self.opt])

        self.e1=tk.Entry(self.toplevel)
        self.e1.grid(row=1,column=1)

        self.l=tk.Label(self.toplevel,image=self.pict)
        self.l.grid(row=2,column=1)

        self.e2=tk.Entry(self.toplevel,font='Times 30')
        self.e2.grid(row=2,column=2)

        self.e3=tk.Entry(self.toplevel)
        self.e3.grid(row=3,column=1)

        self.buto=tk.Button(self.toplevel,text='submit (write as a function of i)',command=self.dis)
        self.buto.grid(row=4,column=1)

        self.display_label=tk.Label(self.toplevel,text='',font='times 15')
        self.display_label.grid(row=5,column=1)

    def dis(self):
        self.up=int(self.e1.get())
        self.low=int(self.e3.get())
        ret=0
        if self.opt==0:
            for i in range(self.low,self.up+1):
                ret+=eval(self.e2.get())
            self.display_label.config(text=ret)
        if self.opt==1:
            chunk=0.0001
            i=self.low
            while i<self.up:
                ret+=(int(eval(self.e2.get()))*chunk)
                i+=chunk
            self.display_label.config(text=ret)
            


#defining determinant class (for calculating determinants and crammers rule)
class Det:
    def __init__(self,arr):
        self.matrix = list(arr)
        self.order = len(self.matrix)
    def get(self,i,j):
        return self.matrix[i-1][j-1]
    def show(self):
        string_det=''
        for i in self.matrix:
            string_det += '|'+'  '.join([str(x) for x in i])+'|'+'\n'
        return string_det
    def newdet(self,i,j):
        mm = [i[:] for i in self.matrix]
        mm.pop(i-1)
        for i in mm:
            i.pop(j-1)
        return mm

    def cal(self,det = None):
        det = Det([i[:] for i in self.matrix]) if det == None else det
        dsum = 0
        if det.order > 2:
            for i in range(1,det.order+1):
                dsum += ((-1)**(1+i))*det.get(1,i)*self.cal(Det(det.newdet(1,i)))
        elif det.order == 1:
            dsum = det.get(1,1)
        else:
            dsum += det.get(1,1)*det.get(2,2) - det.get(2,1)*det.get(1,2)
        return dsum

#def quadrat():

class le: # for calculating determinants and lineer equations

    def __init__(self,MAIN_WINDOW,opt):
        self.a = tk.Toplevel(MAIN_WINDOW)
        self.opt=opt # 2 means lineer equations and 1 means only deteminants
        self.order = None
        self.entrys=[]
        self.results = [] if self.opt-1 else None #for lineer equations
        self.of = tk.Frame(self.a)
        self.of.grid(row =1,column =1)
        self.ol = tk.Label(self.of, text = 'please enter number of variables' if self.opt-1 else 'please enter order of determinant')
        self.ol.pack()
        self.oe = tk.Entry(self.of, relief = 'ridge')
        self.oe.pack()
        self.ob = tk.Button(self.of , text = 'ok', command = self.button_ob)
        self.ob.pack()
        self.a.bind("<Return>", self.button_ob)

    def button_ob(self,event = None):
        self.order = int(self.oe.get())
        self.of.destroy()
        for i in range(0,self.order):
            self.entrys.append([])
            for j in range(0,self.order):
                self.entrys[-1].append(tk.Entry(self.a))
                self.entrys[i][j].grid(row = i*self.opt+1, column=j*self.opt+1)
        if self.opt-1:
            for i in range(0,self.order):
                for j in range(0,self.order):
                    tk.Label(self.a, text='coeff. of var {} {}'.format(j+1 , '+' if j<self.order-1 else '=')).grid(row = i*self.opt+1, column=j*self.opt+2)
                self.results.append(tk.Entry(self.a))
                self.results[i].grid(row = i*self.opt+1, column=j*self.opt+3)
            
                
        self.F_But = tk.Button(self.a , text = 'ok' ,command = self.solve if self.opt-1 else self.calc)
        self.F_But.grid(row = self.order*self.opt+1,column = self.order*self.opt+1)
        
    def calc(self):
        try:
            for i in range(0,self.order):
                for j in range(0,self.order):
                    self.entrys[i][j] = int(self.entrys[i][j].get())
        except:
            print('input already recieved')
            pass

        value = Det(self.entrys)

        self.F_LAB = tk.Label(self.a , text = value.cal())
        self.F_LAB.grid(row = self.order*self.opt+1,column = self.order*self.opt)

        print(self.entrys)

    def solve(self):
        try:
            for i in range(0,self.order):
                for j in range(0,self.order):
                    self.entrys[i][j] = int(self.entrys[i][j].get())
                self.results[i] = int(self.results[i].get())
        except:
           print('input already recieved')
           pass

        delta = Det(self.entrys).cal()
        deltas = []
        if delta:
            for i in range(0,self.order):
                new_array = [x[:] for x in self.entrys]
                for j in range(self.order):
                    new_array[j][i] = self.results[j]
                deltas.append(Det(new_array))

            for i in range(len(deltas)): #applying crammers rule
                self.results[i] = deltas[i].cal()/delta

        else:
            self.results = ['no unique solution please try again']

        text = ''
        for i in self.results:
            if type(i)!=str:
                text+=' var{} = {}\n'.format(self.results.index(i)+1,i)
            else : text = i
        self.F_LAB = tk.Label(self.a , text = text)
        self.F_LAB.grid(row = self.order*self.opt+1,column = self.order*self.opt)



    
quadra=tk.Button(f,text='solve quadratic equations',wraplength=90,width=15)
quadra.grid(row=1,column=1)

lin_eqn=tk.Button(f, text='solv lineer equation',wraplength=90,width=15,command = lambda: le(f,2))
lin_eqn.grid(row=1,column=2)

summ=tk.Button(f,text='finite summations', wraplength=90,width=14,command=lambda: topl(0))
summ.grid(row=1,column=3)

integr=tk.Button(f,text='definite integration',wraplength=90,width=15,command=lambda: topl(1))
integr.grid(row=1,column=4)

determinants = tk.Button(f, text='Calculate Determinants', wraplength=90,width=15,command = lambda: le(f,1))
determinants.grid(row=2,column = 1)

mat.mainloop()

