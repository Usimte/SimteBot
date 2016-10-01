#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import telepot
if len(sys.argv)<2:
	print "Error correct method: python SimteBot.py <'Token'>"
else:
	bot=telepot.Bot(sys.argv[1])
	print bot.getMe()