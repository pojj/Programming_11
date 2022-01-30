# Does the following comments with lists by william

# Get user input for number of adjectives and number of nouns
adjectives_num = int(input("Enter number of adjectives"))
nouns_num = int(input("Enter number of nouns"))

# Create empty lists called adjectives and nouns 
adjectives = []
nouns = []


# Use a for loop to input the correct number of adjectives 
# and append each one to the adjectives list
for i in range(adjectives_num):
    adjectives.append(input("give adjective:"))

# Use a for loop to input the correct number of nouns and 
# append each one to the nouns list
for i in range(nouns_num):
    nouns.append(input("give noun:"))

# Use nested for loops to print similes in the form
# adjective + as + noun 
for i in adjectives:
    for j in nouns:
        print(i+" as "+j)

     

