#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Este es el bot de telegram para la coordinación y
manejo de las tareas del grupo,se van a utilizar
como API para la comunicación con Python
python-telegram-bot, esta es la versión para Python3

 """
# import sys
# import imp
import os   # Heroku
import pickle
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardHide, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)

token = os.environ.get('TOKEN')  # Heroku
appname = os.environ.get('APPNAME')  # Heroku
port = int(os.environ.get('PORT', '5000'))  # Heroku
clave = os.environ.get('CLAVE')  # Heroku
# Para evitar problemas con algunos caracteres poco comunes en el servidor
# imp.reload(sys)
# sys.setdefaultencoding('utf8')
# No funciona en python3


class Tarea:
        """Las tareas que va a realizar el grupo"""
        def __init__(self, title, shortAbout, about, coordinator, p):
                self.title = title
                if len(shortAbout.split()) < 11:
                        self.shortAbout = shortAbout
                else:
                        raise ValueError("Invalid length shortAbout",
                                         shortAbout)
                self.about = about

                self.coordinator = coordinator
                self.group = list()
                self.group.append(coordinator)
                self.p = int(p)

        def edit(self, user, p, about=None):
                if user in self.group:
                        if about is not None:
                                self.about = about
                        self.p = int(p)

        def add(self, user):
                if user not in self.group:
                        self.group.append(user)
                        return True
                else:
                        return False

        def remove(self, user):
                if not user == self.coordinator and user in self.group:
                        self.group.remove(user)
                        return True
                else:
                        return False

        def delegate(self, user, aux):
                if user == self.coordinator:
                        self.coordinator = aux
                        return True
                else:
                        return False

        def showGroup(self):
                cdn = "*Grupo de trabajo:*\n"
                for x in self.group:
                        cdn = cdn + "\t @" + x + "\n"
                return cdn

        def show(self):
                text = "*Titulo:*\t"+self.title
                text += "\n*Descripción corta:*\t"+self.shortAbout
                text += "\n*Descripción:* \n"+self.about
                text += "\n*coordinador:*\n @"+self.coordinator
                text += "\n"+self.showGroup()+"\n*Avance* "+str(self.p)+" % "
                return text

        def showShort(self):
                text = "[ <b>"+self.title+"</b>\t"+str(self.p)+"% @"
                text += self.coordinator + "\n" + self.shortAbout + "\n<b>"
                text += self.showGroup()+"</b>]\n"
                return text

# EndClass


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
CHOOSING, OPCION, REPLY, CHOICE, TITLE, DC, DL, COOR, AVAN, DONE = range(10)
filename = clave+".data"
reply_keyboardg = [['/verTareas'],
                   ['salir']]
reply_keyboardp = [['/verTareas', 'Agregar tarea',
                    'Modificar avance'],
                   ['Unirse', 'Retirarse', 'Delegar'],
                   ['salir']]
ok_keyboard = [['Aceptar', '/Cancelar']]
cancel_keyboard = [['/Cancelar']]
term_key = [['Siguiente']]
markupg = ReplyKeyboardMarkup(reply_keyboardg,
                              one_time_keyboard=True,
                              selective=True)
markupp = ReplyKeyboardMarkup(reply_keyboardp, one_time_keyboard=True)
markupo = ReplyKeyboardMarkup(ok_keyboard,
                              resize_keyboard=True,
                              one_time_keyboard=True)
markupc = ReplyKeyboardMarkup(cancel_keyboard,
                              resize_keyboard=True,
                              one_time_keyboard=True)
markupt = ReplyKeyboardMarkup(term_key,
                              resize_keyboard=True,
                              one_time_keyboard=True)


def saveList(obj):
        with open(filename, 'wb') as output:
                pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def unsaveList():
        try:
                with open(filename, 'rb') as input:
                        return pickle.load(input)
        except (IOError, OSError):
                return list()


TAREAS = unsaveList()


def user_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('%s - %s' % (key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
        teclado = markupg
        if(update['message']['chat']['type'] == 'private'):
                teclado = markupp
        update.message.reply_text(
                "Hola, soy *SimteBot* espero poderte ayudar,"
                "selecciona alguna de las opciones que aparecen"
                " a continuación",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=teclado)
        return CHOOSING


def listar(bot, update):
        teclado = markupg
        if(update['message']['chat']['type'] == 'private'):
                teclado = markupp
                for t in TAREAS:
                        bot.sendMessage(chat_id=update.message.chat_id,
                                        text=t.show(),
                                        parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=teclado)
        else:
                bot.sendMessage(chat_id=update.message.chat_id,
                                text="Las tareas del grupo son:\n",
                                reply_markup=teclado)
                for t in TAREAS:
                        bot.sendMessage(chat_id=update.message.chat_id,
                                        text=t.showShort(),
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=teclado)
        return CHOOSING


def addWork(bot, update, user_data):
        update.message.reply_text(
                "Vas a crear una nueva tarea tienes que llenar unos"
                "datos que vamos a solicitar uno a la vez; si te arrepientes"
                " cancela la operación.\n*Agrega el titulo*\n"
                "Escribe el *titulo* de la tarea a continuación,"
                " intenta ser claro y breve",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markupc)
        return TITLE


def addTitle(bot, update, user_data):
        text = update.message.text
        user_data['Titulo'] = text.upper()
        update.message.reply_text("*Agrega tu descripción breve*\n"
                                  "Escribe una descripción breve de tu"
                                  " tarea máximo 10 palabras",
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=markupc)
        return DC


def addDC(bot, update, user_data):
        text = update.message.text
        if len(text.split(' ')) > 10:
                update.message.reply_text("*ERROR*"
                                          "Su descripción corta excede"
                                          " el máximo de *diez* palabras,"
                                          " vuelve a escribirla",
                                          parse_mode=ParseMode.MARKDOWN,
                                          reply_markup=markupc)
                return DC
        user_data['DescripciónC'] = text
        update.message.reply_text("*Agrega la descripción larga*"
                                  "Escribe la descripción de la tarea,"
                                  " intenta ser claro no te excedas del"
                                  " máximo numero de caracteres de Telegram",
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=markupc)
        return DL


def addDL(bot, update, user_data):
        text = update.message.text
        user_data['DescripciónL'] = text
        update.message.reply_text("*Agrega el avance*"
                                  "Escribe cuanto llevas de avance en la tarea "
                                  "usa un número entero entre *0* y *100*.Donde"
                                  " 100 significa que la tarea esta"
                                  " completada.",
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=markupc)
        return AVAN


def addAvan(bot, update, user_data):
        text = update.message.text
        if not text.isdigit() or int(text) < 0 or int(text) > 100:
                update.message.reply_text("*ERROR*"
                                          "Escribe un numero entero entre *0*"
                                          " y *100* no agregues espacios.",
                                          parse_mode=ParseMode.MARKDOWN)
                return AVAN
        user_data['avance'] = text
        user = update.message.from_user.username
        user_data['coordinador'] = user
        update.message.reply_text("Vamos a crear una tarea %s"
                                  % user_str(user_data),
                                  reply_markup=markupo)
        return COOR


def addCoor(bot, update, user_data):
        tareatmp = Tarea(user_data['Titulo'],
                         user_data['DescripciónC'],
                         user_data['DescripciónL'],
                         user_data['coordinador'],
                         user_data['avance'])
        TAREAS.append(tareatmp)
        saveList(TAREAS)
        update.message.reply_text("se agrego exitosamente le tarea"
                                  " \n %s \ngracias " % tareatmp.show(),
                                  reply_markup=markupp)
        user_data.clear()
        return ConversationHandler.END


def cancelO(bot, update, user_data):
        update.message.reply_text("Se cancelo la operación, Adiós",
                                  reply_markup=markupp)
        user_data.clear()
        return ConversationHandler.END


def showWorks():
        nombres = list()
        for x, y in enumerate(TAREAS):
                nombres.append("%s - %s" % (str(x), y.title))
        return "\n".join(nombres).join(['\n', '\n'])


def obtener(bot, update, user_data):
        i = update.message.text
        if not i.isdigit() or int(i) < 0 or int(i) >= len(TAREAS):
                update.message.reply_text("Escriba un número adecuado entre"
                                          " 0 y menor que  %s" % len(TAREAS),
                                          reply_markup=markupc)
                return OPCION
        user_data['Tarea'] = TAREAS[int(i)]
        user_data['Index'] = int(i)
        update.message.reply_text(user_data['msj'], reply_markup=markupo)
        return AVAN


def modAvan(bot, update, user_data):
        text = update.message.text
        act = user_data['Tarea'].p
        if not text.isdigit() or int(text) < act or int(text) > 100:
                update.message.reply_text("Escribe un número entero entre %s"
                                          " y 100 no agregues espacios."
                                          % str(act))
                return AVAN
        user_data['avance'] = int(text)
        user = update.message.from_user.username
        user_data['usuario'] = user
        update.message.reply_text("SI NO desea cambiar cambiar completamente"
                                  " la descripción larga de la tarea oprima la"
                                  " opción Siguiente sino escríbala a"
                                  " continuación. La actual es:\n %s"
                                  % user_data['Tarea'].about,
                                  reply_markup=markupt)
        return DONE


def modDone(bot, update, user_data):
        text = update.message.text

        if text == 'Siguiente':
                user_data['Tarea'].edit(user_data['usuario'],
                                        user_data['avance'])
        else:
                user_data['Tarea'].edit(user_data['usuario'],
                                        user_data['avance'], about=text)
        saveList(TAREAS)
        update.message.reply_text("Se modifico la tarea %s"
                                  % user_data['Tarea'].show(),
                                  reply_markup=markupp)
        user_data.clear()
        return ConversationHandler.END


def modWork(bot, update, user_data):
        update.message.reply_text("Desea modificar una de las tareas"
                                  " escriba el número de uno de ellas\n %s"
                                  % showWorks(),
                                  reply_markup=markupc)
        user_data['msj'] = "Escriba el nuevo avance que tiene la"\
                           " tarea recuerde que debe ser un numero entero" \
                           " mayor al avance actual y 100"
        return OPCION


def verTarea(bot, update, user_data):
        update.message.reply_text("La tarea a la que se quiere %s es:\n"
                                  " %s \n¿esta usted seguro? "
                                  % (user_data['palabra'],
                                     user_data['Tarea'].show()),
                                  reply_markup=markupo)
        user_data['usuario'] = update.message.from_user.username
        return DONE


def addUser(bot, update, user_data):
        if user_data['Tarea'].add(user_data['usuario']):
                saveList(TAREAS)
                update.message.reply_text("Se realizo la tarea exitosamente %s"
                                          % user_data['Tarea'].show(),
                                          reply_markup=markupp)
        else:
                update.message.reply_text("Usted ya es parte del equipo",
                                          reply_markup=markupp)
        user_data.clear()
        return ConversationHandler.END


def addPerson(bot, update, user_data):
        update.message.reply_text("Desea unirse a alguna de las tareas del"
                                  " grupo, escriba el número correspondiente"
                                  " a alguna de ellas \n %s" % showWorks(),
                                  reply_markup=markupc)
        user_data['msj'] = "Desea continuar escriba ok de"\
                           " lo contrario cancelar"
        user_data['palabra'] = "agregar"
        return OPCION


def byeUser(bot, update, user_data):
        if user_data['Tarea'].remove(user_data['usuario']):
                saveList(TAREAS)
                update.message.reply_text("Se realizo la tarea exitosamente %s"
                                          % user_data['Tarea'].show(),
                                          reply_markup=markupp)
        else:
                update.message.reply_text("Usted no es parte del equipo o es"
                                          " el coordinador",
                                          reply_markup=markupp)
        user_data.clear()
        return ConversationHandler.END


def byePerson(bot, update, user_data):
        update.message.reply_text("Desea retirarse de alguna de las tareas"
                                  " del grupo, escriba el número correspondiente"
                                  " a alguna de ellas \n %s" % showWorks(),
                                  reply_markup=markupc)
        user_data['msj'] = "Desea continuar escriba ok de lo contrario cancelar"
        user_data['palabra'] = "retirar"
        return OPCION


def showGroup(bot, update, user_data):
        mem = user_data['Tarea'].group
        msj = ""
        for x, y in enumerate(mem):
                msj = msj+str(x)+" - @"+y+"\n"
        update.message.reply_text("Seleccione alguno de los miembros"
                                  " del equipo enviando el número"
                                  " correspondiente \n %s" % msj,
                                  reply_markup=markupc)
        user_data['Group'] = msj
        return CHOICE


def selectU(bot, update, user_data):
        text = update.message.text
        if not text.isdigit() or int(text) < 0 or \
           int(text) >= len(user_data['Tarea'].group):
                update.message.reply_text("Seleccione una opción valida /n"
                                          " %s" % user_data['Group'],
                                          reply_markup=markupc)
                return CHOICE
        user_data['nuevo'] = user_data['Tarea'].group[int(text)]
        update.message.reply_text("Se convertirá el usuario @%s en el"
                                  " coordinador de la tarea %s"
                                  % (user_data['nuevo'], user_data['Tarea'].title),
                                  reply_markup=markupo)
        return DONE


def coorUser(bot, update, user_data):
        if user_data['Tarea'].delegate(update.message.from_user.username,
                                       user_data['nuevo']):
                saveList(TAREAS)
                update.message.reply_text("Se realizo la tarea exitosamente %s"
                                          % user_data['Tarea'].show(),
                                          reply_markup=markupp)
        else:
                update.message.reply_text("Usted no es el coordinador y solo"
                                          " el puede hacer esta operación.",
                                          reply_markup=markupp)
        user_data.clear()
        return ConversationHandler.END


def passCoor(bot, update, user_data):
        update.message.reply_text("Desea delegar la coordinación a"
                                  " otra persona,asegúrese que la persona haga"
                                  " parte del equipo de trabajo de la tarea y"
                                  " escriba el número correspondiente a la tarea"
                                  " que desea\n %s" % showWorks(),
                                  reply_markup=markupc)
        user_data['msj'] = "¿Desea continuar?"
        return OPCION


def salir(bot, update, user_data):
        update.message.reply_text("Gracias Adiós",
                                  reply_markup=ReplyKeyboardHide())
        print (str(user_data))
        user_data.clear()
        return ConversationHandler.END


def error(bot, update, error):
        logger.warn('Update "%s" causo el error "%s"'
                    (update, error))


def main():
        updater = Updater(token)  # Heroku
        dp = updater.dispatcher
        conv_handler = ConversationHandler(
                entry_points=[CommandHandler('start'+clave, start)],
                states={
                        CHOOSING: [CommandHandler('verTareas',
                                                  listar),
                                   ConversationHandler(
                                           entry_points=[RegexHandler(
                                                   '^Agregar tarea$',
                                                   addWork,
                                                   pass_user_data=True)],
                                           states={
                                                   TITLE: [MessageHandler(
                                                           Filters.text,
                                                           addTitle,
                                                           pass_user_data=True)],
                                                   DC: [MessageHandler(
                                                           Filters.text,
                                                           addDC,
                                                           pass_user_data=True)],
                                                   DL: [MessageHandler(
                                                           Filters.text,
                                                           addDL,
                                                           pass_user_data=True)],
                                                   AVAN: [MessageHandler(
                                                           Filters.text,
                                                           addAvan,
                                                           pass_user_data=True)],
                                                   COOR: [RegexHandler(
                                                           '^Aceptar$',
                                                           addCoor,
                                                           pass_user_data=True)],
                                           },
                                           fallbacks=[CommandHandler(
                                                   'Cancelar',
                                                   cancelO,
                                                   pass_user_data=True)]),
                                   ConversationHandler(
                                           entry_points=[RegexHandler(
                                                   '^Modificar avance$',
                                                   modWork,
                                                   pass_user_data=True)],
                                           states={
                                                   OPCION: [MessageHandler(
                                                           Filters.text,
                                                           obtener,
                                                           pass_user_data=True)],
                                                   AVAN: [MessageHandler(
                                                           Filters.text,
                                                           modAvan,
                                                           pass_user_data=True)],
                                                   DONE: [MessageHandler(
                                                           Filters.text,
                                                           modDone,
                                                           pass_user_data=True)]
                                                  },
                                           fallbacks=[CommandHandler(
                                                   'Cancelar',
                                                   cancelO,
                                                   pass_user_data=True)]
                                          ),
                                   ConversationHandler(
                                           entry_points=[RegexHandler(
                                                   '^Unirse$',
                                                   addPerson,
                                                   pass_user_data=True)],
                                           states={
                                                   OPCION: [MessageHandler(
                                                          Filters.text,
                                                          obtener,
                                                          pass_user_data=True)],
                                                   AVAN: [MessageHandler(
                                                           Filters.text,
                                                           verTarea,
                                                           pass_user_data=True)],
                                                   DONE: [RegexHandler(
                                                           '^Aceptar$',
                                                           addUser,
                                                           pass_user_data=True)]
                                                  },
                                           fallbacks=[CommandHandler(
                                                   'Cancelar',
                                                   cancelO,
                                                   pass_user_data=True)]
                                          ),
                                   ConversationHandler(
                                           entry_points=[RegexHandler(
                                                   '^Retirarse$',
                                                   byePerson,
                                                   pass_user_data=True)],
                                           states={
                                                   OPCION: [MessageHandler(
                                                           Filters.text,
                                                           obtener,
                                                           pass_user_data=True)],
                                                   AVAN: [MessageHandler(
                                                           Filters.text,
                                                           verTarea,
                                                           pass_user_data=True)],
                                                   DONE:[RegexHandler(
                                                           '^Aceptar$',
                                                           byeUser,
                                                           pass_user_data=True)]
                                                  },
                                           fallbacks=[CommandHandler(
                                                   'Cancelar',
                                                   cancelO,
                                                   pass_user_data=True)]
                                          ),
                                   ConversationHandler(
                                           entry_points=[RegexHandler(
                                                   '^Delegar$',
                                                   passCoor,
                                                   pass_user_data=True)],
                                           states={
                                                   OPCION: [MessageHandler(
                                                           Filters.text,
                                                           obtener,
                                                           pass_user_data=True)],
                                                   AVAN: [RegexHandler(
                                                           '^Aceptar$',
                                                           showGroup,
                                                           pass_user_data=True)],
                                                   CHOICE: [MessageHandler(
                                                           Filters.text,
                                                           selectU,
                                                           pass_user_data=True)],
                                                   DONE: [RegexHandler(
                                                           '^Aceptar$',
                                                           coorUser,
                                                           pass_user_data=True)],
                                                  },
                                           fallbacks=[CommandHandler(
                                                   'Cancelar',
                                                   cancelO,
                                                   pass_user_data=True)]
                                   )
                        ],
                },
                fallbacks=[RegexHandler('^salir$',
                                        salir,
                                        pass_user_data=True)]
                )
        dp.add_handler(conv_handler)
        dp.add_error_handler(error)
        updater.start_webhook(listen="0.0.0.0",  # Heroku
                              port=port,
                              url_path=token)
        updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(appname, token))  # Heroku
        updater.idle()


if __name__ == '__main__':
        main()


"""
Local
if len(sys.argv) < 3:
        print ("Error correct method: python Simtebot.py 'token' 'name'")
else:
        main(sys.argv[1])
"""
