import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import config
from auth.login import login_user
from gui.dashboard import Dashboard
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{config.APP_TITLE} - Login")
        self.root.geometry("500x730")
        self.root.configure(bg=config.BG_MAIN)
        self.root.resizable(False, False)
        # Main Card container
        card = tk.Frame(self.root, bg=config.BG_CARD, padx=30, pady=20, bd=0)
        card.pack(expand=True, fill="both", padx=20, pady=20)
        # Logo Image
        self._load_logo(card, size=(200, 150))
        # Title Label
        title_label = tk.Label(
            card,
            text=config.APP_TITLE.upper(),
            font=config.FONT_TITLE,
            bg=config.BG_CARD,
            fg=config.ACCENT
        )
        title_label.pack(pady=(4, 0))
        subtitle_label = tk.Label(
            card,
            text="Travel With AI",
            font=config.FONT_SMALL,
            bg=config.BG_CARD,
            fg=config.TEXT_MUTED
        )
        subtitle_label.pack(pady=(0, 14))
        # Username Input
        username_label = tk.Label(
            card,
            text="Username",
            font=config.FONT_BODY,
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT,
            anchor="w"
        )
        username_label.pack(fill="x", pady=(5, 2))
        self.username = tk.Entry(
            card,
            font=config.FONT_BODY,
            bg=config.BG_INPUT,
            fg=config.TEXT_LIGHT,
            insertbackground=config.TEXT_LIGHT,
            relief="flat",
            bd=5
        )
        self.username.pack(fill="x", pady=(0, 12))
        # Password Input
        password_label = tk.Label(
            card,
            text="Password",
            font=config.FONT_BODY,
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT,
            anchor="w"
        )
        password_label.pack(fill="x", pady=(5, 2))
        self.password = tk.Entry(
            card,
            show="*",
            font=config.FONT_BODY,
            bg=config.BG_INPUT,
            fg=config.TEXT_LIGHT,
            insertbackground=config.TEXT_LIGHT,
            relief="flat",
            bd=5
        )
        self.password.pack(fill="x", pady=(0, 18))
        # Login Button
        login_btn = tk.Button(
            card,
            text="Login",
            font=("Segoe UI", 12, "bold"),
            bg=config.ACCENT,
            fg=config.BG_MAIN,
            activebackground=config.ACCENT2,
            activeforeground=config.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=self.login,
            pady=6
        )
        login_btn.pack(fill="x", pady=(0, 12))
        # Register Toggle Link
        register_link = tk.Label(
            card,
            text="Don't have an account? Register Here",
            font=("Segoe UI", 11, "underline"),
            bg=config.BG_CARD,
            fg=config.ACCENT2,
            cursor="hand2"
        )
        register_link.pack(pady=(8, 0))
        register_link.bind("<Button-1>", lambda e: self.go_to_register())
        register_link.bind("<Enter>", lambda e: register_link.config(fg=config.ACCENT))
        register_link.bind("<Leave>", lambda e: register_link.config(fg=config.ACCENT2))
    def _load_logo(self, parent, size=(110, 110)):
        """Load and display the logo image. Silently skips if file not found."""
        try:
            img = Image.open(LOGO_PATH).convert("RGBA")
            img = img.resize(size, Image.LANCZOS)
            self._logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(
                parent,
                image=self._logo_img,
                bg=config.BG_CARD,
                bd=0
            )
            logo_label.pack(pady=(0, 2))
        except Exception as e:
            print(f"Logo not loaded: {e}")
    def login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        user_id = login_user(username, password)
        if user_id:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.root.destroy()
            # Open Dashboard
            new_root = tk.Tk()
            Dashboard(new_root, user_id=user_id, username=username)
            new_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    def go_to_register(self):
        self.root.destroy()
        new_root = tk.Tk()
        from gui.register_ui import RegisterUI
        RegisterUI(new_root)
        new_root.mainloop()