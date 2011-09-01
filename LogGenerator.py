'''
Created on 01-09-2011

@author: Monika
'''

import random, time

if __name__ == '__main__':
    
    while True:
        file = open('thread.log', 'a')
        
        number = random.randint(0, 3)
        if number == 0:
            file.write('[INFO]' + str(random.randint(0, 100)) + '\n')
        elif number == 1:
            file.write('[WARNING]' + str(random.randint(100, 200)) + '\n')
        else:
            file.write('[DEBUG]' + str(random.randint(200, 300)) + '\n')
        
        print 'written'
        file.close()
        
        time.sleep(random.randint(0, 2))
