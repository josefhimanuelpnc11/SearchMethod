import tkinter as tk
from gui import RouteFindingGUI

def main():
    root = tk.Tk()
    gui = RouteFindingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()