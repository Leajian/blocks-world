# blocks-world
My solution to BW20019 assignment for Artificial Intelligence subject in UoM.

## Lazy problem description
We have an initial state, which it looks like this...  
             &nbsp;\_  
            |__A__|&nbsp;&nbsp;\_  
            |__B__|&nbsp;|__C__|  
            ======== <-- __table__  
  
We have a goal state, which it looks like this...  
             &nbsp;\_  
            |__B__|  
            |__C__|  
            |__A__|  
            ======== <-- __table__  
Now to reach from initial state to goal state, we need to perform some steps. The algorithms do that their own way.
So, a solution would be:
1. Move A on table
2. Move C on A
3. Move B on C

### Usage
`python3 solution.py <algorithm> <problem_file_name.pddl> [solution_file_name]`

#### Available algorithms
* breadth _([Breadth First Search](https://en.wikipedia.org/wiki/Breadth-first_search))_
* depth _([Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search))_
* best _([Best First Search](https://en.wikipedia.org/wiki/Best-first_search))_
* astar _([A* Search](https://en.wikipedia.org/wiki/A*_search_algorithm))_

### Test all the problems
If you are using Linux, use `chmod +x test.sh` to give the script execution permissions, then navigate to it's location via terminal an run it using `./tests.sh` to test all problems under [problems](/problems) folder. For more problems in your life, see [this](http://www.cs.colostate.edu/meps/repository/aips2000.html#blocks).
