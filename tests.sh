for problem in $(ls problems)
do
  # bfs
  python3 solution.py breadth problems/$problem
  # dfs
  python3 solution.py depth problems/$problem
  # best
  python3 solution.py best problems/$problem
  # astar
  python3 solution.py astar problems/$problem
done
