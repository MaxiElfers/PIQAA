def donuts(count):
    # +++your code here+++
    return

# verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    # error handling
    if type(s) != str:
        print('Input must be a string')
        return
    
    if len(s) >= 3:
        if s[-3:] == 'ing':
            s += 'ly'
        else:
            s += 'ing'  
    return s

def remove_adjacent(nums):
    # +++your code here+++
    return

def main():
    print('donuts')

    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts('twentyone'))

    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))
    print('remove_adjacent')

    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))
    
# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()