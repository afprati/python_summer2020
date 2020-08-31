## Write a function that counts how many vowels are in a word
## Raise a TypeError with an informative message if 'word' is passed as an integer
## When done, run the test file in the terminal and see your results.
def count_vowels(word):
    try:
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        counter = 0
        for i in range(len(word)):
            test = word[i]
            if test in vowels:
                counter += 1
            
        print(counter)
    except TypeError:
        print("Enter a string! (You're a dummy)")
    except NameError:
        print("Name error!")
    else:
        print("Some other error that's not a name or type")
    

#count_vowels("Reese")
#count_vowels(5)
        





