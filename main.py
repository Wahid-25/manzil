import tkinter as tk
import sys
import os
# Add the project root directory to the python path to resolve submodules cleanly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from gui.login_ui import LoginUI
def main():
    root = tk.Tk()
    # Apply initial main window configuration
    root.iconify()  # Hide briefly during loading setup
    root.deiconify()
    
    # Initialize the Login interface
    LoginUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()