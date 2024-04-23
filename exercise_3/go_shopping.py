import easy_shopping

if __name__ == '__main__':
    calc = easy_shopping.calculator.Calculator()
    print(calc.add(7, 5))
    print(calc.subtract(34,21))
    print(calc.multiply(54, 2))
    print(calc.divide(144, 2))
    print(calc.divide(45, 0))

    shop = easy_shopping.shopping.ShoppingCart()
    shop.add('apple', 5)
    shop.add('banana', 3)
    shop.add('soap', 2)
    print(shop.getCart())
    print(shop.countQuantities())
    shop.remove('apple', 2)
    print(shop.getCart())
    print(shop.countQuantities())