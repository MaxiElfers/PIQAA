class ShoppingCart:
    
    # Defines private list for the cart
    # items are added as tupels [item, quantity]
    __cart = []

    def __init__(self):
        pass

     # Returns the cart
    def getCart(self):
        return self.__cart  


    # Adds the given item and quantity to the cart
    def add(self, item, quantity):
        if type(item) != str or type(quantity) != int or quantity <= 0:
            print(f"Item {item} should be string. Quantity {quantity} should be integer and bigger than 0.")
        else:
            self.__cart.append([item, quantity])


    # Removes the given item and quantity from the cart
    def remove(self, item, quantity):
        if type(item) != str or type(quantity) != int or quantity <= 0 :
            print(f"Item {item} should be string. Quantity {quantity} should be integer and bigger than 0.")
            return
        for element in self.__cart:
            if element[0] == item:
                if element[1]>quantity:
                    # only removes given quantity of item
                    element[1] -= quantity
                    return
                else:
                    # removes complete item
                    self.__cart.remove(element)
                    return
        print(f"Item {item} not found.")


    # Counts the quantities of the items in the cart
    def countQuantities(self):
        count = 0
        for element in self.__cart:
            count += element[1]
        return count           
    