## Exercise 1
## Write a function using recursion to calculate the greatest common divisor of two numbers

## Helpful link:
## https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm
def gcd(x, y):
    min_num = min(x,y)
    max_num = max(x,y)
    if x == 0 or y ==0:
        return max_num
    elif max_num % min_num == 0:
        return min_num
    else:
        x_new = max_num % min_num
        y_new = min_num
        return gcd(x_new, y_new)

gcd(20, 15)
gcd(8, 24)
gcd(16, 19)
gcd(19, 19)





## Problem 2
## Write a function using recursion that returns prime numbers less than 121
def find_primes(me = 10, primes = []):
    for i in range(1, me+1):
        if i == 1:
            continue
        else:
            for j in range(2,i):
                if i%j == 0:
                    print(i)
                    break
            else:
                primes.append(i)

    print(primes)
    # return find_primes(me-1, primes = primes)
find_primes()





## Problem 3
## Write a function that gives a solution to Tower of Hanoi game
## https://www.mathsisfun.com/games/towerofhanoi.html
# find number of movements

move_counter = 0
def tower_hanoi(disks, source, spare, destination):
    pass

# Recursive Python function to solve the tower of hanoi 
  
def TowerOfHanoi(n , source, destination, spare):
    if n==1: #disk 1
        print ("Move disk 1 from source",source,"to destination",destination )
        return
    else:
        TowerOfHanoi(n-1, source, spare, destination)
        print ("Move disk",n,"from source",source,"to destination",destination )
        TowerOfHanoi(n-1, spare, destination, source)
          
# Driver code 
n = 3
TowerOfHanoi(n,'A','B','C')  
# A, C, B are the name of rods 
  
# Contributed By Dilip Jain




