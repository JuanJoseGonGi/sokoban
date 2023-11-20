def returnArrayOfMap(width,height,map_structure):
    arr = []
    for _ in range(height):
        arr2 = []
        for j in range(width):
            arr2.append([])    
        arr.append(arr2)
    # print(arr)
    for i in arr:
        print(i)
    # print(arr[1][5])
    for i in map_structure:
        for j in map_structure[i]:
            x,y = j[1]
            print(x,y)
            arr[y][x].append(j[0])
    for i in arr:
        print(i)

returnArrayOfMap(5,7,{'paths': [('C', (1, 1)), ('C', (2, 1)), ('C', (3, 1)), ('C', (1, 2)), ('C', (2, 2)), ('C', (3, 2)), ('C', (3, 3)), ('C', (2, 4)), ('C', (3, 4)), ('C', (1, 5)), ('C', (2, 5))], 'rocks': [('R', (0, 0)), ('R', (1, 0)), ('R', (2, 0)), ('R', (3, 0)), ('R', (4, 0)), ('R', (0, 1)), ('R', (4, 1)), ('R', (0, 2)), ('R', (4, 2)), ('R', (0, 3)), ('R', (1, 3)), ('R', (2, 3)), ('R', (4, 3)), ('R', (0, 4)), ('R', (4, 4)), ('R', (0, 5)), ('R', (4, 5)), ('R', (0, 6)), ('R', (1, 6)), ('R', (2, 6)), ('R', (3, 6)), ('R', (4, 6))], 'goals': [('M', (1, 4)), ('M', (3, 5))], 'robots': [('A-1', (1, 1)), ('A-2', (1, 5))], 'boxes': [('B-1', (2, 2)), ('B-2', (2, 4))]}
)