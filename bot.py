import pzgram, pickle, threading, subprocess, decimal

bot = pzgram.Bot("706070524:AAGA-aIaEnFaZh_7Q1rxooqxvJFTYUJCRQU")

CID=238796511

#_______START_______

def start_command(chat):
	keyboard = pzgram.create_keyboard([["/Temperatura","/Luce"],["/Altitudine", "/Pressione"]])
	chat.send("Select a command", reply_markup=keyboard)

#_______TMP_______

def show_temp(chat):
	keyboard = pzgram.create_keyboard([["/InstantTmp","/LastMinTmp"],["/Last10MinTmp", "/LastHourTmp"]])
	chat.send("Select a command", reply_markup = keyboard)

def sendInstantTmp(chat):
	global listaDati
	chat.send("{} C°".format(listaDati[-1]["temperatura"]))

def sendLastMinuteTmp(chat):
	global listaDati, lockDati
	with lockDati:
		chat.send("{} C°".format(listaDati[-2]["temperatura"]))

def sendLastTenMinutesTmp(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,11):
			media=media+listaDati[-i]["temperatura"]
	media=media/10
	#output = decimal.Decimal(media,2)
	chat.send("{} C°".format(media))

def sendLastHourTmp(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,61):
			media=media+listaDati[-i]["temperatura"]
	media=media/60
	#output = decimal.Decimal(media,2)
	chat.send("{} C°".format(media))

#_______PRESSURE_______

def show_press(chat):
	keyboard = pzgram.create_keyboard([["/InstantPrs","/LastMinPrs"],["/Last10MinPrs", "/LastHourPrs"]])
	chat.send("Select a command", reply_markup=keyboard)

def sendInstantPrs(chat):
	global listaDati
	chat.send("{} Pa".format(listaDati[-1]["pressione"]))

def sendLastMinutePrs(chat):
	global listaDati, lockDati
	with lockDati:
		chat.send("{} Pa".format(listaDati[-2]["pressione"]))

def sendLastTenMinutesPrs(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,11):
			media=media+listaDati[-i]["pressione"]
	media=media/10
	#output = decimal.Decimal(media,2)
	chat.send("{} Pa".format(media))

def sendLastHourPrs(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,61):
			media=media+listaDati[-i]["pressione"]
	media=media/60
	#output = decimal.Decimal(media,2)
	chat.send("{} Pa".format(media))

#_______ALTITUDE_______

def show_alt(chat):
	keyboard = pzgram.create_keyboard([["/InstantAlt","/LastMinAlt"],["/Last10MinAlt", "/LastHourAlt"]])
	chat.send("Select a command", reply_markup=keyboard)

def sendInstantAlt(chat):
	global listaDati
	chat.send("{} m".format(listaDati[-1]["altitudine"]))

def sendLastMinuteAlt(chat):
	global listaDati, lockDati
	with lockDati:
		chat.send("{} m".format(listaDati[-2]["altitudine"]))

def sendLastTenMinutesAlt(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,11):
			media=media+listaDati[-i]["altitudine"]
	media=media/10
	#output = decimal.Decimal(media,2)
	chat.send("{} m".format(media))

def sendLastHourAlt(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,61):
			media=media+listaDati[-i]["altitudine"]
	media=media/60
	#output = decimal.Decimal(media,2)
	chat.send("{} m".format(media))

#_______LIGHTNESS_______

def show_lux(chat):
	keyboard = pzgram.create_keyboard([["/InstantLux","/LastMinLux"],["/Last10MinLux", "/LastHourLux"]])
	chat.send("Select a command", reply_markup=keyboard)

def sendInstantLux(chat):
	global listaDati
	chat.send("{}".format(listaDati[-1]["luce"]))

def sendLastMinuteLux(chat):
	global listaDati, lockDati
	with lockDati:
		chat.send("{}".format(listaDati[-2]["luce"]))

def sendLastTenMinutesLux(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,11):
			media=media+listaDati[-i]["luce"]
	media=media/10
	#output = decimal.Decimal(media,2)
	chat.send("{}".format(media))

def sendLastHourLux(chat):
	global listaDati
	global lockDati
	media = 0.0
	with lockDati:
		for i in range(1,61):
			media=media+listaDati[-i]["luce"]
	media=media/60
	#output = decimal.Decimal(media,2)
	chat.send("{}".format(media))

#_______MAIN_______

def Timer():
	global flag, lock
	while True:
		if flag:
			with lock:
				flag = False
			timer = threading.Timer(5.0, getData)
			timer.start()

def getData():
	global flag, lock, listaDati, lockDati
	galf = True
	while galf:
		subprocess.call(["python3","mqtt_subscriber.py"])
		errore = subprocess.check_output(["head","-n","1","dati.txt"])
		if not errore == "":
			galf = False
	with open("dati.txt","rb") as file:
		dati = pickle.load(file)
	del listaDati[0]
	with lockDati:
		listaDati.append(dati)
	with lock:
		flag = True

# bot commands
bot.set_commands({"start" : start_command})
bot.set_commands({"Temperatura" : show_temp})
bot.set_commands({"Altitudine" : show_alt})
bot.set_commands({"Pressione" : show_press})
bot.set_commands({"Luce" : show_lux})
bot.set_commands({"InstantTmp" : sendInstantTmp})
bot.set_commands({"LastMinTmp" : sendLastMinuteTmp})
bot.set_commands({"Last10MinTmp" : sendLastTenMinutesTmp})
bot.set_commands({"LastHourTmp" : sendLastHourTmp})
bot.set_commands({"InstantPrs" : sendInstantPrs})
bot.set_commands({"LastMinPrs" : sendLastMinutePrs})
bot.set_commands({"Last10MinPrs" : sendLastTenMinutesPrs})
bot.set_commands({"LastHourPrs" : sendLastHourPrs})
bot.set_commands({"InstantAlt" : sendInstantAlt})
bot.set_commands({"LastMinAlt" : sendLastMinuteAlt})
bot.set_commands({"Last10MinAlt" : sendLastTenMinutesAlt})
bot.set_commands({"LastHourAlt" : sendLastHourAlt})
bot.set_commands({"InstantLux" : sendInstantLux})
bot.set_commands({"LastMinLux" : sendLastMinuteLux})
bot.set_commands({"Last10MinLux" : sendLastTenMinutesLux})
bot.set_commands({"LastHourLux" : sendLastHourLux})

# global var
flag = True
listaDati = []
subprocess.call(["python3","mqtt_subscriber.py"])
with open("dati.txt","rb") as file:
	dati = pickle.load(file)
for i in range(60):
	listaDati.append(dati)


# threads
lock = threading.Lock()
lockDati = threading.Lock()
t1 = threading.Thread(target = Timer, daemon = True)
t1.start()

try:
	bot.run()
except KeyboardInterrupt:
	print("ciao ciao")
	exit(0)
