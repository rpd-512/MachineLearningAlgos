from random import randint, uniform
import matplotlib.pyplot as plt

def equation(inp):
    a = inp[0]
    b = inp[1]
    c = inp[2]
    d = inp[3]
    val = 5*a**3-10*(abs(b)+0.1)**(-2/(abs(b)+1))+(1/2)*c**2-d**2
    return val

def geneticAlgo(dest, itrn, pop):

    prnts = pop//2
    plotData = []
    plotData.append([])
    plotData.append([])


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
        plotData[0].append(gen)
        plotData[1].append(bestFitnessInPrevGen)

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
    
    return plotData
    

def particleSwarmOpti(dest, itrn, pop):

    plotData = []
    plotData.append([])
    plotData.append([])

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
        plotData[0].append(step)
        plotData[1].append(gbest[0])

        for p in popData:
            [x1,x2,x3,x4] = p[1]
            [v1,v2,v3,v4] = p[2]
            [g1,g2,g3,g4] = gbest[1]
            [p1,p2,p3,p4] = p[3][1]

            v1 *= uniform(0.8,1.2)
            v2 *= uniform(0.8,1.2)
            v3 *= uniform(0.8,1.2)
            v4 *= uniform(0.8,1.2)

            x1 += v1 + (g1-x1)*uniform(0.8,1.2) + (p1-x1)*uniform(0.8,1.2)
            x2 += v2 + (g2-x2)*uniform(0.8,1.2) + (p2-x2)*uniform(0.8,1.2)
            x3 += v3 + (g3-x3)*uniform(0.8,1.2) + (p3-x3)*uniform(0.8,1.2)
            x4 += v4 + (g4-x4)*uniform(0.8,1.2) + (p4-x4)*uniform(0.8,1.2)

            p[1] = [x1,x2,x3,x4]
            p[2] = [v1,v2,v3,v4]
            p[0] = fitness(p[1])

            if(p[0] >= p[3][0]):
                p[3] = [p[0],p[1]]
    return plotData

iterationNum = 100
populationSize = 1000
genData = geneticAlgo(50,iterationNum,populationSize)
psoData = particleSwarmOpti(50,iterationNum,populationSize)

plt.plot(genData[0],genData[1],color='r',label='Genetic Algorithm')
plt.plot(psoData[0],psoData[1],color='b',label='Particle Swarm Optimization')

plt.xlabel("Iternation Number")
plt.ylabel("Fitness value")
plt.title("Genetic VS Particle Swarm")

plt.legend()
plt.show()