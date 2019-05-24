
import subprocess, threading, pickle

def getData(var):
	try:
		repeat = True
		global dictDati, lock
		t = "/calvino-07/" + var
		while repeat:
			dato = subprocess.check_output(["mosquitto_sub","-u","calvino00","-t",t,"-P","0123456789","-h","broker.shiftr.io","-W","5"])
			with lock:
				dato = dato.decode("utf-8")
				dato = dato.strip()
				try:
					dictDati[var] = float(dato)
				except:
					repeat = True
				else:
					repeat = False
		if len(dictDati) == 4:
			with open("dati.txt", "wb") as file:
				pickle.dump(dictDati, file)
				print(dictDati)### tmp
	except KeyboardInterrupt:
		exit(0)

if __name__ == "__main__":
	dictDati = {}
	lock = threading.Lock()
	subprocess.call(["rm", "dati.txt"])
	subprocess.call(["touch", "dati.txt"])
	for i in range(0,4):
		if i == 0:
			var = "temperatura"
		elif i == 1:
			var = "altitudine"
		elif i == 2:
			var = "pressione"
		else:
			var = "luce"
		t = threading.Thread(target = getData, args = (var, ))
		t.start()