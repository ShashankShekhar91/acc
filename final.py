from http.server import HTTPServer, BaseHTTPRequestHandler
from pymongo import MongoClient
import json

#open json file and give it to data variable as a dictionary
with open("db.json") as data_file:
	data = json.load(data_file)

try:
    connect = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database
db = connect.demoAPIDB

# creating or switching to demoCollection
collection = db.apiCollection


#Defining a HTTP request Handler class
class ServiceHandler(BaseHTTPRequestHandler):
	#sets basic headers for the server
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type','text/json')
		#reads the length of the Headers
		length = int(self.headers['Content-Length'])
		#reads the contents of the request
		content = self.rfile.read(length)
		input = str(content).strip('b\'')
		self.end_headers()
		return input
		
    	######
	#LIST#
	######
	#GET Method Defination
	def do_GET(self):
		#defining all the headers
		self.send_response(200)
		self.send_header('Content-type','text/json')
		self.end_headers()
		#prints all the keys and values of the json file
		self.wfile.write(json.dumps(data).encode())
		

	def do_getTheraphy(self):
		display = {}
		input = self._set_headers()
		print("value of input", input)

		try:
			text_from_db = collection.find_one({}, {'_id': 0, input: 1})
			print("Text from database: ", text_from_db[input])
			text_from_db = text_from_db[input]

			#check if the key is present in the dictionary
			display[input] = text_from_db
			#print the keys required from the json file
			self.wfile.write(json.dumps(display).encode())
		except:
			error = "DATA NOT FOUND!"
			self.wfile.write(bytes(error, 'utf-8'))
			self.send_response(404)


	########
	#UPDATE#
	########
	#PUT method Defination
	def do_PUT(self):

		collection.insert_one(data)

		self.send_response(200)


#Server Initialization
server = HTTPServer(('127.0.0.1',8080), ServiceHandler)
server.serve_forever()
