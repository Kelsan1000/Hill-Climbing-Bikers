# Author: Kelsan Dorjee
# Credit (names of individuals, textbooks, forums, websites, etc.
# that help you):  stackexchange, Jon, Son, Greg, Quinn, Tony, Chuck
# MCS-375 Fall 2018
# Project 05 Hill Climbing Bikers
# Description: determine the smallest maximum slope of any path that
# connects the two locations. Consider only rectilinear paths (no diagonal
# travel). Following such a path should minimize the loss of water.
# Date: 2 December 2018
# Status: Completed

import sys

def main():
    file = sys.stdin.readlines()
    #a list of the cases from the file
    caseList = caseSetter(file)
    #the answers for each case
    ans = caseRunner(caseList)
    #fixes the order
    ans.reverse()
    #prints the cases and the outputs for them
    caseMaker(ans)
    
#This function returns a list of keys and values back as a dictionary
def makeDictionary(keys,values):
    dict1={}
    for i in range(len(keys)):
        dict1[keys[i]]=values[i]
    return dict1

#sets up the cases
def caseSetter(file):
    #a list to hold the cases
    caseList = []
    #initializes information of the graph, size of the graph, and table to hold
    #our graph
    #the info contains the size and starting/ending position
    #starting/ending row and column
    info, size, table = '', 0, []
    for line in file:
        #starts a case
        if size == 0:
            info = [int(col) for col in line.split()]
            size = info[0]
        #end of input
        elif [0]*5 == [int(col) for col in line.split()]:
            break
        #end of the case
        elif size == 1:
            table.append([int(col) for col in line.split()])
            #resets the size
            size = 0
            #a 2D list to hold the info and table
            twoList = [info,table]
            #resets the table
            table = []
            caseList.append(twoList)
        else:
            table.append([int(col) for col in line.split()])
            size -= 1
    return caseList
    
#makes a vertex graph using the coordinates from a table
def graphMaker(table):
    #dictionary for the graph
    graph = {}
    #the unicode value of 'A'
    acc = 65
    for row in range(len(table)):
        for col in range(len(table[0])):
            #maps a vertex to a coordinate
            graph[chr(acc)]=[row,col]
            acc=acc+1
    return graph

#makes a dictionary that shows which vertices are edges to each other
#as well as the distances from each other
def edgeMaker(graph,table):
    edges={}
    #placeholder for edges
    temp=[]
    #placeholder for the distances
    tmp=[]
    #x-cord=0,y-cord=1
    for i in graph:
        for j in graph:
            #on the same row
            if (graph[i][0]==graph[j][0]):
                #i is either above or below j
                if ((graph[i][1]==(graph[j][1]-1))|(graph[i][1]==(graph[j][1]+1))):
                    temp+=[j]
                    tmp+=[table[graph[j][0]][graph[j][1]]-table[graph[i][0]][graph[i][1]]]
            #on the same column
            if (graph[i][1]==graph[j][1]):
                #i is either left or right of j
                if ((graph[i][0]==graph[j][0]-1)|(graph[i][0]==graph[j][0]+1)):
                    temp+=[j]
                    tmp+=[table[graph[j][0]][graph[j][1]]-table[graph[i][0]][graph[i][1]]]
        #maps a vertex to another vertex and the distance between them
        for k in temp:
            edges[i]=makeDictionary(temp,tmp)
        temp,tmp=[],[]
    return edges

#calculates the shortest path tree from src
def dijkstra(graph,src,dest,visited,distances,predecessors):
    global dist       
    #ending condition
    if src == dest:
        print(predecessors)
        #we build the shortest path and display it
        path=[]
        #tracking backwards to where we started
        pred=dest
        while pred != None:
            tmp = pred
            #add vertex to path
            path += pred
            #grab the previous vertex
            pred=predecessors.get(pred)
            if pred != None:
                #grab the distance
                dist += [(graph[tmp][pred])*-1]
    else :
        if not visited: 
            distances[src]=0
        #visit neighbors
        for neighbor in graph[src]:
            #have not been there yet
            if neighbor not in visited:
                newDistance = distances[src] + abs(graph[src][neighbor])
                #found a smaller option
                if newDistance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = newDistance
                    predecessors[neighbor] = src
        #mark as visited
        visited += src
        #next smallest neighbor to be selected that has not been
        #visited yet
        unvisited={}
        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k,float('inf'))
        #index of the minimum 
        i = (min(list(unvisited.values())))
        #position of the minimum
        pos = list(unvisited.values()).index(i)
        #sets the next vertex going to the destination
        #x marks the spot!
        x=list(unvisited.keys())[pos]
        #recurse with new src
        dijkstra(graph,x,dest,visited,distances,predecessors)

#runs each case
def caseRunner(caseList):
    global dist
    #a list to hold the outputs for each case
    caseAnswers = []
    for item in caseList:
        info = item[0]
        table = item[1]
        #starting index from input
        s = [info[1]-1,info[2]-1]
        #ending index from input
        e = [info[3]-1,info[4]-1]
        #if the person does not move
        if s == e:
            caseAnswers.append(0)
        else:
            graph = graphMaker(table)
            neighbors = edgeMaker(graph,table)
            #holds the distances from each vertex to the next
            dist = []
            #graph starting position
            gsp = list(graph.values()).index(s)
            #graph ending position
            gep = list(graph.values()).index(e)
            #graph starting vertex
            gsv = list(graph.keys())[gsp]
            #graph ending vertex
            gev = list(graph.keys())[gep]
            #print('starting vertix = '+gsv+'\n'+'ending vertix = '+gev)
            dijkstra(neighbors,gsv,gev,[],{},{})
            #mini is made in case there is a big negative number
            #which would then be minimum in the list
            mini = (min(dist))
            maxi = (max(dist))
            if abs(mini) > abs(maxi):
                caseAnswers.append(mini)
            elif abs(maxi) > abs(mini):
                caseAnswers.append(maxi)
            #defaults into selecting the positive slope despite being
            #the same distance away
            elif abs(maxi) == abs(mini):
                caseAnswers.append(maxi)
    return caseAnswers

#prints out the cases
def caseMaker(cases):
    for i in range(len(cases)):
        print('Case '+str(i+1)+': '+str(cases[len(cases)-i-1])) 

if __name__ == '__main__':
    main()
