# SimteBot
<h3> Alojar en heroku.</h3>
A continuación estan los pasos que hay que seguir para que el bot se ejecute en heroku:

1. Cree una cuenta en https://heroku.com/
2. Instale [Hetoku Toolbelt](https://devcenter.heroku.com/articles/heroku-cli) y averigue como usarlo en su sistema operativo.
3. Clone este repositorio: `git clone https://github.com/Usimte/SimteBot.git` 
4. Abra el directorio `SimteBot`
5. Autentiquese con `heroku login` le solicitara su correo y contraseña
6. Cree la app con `heroku apps:create #coloque el nombre de su app# --buildpack heroku/python` (Solo se permite nombres en letras minusculas y guiones)
7. Para facilitar las cosas `heroku gir:remote -a #coloque el nombre de su app#`
8. Debe tener su bot creado con el [BotFather](https://t.me/botfather) copie el Token
9. Ahora ejecute `heroku config:set TOKEN=#coloque su token aquí#`
10. Ahora `heroku config:set APPNAME=#coloque el nombre de su app#`
11. Ahora `heroku config:set CLAVE=#coloque la palabra clave aquí#`
12. Finalmente ejecuta `git add .`, `git commit -m "Mi primer commit"` y `git push heroku master`.
13. Ve a Telegram y escibele al bot `/startCLAVE` (siendo CLAVE la palabra que pusiste en el paso 11).


<h3> Justificación.</h3>
Debido a que no encontramos soluciones para gestionar los diferentes proyectos del grupo, vimos en la creación de un bot para Telegram una manera un poco mas efectiva de solucionar los problemas de comunicación y organización que existen en el grupo.


En principio se desea que el Bot:


   1.Pueda llevar el control de que tareas se encuentran activas dentro del grupo.


   	  -Listando por medio de un mensaje los títulos y una breve descripción de cada una de las tareas (máximo 10 palabras) y los responsables de las mismas. Esta función estará habilitada para que funcione en el grupo.
	  
	-El creador de la tarea sera el responsable ante el bot de dicha tarea

   2.Que permita gestionar las tareas y los grupos de trabajo asociados a ellas


   	 -Permitir agregar una nueva tarea que tenga: Titulo, descripción corta(máximo 10 palabras), Descripción larga o detallada, Porcentaje de avance, Persona responsable y grupo de trabajo.


	 -Permitir modificar las tareas y su descripción larga dependiendo del avance en el desarrollo de la misma


	 -Permitir unirse a grupos de tareas ya existentes, así como retirarse de los mismos(Se busca que esto se realice individualmente, con mensajes directos)
	 
	 -Permitirá a un responsable delegar (reasignar) dicha tarea a otro que este colaborando como auxiliar en esta tarea


   3.Llevar un control del lugar y la fecha de las reuniones así como de eventos del grupo.
   
