# Given an integer count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word 'many'
# instead of the actual count.
def donuts(count):
    try:
        if count < 10:
            return 'Number of donuts: ' + str(count)
        else:
            return 'Number of donuts: many'
    except:
        return 'Not a valid number'


# Given a string, if its length is at least 3, add 'ing' to its end.
# Unless it already ends in 'ing', in which case add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
def verbing(s):
    try:
        if len(s) >= 3:
            # test if last 3 characters are equal to 'ing'
            if s[-3:] == 'ing':
                s = s.replace('ing', 'ly')
            else:
                s += 'ing'  
        return s
    except:
        return 'Input must be a string'
    
    

# Given a list of numbers, return a list where all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or modify the passed in list.
def remove_adjacent(nums):
    try:
        if len(nums) != 0:
            newList = []
            # set currentElement to a unique value that is not a number
            currentElement = ''
            for element in nums:
                # if earlier checked element unequal to new, append and set
                if element != currentElement:
                    newList.append(element)
                    currentElement = element
            return newList
        else:
            return 'Empty Array provided'
    except:
        return 'error'
        
        

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