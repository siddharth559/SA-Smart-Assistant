import os,platform
# algorithm in sa
# if open ... then lstrip 'open '
# during initialisation do any file search with .exe and store the file names as command in database tb with their path
# when user searches some open ... which is not open word or anything else then first search in database for the file
# if found show it as first preference and then do any file search
# if not found then do any file search
# if user click the file already stored in database(tb) then edit the command from the <filename>.exe to user command given like open cinema4d for cinema4d.exe


def compr(x,y):
    #x is to be compared with y
    val=0
    for i in range(0,len(x)//2-1):
        if x in y:
            val=1
        x=x[0:len(x)-1]
        
    else:
        if val==1:
            return True
        else:
            return False


def delte(n):
    '''takes the path argument and removes the rightmost file/directory and returns
    e.g. if given "C\\Windows\\System" then it returns "C\\Windows"'''
 
    n=str(n)
    n=n.split('\\')
    n.pop(-1)
    m='\\'.join(n)
    return m


def bill(inp , path = None):
    if path==None:

        if platform.architecture()[0]=='32bit':
            path='C:\\Program Files'
        else:
            path='C:\\Program Files (x86)'
            path2='C:\\Program Files'
    inp=inp.lower()
    r=1
    end=0
    ind=[0]
    files_searched=0
    results=[]
    while end!=1:
        p=os.listdir(path)    
        start_ind=ind[len(ind)-1]
        files_searched+=1
        if files_searched>=14000:
            break
        for i in p[start_ind:]:
            if compr(inp.replace(' ',''),i.lower().replace(' ',''))==True and os.path.isfile(path+'\\'+str(i))==1:
                ind[len(ind)-1]+=1
                results.append(path+'\\'+str(i))
                r+=1
            else:
                if 'CLIPART' in i: continue
                elif os.path.isdir(path+'\\'+str(i))==1:
                    path=path+'\\'+str(i)
                    ind[len(ind)-1]+=1
                    ind+=[0]
                    break
                else:
                    ind[len(ind)-1]+=1
        else:
            if ind[len(ind)-1]==len(p):
                path=delte(path)
                ind.pop(-1)
            if len(ind)==0:
                end=1
    else:
        return results

    
