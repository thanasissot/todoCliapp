# delete/remove todos
from pymongo import MongoClient, collection
import sys

# connect to MongoD
client = MongoClient('mongodb://localhost:27017/')
# connect to specific database
db = client.todo

# user collection
userCollection = db.user
# todo collection
todoCollection = db.todo

class TodoApp():
	def __init__(self):
		while(True):
			self.firstMenu()


	def showFirstMenu(self):
		print('\n\n=====--===\n1. Login\n2. SignUp\n=====--===\n\n')

	def showSecondMenu(self):
		print('\n\n--------------------\n1. See Todos\n2. Add Todo\n3. Delete Todo\n4. Logout\n5. Logout and Quit\n--------------------\n\n')

	def userInput(self):
		''' get input from user'''
		try : argument = int(input()[0])
		except Exception as e:
			print('wrong input')
			argument = 0
		return argument

	
	def firstMenu (self):
		'''Login first "screen" menu"'''
		self.showFirstMenu()
		argument = self.userInput()
		if argument == 1:
			self.login()
		elif argument == 2:
			self.createUser()
		else : print('Wrong Input','\nTry typing 1 or 2 and then hit enter!')


	def secondMenu (self, user_object):
		''' after log in menu '''
		self.showSecondMenu()
		argument = self.userInput()
		if (argument == 1):
			self.printTodos(user_object['_id'])
		elif (argument == 2):
			newTodo = input('Insert Todo: ')
			self.insertTodo(newTodo, user_object['_id'])
		elif (argument == 3):
			index = self.userInput()
			self.deleteTodo(index-1, user_object['_id'])
		elif (argument == 4):
			self.firstMenu()
		elif (argument == 5):
			sys.exit()

	def deleteTodo(self, index, user_id):
		todoID = todoCollection.find({'username' : user_id})[index]['_id']
		todoCollection.delete_one({'_id' : todoID})
		print('Deleted Todo')
		

	def login(self):
		''' login user '''
		username = input('Username: ').strip()
		password = input('password: ').strip()
		if userCollection.find_one({'username': username}) == None:
			print('\t\t\tUser Not Found')
		else:
			if userCollection.find_one({'username': username})['password'] == password:
				while(True):
					self.secondMenu(userCollection.find_one({'username': username}))	

	def printTodos(self, user_id):
		''' show list of users todo'''
		print("\n\nList of Todo's to do (pun intented):")
		print('-----------------------------------------')
		for todo in enumerate(todoCollection.find({'username' : user_id})):
			print('', todo[0] + 1, '. ', todo[1]['item'], sep = '')
		print('-----------------------------------------\n\n')


	def insertTodo(self, newTodo, user_id):
		todoCollection.insert_one({'username' : user_id, 'item' : newTodo})

	def createUser(self):
		''' signup a new user'''
		while (True):
			username = input("pick a username: ")
			if userCollection.find_one({'username' : username}) != None or username == '':
				print("This username is not available! Pick something else")
				continue

			password = input('pick a password: ')
			if password == '':
				print('password cannot be empty!')
				continue

			userCollection.insert_one({'username' : username, 'password' : password})
			print('Succesfully Signed Up a new user!2')
			break
	
	def removeTodo(self):
		# to be continue
		pass

app = TodoApp()