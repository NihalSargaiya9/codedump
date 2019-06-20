from flask import Flask , render_template,request,session
import subprocess
import sys
import uuid
import random
import time
import string
import hashlib 


app = Flask(__name__)
id = uuid.uuid1()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

app.secret_key = "jsd@wdNl}os[k!d!.{"
@app.route("/compile",methods=["POST"])
def compile():
	f = open(session["id"]+".cpp","w")
	f.write(request.form["code"])
	f.close()
	command ="g++ -o "+session["id"]+".out "+ session["id"]+".cpp 2> "+session["id"]+".txt";
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	time.sleep(2)
	f = open(session["id"]+".txt", 'r+')
	res=f.read()
	f.close()
	print(str(res))
	if(res==""):
		command="timeout 1s ./"+session["id"]+".out  -x 'status' > "+session["id"]+".txt ; echo $? > "+session["id"]+".t.txt"
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		time.sleep(1)
	else:
		tempo=str(session["id"]+".cpp:")
		res = str(res).replace(tempo,"")
		return res
	time.sleep(1)
	timeOut = open(session["id"]+".t.txt", 'r')
	dataTimeOut= str(timeOut.read()).strip()
	if dataTimeOut!="124":
		timeOut.close()
		f = open(session["id"]+".txt", 'r')
		res=f.read()
		res=res.replace("\n","<br/>")
		print(res)
		f.close()
	else:
		res = "Time limit exceeded"
	print(res)
	time.sleep(2)
	command="rm "+session["id"]+".*"
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	return res

def generateId():
	shash = hashlib.md5(id_generator().encode()).hexdigest()
	xyz=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)   

	idhe = id.hex

	finalId = hashlib.md5((str(shash)+str(random.randrange(1000000, 5000000))).encode()).hexdigest()
	finalId = str(finalId) + str(xyz)+str(idhe)

	finalId = str(hashlib.md5(finalId.encode()).hexdigest())
	return finalId

@app.route("/")
def hello():


	if "id" not in session :
		session['id']=generateId()
	print(session)
	return render_template('/home.html')

# if (__name__ == "__main__"):
# 	app.run(host='192.168.43.68',port = 5000,debug=True)
