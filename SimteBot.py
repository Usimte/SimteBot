#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import telepot
class Tarea:       
        """Las tareas que va a realizar el grupo"""
        group=[]
        def __init__(self,title,shortAbout,about,coordinator,p):
                self.title=title
                if len(shortAbout.split())<11:
                        self.shortAbout=shortAbout
                else:
                        raise ValueError("Invalid length shortAbout", shortAbout)
                self.about=about
                self.coordinator=coordinator
                self.group.append(coordinator)
                self.p=float(p)
        def edit(self,user,about,p):
                if user in self.group:
                        self.about=about
                        self.p=float(p)
        def add(self,user):
                if not user in self.group:
                        self.group.append(user)
        def show(self):
                return "Titulo:"+self.title+"\nDescripción corta:"+self.shortAbout+"\nDescripción: "+self.about+"\nCoordinador: "+self.coordinator+"\nGrupo: "+str(self.group)+"\nAvance "+str(self.p)+"%"
        def showShort(self):
                return self.title+"\t"+str(self.p)+"% \n"+self.shortAbout+"\n"+self.coordinator
                

if len(sys.argv)<2:
	print "Error correct method: python SimteBot.py <'Token'>"
else:
	bot=telepot.Bot(sys.argv[1])
	print bot.getMe()
	response=bot.getUpdates()
	print response
