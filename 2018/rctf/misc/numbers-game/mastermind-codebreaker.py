from random import randint

import itertools

SECRET_LENGTH = 4
num = [1, 2, 3, 4, 5, 6]
num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

secret = [randint(min(num),max(num)),randint(min(num),max(num)),randint(min(num),max(num)),randint(min(num),max(num))]

#secret = [1,1,4,1]

if not len(secret) == SECRET_LENGTH:
	exit()

print("Secret: " + str(secret))

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
	possibilities = []

	#Create S
	for possibility in itertools.product(num, repeat=4):
		#if len(set(possibility)) == 4:
		possibilities.append(possibility)


	full_set = possibilities


	#kuth recommends 1122 for 1-6, which will be 0011 for 0-9
	first_guess=(min(num),min(num),min(num) + 1, min(num) + 1)


	current_guess = first_guess
	#print(" ".join(map(str,current_guess)))
	#exit()
	guesses = []
	guesses.append(current_guess)
	#Make the current guess
	while len(possibilities)>=1:
		print (current_guess)
		result = guess(current_guess,secret)

		print(result)
		correct_positions = result[0]
		correct_numbers = result[1]

		#exit()

		if correct_positions == SECRET_LENGTH:
			print("You have won the game!")
			exit()

		#clean up S a.k.a. possibilities

		temp_possiblities = []
		for possibility in possibilities:

			#print (possibility)
			#we compare our current_guess against all remaining elements in S
			#we remove all elements that don't behave the same, e.g. if we got (0,0) we only keep elements where we would also get (0,0) with our guess
			temp_result = guess(current_guess,possibility)
			#print(temp_result)
			if temp_result == result:
				#same result = same behaviour
				temp_possiblities.append(possibility)
				

		possibilities = temp_possiblities

		print(str(len(possibilities)) + " Elements left")
		#vars(possibilities)

		#TODO: Use the Knuth Approach
		#max_min_eliminations = 0
		#best_guess = current_guess
			
		#we iterate over the full set
		#for temp_guess in full_set:
		#	eliminations_array =[]
			#for possible_result in [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[3,0]]:
			#for possible_result in [[0,0],[0,1],[0,2],[1,0],[1,1],[2,0]]:
		#	for possible_result in [[0,1]]:
		#		eliminations = 0
		#		for possibility in possibilities:
		#			#print(possible_result)
		#			temp_result = guess(temp_guess,possibility)
		#			if not temp_result == possible_result:
		#				eliminations += 1

		#		eliminations_array.append(eliminations)
			
		#	if min(eliminations_array) > max_min_eliminations:
		#		max_min_eliminations = min(eliminations_array)
		#		best_guess = temp_guess
		#		print(max_min_eliminations)
		#		print(best_guess)

			#print(possible_result[0])

		#current_guess = possibilities[randint(0,len(possibilities)-1)]

		current_guess = possibilities[randint(0,len(possibilities)-1)]




