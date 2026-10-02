def dfs_n_queens(n):
    if n < 1:
        return []

    solutions = []
    cols, diag1, diag2 = set(), set(), set()
    placement = []  # placement[row] = column of the queen in that row

    def dfs(row):
        if row == n:
            solutions.append(placement[:])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            placement.append(col)

            dfs(row + 1)

            placement.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    dfs(0)
    return solutions


def print_board(solution):
    n = len(solution)
    for col in solution:
        print(" ".join("Q" if c == col else "." for c in range(n)))


if __name__ == "__main__":
    try:
        n = int(input("Enter n: "))
    except ValueError:
        print("Please enter a whole number.")
        raise SystemExit(1)

    result = dfs_n_queens(n)
    print(f"\nNumber of solutions for n={n}: {len(result)}")

    if result:
        if len(result) <= 20:
            print("\nAll solutions:")
            for s in result:
                print(s)
        else:
            print("\nFirst 5 solutions:")
            for s in result[:5]:
                print(s)

        print("\nBoard for the first solution:")
        print_board(result[0])
    else:
        print("No solutions exist.")