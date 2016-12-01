import PushToGameResultsTest2
import time

x = 0
    

while x < 1000:
    print ('Running')
    PushToGameResultsTest2.myMainFunction()
    x = x + 1
    print ('Sleeping')
    time.sleep(30)
    