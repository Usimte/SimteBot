#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import telepot
class Tarea:
        """Las tareas que va a realizar el grupo"""
        group=[]
        def __init__(self,title,shortAbout,about,coordinator,p):
                

if len(sys.argv)<2:
	print "Error correct method: python SimteBot.py <'Token'>"
else:
	bot=telepot.Bot(sys.argv[1])
	print bot.getMe()
	response=bot.getUpdates()
	print response
