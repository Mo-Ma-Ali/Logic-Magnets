from collections import deque
from copy import deepcopy
import heapq
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
    


    def UCS(self):
        initial_state = tuple((ball_type, (row, col)) for ball_type, (row, col) in self.game.level_data[1])
        priority_queue = [(0, initial_state, [])]  # (cost, state, path)
        visited = set()

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        while priority_queue:
            cost, current_state, path = heapq.heappop(priority_queue)

            if current_state in visited:
                continue
            visited.add(current_state)

            self.game.level_data[1] = list(current_state)

            if self.game.win():
                print("Winning state reached:", current_state)
                return path

            for i, (ball_type, (row, col)) in enumerate(current_state):
                if ball_type == "Immobile":
                    continue

                for dr, dc in directions:
                    new_row, new_col = row, col
                    move_cost = 0

                    while (0 <= new_row + dr < self.grid.rows and
                           0 <= new_col + dc < self.grid.cols and
                           not self.position_occupied(new_row + dr, new_col + dc, current_state)):
                        new_row += dr
                        new_col += dc
                        move_cost += 1  # Each step costs 1

                    self.game.movement(new_row, new_col, i)

                    new_state = tuple(
                        (bt, pos)
                        for idx, (bt, pos) in enumerate(self.game.level_data[1])
                    )

                    if new_state not in visited:
                        heapq.heappush(priority_queue, 
                                       (cost + move_cost, new_state, path + [(i, (new_row, new_col))]))

        print("No solution found")
        return None
        

    def position_occupied(self, row, col, state):
        return any(pos == (row, col) for _, pos in state)

    def hill_climbing(self):
        print("Stage 1: Solving the game to find target positions.")
        initial_state = tuple((ball_type, (row, col)) for ball_type, (row, col) in self.game.level_data[1])

        bfs_solution = self.BFS()
        if bfs_solution is None:
            print("Unable to find an initial solution.")
            return None

        target_positions = {
            ball_type: (row, col) for ball_type, (row, col) in self.game.level_data[1]
        }
        print("Target positions established:", target_positions)

        print("Stage 2: Using hill climbing to optimize the path to target positions.")
        current_state = initial_state
        visited = set()
        visited.add(current_state)
        path = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        while True:
            self.game.level_data[1] = list(current_state)

            if all(pos == target_positions[ball_type] for ball_type, pos in current_state):
                print("Reached target positions:", current_state)
                return path

            neighbors = []

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
                        (bt, pos)
                        for idx, (bt, pos) in enumerate(self.game.level_data[1])
                    )

                    if new_state not in visited:
                        heuristic = self.evaluate_heuristic(new_state, target_positions)
                        neighbors.append((heuristic, new_state, (i, (new_row, new_col))))

                    # Restore the ball's position
                    self.game.level_data[1][i] = (ball_type, (row, col))

            if not neighbors:
                print("No better neighbors found, stopping and back to first sulotion.")
                self.BFS()
                return None

            neighbors.sort(reverse=True, key=lambda x: x[0])  # Sort by heuristic descending
            best_heuristic, best_state, best_move = neighbors[0]

            if best_heuristic <= self.evaluate_heuristic(current_state, target_positions) and self.game.win():
                print("Local maximum reached.",best_state)
                return None

            current_state = best_state
            visited.add(current_state)
            path.append(best_move)

    def evaluate_heuristic(self, state, target_positions):
        heuristic = 0
        for ball_type, (row, col) in state:
            if ball_type in target_positions:
                target_row, target_col = target_positions[ball_type]
                heuristic -= abs(row - target_row) + abs(col - target_col)  # Lower is better
        return heuristic
