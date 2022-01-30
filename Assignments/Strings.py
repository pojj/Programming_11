#gives length of use name, gives greeting, gives last letter
#and makes nickname. by william

first = input("Give me your first name:")

last = input("Give me your last name:")

print("Your full name is "+str(len(first)+len(last))+" letters long")

full_name = first+" "+last

print("Good morning "+full_name+"!")

print("The last letter of your first name is "+first[-1])

print("Here is your nickname is: "+first[:3]+last[:3])