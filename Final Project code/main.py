import tkinter as tk
from volunteer_app import VolunteerApp

def main():
    root = tk.Tk()
    app = VolunteerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
