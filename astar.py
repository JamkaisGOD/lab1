import heapq

from pyamaze import COLOR, agent, maze, textLabel


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def AStar(m):
    start = (m.rows, m.cols)
    goal = (1, 1)

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))

    came_from = {}
    g_score = {start: 0}
    searchPath = [start]

    while open_set:
        _, curr_cost, currCell = heapq.heappop(open_set)

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

                tentative_cost = curr_cost + 1
                if tentative_cost < g_score.get(childCell, float('inf')):
                    came_from[childCell] = currCell
                    g_score[childCell] = tentative_cost
                    searchPath.append(childCell)
                    f_score = tentative_cost + heuristic(childCell, goal)
                    heapq.heappush(open_set, (f_score, tentative_cost, childCell))

    fwdPath = {}
    path = [goal]
    cell = goal
    while cell != start:
        fwdPath[came_from[cell]] = cell
        cell = came_from[cell]
        path.append(cell)

    path.reverse()
    return searchPath, came_from, fwdPath, path


if __name__ == "__main__":
    m = maze(20, 20)
    m.CreateMaze(loopPercent=20)
    searchPath, astarPath, fwdPath, path = AStar(m)

    a = agent(m, footprints=True, color=COLOR.yellow, shape='square', filled=True)
    b = agent(m, 1, 1, footprints=True, color=COLOR.red, goal=(m.rows, m.cols))
    c = agent(m, footprints=True, color=COLOR.cyan)

    m.tracePath({a: searchPath}, delay=2)
    m.tracePath({b: astarPath}, delay=2)
    m.tracePath({c: fwdPath}, delay=5)
    textLabel(m, 'A Star Path Length', len(path))
    textLabel(m, 'A Star Searched Length', len(searchPath))
    m.run()
