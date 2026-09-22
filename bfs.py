from collections import deque

from pyamaze import COLOR, agent, maze, textLabel


def BFS(m):
    start = (m.rows, m.cols)
    explored = [start]
    frontier = deque([start])
    searchPath = [start]
    bfsPath = {}

    while len(frontier) > 0:
        currCell = frontier.popleft()
        if currCell == (1, 1):
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

                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = currCell
                searchPath.append(childCell)

    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]

    return searchPath, bfsPath, fwdPath


if __name__ == "__main__":
    m = maze(20, 20)
    m.CreateMaze(loopPercent=30)
    searchPath, bfsPath, fwdPath = BFS(m)

    a = agent(m, footprints=True, color=COLOR.yellow, shape='square', filled=True)
    b = agent(m, 1, 1, footprints=True, color=COLOR.red, goal=(m.rows, m.cols))
    c = agent(m, footprints=True, color=COLOR.cyan)

    m.tracePath({a: searchPath}, delay=50)
    m.tracePath({b: bfsPath}, delay=50)
    m.tracePath({c: fwdPath}, delay=100)
    l = textLabel(m, 'BFS Length', len(searchPath))
    m.run()