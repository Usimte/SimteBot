#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler,MessageHandler,Filters, RegexHandler, ConversationHandler)

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

# EndClass

logging.basicConfig(filname='SimteLog.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger= logging.getLogger(__name__)
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
Tareas=[]
reply_keyboardg=[['ver tareas'],
                 ['salir']]
reply_keyboardp=[['Agregar tarea','Modificar tarea'],
                 ['Unirse','Retirarse','Delegar'],
                 ['salir']]
markupg=ReplyKeyboardMarkup(reply_keyboardg, one_time_keyboard=True)
markupp=ReplyKeyboardMarkup(reply_keyboardp, one_time_keyboard=True)
def start(bot, update):
        teclado=markupg
        if(update['message']['chat']['type']=='private'):
                teclado=markupp
        update.message.reply_text(
                "Hola, soy SimteBot espero poderte ayudar, selecciona alguna de las opciones que aparecen a continuación",
                reply_markup=teclado)
        return CHOOSING

def listar(bot,update,user_data):
        pass

def addWork(bot,update,user_data):
        pass
def modWork(bot,update,user_data):
        pass
def addPerson(bot,update,user_data):
        pass
def byePerson(bot,update,user_data):
        pass
def passCoor(bot,update,user_data):
        pass
def salir(bot,update,user_data):
        print str(user_data)
        user_data.clear()
        return ConversationHandler.END

def error(bot, update,error):
        logger.warn('Update "%s" causo el error "%s"'(update,error))
        
def main(token):
        updater=Updater(token)
        dp=updater.dispatcher
        conv_handler=ConversationHandler(
                entry_points=[CommandHandler('start'+sys.argv[2],start)],
                states={
                        CHOOSING:[RegexHandler('^ver tareas$',
                                               listar,
                                               pass_user_data=True),
                                  RegexHandler('^Agregar tarea$',
                                               addWork,
                                               pass_user_data=True),
                                  RegexHandler('^Modificar tarea$',
                                               modWork,
                                               pass_user_data=True),
                                  RegexHandler('^Unirse$',
                                               addPerson,
                                               pass_user_data=True),
                                  RegexHandler('^Retirarse$',
                                               byePerson,
                                               pass_user_data=True),
                                  RegexHandler('^Delegar$',
                                               passCoor,
                                               pass_user_data=True)
                        ],
                        },
                fallbacks=[RegexHandler('^salir$',
                                        salir,
                                        pass_user_data=True)]
                )
        dp.add_handler(conv_handler)
        dp.add_error_handler(error)
        updater.start_polling()
        updater.idle()
        
if len(sys.argv)<3:
        print "Error correct method: python SimteBot.py 'Token' 'pass'"
else:
        main(sys.argv[1])
