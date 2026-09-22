import heapq
import sys

from pyamaze import COLOR, agent, maze


def h(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def Greedy(m):
    start = (m.rows, m.cols)
    goal = (1, 1)

    explored = [start]
    frontier = []
    heapq.heappush(frontier, (h(start, goal), start))
    searchPath = [start]
    greedyPath = {}

    while len(frontier) > 0:
        _, currCell = heapq.heappop(frontier)

        if currCell == goal:
            break

        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                if childCell in explored:
                    continue

                heapq.heappush(frontier, (h(childCell, goal), childCell))
                explored.append(childCell)
                greedyPath[childCell] = currCell
                searchPath.append(childCell)

    fwdPath = {}
    cell = goal
    while cell != start:
        fwdPath[greedyPath[cell]] = cell
        cell = greedyPath[cell]

    return searchPath, greedyPath, fwdPath


m = maze(5, 5)
m.CreateMaze(loopPercent=30)
searchPath, greedyPath, fwdPath = Greedy(m)

a = agent(m, footprints=True, color=COLOR.yellow, shape='square', filled=True)
b = agent(m, 1, 1, footprints=True, color=COLOR.red, goal=(m.rows, m.cols))
c = agent(m, footprints=True, color=COLOR.cyan)

m.tracePath({a: searchPath}, delay=50)
m.tracePath({b: greedyPath}, delay=50)
m.tracePath({c: fwdPath}, delay=100)

m.run()