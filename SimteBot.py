#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler,MessageHandler,Filters, RegexHandler, ConversationHandler)
reload(sys)  
sys.setdefaultencoding('utf8')
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
                self.p=int(p)
        def edit(self,user,about,p):
                if user in self.group:
                        self.about=about
                        self.p=int(p)
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
                return "Titulo:"+self.title+"\nDescripción corta:"+self.shortAbout+"\nDescripción: "+self.about+"\nCoordinador: @"+self.coordinator+"\nGrupo: "+self.showGroup()+"\nAvance "+str(self.p)+" % "
        def showGroup(self):
                cdn=""
                for x in self.group:
                       cdn=cdn+"\n\t @"+x
                return cdn
        def showShort(self):
                return "[ "+self.title+"\t"+str(self.p)+"% \n"+self.shortAbout+"\n @"+self.coordinator+"]\n"

# EndClass

logging.basicConfig(filname='SimteLog.log',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger= logging.getLogger(__name__)
CHOOSE,CHOOSING, TYPING_REPLY, TYPING_CHOICE, TITLE, DC, DL,COOR,AVAN,DONE= range(10)
TAREAS=[]
reply_keyboardg=[['ver tareas'],
                 ['salir']]
reply_keyboardp=[['Agregar tarea','Modificar tarea'],
                 ['Unirse','Retirarse','Delegar'],
                 ['salir']]
ok_keyboard=[['Aceptar','/Cancelar']]
cancel_keyboard=[['/Cancelar']]
markupg=ReplyKeyboardMarkup(reply_keyboardg, one_time_keyboard=True)
markupp=ReplyKeyboardMarkup(reply_keyboardp, one_time_keyboard=True)
markupo=ReplyKeyboardMarkup(ok_keyboard,one_time_keyboard=True)
markupc=ReplyKeyboardMarkup(cancel_keyboard,resize_keyboard=True,one_time_keyboard=True)
def start(bot, update):
        teclado=markupg
        if(update['message']['chat']['type']=='private'):
                teclado=markupp
        update.message.reply_text(
                "Hola, soy SimteBot espero poderte ayudar, selecciona alguna de las opciones que aparecen a continuación",
                reply_markup=teclado)
        return CHOOSING

def listar(bot,update,user_data):
        cdn=""
        for t in TAREAS:
                cdn=cdn+t.showShort()
        bot.sendMessage(chat_id=update.message.chat_id, text="Las tareas del grupo son: \n"+cdn)
        return ConversationHandler.END
def addWork(bot,update,user_data):
        update.message.reply_text(
                "Vas a crear una nueva tarea tienes que llenar unos datos que vamos a solicitar uno a la vez si te arrepientes cancela la operación",reply_markup=markupo)
        return TITLE

def addTitle(bot,update,user_data):
        update.message.reply_text("Escribe el titulo de la tarea, intenta ser claro y breve",reply_markup=markupc)
        return DC
def addDC(bot,update,user_data):
        text=update.message.text
        user_data['Titulo']=text
        update.message.reply_text("Escribe una descripción breve de tu tarea máximo 10 palabras",reply_markup=markupc)
        return DL
def addDL(bot,update,user_data):
        text=update.message.text
        if len(text.split(' '))>10:
                update.message.reply_text("Su descripción corta excede el másximo de diez palabras, vuelve a escribirla",reply_markup=markupc)
                return DL
        user_data['DescripciónC']=text
        update.message.reply_text("Escribe la descripción de la tarea, intenta ser claro no te excedas del máximo numero de caracteres de Telegram",reply_markup=markupc)
        return AVAN
def addAvan (bot,update,user_data):
        text=update.message.text
        user_data['DescripciónL']=text
        update.message.reply_text("Escribe cuanto llevas de avance en la tarea usa un número entero entre 0 y 100.Donde 100 significa que la tarea esta completada.",reply_markup=markupc)
        return COOR
def addCoor(bot,update,user_data):
        text=update.message.text
        if not text.isdigit() or int(text)<0 or int(text)>100:
                update.message.reply_text("Escribe un numero entero entre 0 y 100 no agregues espacios.")
                return COOR
        user_data['avance']=text
        user=update.message.from_user.username
        user_data['coordinador']=user
        update.message.reply_text("Vamos a crear una tarea %s"%str(user_data),reply_markup=markupo)
        return DONE
def doneW(bot,update,user_data):
        tareatmp=Tarea(user_data['Titulo'],user_data['DescripciónC'],user_data['DescripciónL'],user_data['coordinador'],user_data['avance'])
        TAREAS.append(tareatmp)
        update.message.reply_text("se agrego exitosamente le tarea \n%s"%tareatmp.show(),reply_markup=markupp)
        user_data.clear()
        return [ConversationHandler.END,CHOOSING]
def cancelO(bot,update,user_data):
        update.message.reply_text("Se cancelo la operción, Adiós",reply_markup=markupp)
        user_data.clear()
        return [ConversationHandler.END,CHOOSING]
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
                                  ConversationHandler(
                                          entry_points=[RegexHandler('^Agregar tarea$',
                                                                     addWork,
                                                                     pass_user_data=True)],
                                          states={
                                                  TITLE:[MessageHandler(Filters.text,addTitle,pass_user_data=True)],
                                                  DC:[MessageHandler(Filters.text,addDC,pass_user_data=True)],
                                                  DL:[MessageHandler(Filters.text,addDL,pass_user_data=True)],
                                                  AVAN:[MessageHandler(Filters.text,addAvan,pass_user_data=True)],
                                                  COOR:[MessageHandler(Filters.text,addCoor,pass_user_data=True)],
                                                  DONE:[RegexHandler('^Aceptar$',doneW,pass_user_data=True)]
                                                  },
                                          fallbacks=[CommandHandler('Cancelar',cancelO,pass_user_data=True)]
                                          ),                                  
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
