def donuts(count):
    try:
        type(count) == int
        if count < 10:
            return 'Number of donuts: ' + str(count)
        else:
            return 'Number of donuts: many'
    except:
        return 'Not a valid number'


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
    if len(nums) == 0:
        return 'Empty Array provided'
    else:
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