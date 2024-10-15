import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from data_loader import load_cities, load_adjacencies
from algorithms import bfs, dfs, id_dfs, best_first_search, a_star, haversine_distance
from map_utils import create_map

class RouteFindingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Route Finding Program")
        master.geometry("1200x800")  # Increased window size for better map visibility

        self.solution_path = None  # Store the current solution path
        self.panning = False
        self.last_x = 0
        self.last_y = 0

        try:
            self.graph = self.load_data()
            self.create_widgets()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            master.destroy()

    def load_data(self):
        try:
            graph = load_cities('coordinates.csv')
            load_adjacencies('Adjacencies.txt', graph)
            return graph
        except FileNotFoundError as e:
            raise Exception(f"Could not find file: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def create_widgets(self):
        # Create a frame for the controls
        control_frame = ttk.Frame(self.master)
        control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # City selection
        ttk.Label(control_frame, text="Start City:").grid(row=0, column=0, padx=5, pady=5)
        self.start_city = ttk.Combobox(control_frame, values=list(self.graph.cities.keys()))
        self.start_city.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(control_frame, text="Goal City:").grid(row=1, column=0, padx=5, pady=5)
        self.goal_city = ttk.Combobox(control_frame, values=list(self.graph.cities.keys()))
        self.goal_city.grid(row=1, column=1, padx=5, pady=5)

        # Algorithm selection
        ttk.Label(control_frame, text="Search Algorithm:").grid(row=2, column=0, padx=5, pady=5)
        self.algorithm = ttk.Combobox(control_frame, values=["BFS", "DFS", "ID-DFS", "Best-First Search", "A* Search"])
        self.algorithm.grid(row=2, column=1, padx=5, pady=5)

        # Search button
        ttk.Button(control_frame, text="Find Route", command=self.find_route).grid(row=3, column=0, columnspan=2, pady=10)

        # Results display
        self.result_text = tk.Text(control_frame, height=10, width=50)
        self.result_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Create a frame for the map
        self.map_frame = ttk.Frame(self.master)
        self.map_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Initial map display
        self.create_map()

        # Configure grid
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

    def create_map(self):
        # Clear the map frame
        for widget in self.map_frame.winfo_children():
            widget.destroy()

        # Create a new figure and canvas
        self.fig = create_map(self.graph, self.solution_path)
        self.map_canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.map_canvas.draw()
        self.map_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add toolbar
        self.toolbar = NavigationToolbar2Tk(self.map_canvas, self.map_frame)
        self.toolbar.update()

        # Bind the scroll event to the zoom function
        self.map_canvas.get_tk_widget().bind('<MouseWheel>', self.zoom)  # For Windows
        self.map_canvas.get_tk_widget().bind('<Button-4>', self.zoom)  # For Linux (scroll up)
        self.map_canvas.get_tk_widget().bind('<Button-5>', self.zoom)  # For Linux (scroll down)

        # Bind middle mouse button events for panning
        self.map_canvas.get_tk_widget().bind('<Button-2>', self.start_pan)  # Middle mouse button press
        self.map_canvas.get_tk_widget().bind('<B2-Motion>', self.pan)  # Middle mouse button drag
        self.map_canvas.get_tk_widget().bind('<ButtonRelease-2>', self.stop_pan)  # Middle mouse button release

    def find_route(self):
        start = self.start_city.get()
        goal = self.goal_city.get()
        algorithm = self.algorithm.get()

        if not start or not goal or not algorithm:
            messagebox.showerror("Error", "Please select start city, goal city, and algorithm.")
            return

        search_function = {
            "BFS": bfs,
            "DFS": dfs,
            "ID-DFS": lambda g, s, e: id_dfs(g, s, e, max_depth=20),
            "Best-First Search": best_first_search,
            "A* Search": a_star
        }.get(algorithm)

        start_time = time.time()
        path = search_function(self.graph, start, goal)
        end_time = time.time()

        self.result_text.delete(1.0, tk.END)
        if path:
            route = ' -> '.join(path)
            time_taken = end_time - start_time
            total_distance = sum(haversine_distance(self.graph.cities[path[i]], self.graph.cities[path[i+1]]) 
                                 for i in range(len(path)-1))
            
            result = f"Route found: {route}\n"
            result += f"Time taken: {time_taken:.4f} seconds\n"
            result += f"Total distance: {total_distance:.2f} km"
            
            self.result_text.insert(tk.END, result)

            # Update the solution_path and redraw the map
            self.solution_path = path
            self.create_map()
        else:
            self.result_text.insert(tk.END, "No route found.")
            # Clear the solution path from the map
            self.solution_path = None
            self.create_map()

    def zoom(self, event):
        # Get the current axis limits
        ax = self.fig.gca()
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        # Set the zoom factor
        zoom_factor = 1.1

        # Determine the direction of zoom based on the scroll direction
        if event.num == 5 or event.delta == -120:  # Scroll down or away
            zoom_factor = 1 / zoom_factor

        # Calculate new axis limits
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        new_width = (x_max - x_min) * zoom_factor
        new_height = (y_max - y_min) * zoom_factor

        # Set new axis limits
        ax.set_xlim(x_center - new_width / 2, x_center + new_width / 2)
        ax.set_ylim(y_center - new_height / 2, y_center + new_height / 2)

        # Redraw the canvas
        self.map_canvas.draw()

    def start_pan(self, event):
        self.panning = True
        self.last_x = event.x
        self.last_y = event.y

    def pan(self, event):
        if self.panning:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            
            ax = self.fig.gca()
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            
            # Calculate the range of x and y
            x_range = x_max - x_min
            y_range = y_max - y_min
            
            # Calculate the shift based on the pixel movement and axis range
            x_shift = -dx * x_range / self.fig.get_figwidth() / self.fig.dpi
            y_shift = dy * y_range / self.fig.get_figheight() / self.fig.dpi
            
            # Update the axis limits
            ax.set_xlim(x_min + x_shift, x_max + x_shift)
            ax.set_ylim(y_min + y_shift, y_max + y_shift)
            
            self.map_canvas.draw()
            
            self.last_x = event.x
            self.last_y = event.y

    def stop_pan(self, event):
        self.panning = False