from random import *
x = 0
while True:
    list = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    if x < 21:
        print("Máš",x,"bodů.")
        ans = input("Chceš otočit kartu?: ").lower()
        if ans == "ano".lower():
            y = choice(list)
            print("Vytáhl sis", y)
            x += y
        elif ans == "ne".lower():
            prot = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21)
            z = choice(prot)
            print("Hra končí. Máš",x,"bodů.")
            print("Protivník má",z,"bodů")
            if x > z:
                print("Vyhráls!")
                break
            elif x<z:
                print("Prohráls!")
                break
            elif x == z:
                print("Remíza!")
                break
    elif x == 21:
        print("Součet je",x,"vyhráls!")
        break
    elif x> 21:
        print("Součet je",x,"prohráls!")
        break