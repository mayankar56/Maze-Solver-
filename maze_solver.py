import tkinter as tk
from tkinter import messagebox
import heapq
import random

CELL_SIZE = 35
ROWS, COLS = 15, 15

# Color theme
WALL_COLOR = "#2c3e50"
START_COLOR = "#27ae60"
END_COLOR = "#e74c3c"
PATH_COLOR = "#3498db"
GRID_COLOR = "#ecf0f1"
BG_COLOR = "#bdc3c7"

class MazeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Maze Solver - Dijkstra’s Algorithm")
        self.root.configure(bg=BG_COLOR)

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg=GRID_COLOR, highlightthickness=0)
        self.canvas.pack(pady=10)

        self.maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.rects = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.start = None
        self.end = None

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)

        control_frame = tk.Frame(root, bg=BG_COLOR)
        control_frame.pack(pady=10)

        self.create_styled_button(control_frame, "🧠 Solve Maze", self.solve_maze).pack(side=tk.LEFT, padx=8)
        self.create_styled_button(control_frame, "🔄 Reset Maze", self.reset_maze).pack(side=tk.LEFT, padx=8)

        info = tk.Label(control_frame, text="Left Click: Wall | Right Click: Start → End", bg=BG_COLOR, font=("Segoe UI", 10))
        info.pack(side=tk.LEFT, padx=10)

        self.show_instructions()  # Show multi-step popup instructions

    def show_instructions(self):
        steps = [
            "👋 Welcome to Maze Solver!",
            "🖱 Left Click: Add wall blocks",
            "🖱 Right Click: Set Start and End points (in that order)",
            "🧱 Random walls are auto-generated after setting the start point",
            "🧠 Click 'Solve Maze' to find the shortest path using Dijkstra’s Algorithm",
            "🔄 Click 'Reset Maze' to start over",
            "🎯 Tip: You can reset anytime to try new maze patterns!",
            "✅ Ready? Let's build and solve your maze! 🧩"
        ]
        for step in steps:
            messagebox.showinfo("Instructions", step)

    def create_styled_button(self, frame, text, command):
        return tk.Button(frame, text=text, command=command,
                         bg="#34495e", fg="white", activebackground="#2c3e50",
                         activeforeground="white", font=("Segoe UI", 11, "bold"),
                         bd=0, relief="flat", padx=15, pady=6, cursor="hand2")

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                x1, y1 = col * CELL_SIZE, row * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="#bdc3c7", fill=GRID_COLOR)
                self.rects[row][col] = rect

    def left_click(self, event):
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if self.maze[row][col] == 0 and (row, col) != self.start and (row, col) != self.end:
            self.maze[row][col] = 1
            self.canvas.itemconfig(self.rects[row][col], fill=WALL_COLOR)

    def right_click(self, event):
        row, col = event.y // CELL_SIZE, event.x // CELL_SIZE
        if not self.start:
            self.start = (row, col)
            self.canvas.itemconfig(self.rects[row][col], fill=START_COLOR)
            self.generate_random_walls()
        elif not self.end:
            if (row, col) == self.start:
                return
            self.end = (row, col)
            self.canvas.itemconfig(self.rects[row][col], fill=END_COLOR)

    def generate_random_walls(self, density=0.25):
        wall_count = int(ROWS * COLS * density)
        placed = 0
        while placed < wall_count:
            r = random.randint(0, ROWS - 1)
            c = random.randint(0, COLS - 1)
            if (r, c) != self.start and (r, c) != self.end and self.maze[r][c] == 0:
                self.maze[r][c] = 1
                self.canvas.itemconfig(self.rects[r][c], fill=WALL_COLOR)
                placed += 1

    def reset_maze(self):
        self.maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.start = None
        self.end = None
        for row in range(ROWS):
            for col in range(COLS):
                self.canvas.itemconfig(self.rects[row][col], fill=GRID_COLOR)

    def solve_maze(self):
        if not self.start or not self.end:
            messagebox.showwarning("Missing Points", "Please set both start and end points first!")
            return

        path = self.dijkstra(self.maze, self.start, self.end)
        if path:
            for (r, c) in path[1:-1]:
                self.canvas.itemconfig(self.rects[r][c], fill=PATH_COLOR)
        else:
            messagebox.showinfo("No Path", "No path could be found!")

    def dijkstra(self, maze, start, end):
        rows, cols = len(maze), len(maze[0])
        dist = [[float('inf')] * cols for _ in range(rows)]
        dist[start[0]][start[1]] = 0
        prev = [[None] * cols for _ in range(rows)]
        pq = [(0, start)]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while pq:
            d, (x, y) = heapq.heappop(pq)
            if (x, y) == end:
                break
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:
                    new_dist = d + 1
                    if new_dist < dist[nx][ny]:
                        dist[nx][ny] = new_dist
                        prev[nx][ny] = (x, y)
                        heapq.heappush(pq, (new_dist, (nx, ny)))

        path = []
        x, y = end
        if dist[x][y] == float('inf'):
            return None
        while (x, y) != start:
            path.append((x, y))
            x, y = prev[x][y]
        path.append(start)
        path.reverse()
        return path

# Run the GUI app
root = tk.Tk()
app = MazeSolverApp(root)
root.mainloop()
