# recursivePathFinder.py
# 539 Fall 2015 Question 5

# Example from slides in class
# tableD = [ [(0, []), (4, [(0,1)]), (44, [(0,1)]), (62, [(0,1)]), (77, [(0,1)])],
#           [(5, [(1,0)]), (1, [(1,1)]), (39, [(1,2)]), (57, [(0,1),(1,1),(1,2)]), (72, [(0,1),(1,1),(1,2)])],
#           [(63, [(1,0)]), (6, [(1,0),(1,1)]), (19, [(1,1),(1,2),(2,2)]), (1, [(1,2)]), (16, [(0,1)])],
#           [(79, [(1,0)]), (22, [(1,0)]), (30, [(1,1)]), (17, [(1,0),(2,2)]), (2, [(1,1)])] ]

# Made-up example with multiple paths
# tableD = [ [(0, []),        (4, [(0,1)]),       (44, [(0,1)]),              (62, [(0,1)]),              (77, [(0,1)])],
#           [(5, [(1,0)]),   (1, [(1,1)]),       (39, [(1,2)]),              (57, [(0,1),(1,1),(1,2)]),  (72, [(0,1),(1,1),(1,2)])],
#           [(63, [(1,0)]),  (6, [(1,0),(1,1)]), (19, [(1,1),(1,2),(2,2)]),  (1, [(1,2),(1,1)]),         (16, [(0,1)])],
#           [(79, [(1,0)]),  (22, [(1,0)]),      (30, [(1,1)]),              (17, [(1,0),(2,2)]),        (20, [(1,1)])] ]


# Made-up example with two equal paths
tableD = [[(0, []), (4, [(0, 1)]), (44, [(0, 1)]), (62, [(0, 1)]), (77, [(0, 1)])],
          [(5, [(1, 0)]), (1, [(1, 1)]), (1, [(1, 2)]), (57, [(0, 1), (1, 1), (1, 2)]), (72, [(0, 1), (1, 1), (1, 2)])],
          [(63, [(1, 0)]), (6, [(1, 0), (1, 1)]), (19, [(1, 1), (1, 2), (2, 2)]), (1, [(1, 2), (1, 1)]),
           (16, [(0, 1)])],
          [(79, [(1, 0)]), (22, [(1, 0)]), (30, [(1, 1)]), (17, [(1, 0), (2, 2)]), (20, [(1, 1), (1, 2)])]]


# Display the table in a somewhat easily readable form
def printTable(tableIn):
    print ("* Displaying D(i,j) table: ")
    sizeI = len(tableIn)
    sizeJ = len(tableIn[0])

    # Header
    print ("i\\j\t"),
    for j in range(0, sizeJ):
        strOut = "t" + str(j)
        print ('%30s' % strOut),
    print ("")

    # Table
    for i in range(sizeI - 1, -1, -1):
        print (str("s" + str(i) + "\t")),
        for j in range(0, sizeJ):
            cost = tableIn[i][j][0]
            possibleAlignments = tableIn[i][j][1]
            strOut = str(cost) + " / " + str(possibleAlignments)
            print ('%30s' % strOut),

        print ("")


# Calculate the most optimal path (entry point)
def findBestPath(tableIn):
    print ("* findBestPath: started... ")
    sizeI = len(tableIn) - 1
    sizeJ = len(tableIn[0]) - 1

    (minCost, paths) = findBestPathRecurse(tableIn, sizeI, sizeJ, 0, [])

    print ("")
    print ("")
    print ("* findBestPath: minCost: " + str(minCost))
    for path in paths:
        print ("* findBestPath: Alignment Path: " + str(path))


# Recursive function for finding the best path -- entry point is findBestPath() above.
#
# tableIn: table
# startI, startJ: location to begin pathfinding from (should be size_i, size_j of tableIn for initial call)
# costSoFar: cost (recursive)
# pathSoFar: path (recursive)
def findBestPathRecurse(tableIn, startI, startJ, costSoFar, pathSoFar):
    print("* findBestPathRecurse started... (startI: " + str(startI) + "   startJ: " + str(startJ) + ")")

    # Step 1: Cost/Alignments at this step
    cost = tableIn[startI][startJ][0]
    possibleAlignments = tableIn[startI][startJ][1]

    # Step 2: Add cost for being in this cell
    newCost = costSoFar + cost

    # Invalid State
    if (startI < 0) or (startJ < 0):
        print ("Invalid state!")
        return (-1, [[]])

    # Stop Case: Have we reached the end of the path?
    if (startI == 0) and (startJ == 0):
        print ("End State!")
        # End of path!
        return (costSoFar, [pathSoFar])

    # Recursive case: Not at the end of path -- check all possible paths downstream
    leafNodes = []
    for possibleAlignment in possibleAlignments:
        deltaI = possibleAlignment[0]
        deltaJ = possibleAlignment[1]

        print ("deltaI: " + str(deltaI) + "    deltaJ: " + str(deltaJ))
        # Append this possible alignment to the path
        # Deep copy list
        newPathSoFar = list(pathSoFar)
        newPathSoFar.append(possibleAlignment)

        # Recurse (each returns a (cost, path) tuple
        cpTuple = findBestPathRecurse(tableIn, startI - deltaI, startJ - deltaJ, newCost, newPathSoFar)
        print ("   returned from recurse: " + str(newPathSoFar))
        # Ensure that it's a valid state before adding
        cpCost = cpTuple[0]
        cpPaths = cpTuple[1]
        print ("    cpPaths: " + str(cpPaths))
        if (cpCost >= 0):
            for path in cpPaths:
                leafNodes.append((cpCost, path))

    # Ensure we have one or more leaf nodes, or return default (invalid state/failed) value
    if (len(leafNodes) == 0):
        return (-1, [[]])

    # Find the minimum cost of all leafs
    minCost = leafNodes[0][0]
    for leaf in leafNodes:
        if (leaf[0] < minCost):
            minCost = leaf[0]

    # Collect all leaves with that minimum cost
    out = []
    for leaf in leafNodes:
        if (leaf[0] == minCost):
            out.append(leaf[1])  # Append path

    print ("* findBestPathRecurse complete... (minCost = " + str(minCost) + "    path: " + str(out))
    return (minCost, out)


# Main Program

# Step 1: Display Table
printTable(tableD)
print ("")
print ("")

# Step 2: Find the best alignment path
findBestPath(tableD)
