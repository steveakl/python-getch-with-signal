#!/usr/bin/env python
import os,sys,time,signal
import getch

def getMappedStr():
    #mapping = " -playpause,r-record,\x7f,back;[1~,home;[5~,chup;[6~,chdown;[4~,end;[d,left;[a,up;[c,right;[b,down"
    mapping = "\x7f,backspace;[1~,home;[5~,pgup;[6~,pgdown;[4~,end;[D,left;[A,up;[C,right;[B,down"
    dicm= {}
    for m in mapping.split(';'):
      k,v = m.split(',')
      dicm[k] = v
    return dicm

def collectAll_getch():
    k = []
    
    def h(alm,frm):
        pass
         #print(alm,frm)
        #raise Exception('detected alarm!')
    signal.signal(signal.SIGALRM,h)

    signal.setitimer(signal.ITIMER_REAL,.01)
    
    try:
        #print('try start')
        while 1:
            k.append(getch.getch())

        print('time 5 ends')
    except:
        signal.setitimer(signal.ITIMER_REAL,0)
        # print ('DEBUG: collected from getch: ',k)
        return ''.join(k)

dickey = getMappedStr()

while 1:
    e = getch.getch()
    #print(repr(e))

    if e == '\x1b':
        followingChars = collectAll_getch()
        if followingChars == '':
            k = '\x1b'
        elif followingChars in dickey.keys():
            k = dickey[ followingChars ]
        else:
            k = '\x1b'
    else:
        k = e

    def map2remote(k1):
        mappingStr = ' -playpause,p-play,m-mute,[-rew,]-ff,r-record,\n-select,pgup-chup,pgdown-chdown,left-left,righ-righ,up-up,down-down,\x7f-back'
        dic2 = {}
        for m in mappingStr.split(','):
            k2,v2 = m.split('-')
            dic2[k2] = v2

        vRtn = ''
        if k1 in dic2.keys():
            vRtn = dic2[k1]
        else:
            vRtn = k1
        #print ('DEBUG: remote key is: ',vRtn)
        return vRtn

    remoteK = map2remote(k)
    print ('sending:',remoteK)
    os.system('./inputK.py %s'%remoteK)

