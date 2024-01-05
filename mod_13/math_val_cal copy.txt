import random
def printFibbonacci():# make fibbanaci vals
    
    vals = [1,1]
    for a in range(1000):
        vals.append(vals[-1]+vals[-2])
        # print(vals[-1]/vals[-2])
    print(vals[14])
    print(vals[24])
    start_val = random.randint(0,1000)
    tot = []
    for a in range(4):
        print(vals[start_val])
        tot.append( vals[start_val])
    print(sum(tot))
    print((tot[2] * 2) - (tot[3]))
        
def printRiceGrains():
    vals = [1]
    for a in range(64):
        vals.append(vals[-1]*2)
    print(vals)
    print(sum(vals)/250000000)
    print(sum(vals)/250000000/735 )
        
def printHands():
    for num in range(2,100):
        print(str(num)+ " "+str(int((num/2) * num-1)))

def printProves():
    a = 0
    while(a < 1000):
        if (((a**2)-a)%2 != 0):
            print(a)
            break
        a+=1
    a= 0
    while(a < 1000):
        if (((a**3)+2*a)%3 != 0):
            print(a)
            break
        a+=1
    a= 1
    while( a < 10000):
        if (((a**4)+(a**3)-(2*(a**2)))%4 == 0):
            print(a)
            break
        a+=1
    while( a < 10000):
        if (((a**3)-(a**3)-(2*(a**2)))%4 == 0):
            print(a)
            break
        a+=1
def investments():
    val = 1000
    for b in range(150):
        for a in range(100):
            val = (1+(b/1000))*val
            # print(val)
            if a == 24 and val > 1500:
                print(b/1000)
                break
        val = 1000
if __name__ == "__main__":
    # printFibbonacci()
    # printRiceGrains()
    # printHands()
    # printProves()
    investments()