#!/bin/python

num_ber=20
Round=0
def test():
    global Round
    while True:
        user=int(input("please input your password to pass: "))
        Round+=1
        if user == num_ber:
            print("oh you password is correct")
            print("Total rounds: ",Round)
            break
            
        else:
            
            print("Password is not correct round = ",Round)
            print("you sholud input your password until you correct") 
            
test()
        
