from flask import Flask , render_template,request,session
import subprocess
import sys
import uuid
import time

app = Flask(__name__)
id = uuid.uuid1()
app.secret_key = "NIHALSARGAIYA98"
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
		command="./"+session["id"]+".out > "+session["id"]+".txt"
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		time.sleep(1)
	else:
		tempo=str(session["id"]+".cpp:")
		res = str(res).replace(tempo,"")
		return res
	f = open(session["id"]+".txt", 'r')
	res=f.read()
	res=res.replace("\n","<br/>")
	print(res)
	f.close()
	time.sleep(2)
	command="rm "+session["id"]+".*"
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	return res

@app.route("/")
def hello():
	if "id" not in session :
		session['id']=id.hex
	print(request.remote_addr)
	print(session)
	return render_template('/home.html')

if (__name__ == "__main__"):
	app.run(port = 5000,debug=True)
