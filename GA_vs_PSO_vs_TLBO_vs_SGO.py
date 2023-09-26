from random import randint, uniform
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import numpy as np
from math import floor
from copy import deepcopy

def equation(inp):
    val = 0
    for xi in range(len(inp)):
        val+=inp[xi]**2
    return val


def generateRandom(pop,size,min,max):
    rArr = []
    for _ in range(pop):
        a=[]
        for __ in range(size):
            a.append(randint(-100,100))
        rArr.append(a)
    return rArr

def geneticAlgo(dest, itrn, pop, rpop):
    crossValue = .1
    crossProb = 0.75
    mutateProb = 0.25
    eliteVal = pop//10

    plotData = []
    plotData.append([[],[]])
    plotData.append([[],[]])

    if(itrn<=0):
        raise ValueError("Can't have number of iterations less than or equal to zero")

    #create generation 0
    popData = []
    for u in range(pop):
        valArr = rpop[u]
        popData.append([equation(valArr),valArr])
    
    
    #initiate evolution loop
    popData.sort()
    print("Evaluating Genetic Algorithm")
    for gen in tqdm (range(itrn+1), desc="Working..."):
        initTime = time.time()
        popData.sort()
        plotData[0][0].append(gen)
        plotData[1][0].append(gen)

        best_pop = popData[0]
        plotData[0][1].append(best_pop[0])

        eliteParents = deepcopy(popData[0:randint(1,eliteVal)])
        #evolution
        #selection by ranking
        for p in range(pop):
            #chromosome by value encoding
            chromoMain = popData[p][1]
            #random selection of second parent
            randPer = popData[randint(0,pop-1)]
            chromoRand = randPer[1]
            crossoverdist = int(len(rpop[0])*crossValue)
            crossOverNum = randint(0,len(rpop[0])-crossoverdist-1)
            
            #crossover
            if(uniform(0,1)<crossProb):
                chromoMain[crossOverNum:crossOverNum+crossoverdist], chromoRand[crossOverNum:crossOverNum+crossoverdist] = \
                chromoRand[crossOverNum:crossOverNum+crossoverdist], chromoMain[crossOverNum:crossOverNum+crossoverdist]
            
            #mutation
            for g in range(crossOverNum,crossOverNum+crossoverdist):
                if(uniform(0,1)<mutateProb):
                    chromoMain[g] = chromoMain[randint(crossOverNum,crossOverNum+crossoverdist)]
                    chromoRand[g] = chromoRand[randint(crossOverNum,crossOverNum+crossoverdist)]
            popData[p][0] = equation(chromoMain)
        popData+=eliteParents
        plotData[1][1].append(time.time()-initTime)
    print("Genetic Algorithm evaluation complete\n")
    return plotData

def particleSwarmOpti(dest, itrn, pop, rpop):
    Cg = 1
    Cp = .1
    w = .8

    plotData = []
    plotData.append([[],[]])
    plotData.append([[],[]])
    
    #Error handling
    if(itrn<=0):
        raise ValueError("Can't have number of iterations less than or equal to zero")
    
    #create particle swarm
    gbest = [0,None]
    popData = []
    for u in range(pop):
        posArr = rpop[u]
        velArr = [randint(-10,10) for e in range(len(rpop[0]))]
        pbest = [equation(posArr),posArr]
        popData.append([equation(posArr),posArr,velArr,pbest])
    popData.sort()
    gbest = [popData[0][0],popData[0][1]]

    #initiate particle motion
    print("Evaluating Particle Swarm Optimization")
    for step in tqdm (range(itrn+1), desc="Working..."):
        initTime = time.time()

        popData.sort()

        #if found a fitness better than global best than assign new global best
        if(popData[0][0] <= gbest[0]):
            gbest = [popData[0][0],popData[0][1]]


        plotData[0][0].append(step)
        plotData[1][0].append(step)
        
        plotData[0][1].append(gbest[0])

        for p in popData:
            xArr = []

            for e in range(len(rpop[0])):
                xArr.append(p[1][e])
    
            vArr = p[2]
            gArr = gbest[1]
            pArr = p[3][1]
            
            #mutate current velocity
            for e in range(len(rpop[0])):
                vArr[e] *= uniform(0.8,1.2)

            #new direction = current direction + global best + personal best
            for e in range(len(rpop[0])):
                xArr[e] += w*vArr[e] + Cg*(gArr[e]-xArr[e])*uniform(0.8,1.2) + Cp*(pArr[e]-xArr[e])*uniform(0.8,1.2)

            p[1] = xArr
            p[2] = vArr
            p[0] = equation(p[1])

            #if found a fitness better than personal best than assign new personal best
            if(p[0] <= p[3][0]):
                p[3] = [p[0],p[1]]

        plotData[1][1].append(time.time()-initTime)
    print("Particle Swarm Optimization evaluation complete\n")
    return plotData

def teachingLearningBasedOpti(dest, itrn, pop, rpop):
    tf=1.1
    plotData = []
    plotData.append([[],[]])
    plotData.append([[],[]])
    
    #Error handling
    if(itrn<=0):
        raise ValueError("Can't have number of iterations less than or equal to zero")
    
    classData = []
    for u in range(pop):
        subArr = rpop[u]
        classData.append([equation(subArr),subArr])
    
    classData.sort()
    print("Evaluating Teaching Learning Based Optimization")
    for per in tqdm (range(itrn+1), desc="Working..."):
        initTime = time.time()
        tchr = classData[0]
        nClassData=[]

        plotData[0][0].append(per)
        plotData[1][0].append(per)
        
        plotData[0][1].append(tchr[0])
        
        #initiating teaching phase
        #calculating mean for all subjects
        meanArr = [0]*len(rpop[0])
        for stdnt in classData:
            meanArr = [meanArr[e]+stdnt[1][e] for e in range(len(rpop[0]))]

        #calculating difference mean
        dMeanArr = [uniform(0.8,1.2)*tf*(tchr[1][e]-meanArr[e]) for e in range(len(rpop[0]))]

        #updating class by adding difference mean to each student
        for stdntInd in range(pop):
            cdat = [classData[stdntInd][1][e] + dMeanArr [e] for e in range(len(rpop[0]))]
            nClassData.append([0,cdat])
        #initiating learning phase
        for stdnt in nClassData:
            clDat = nClassData.copy()
            clDat.remove(stdnt)

            randStdnt = clDat[randint(0,pop-2)]
            stdnt[1] = [uniform(0.8,1.2)*(randStdnt[1][e] - stdnt[1][e]) for e in range(len(rpop[0]))]

        #updating fitness values
        for stdnt in nClassData:
            stdnt[0] = equation(stdnt[1])
            
        nClassData+=classData
        nClassData.sort()
        classData = nClassData[:pop]
        
        plotData[1][1].append(time.time()-initTime)

    print("Teaching Learning Based Optimization evaluation complete\n")
    return plotData

def socialGroupOpti(dest, itrn, pop, rpop):
    cVal = 0.2

    plotData = []
    plotData.append([[],[]])
    plotData.append([[],[]])
    
    #Error handling
    if(itrn<=0):
        raise ValueError("Can't have number of iterations less than or equal to zero")

    
    popData = []

    #creating first social group
    for p in rpop:
        popData.append([equation(p),p])

    popData.sort()
    gBest = popData[0]

    print("Evaluating Social Group Optimization")
    for sP in tqdm (range(itrn+1), desc="Working..."):
        initTime = time.time()

        if(popData[0][0]<gBest[0]):
            gBest = popData[0]
        #print(sP,"\t",gBest)
    
        plotData[0][0].append(sP)
        plotData[1][0].append(sP)
    
        plotData[0][1].append(gBest[0])

        #improving phase
        for popl in range(pop-1):
            p = popData[popl]
            nP = [cVal*p[1][e]+uniform(0,1)*(gBest[1][e]-p[1][e]) for e in range(len(rpop[0]))]
            popData[popl]=[equation(nP),nP]
        
        #aquiring phase
        for popl in range(pop-1):
            p = popData[popl]
            rp = popData[randint(0,pop-1)]
            if(p[0]>rp[0]):
                nP = [p[1][e]+uniform(0,1)*(p[1][e]-rp[1][e])+uniform(0,1)*(gBest[1][e]-p[1][e]) for e in range(len(rpop[0]))]
                popData[popl]=[equation(nP),nP]
            else:
                nP = [p[1][e]+uniform(0,1)*(rp[1][e]-p[1][e])+uniform(0,1)*(gBest[1][e]-p[1][e]) for e in range(len(rpop[0]))]
                popData[popl]=[equation(nP),nP]
    
        popData.sort()
        plotData[1][1].append(time.time()-initTime)
    print("Social Group Optimization evaluation complete\n")
    return plotData


#--------------parameters--------------#
iterationNum = int(input("Enter number of iterations\t: "))
populationSize = int(input("Enter population size\t\t: "))
minRand = float(input("Enter minimum value for range\t: "))
maxRand = float(input("Enter maximum value for range\t: "))
destinationValue = 0
dimensions = 30
randGen = generateRandom(populationSize,dimensions,minRand,maxRand)
#--------------------------------------#

psoData = particleSwarmOpti(destinationValue,iterationNum,populationSize,randGen)
tloData = teachingLearningBasedOpti(destinationValue,iterationNum,populationSize,randGen)
sgoData = socialGroupOpti(destinationValue,iterationNum,populationSize,randGen)
genData = geneticAlgo(destinationValue,iterationNum,populationSize,randGen)

genFitData = genData[0]
psoFitData = psoData[0]
tloFitData = tloData[0]
sgoFitData = sgoData[0]

genTimeData = genData[1]
psoTimeData = psoData[1]
tloTimeData = tloData[1]
sgoTimeData = sgoData[1]

#graph for time
"""
plt.figure(figsize=(15,8))

plt.plot(genTimeData[0],genTimeData[1],color='r',label='Genetic Algorithm')
plt.plot(psoTimeData[0],psoTimeData[1],color='b',label='Particle Swarm Optimization')
plt.plot(tloTimeData[0],tloTimeData[1],color='g',label='Teaching Learning Based Optimization')
plt.plot(sgoTimeData[0],sgoTimeData[1],color='m',label='Social Group Optimization')

plt.xlabel("Iternation Number")
plt.ylabel("Time Required in single iteration")
plt.title("Genetic VS Particle Swarm Vs Teaching Learning Vs Social Group\nTime per iteration")
plt.legend()
"""
#graph for fitness
plt.figure(figsize=(15,8))

plt.plot(genFitData[0],genFitData[1],color='r',label='Genetic Algorithm')
plt.plot(psoFitData[0],psoFitData[1],color='b',label='Particle Swarm Optimization')
plt.plot(tloFitData[0],tloFitData[1],color='g',label='Teaching Learning Based Optimization')
plt.plot(sgoFitData[0],sgoFitData[1],color='m',label='Social Group Optimization')

plt.xlabel("Iternation Number")
plt.ylabel("Fitness value")
plt.title("Genetic VS Particle Swarm Vs Teaching Learning Vs Social Group\nFitness Value")

plt.legend()

plt.show()

