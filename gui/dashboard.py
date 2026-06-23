import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import config
from services.city_service import get_all_cities, get_city_coordinates
from services.haversine import haversine
from services.transport import calculate_transport, save_search
from services.recommendation import recommend_transport
from gui.results import ResultsWindow
from graphs.plots import plot_fares
 
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
 
class Dashboard:
    def __init__(self, root, user_id=None, username=None):
        self.root = root
        self.user_id = user_id
        self.username = username or "Traveler"
        self.root.title(f"{config.APP_TITLE} - Travel Planner Dashboard")
        self.root.geometry("950x650")
        self.root.configure(bg=config.BG_MAIN)
        
        # Configure ttk style for Dark Theme
        self.setup_styles()
 
        # Top Control/Header Bar - Logo only, no text title
        header = tk.Frame(self.root, bg=config.BG_CARD, height=90)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
 
        # Logo in header (large, preserving aspect ratio)
        self._load_header_logo(header, max_size=(130, 130))
 
        welcome_text = f"Logged in as: {self.username}"
        user_label = tk.Label(
            header,
            text=welcome_text,
            font=config.FONT_SMALL,
            bg=config.BG_CARD,
            fg=config.TEXT_MUTED
        )
        user_label.pack(side="right", padx=(0, 20))
        
        logout_btn = tk.Button(
            header,
            text="Logout",
            font=config.FONT_SMALL,
            bg=config.DANGER,
            fg=config.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=10,
            command=self.logout
        )
        logout_btn.pack(side="right", padx=10)
 
        # Content frame
        content = tk.Frame(self.root, bg=config.BG_MAIN, padx=20, pady=20)
        content.pack(expand=True, fill="both")
 
        # Corrected Frame Container
        input_container = tk.Frame(content, bg=config.BG_CARD, padx=20, pady=20)
        input_container.pack(fill="x", pady=(0, 20))
 
        tk.Label(
            input_container,
            text="Departure City",
            font=config.FONT_BODY,
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT
        ).grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
 
        cities = get_all_cities()
        self.departure = ttk.Combobox(
            input_container,
            values=cities,
            width=25,
            font=config.FONT_BODY,
            state="readonly"
        )
        self.departure.grid(row=0, column=1, padx=(0, 20), pady=10)
 
        tk.Label(
            input_container,
            text="Destination City",
            font=config.FONT_BODY,
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT
        ).grid(row=0, column=2, padx=(0, 10), pady=10, sticky="w")
 
        self.destination = ttk.Combobox(
            input_container,
            values=cities,
            width=25,
            font=config.FONT_BODY,
            state="readonly"
        )
        self.destination.grid(row=0, column=3, padx=(0, 20), pady=10)
 
        # Action Buttons Container
        btn_frame = tk.Frame(input_container, bg=config.BG_CARD)
        btn_frame.grid(row=0, column=4, padx=(10, 0), pady=10)
 
        calc_btn = tk.Button(
            btn_frame,
            text="Calculate Route",
            font=("Segoe UI", 11, "bold"),
            bg=config.ACCENT,
            fg=config.BG_MAIN,
            activebackground=config.ACCENT2,
            activeforeground=config.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=self.calculate
        )
        calc_btn.pack(side="left", padx=5)
 
        self.plot_btn = tk.Button(
            btn_frame,
            text="Compare Fares",
            font=("Segoe UI", 11, "bold"),
            bg=config.ACCENT2,
            fg=config.TEXT_LIGHT,
            activebackground=config.ACCENT,
            activeforeground=config.BG_MAIN,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5,
            command=self.show_fares_plot,
            state="disabled"  # Disabled initially until a search is run
        )
        self.plot_btn.pack(side="left", padx=5)
 
        # Table Container
        table_frame = tk.Frame(content, bg=config.BG_CARD, padx=15, pady=15)
        table_frame.pack(expand=True, fill="both")
 
        table_title = tk.Label(
            table_frame,
            text="Available Transport Options",
            font=config.FONT_HEADER,
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT,
            anchor="w"
        )
        table_title.pack(fill="x", pady=(0, 10))
 
        columns = ("Company", "Fare", "Time", "Comfort", "Safety")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=150)
        self.tree.pack(fill="both", expand=True)
 
        self.last_results = []
 
    def _load_header_logo(self, parent, max_size=(160, 140)):
        """
        Load and display the logo in the header bar, preserving aspect ratio.
        The image will scale to fit within max_size (width, height) without distortion.
        Silently skips if file not found.
        """
        try:
            img = Image.open(LOGO_PATH).convert("RGBA")
 
            # --- Aspect-ratio-preserving resize ---
            max_w, max_h = max_size
            orig_w, orig_h = img.size
 
            scale = min(max_w / orig_w, max_h / orig_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)
 
            img = img.resize((new_w, new_h), Image.LANCZOS)
            # --------------------------------------
 
            self._header_logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(
                parent,
                image=self._header_logo_img,
                bg=config.BG_CARD,
                bd=0
            )
            logo_label.pack(side="left", padx=(12, 0), pady=10)
        except Exception as e:
            print(f"Header logo not loaded: {e}")
 
    def setup_styles(self):
        style = ttk.Style()
        # Use a style base that is highly configurable
        style.theme_use("clam")
        
        # Configure Table/Treeview styles matching our dark theme
        style.configure(
            "Custom.Treeview",
            background=config.BG_CARD,
            foreground=config.TEXT_LIGHT,
            fieldbackground=config.BG_CARD,
            rowheight=30,
            font=config.FONT_BODY,
            borderwidth=0
        )
        
        style.configure(
            "Custom.Treeview.Heading",
            background=config.BG_INPUT,
            foreground=config.TEXT_LIGHT,
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            relief="flat"
        )
        # Map selection and active colors
        style.map(
            "Custom.Treeview",
            background=[("selected", config.ACCENT2)],
            foreground=[("selected", config.TEXT_LIGHT)]
        )
        
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", config.ACCENT), ("pressed", config.ACCENT2)],
            foreground=[("active", config.BG_MAIN)]
        )
 
    def calculate(self):
        dep = self.departure.get()
        des = self.destination.get()
        if not dep or not des:
            messagebox.showerror("Error", "Please select departure and destination cities.")
            return
        if dep == des:
            messagebox.showerror("Error", "Select different cities.")
            return
        lat1, lon1 = get_city_coordinates(dep)
        lat2, lon2 = get_city_coordinates(des)
        distance = haversine(lat1, lon1, lat2, lon2)
        results = calculate_transport(distance)
        self.last_results = results
        # Save history in background database log
        save_search(self.user_id, dep, des, distance)
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Populate rows
        for row in results:
            self.tree.insert(
                "",
                "end",
                values=(
                    row["company"],
                    f"Rs. {row['fare']:,}",
                    f"{row['time']} hours",
                    f"{row['comfort']}/10",
                    f"{row['safety']}/10"
                )
            )
        # Enable plot button
        self.plot_btn.config(state="normal")
        # Open detailed results modal
        ResultsWindow(results, distance)
 
    def show_fares_plot(self):
        if self.last_results:
            plot_fares(self.last_results)
 
    def logout(self):
        self.root.destroy()
        new_root = tk.Tk()
        from gui.login_ui import LoginUI
        LoginUI(new_root)
        new_root.mainloop()