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
                self.p=float(p)
                

if len(sys.argv)<2:
	print "Error correct method: python SimteBot.py <'Token'>"
else:
	bot=telepot.Bot(sys.argv[1])
	print bot.getMe()
	response=bot.getUpdates()
	print response
