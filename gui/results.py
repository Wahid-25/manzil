import tkinter as tk
from tkinter import ttk
import config
from services.recommendation import recommend_transport
from graphs.plots import plot_fares
class ResultsWindow:
    def __init__(self, results, distance):
        self.results = results
        self.window = tk.Toplevel()
        self.window.title("Travel Route Analysis")
        self.window.geometry("820x540")
        self.window.configure(bg=config.BG_MAIN)
        self.window.transient()  # Keep on top of main window
        self.window.grab_set()   # Focus modal
        # Title/Distance Display
        title_frame = tk.Frame(self.window, bg=config.BG_CARD, pady=15)
        title_frame.pack(fill="x")
        
        tk.Label(
            title_frame,
            text=f"ROUTE ANALYSIS RESULTS",
            font=config.FONT_HEADER,
            bg=config.BG_CARD,
            fg=config.ACCENT
        ).pack()
        tk.Label(
            title_frame,
            text=f"Total Distance: {distance} KM",
            font=config.FONT_BODY,
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT
        ).pack()
        # Recommendation Cards Frame
        recommend_frame = tk.Frame(self.window, bg=config.BG_MAIN, pady=10)
        recommend_frame.pack(fill="x", padx=15)
        cheapest, fastest, best_balanced = recommend_transport(results)
        # Draw recommendations in nice themed labels
        if cheapest and fastest and best_balanced:
            self.create_card(recommend_frame, "CHEAPEST", cheapest, config.SUCCESS, 0)
            self.create_card(recommend_frame, "FASTEST", fastest, config.ACCENT2, 1)
            self.create_card(recommend_frame, "RECOMMENDED", best_balanced, config.WARNING, 2)
        # Treeview Comparison Table
        table_frame = tk.Frame(self.window, bg=config.BG_CARD, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(5, 10))
        columns = ("Company", "Fare", "Travel Time", "Comfort", "Safety")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=120)
        tree.pack(fill="both", expand=True)
        for item in results:
            tree.insert(
                "",
                "end",
                values=(
                    item["company"],
                    f"Rs. {item['fare']:,}",
                    f"{item['time']} hours",
                    f"{item['comfort']}/10",
                    f"{item['safety']}/10"
                )
            )
        # Action Buttons
        btn_frame = tk.Frame(self.window, bg=config.BG_MAIN, pady=10)
        btn_frame.pack(fill="x")
        plot_btn = tk.Button(
            btn_frame,
            text="Plot Fare Comparison",
            font=("Segoe UI", 11, "bold"),
            bg=config.ACCENT,
            fg=config.BG_MAIN,
            activebackground=config.ACCENT2,
            activeforeground=config.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=5,
            command=self.plot
        )
        plot_btn.pack(side="left", padx=15)
        close_btn = tk.Button(
            btn_frame,
            text="Close Results",
            font=("Segoe UI", 11, "bold"),
            bg=config.BG_CARD,
            fg=config.TEXT_MUTED,
            activebackground=config.DANGER,
            activeforeground=config.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=5,
            command=self.window.destroy
        )
        close_btn.pack(side="right", padx=15)
    def create_card(self, parent, label_text, option, accent_color, col_num):
        card = tk.Frame(parent, bg=config.BG_CARD, bd=1, relief="flat", padx=10, pady=10)
        card.grid(row=0, column=col_num, sticky="nsew", padx=5)
        parent.grid_columnconfigure(col_num, weight=1)
        tk.Label(
            card,
            text=label_text,
            font=("Segoe UI", 9, "bold"),
            bg=config.BG_CARD,
            fg=accent_color
        ).pack(anchor="w")
        tk.Label(
            card,
            text=option["company"],
            font=("Segoe UI", 13, "bold"),
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT
        ).pack(anchor="w", pady=(2, 2))
        details = f"Rs. {option['fare']:,} | {option['time']}h"
        tk.Label(
            card,
            text=details,
            font=config.FONT_SMALL,
            bg=config.BG_CARD,
            fg=config.TEXT_MUTED
        ).pack(anchor="w")
    def plot(self):
        plot_fares(self.results)