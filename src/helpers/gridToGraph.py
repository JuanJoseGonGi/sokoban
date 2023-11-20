def esPared(grafoArraysDeArrays,i,j):
    try:
        if "P" in grafoArraysDeArrays[i][j]:
            return True
        return False
    except IndexError:
        return None


def crearGrafoConListaAdyacencia(grafoArraysDeArrays):
    grafo = {}
    for i in range(len(grafoArraysDeArrays)):
        for j in range(len(grafoArraysDeArrays[0])):
            grafo[str([i,j])] = []
            #verificar si el nodo es una pared
            if esPared(grafoArraysDeArrays,i,j) == True:
                #si es una pared vaya al siguiente nodo
                continue
            else:    
                if esPared(grafoArraysDeArrays,i+1,j) != True and i+1>=0:
                    grafo[str([i,j])].append(str([i+1,j]))  

                if esPared(grafoArraysDeArrays,i-1,j) != True and i-1>=0:
                    grafo[str([i,j])].append(str([i-1,j])) 

                if esPared(grafoArraysDeArrays,i,j+1) != True and j+1>=0:
                    grafo[str([i,j])].append(str([i,j+1]))  

                if esPared(grafoArraysDeArrays,i,j-1) != True and j-1>=0:
                    grafo[str([i,j])].append(str([i,j-1]))   

    for k in grafo:
        print(k,grafo[k])
    return grafo
                
if __name__=="__main__":
    entrada = [
        [["A"],[],[],[]],
        [[],["P"],[],["A"]],
        [["A","A"],[],["A"],[]]
    ]

    crearGrafoConListaAdyacencia(entrada)