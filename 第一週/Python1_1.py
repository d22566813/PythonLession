list=[['A','B','C'], ['A','C','B'], ['B','A','C']]
number=input("How many plates?")

while number.isdigit():
    if int(number)==1:
        list[0]
        print(list[0]+"number=1, move from A to C")
        exit(0)
    if int(number)!=1:
        i=2
        while i<int(number):
            list=list[i]
            ifi==2:
                print(list[i]+"number=number-1, move from B to C")
            if i==1:
                print(list[i]+"number=number-1, move from A to B")
            i-=1           
                  
            if int(number)<=0:
                exit(0)

    