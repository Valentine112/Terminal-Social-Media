import json
import re
import os
import datetime

#Class to handle the users reg details
class handlingFiles:
	
	def __init__(self, filename):
		self.filename = filename
		self.result = ""

	def createFile(self, file):
		if not bool(os.path.isfile(file)):
			f = open(file, "w+")
			f.close()
		
	def readFile(self, files):
		with open(files, "r") as file:
			if file.mode == 'r':
				self.result = file.readlines()
			file.close()

	def loadFile(self, files):
		with open(files, 'r') as file:
			if file.mode == 'r':
				return json.load(file)
			file.close()
		
	def startFile(self):
		list = []
		startUp = {
			'user': 'admin',
			'pass': 'root',
			'date': datetime.datetime.now().strftime("%x"),
			'id': 0
		}
		list.append(startUp)
		with open(self.filename, 'w') as file:
			json.dump(list, file)
			file.close()
			
	def writeFile(self, file, value):
		result = ""
		with open(file, 'r') as files:
			result = json.load(files)
			files.close()
		with open(file, 'w') as files:
			result.append(value)
			json.dump(result, files)
			files.close()
			
		
	def getResult(self):
		return self.result


'''
Class to handle users posts
 Inherits the users reg class
'''
		
class handlingPost(handlingFiles):
	
	def __init__ (self, filename):
		self.filename = filename

	def startPost(self):
		list = []
		startUp = {
			'user': 'admin',
			'post': 'Stay Safe',
			'date': datetime.datetime.now().strftime("%x"),
			'id': 0
		}
		list.append(startUp)
		with open(self.filename, 'w') as file:
			json.dump(list, file)
			file.close()


#Function to delete user under admin control

def view_users(start, filename):
	result = start.loadFile(filename)
	for val in result:
		print(val['user'], ' | ', val['date'], ' | ', val['id'])	

#Function to delete user post under admin control
def view_post(start, filename):
	result = start.loadFile(filename)
	for val in result:
		print(val['user'], ' | ', val['post'], ' | ', val['date'], ' | ', val['id'])

def change_password(start, filename, session):
	isStrong = 0
	new = input("New password: ")
	valid = re.search("[0-9]", new)
	if bool(valid) and len(new) > 6:
		isStrong = 1
		user = start.loadFile(filename)
		work = 0
		result = ""
		for val in user:
			if val['user'] == session:
				val['pass'] = new
				result = user
				work = 1
				break
			else:
				work = 0
		if bool(work):
			with open(filename, 'w') as file:
				json.dump(result, file)
				print("SUCCESSFUL")
		else:
			print("FAILED TO CHANGE")
	else:
		isStrong = 0
	if not bool(isStrong):
		print("Password should have a number and greater than 6 letters")

def delete_user(start, filename, val, mode):
	value = start.loadFile(filename)
	val_len = len(value)
	result = ""
	false = 1
	for i in range(0, val_len):
		if value[i][mode] == val:
			if val != "admin":
				del(value[i])
				result = value
				false = 0
			else:
				false = 1
			break
		else:
			false = 1

	if not bool(false):
		with open(filename, "w") as file:
			json.dump(result, file)
			return 1
			file.close()
	else:
		return 0


def delete_post(post, postfile, val, mode):
	value = post.loadFile(postfile)
	val_len = len(value)
	result = ""
	false = 1
	for i in range(0, val_len):
		if value[i][mode] == val:
			if value[i]['user'] != 'admin':
				del(value[i])
				result = value
				false = 0
			else:
				print("You can't delete the Administration post")
				false = 1
			break
		else:
			false = 1

	if not bool(false):
		with open(postfile, 'w') as file:
			json.dump(result, file)
			return 1
			file.close()
	else:
		return 0

class all_process:
	
	def __init__(self, opt):
		self.opt = opt

	def all_view(self, start, filename, post, postfile):
			
			if self.opt == "VU":
				view_users(start, filename)
				
			elif self.opt == "VP":
				view_post(post, postfile)

			elif self.opt == "DU":
				mode = int(input("Id of person to be deleted: "))
				if bool(delete_user(start, filename, mode, 'id')):
					print("SUCCESSFUL")
					print("/////////////////////////////////////////////////////////")
				else:
					print("Failed to Delete User")

					view_users(start, filename)
			elif self.opt == "DP":
				view_post(post, postfile)
				mode = input("Id of post to be deleted: ")
				if bool(delete_post(post, postfile, int(mode), 'id')):
					print("SUCCESSFUL")
					print("/////////////////////////////////////////////////////////")
				else:
					print("Failed to Delete Post")
					view_post(post, postfile)


def loginMode(session, post, postfile, start, filename):
			type = input("View post (v), Create post (c), Change pass (p), any other letter to logout: ")
			if type == "c":
				
				empty = ""
				userpost = input("Write post: ")
				article = {
					'user': session,
					'post': userpost,
					'date': datetime.datetime.now().strftime("%x")
				}
				
				#Got the id of the last post and added one to it for the new post

				val = post.loadFile(postfile)
				val_len = len(val) - 1
				last_id = int(val[val_len]['id']) + 1
				article['id'] = last_id

				post.writeFile(postfile, article)
				print("Post created successfully")
				loginMode(session, post, postfile, start, filename)

			elif type == "v":
				posts = post.loadFile(postfile)
				for myPost in posts:
					if myPost['user'] == session:
							print(myPost['post'], '\n', 'date:- ', myPost['date'])
							empty = 1
					else:
						empty = 0;
				if not bool(empty):
					print("You haven't made any post yet")
				loginMode(session, post, postfile, start, filename)
			elif type == "p":
				change_password(start, filename, session)
				loginMode(session, post, postfile, start, filename)
			else:
				print("You have logged out")
				


filename = "database.txt"

start = handlingFiles(filename)
start.createFile(filename)
start.readFile(filename)
result = start.getResult()

if not bool(result):
	start.startFile()

postfile = "userpost.txt"
post = handlingPost(postfile)
post.createFile(postfile)
post.readFile(postfile)
result1 = post.getResult()

if not bool(result1):
	post.startPost()

data = start.loadFile(filename)
default = ""

for i in data:
	if i['user'] == 'admin':
		default = i['pass']
		break
		
if default == "root":
	print("CHANGE YOUR ADMIN PASSWORD -- \n Current Username -- admin \n Current Password -- root")

form = input("Login, Register or admin:")
	
if form == "Register":
	name = input("Username: ")
	password = input("Password: ")
	
	name_valid = re.search("\W", name)
	pass_valid = re.search("[0-9]", password)
	
	if bool(name_valid):
		print("Username should contain just letters and digits")
	elif not bool(pass_valid) or len(password) < 7:
		print("Password should be greater than 6 letters and have a number")
	else:
		value = {
			'user': name,
			'pass': password,
			'date': datetime.datetime.now().strftime("%x")
		}
		values = ""
		isEmpty = ""
		
		users = start.loadFile(filename)
		val_len = len(users) - 1
		last_id = int(users[val_len]['id']) + 1
		value['id'] = last_id
		for val in values:
			if val['user'] == name:
				print("User exist already")
				isEmpty = 1
				break;
			else:
				isEmpty = 0
				
		if not bool(isEmpty):
				start.writeFile(filename, value)
				print("Registered Successfully")
				
elif form == "Login":
		user = input("Username: ")
		password = input("Password: ")
		
		session = ""
		authenticate = ""
		users = start.loadFile(filename)
		
		for val in users:
			if val['user'] == user and val['pass'] == password:
				session = val['user']
				authenticate = 1
				break
			else:
				authenticate = 0

				
#If authenticate is 1 start session and allow user access

		if not bool(authenticate):
			print("Incorrect username or password")
		else:
			
			loginMode(session, post, postfile, start, filename)
		
		
		
elif form == "admin":
	name = input("Username: ")
	password = input("password: ")
		
	result = start.loadFile(filename)
	correct = ""
	for val in result:
		if val['user'] == 'admin':
			if val['user'] == name and val['pass'] == password:
				correct = 1
			else:
				correct = 0
				print("Invalid details")


#Check if correct is 1 and start a new loop

	if bool(correct):
		print("---------------------------------A-------------------------------------")
		print(" ")
		print("---------------------------------D-------------------------------------")
		print(" ")
		print("---------------------------------M-------------------------------------")
		print(" ")
		print("---------------------------------I-------------------------------------")
		print(" ")
		print("---------------------------------N-------------------------------------")
		print(" ")
		option = input("View users(VU), View posts(VP), Delete user (DU), Delete post(DP), Change Pass(CP): ")
		
		if option == "VU":
			view_users(start, filename)
			options1 = input("VP, DU, DP: ")
			
			all = all_process(options1)
			all.all_view(start, filename, post, postfile)
			
		elif option == "VP":
			view_post(post, postfile)
			options1 = input("VU, DU, DP: ")
			
			all = all_process(options1)
			all.all_view(start, filename, post, postfile)
			
		elif option == "DP":
			view_post(post, postfile)
			
			id = int(input("Id of post to be deleted: "))
			if bool(delete_post(post, postfile, id, 'id')):
				print("POST DELETED SUCCESSFULLY")
				print("///////////////////////////////////////////")
		
		elif option == "DU":
			view_users(start, filename)
			
			uN = int(input("Id of person to be deleted: "))
			if bool(delete_user(start, filename, uN, 'id')):
				print("RECORD DELETED SUCCESSFULLY")
				print("///////////////////////////////////////////")
				
		elif option == "CP":
			change_password(start, filename, 'admin')
			
		else:
			print("INVALID SELECTION!!!")
			print("You din't stay on path and now Valentine has ended it")