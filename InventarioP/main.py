import os
import sys
import customtkinter as tk


project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)


from gui.product_gui import ProductGUI

def main():

    root = tk.CTk()
    app = ProductGUI(root)
    app.run()

if __name__ == "__main__":
    main()
