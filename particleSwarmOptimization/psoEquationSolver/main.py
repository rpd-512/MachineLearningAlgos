from random import randint, uniform

def equation(inp):
    a = inp[0]
    b = inp[1]
    c = inp[2]
    d = inp[3]
    val = 5*a**3-10*(abs(b)+0.1)**(-2/(abs(b)+1))+(1/2)*c**2-d**2
    return val


def particleSwarmOpti(dest, itrn, pop):
    #Error handling
    if(itrn<=0):
        raise ValueError("Can't have number of iterations less than or equal to zero")
    
    #fitness function
    def fitness(vals):
        v = equation(vals)
        if(v == dest):
            return 999999
        return abs(1/(v-dest))
    
    #create particle swarm
    gbest = [0,None]
    popData = []
    for _ in range(pop):
        x1,x2,x3,x4 = randint(-100,100),randint(-100,100),randint(-100,100),randint(-100,100)
        v1,v2,v3,v4 = randint(-10,10),randint(-10,10),randint(-10,10),randint(-10,10)
        posArr = [x1,x2,x3,x4]
        velArr = [v1,v2,v3,v4]
        pbest = [fitness(posArr),posArr]
        popData.append([fitness(posArr),posArr,velArr,pbest])
    popData.sort(reverse=True)
    gbest = [popData[0][0],popData[0][1]]

    #initiate particle motion
    for step in range(itrn+1):
        popData.sort(reverse=True)
        if(popData[0][0] >= gbest[0]):
            gbest = [popData[0][0],popData[0][1]]
        print(step,"\t",gbest[0],"\t",gbest[1])

        for p in popData:
            #print("\t",p[0],p[1])
            [x1,x2,x3,x4] = p[1]
            [v1,v2,v3,v4] = p[2]
            [g1,g2,g3,g4] = gbest[1]
            [p1,p2,p3,p4] = p[3][1]

            #--------------------------------------------------------------------#
            v1 *= uniform(0.8,1.2)
            v2 *= uniform(0.8,1.2)
            v3 *= uniform(0.8,1.2)
            v4 *= uniform(0.8,1.2)
            #--------------------------------------------------------------------#
            x1 += v1 + (g1-x1)*uniform(0.8,1.2) + (p1-x1)*uniform(0.8,1.2)
            x2 += v2 + (g2-x2)*uniform(0.8,1.2) + (p2-x2)*uniform(0.8,1.2)
            x3 += v3 + (g3-x3)*uniform(0.8,1.2) + (p3-x3)*uniform(0.8,1.2)
            x4 += v4 + (g4-x4)*uniform(0.8,1.2) + (p4-x4)*uniform(0.8,1.2)
            #--------------------------------------------------------------------#

            p[1] = [x1,x2,x3,x4]
            p[2] = [v1,v2,v3,v4]
            p[0] = fitness(p[1])

            if(p[0] >= p[3][0]):
                p[3] = [p[0],p[1]]
        #print()
particleSwarmOpti(50,1000,120)