import numpy
import sys
import os

# First argument is the number of tests for each executor, the other
# is the scheduling policy used


delta = 0.1
#slowdown = [1,1,1.1,1.6,2.2,2.7,3.2,3.8,4.1,4.6,5.1]
#slowdown = [1]* 16
threshold = 90000
#threshold = 350
slowdown = [1,1]
for x in range(2,16):
    slowdown.append(0.4*x+1)

#slowdown = [1,1,2,3]
#print(slowdown)
#print(len(slowdown))
tests = int(sys.argv[1])

makespanlist = [[] for _ in range(16)]
avgRespTimeList = [[] for _ in range(16)]
avgmakespanList = [[] for _ in range(16)]

#f = open('/repo/ebevikt/masterthesis/paretoBench','r')
f = open('paretoBench','r')
#f = open('testBench','r')
queueception = f.readlines()
f.close()

for yy in range(tests):
    
    
    sys.stdout.write('\r'+str(yy+1))
    sys.stdout.flush()
    
    # init
    for ex in range(2,16):

        nmbrOfNodes = 2
        nmbrOfSlots = ex
        
        queue = list(map(int,queueception[yy][1:-2].split(',')))

        # avg makespan shit

        que = []
        x = int(len(queue)/4)
        ii = 0
        for i in queue[:x]:
            aa = (0,queue[ii])
            que.append(aa)
            ii = ii + 1
        for i in queue[x:x*2]:
            aa = (1,queue[ii])
            que.append(aa)
            ii = ii + 1
        for i in queue[x*2:x*3]:
            aa = (2,queue[ii])
            que.append(aa)
            ii = ii + 1
        for i in queue[x*3:x*4]:
            aa = (3,queue[ii])
            que.append(aa)
            ii = ii + 1

        queue = que

        #queue = [(0,100),(1,100),(2,200),(3,300),(1,300)]

        if sys.argv[2] == 'LJF':
        #print(queue)
            #queue = sorted(queue)
            queue = sorted(queue, key=lambda tup: tup[1])
            queue.reverse()
        #queue = [2,1,2,4,2,3,4,1,1,1]

        if sys.argv[2] == 'SJF':
            #queue = sorted(queue)
            queue = sorted(queue, key=lambda tup: tup[1])

        if sys.argv[2] == 'LJF-aging':
            x = int(len(queue)/4)
            #q1 = sorted(queue[:x])
            q1 = sorted(queue[:x], key=lambda tup: tup[1])
            q1.reverse()
            #q2 = sorted(queue[x:x*2])
            q2 = sorted(queue[x:x*2], key=lambda tup: tup[1])
            q2.reverse()
            #q3 = sorted(queue[x*2:x*3])
            q3 = sorted(queue[x*2:x*3], key=lambda tup: tup[1])
            q3.reverse()
            #q4 = sorted(queue[x*3:x*4])
            q4 = sorted(queue[x*3:x*4], key=lambda tup: tup[1])
            q4.reverse()
            queue = q1 + q2 + q3 + q4

        if sys.argv[2] == 'SJF-aging':
            x = int(len(queue)/4)
            #q1 = sorted(queue[:x])
            q1 = sorted(queue[:x], key=lambda tup: tup[1])
            #q2 = sorted(queue[x:x*2])
            q2 = sorted(queue[x:x*2], key=lambda tup: tup[1])
            #q3 = sorted(queue[x*2:x*3])
            q3 = sorted(queue[x*2:x*3], key=lambda tup: tup[1])
            #q4 = sorted(queue[x*3:x*4])
            q4 = sorted(queue[x*3:x*4], key=lambda tup: tup[1])
            queue = q1 + q2 + q3 + q4

        nodes = []

        #print(queue)

        for i in range(nmbrOfNodes):
            nodes.append([[] for _ in range(nmbrOfSlots)])


        makespan = [0] * len(nodes)


        avgRespTimes = []
        for i in range(nmbrOfNodes):
            avgRespTimes.append( [[0] for _ in range(nmbrOfSlots)] )

        #print(avgRespTimes)

        avgmakespan = [0,0,0,0]

        # start simulation

        slotTaken = True
        while slotTaken or queue != []:

            slotTaken = False
            freeSlots = False

            for node in nodes:
                for slot in node:
                    if slot == []:
                        freeSlots = True
                        break
                if freeSlots:
                    break

            if freeSlots and queue != []:
                slotTaken = True

                # loadBalancer

                highestScore = 0
                nodeIndex = 0

                for i in range(len(nodes)):
                    busy = 0
                    node = nodes[i]
                    for slot in node:
                        if slot != []:
                            busy += 1
                    score = len(node)/(busy+0.5)
                    if score > highestScore:
                        highestScore = score
                        nodeIndex = i

                # find slot
                for slot in nodes[nodeIndex]:
                    if slot == []:
                        job = queue.pop(0)
                        if job[1] > threshold:
                            heavy = True
                        else:
                            heavy = False
                        slot.append(job[1])
                        slot.append(heavy)
                        slot.append(job[0])
                        break

            else:
                nodeCounter = 0

                for node in nodes:

                    heavyjobs = 0
                    for slot in node:
                        if slot != []:
                            if slot[1]:
                                heavyjobs += 1

                    deltaMoved = False

                    slotCounter = 0
                    for slot in node:
                        if slot != []:
                            deltaMoved = True

                            #print('\n--slot: '+ str(slot[0]) +'\n')

                            slot[0] = slot[0] - delta/slowdown[heavyjobs]


                            #print('\nnodeCounter: ' + str(nodeCounter) + ' '  + 'slotCounter: ' + str(slotCounter)+'\n')
                            #print(str(avgRespTimes[nodeCounter][slotCounter][-1]))
                            avgRespTimes[nodeCounter][slotCounter][-1] += delta




                            if slot[0] <= 0:
                                #print('----change job -----')
                                maxVal = avgRespTimes[nodeCounter][slotCounter][-1]
                                # avg makespan shit
                                if slot[2] == 0 and maxVal > avgmakespan[0]:
                                    avgmakespan[0] = maxVal
                                elif slot[2] == 1 and maxVal > avgmakespan[1]:
                                    avgmakespan[1] = maxVal
                                elif slot[2] == 2 and maxVal > avgmakespan[2]:
                                    avgmakespan[2] = maxVal
                                elif slot[2] == 3 and maxVal > avgmakespan[3]:
                                    avgmakespan[3] = maxVal

                                slot.pop()
                                slot.pop()
                                slot.pop()

                                # will add one extra, remove in the end.
                                avgRespTimes[nodeCounter][slotCounter].append(maxVal)
                            else:
                                slotTaken = True

                        slotCounter += 1

                    if deltaMoved: 
                        makespan[nodeCounter] += delta
                        #avgRespTime[nodeCounter][len(avgRespTime[nodeCounter])-1] += delta 
                    nodeCounter += 1
        makespanlist[ex].append(max(makespan))
        avgRespTimeList[ex].append(avgRespTimes)
        avgmakespanList[ex].append(avgmakespan)

#print(makespanlist)
#print('-------------------\n')
#print(avgRespTimeList)        #avgmakespan[]
#print(avgmakespanList)

#check if results exist

if not os.path.isdir('./results'):   
    os.makedirs('./results')

#Calculate makespans ..     and insert into files
exeNum = 0
for exList in makespanlist:
    if exList != []:
        f = open('./results/'+ sys.argv[2] + '_makespans_' + str(exeNum),'w')
        for test in exList:
            f.write(str(test)+'\n')
        f.close()
    exeNum += 1

# Calculate average makespans and insert into files 

exeNum = 0
for exList in avgmakespanList:
    if exList != []:
        f = open('./results/'+ sys.argv[2] + '_avgMakespan_' + str(exeNum),'w')
        for test in exList:
            accmksp = 0
            for mksp in test:
                accmksp += mksp
            f.write(str(accmksp/4)+'\n')
        f.close()
    exeNum += 1


# Calculate average Response Times and insert into files

exeNum = 0
for exList in avgRespTimeList:
    if exList != []:
        f = open('./results/'+ sys.argv[2] + '_avgRespTime_' + str(exeNum),'w')
        for test in exList: # exList: list of tests for an exec
            avgRes = 0
            for ii in test: #i: one test
                for iii in ii: #node
                    for iiii in iii[:-1]: # slot, last one is doubled by lazy coding
                        avgRes += iiii
                avgRes = avgRes / 100
            f.write(str(avgRes)+'\n')
        f.close()
    exeNum += 1

#avgResp variance:
    
#mha makespanlist får man enkelt variansen.

#Representera avgRespTime med en lista.
#Som man adderar delta till hela tiden. Men byter index när det kommer ett nytt jobb.
#Så man måste veta vilket index som är det aktuella hela tiden, på varje nod.
#avgRespTime[0] = [2,4,4+delta]
#avgRespTime[1] = [2,3,5+delta]
#När vi har den här listan kan vi bara gå igenom båda listorna, addera alla talen in dem och dela på storleken på båda listorna= len(avgRespTime[0]) + len(avgRespTime[1])

#makespanlist = sorted(makespanlist)
#print('\n' + str(makespanlist) + '\n')
#print(makespanlist)
#for i in range(2,5):
#    print("\naverage "+ str(i) + ': ' + str(sum(makespanlist[i])/len(makespanlist[i])))
#    print("median "+ str(i) + ' ' + str(sorted(makespanlist[i])[int(len(makespanlist[i])/2)]))
#    f = open('/repo/ebevikt/masterthesis/modelJenkinsTestLow'+sys.argv[2],'a')
#    f.write(str(i) + ' ' + str(sorted(makespanlist[i])[int(len(makespanlist[i])/2)])+'\n')
#    f.close()
#print('\n' +str(ex) +' '+str(makespanlist[int(len(makespanlist)/2)]))