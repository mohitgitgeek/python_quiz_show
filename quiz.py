while True:
	d = {1: "guido von rossum", 2: ("import this", "this.c", "this.s", "this.i", "this.d"), 3: ["try", "except", "finally"], 4: "object oriented programming", 5: 23.0, 6: [[2, 11, 29, 70], "reverse = True"], 7: "turtle"}
	print("*" * 70)
	print("\t\t\t\tWELCOME TO THE PYTHON QUIZ SHOW")
	print("*" * 70)
	c = 0
	print("Do you want to play ?")
	ch = input()
	if ch.strip().lower() == "yes":
		print("Let's go !")
		print()
		print("Question 1 :\n Who founded Python ?")
		ch1 = input()
		if ch1.lower() in d[1]:
			c += 1
			print("Correct Answer ! \n Your score :", c)
		else:
			print("Wrong Answer ! \n Your score :", c)
		print()
		print("Question 2 :\n There is an Easter Egg in Python which is in the form of a function and it's four functions.\n What are they?")
		ch2 = input()
		if all(ch2.strip().lower().split(",") == i for i in d[2]):
			c += 1
			print("Correct Answer ! \n Your score :", c)
		else:
			print("Wrong Answer ! \n Your score :", c)
		print()
		print("Question 3 : Write any one function we use to handle exceptions, especially in binary files.")
		ch3 = input()
		if any(ch3.strip().lower() == i for i in d[3]):
			c += 1
			print("Correct Answer ! \n Your score :", c)
		else:
			print("Wrong Answer ! \n Your score :", c)
		print()
		print("Question 4 : Expand OOP?")
		ch4 = input()
		if ch4.lower() == d[4]:
			c += 1
			print("Correct Answer ! \n Your score :", c)
		else:
			print("Wrong Answer ! \n Your score :", c)
		print()
		print("Question 5.What is the value of this expression ? -> (24/(8*1))+20")
		ch5 = float(input())
		if ch5 == (24 / (8 * 1) + 20):
			c += 1
			print("Correct Answer ! \n Your score :", c)
		else:
			print("Wrong Answer ! \n Your score :", c)
		print()
		print("Question 6 : What will [29,2,11,70].sort() obtain? How to sort them in descending order ?")
		l = [29, 2, 11, 70]
		l.sort()
		ch6 = input()  # Enter the sorted list here
		ch6_1 = input()  # Enter the second answer here
		if (ch6 == str(l) and ch6_1.strip().lower() in d[6]):
			print("Correct Answer ! Your score :", c + 1)
		else:
			print("Wrong Answer ! Your score :", c)
		print()
		print("Question 7 : Which library in Python enables us to draw graphics and designs?")
		ch7 = input()
		if ch7.strip().lower() == d[7]:
			print("Correct Answer ! Your score :", c + 1)
		else:
			print("Wrong Answer ! Your score :", c)
		print("\nFinal Score :", c)
	else:
		print("Thanks for playing! Goodbye!")
		break