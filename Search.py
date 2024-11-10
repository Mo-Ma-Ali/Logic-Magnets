from collections import deque
from copy import deepcopy

class Search:
    def __init__(self, grid, level_data, game):
        self.grid = grid
        self.level_data = level_data
        self.game = game

    def BFS(self):
        initial_state = tuple((ball_type, (row, col)) for ball_type, (row, col) in self.game.level_data[1])
        queue = deque([(initial_state, 0, [])])  
        visited = set()  

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

        while queue:
            current_state, depth, path = queue.popleft()
            self.game.level_data[1] = list(current_state)
            if self.game.win():
                print("Winning state reached:", current_state)
                return path

            if depth >= self.level_data[3]:
                visited.add(current_state)
                depth = 0
                self.game.level_data = deepcopy(self.level_data)
                # print("reset game", self.game.level_data[1])
                self.game.load()
                
                
            # print(depth)
            for i, (ball_type, (row, col)) in enumerate(current_state):
                if ball_type == "Immobile":
                    continue

                for dr, dc in directions:
                    new_row, new_col = row, col

                    while (0 <= new_row + dr < self.grid.rows and
                        0 <= new_col + dc < self.grid.cols and
                        not self.position_occupied(new_row + dr, new_col + dc, current_state)):
                        
                        new_row += dr
                        new_col += dc
                    self.game.movement(new_row,new_col,i)
                    new_state = tuple(
                        # (ball_type, (new_row, new_col)) if idx == i else
                        (bt, pos)
                        for idx, (bt, pos) in enumerate(self.game.level_data[1])
                    )

                    if new_state not in visited:
                        queue.append((new_state, depth + 1, path + [(i, (new_row, new_col))]))
                        # print(f"New state added to queue: {new_state}")
                        

        print("No solution found")
        return None


    def DFS(self):
        initial_state = tuple((ball_type, (row, col)) for ball_type, (row, col) in self.game.level_data[1])
        stack = [(initial_state, 0, [])]
        visited = set()

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            current_state, depth, path = stack.pop()
            self.game.level_data[1] = list(current_state)
            if self.game.win():
                print("Winning state reached:", current_state)
                return path

            if depth >= self.level_data[3]:
                visited.add(current_state)
                depth = 0
                self.game.level_data = deepcopy(self.level_data)
                self.game.load()

            for i, (ball_type, (row, col)) in enumerate(current_state):
                if ball_type == "Immobile":
                    continue

                for dr, dc in directions:
                    new_row, new_col = row, col

                    while (0 <= new_row + dr < self.grid.rows and
                           0 <= new_col + dc < self.grid.cols and
                           not self.position_occupied(new_row + dr, new_col + dc, current_state)):
                        
                        new_row += dr
                        new_col += dc
                    self.game.movement(new_row, new_col, i)

                    new_state = tuple(
                        # (ball_type, (new_row, new_col)) if idx == i else 
                        (bt, pos)
                        for idx, (bt, pos) in enumerate(self.game.level_data[1])
                    )

                    if new_state not in visited:
                        stack.append((new_state, depth + 1, path + [(i, (new_row, new_col))]))
                        # print(f"New state added to stack: {new_state}")

        print("No solution found")
        return None
    

    def position_occupied(self, row, col, state):
        return any(pos == (row, col) for _, pos in state)
