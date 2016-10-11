#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import telepot
import time
from pprint import pprint
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
                        return True
                else:
                        return False
        def remove(self,user):
                if not user==self.cordinator and user in self.group:
                        self.group.remove(user)
                        return True
                else:
                        return False
        def delegate(self,user,aux):
                if user == self.coordinator:
                        self.coordinator=aux
                        return True
                else:
                        return False
        def show(self):
                return "Titulo:"+self.title+"\nDescripción corta:"+self.shortAbout+"\nDescripción: "+self.about+"\nCoordinador: "+self.coordinator+"\nGrupo: "+str(self.group)+"\nAvance "+str(self.p)+"%"
        def showShort(self):
                return self.title+"\t"+str(self.p)+"% \n"+self.shortAbout+"\n"+self.coordinator

def privateChat(msg):
        chatId= msg['chat']['id']
        username= msg['chat']['username']
        name=msg['text']
        bot.sendMessage(chatId,'@'+username[1:]+" Esto es un chat privado")
        print msg['chat']
        print msg['from']
        print msg['text']

def groupChat(msg):
        chatId= msg['chat']['id']
        title= msg['chat']['title']
        name=msg['text']
        bot.sendMessage(chatId,title+" Esto es un mensaje publico")
        print msg['chat']
        print msg['from']
        print msg['text']
def handle(msg):
        tchat=msg['chat']['type']
        if tchat=='private':
                privateChat(msg)
        else:
                groupChat(msg)
        
if len(sys.argv)<2:
	print "Error correct method: python SimteBot.py <'Token'>"
else:
	bot=telepot.Bot(sys.argv[1])
	print bot.getMe()
	bot.message_loop(handle) #Para que el Bot este pendiente de los mensajes que le envian en tiempo real.
        print ('Listening ...')
        while 1:    #Para que el programa se quede ejecutando perpetuamente.
                time.sleep(10)
