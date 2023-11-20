def updatePriorities(pq):
    bubbleSortByWeight(pq)

def bubbleSortByWeight(arr):
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j][1] > arr[j + 1][1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        if not swapped:
            return

def addNodesToPQ(graph,node,pq,visited,heuristic_values,weight=0,current=""):
    print("----------------")
    print(node)
    print(pq)
    print(visited)
    print(current)
    print("----------------")
    if node not in visited:
        for i in graph[node]:
            pq.append([i[0],weight+i[1]+heuristic_values[node],node+","+str(current)])
        visited.append(node)

def ucs(graph,start,goal,heuristic_values):
    try:
        graph[start]
        graph[goal]
    except:
        print("start or end needs are not in graph")
        return
    
    visited = []
    pq = []
    addNodesToPQ(graph,start,pq,visited,heuristic_values)

    while len(pq)>0:
        updatePriorities(pq) #sort
        current = pq.pop(0)
        print(current)
        addNodesToPQ(graph,current[0],pq,visited,heuristic_values,current[1],current[2])

        if current[0] == goal:
            print(visited)
            print("found")
            print(current)
            # print(current[2].split(",")[:-1][::-1])
            return current[2].split(",")[:-1][::-1]#return the path in order
            return 
    
    print("path not found")
         
if __name__ == "__main__":
    heuristic_values = {
        "S":5,
        "A":7,
        "B":3,
        "C":4,
        "D":6,
        "E":5,
        "F":6,
        "G1":0,
        "G2":0,
        "G3":0,
    }
    graph = {
        "S":[["A",5],["B",9],["D",6]],
        "A":[["B",3],["G1",9]],
        "B":[["A",2],["C",1]],
        "C":[["S",6],["G2",5],["F",7]],
        "D":[["S",1],["C",2],["E",2]],
        "E":[["G3",7]],
        "F":[["G3",8],["D",2]],
        "G1":[],
        "G2":[],
        "G3":[]
    }
    # A = [[0,55,2],[0,2,3],[3,1,4]]
    # updatePriorities(A)
    # print(A)
    ucs(graph,"S","G1",heuristic_values)
