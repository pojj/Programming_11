# calculates word value and finds best word (most points)

Blood_Boiling_PAIN = {"A":1, "B":3, "C":3, "D":2, "E":1, "F":4,
                      "G":2, "H":4, "I":1, "J":8, "K":5, "L":1,
                      "M":3, "N":1, "O":1, "P":3, "Q":10, "R":1,
                      "S":1, "T":1, "U":1, "V":4, "W":4, "X":8,
                      "Y":4, "Z":10}


def word_value(word):
    points = 0
    word = word.upper()
    for i in word:
        points += Blood_Boiling_PAIN[i]
    return points
        
    
    
def best_word(words):
    best = ["",0]
    for word in words:
        if word_value(word) > best[1]:
            best[0] = word
            best[1] = word_value(word)
    return best[0]


words = ["Satisfactory", "food", "codeskulptor"]

print(best_word(words))

# test case 1:
# words = ["bananas", "Jimmy"]
# output: Jimmy

# test case 2:
# words = ["Satisfactory", "food", "codeskulptor"]
# output: codeskulptor