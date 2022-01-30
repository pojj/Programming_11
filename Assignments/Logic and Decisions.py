#CCC '12 J1 - Speed fines are not fine!
#by william

speed_limit = int(input())
speed = int(input())

speed -= speed_limit

if speed <= 0:
    print("Congratulations, you are within the speed limit!")
elif speed > 30:
    print("You are speeding and your fine is $500.")
elif speed > 20 and speed <= 30:
    print("You are speeding and your fine is $270.")
else:
    print("You are speeding and your fine is $100.")
    
    
# 2 other test cases:
# 10
# 20
#
# You are speeding and your fine is $100.

# 100
# 2000
#
# You are speeding and your fine is $500.