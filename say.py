#import pyttsx3
#import subprocess


##engine = pyttsx3.init()
#engine.setProperty('voice', 'english+f1')

def counter(data,x):
	count = 0
	for d in data:
		if d[0] == x:
			count+=1
	return count

def say(data):
	for d in data:
		if d[0] == "person":
			count = counter(data,"person")
			if count==1 :
				text = f"A Person is in front of you in {d[3]} cm"
				##exit_code = subprocess.check_call("./speech.sh '%s'" %text, shell=True)
			elif counter(data,"person")>1:
				text = f"{count} persons are in front of you in {d[3]} cm"
				#exit_code = subprocess.check_call("./speech.sh '%s'" %text, shell=True)
			return text
		else:
			return "Nai Maalum"
		#if d[0]	== "chair":
			#text = f"A Chair is in front of you in {d[3]} cm"
			#exit_code = subprocess.check_call("./speech.sh '%s'" %text, shell=True)
		##if d[0]	== "laptop":
			#text = f"A Laptop is in front of you in {d[3]} cm"
			#exit_code = subprocess.check_call("./speech.sh '%s'" %text, shell=True)

			#engine.say(f"A Person is in front of you in {d[3]}")
			#engine.runAndWait()
