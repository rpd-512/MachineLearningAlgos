from random import randint, uniform

def equation(inp):
    a = inp[0]
    b = inp[1]
    c = inp[2]
    d = inp[3]
    val = 5*a**3-10*(abs(b)+0.1)**(-2/(abs(b)+1))+(1/2)*c**2-d**2
    return val


def geneticAlgo(dest, itrn, pop):

    prnts = pop//2

    #Error handling
    if(pop<prnts):
        raise ValueError("Can't have parent size bigger than population size")
    if(itrn<=0):
        raise ValueError("Can't have number of iterations less than or equal to zero")

    #fitness function
    def fitness(vals):
        v = equation(vals)
        if(v == dest):
            return 999999
        return abs(1/(v-dest))
    
    #create generation 0
    genData = []
    popData = []
    for _ in range(pop):
        x1,x2,x3,x4 = randint(-100,100),randint(-100,100),randint(-100,100),randint(-100,100)
        valArr = [x1,x2,x3,x4]
        popData.append([fitness(valArr),valArr])
    
    popData.sort(reverse=True)
    genData.append([0,popData])

    #initiate evolution
    for gen in range(itrn+1):
        prev_gen = genData[gen][1]
        prev_gen_best = prev_gen[0:prnts]
        
        bestFitnessInPrevGen = prev_gen_best[0][0]
        print(gen,"\t",bestFitnessInPrevGen)
        
        newPopData = []
        newPopData[0:prnts] = prev_gen_best  #keep parents in new generation
        for p in range (prnts,pop):
            #reproduce and mutate
            nx1 = prev_gen_best[randint(0,prnts-1)][1][0] + uniform(0.8,1.2)
            nx2 = prev_gen_best[randint(0,prnts-1)][1][1] + uniform(0.8,1.2)
            nx3 = prev_gen_best[randint(0,prnts-1)][1][2] + uniform(0.8,1.2)
            nx4 = prev_gen_best[randint(0,prnts-1)][1][3] + uniform(0.8,1.2)
            nArr = [nx1,nx2,nx3,nx4]
            #get fitness value for the mutation
            nFit = fitness(nArr)
            newPopData.append([nFit,nArr])
        newPopData.sort(reverse=True)
        #update new generation to... generation heaven?
        genData.append([p,newPopData])


geneticAlgo(50,1000,120)
#geneticAlgo(destination value, number of generations ,size of population)
