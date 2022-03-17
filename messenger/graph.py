import tkinter as tk
import time
import threading as th

root=tk.Tk()
root.overrideredirect(True)
root.geometry("+250+100")
#root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "black")
root.wm_attributes('-topmost',1)
rlabel = tk.Label(root, bg='black')
rlabel.pack()
s=[]
for i in range(0,45):
    if i<10:
        i='0'+str(i)
    s.append(tk.PhotoImage(file="graphics00{}.png".format(i)))

def load():
    global s
    for i in range(45,72):
        s.append(tk.PhotoImage(file="graphics00{}.png".format(i)))
    print('done1')
def disp():
    i=0
    while i<72:
        if len(s)<i:
            print(len(s),i)
        rlabel.configure(image=s[i])
        root.update()
        i+=1
    time.sleep(2)
    root.destroy()
    print('done2')

th1=th.Thread(target=load)
th1.start()
th2=th.Thread(target=disp)
th2.setDaemon(1)
th2.start()



#root.destroy()


root.mainloop()
