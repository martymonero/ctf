#WE NEED TO SOLVE THAT
#sha256(****+gyGL3f32N1uResZ4) == 4fa45bd058a5f5e2d4ead259212f0ecb8f721eeb411d7521a9b640e05d3675a6
#https://stackoverflow.com/questions/4719850/python-combinations-of-numbers-and-letters
#https://www.owasp.org/index.php/Password_special_characters
#https://puzzling.stackexchange.com/questions/546/clever-ways-to-solve-mastermind

from random import randint

import hashlib,itertools,socket,re

HOST = "149.28.139.172"
PORT = 10002



def brute_force_unknown(known_part,target_hash):
	num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	lower_a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
	upper_a = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	

	#!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	special = [' ','!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']

	all = []
	all = lower_a + upper_a + num
	#all = lower_a + upper_a + num + special


	count = 1
	for s in itertools.product(all, repeat=4):
		unknown_part = ''.join(s)
		hash = hashlib.sha256((unknown_part + known_part).encode('UTF-8'))

		#print(hash.hexdigest())
		if hash.hexdigest() == target_hash:
			print("Found a match for: " + unknown_part)
			return unknown_part

def guess(possibility,secret):
	#we normally don't know the secret
	correct_numbers = []
	#we use an array to be able to correctly count the duplicates
	correct_positions = []

	#we need two passes as we first check for exact positions
	#TODO: Change to enumerate
	for z in range(0,len(possibility)):
		#check if the number is in secret at all
		if possibility[z] in secret:
			if possibility[z] == secret[z]:
				#this has higher priority than just correct number
				correct_positions.append(possibility[z])

	for z in range(0,len(possibility)):
		if possibility[z] in secret:
			if not possibility[z] == secret[z]:
				#only increase this if we are not above the duplicates count
				if not correct_positions.count(possibility[z]) == secret.count(possibility[z]) and not correct_numbers.count(possibility[z]) == secret.count(possibility[z]):
					correct_numbers.append(possibility[z])

	return [len(correct_positions), len(correct_numbers)]


if __name__ == '__main__':
	num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ip = socket.gethostbyname(HOST)
	s.connect ((HOST, PORT))
	response = s.recv(65565).decode('UTF-8')
	print(response)
	matches = re.findall('\([*]{4}\+([^)]+)',response)

	if len(matches) == 0 :
		print("Something went wrong during the extraction of the known part")
		exit()

	known_part = matches[0]

	matches = re.findall('={2}\s*([\w\d]+)',response)

	if len(matches) == 0 :
		print("Something went wrong during the extraction of the target_hash")
		exit()

	target_hash = matches[0]

	response = s.recv(65565).decode('UTF-8')
	print(response)


	print("Brute forcing the first 4 characters")
	print("Known Part: " + known_part)
	print("Target Hash: " + target_hash)

	unknown_part = brute_force_unknown(known_part,target_hash)

	s.sendall(unknown_part.encode('UTF-8'))

	#Stage 2 INTRO
	response = s.recv(65565).decode('UTF-8')
	print(response)


	while True:
		#Stage 2 First Input
		response = s.recv(65565).decode('UTF-8')
		print(response)

		if "Flag" in response or "Bye" in response:
			#print(reponse)
			exit() 

		possibilities = []

		#Create S
		for possibility in itertools.product(num, repeat=4):
			#THE KEY
			if len(set(possibility)) == 4:
				possibilities.append(possibility)

		first_guess=(1,2,3,4)

		current_guess = first_guess
		while len(possibilities)>=1:
			print("Sending " + " ".join(map(str,current_guess)))

			s.sendall(" ".join(map(str,current_guess)).encode('UTF-8'))

			response = s.recv(65565).decode('UTF-8')

			if "Nope" in response:
				print(response)
				matches = re.findall('Nope\.\s(\d{1})\,\s+(\d{1})',response)

				if len(matches) == 0 :
					print("Something went wrong during the extraction of the target_hash")
					exit()

				#print(matches)
				correct_positions = matches[0][0]
				correct_numbers = matches[0][1]

				result =[int(correct_positions),int(correct_numbers)]

				print(result)

				temp_possiblities = []
				for possibility in possibilities: 
					temp_result = guess(current_guess,possibility)
					if temp_result == result:
						#same result = same behaviour
						temp_possiblities.append(possibility)

				possibilities = temp_possiblities

				print(str(len(possibilities)) + " Elements left")
				#vars(possibilities)

				#TODO: Use the Knuth Approach
				current_guess = possibilities[randint(0,len(possibilities)-1)]

			else:
				print(response)
				break
				#exit()




