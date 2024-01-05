import json
import os
def getWeights():
    return json.load(open("paths.json",'r'))
def getPaths():
    with open("all_paths.txt", "r") as f:
        paths = f.readlines()
    paths = [x.split(".")[1][1:].strip().split("-") for x in paths]
    return paths

def getPathWeight(path, weights):
    weight = 0
    for i in range(len(path)-1):
        weight += weights[path[i]][path[i+1]]
    return weight

def bruteForce(paths, weights):
    minWeight = 100000
    minPath = []
    for path in paths:
        weight = getPathWeight(path, weights)
        if weight < minWeight:
            minWeight = weight
            minPath = path

    print(minWeight)
    print(minPath)

def pickShortestPath(paths, weights):
    for a in weights.keys():
        cur_point = a
        end = a
        path = [a]
        while  len(path) < len(weights.items()):
            minWeight = 100000
            for point in weights[cur_point]:
                if point not in path:
                    if weights[cur_point][point] < minWeight:
                        minWeight = weights[cur_point][point]
                        next_point = point
            path.append(next_point)
            cur_point = next_point
        path.append(end)
        print(path)
        print(getPathWeight(path, weights))



def main():
    paths = getPaths()
    fpaths = []
    for path in paths:
        #.replace("B","NYC").replace("C","PNX").replace("D","LA").replace("E","ALB")
        fpath = []
        for point in path:
            if point == "A":
                fpath.append("RIC")
            elif point == "B":
                fpath.append("NYC")
            elif point == "C":
                fpath.append("PNX")
            elif point == "D":
                fpath.append("LA")
            elif point == "E":
                fpath.append("ALB")
        fpaths.append(fpath)
    weights = getWeights()

    bruteForce(fpaths, weights)
    # pickShortestPath(paths, weights)


if __name__ == "__main__":
    main()