'''
Created on 01-09-2011

@author: Monika
'''

import random, time
import sys

if __name__ == '__main__':
    
    while True:
        file = open(sys.argv[1], 'a')
        
        number = random.randint(0, 3)
        if number == 0:
            s = '[INFO]' + str(random.randint(0, 100)) + '\n'
        elif number == 1:
            s = '[WARNING]' + str(random.randint(100, 200)) + '\n'
        else:
            s = '[DEBUG]' + str(random.randint(200, 300)) + '\n'
        file.write(s)        
        file.close()
        print s,
		
        time.sleep(random.randint(0, 2))
