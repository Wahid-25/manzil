import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import config
from auth.register import register_user
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
class RegisterUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{config.APP_TITLE} - Register")
        self.root.geometry("400x600")
        self.root.configure(bg=config.BG_MAIN)
        self.root.resizable(False, False)
        # Main Card container
        card = tk.Frame(self.root, bg=config.BG_CARD, padx=30, pady=18, bd=0)
        card.pack(expand=True, fill="both", padx=20, pady=20)
        # Logo Image (smaller on register screen to save space)
        self._load_logo(card, size=(70, 70))
        # Title Label
        title_label = tk.Label(
            card,
            text="CREATE ACCOUNT",
            font=config.FONT_TITLE,
            bg=config.BG_CARD,
            fg=config.ACCENT
        )
        title_label.pack(pady=(4, 0))
        subtitle_label = tk.Label(
            card,
            text="Join Manzil – Travel With AI",
            font=config.FONT_SMALL,
            bg=config.BG_CARD,
            fg=config.TEXT_MUTED
        )
        subtitle_label.pack(pady=(0, 10))
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
        self.username.pack(fill="x", pady=(0, 10))
        # Email Input
        email_label = tk.Label(
            card,
            text="Email Address",
            font=config.FONT_BODY,
            bg=config.BG_CARD,
            fg=config.TEXT_LIGHT,
            anchor="w"
        )
        email_label.pack(fill="x", pady=(5, 2))
        self.email = tk.Entry(
            card,
            font=config.FONT_BODY,
            bg=config.BG_INPUT,
            fg=config.TEXT_LIGHT,
            insertbackground=config.TEXT_LIGHT,
            relief="flat",
            bd=5
        )
        self.email.pack(fill="x", pady=(0, 10))
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
        # Register Button
        register_btn = tk.Button(
            card,
            text="Register",
            font=("Segoe UI", 12, "bold"),
            bg=config.ACCENT,
            fg=config.BG_MAIN,
            activebackground=config.ACCENT2,
            activeforeground=config.TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=self.register,
            pady=6
        )
        register_btn.pack(fill="x", pady=(0, 12))
        # Login Toggle Link
        login_link = tk.Label(
            card,
            text="Already have an account? Log In",
            font=("Segoe UI", 11, "underline"),
            bg=config.BG_CARD,
            fg=config.ACCENT2,
            cursor="hand2"
        )
        login_link.pack(pady=(8, 0))
        login_link.bind("<Button-1>", lambda e: self.go_to_login())
        login_link.bind("<Enter>", lambda e: login_link.config(fg=config.ACCENT))
        login_link.bind("<Leave>", lambda e: login_link.config(fg=config.ACCENT2))
    def _load_logo(self, parent, size=(70, 70)):
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
    def register(self):
        username = self.username.get().strip()
        email = self.email.get().strip()
        password = self.password.get()
        if not username or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        success = register_user(username, email, password)
        if success:
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.go_to_login()
        else:
            messagebox.showerror("Error", "Registration failed. Username or email might already be taken.")
    def go_to_login(self):
        self.root.destroy()
        new_root = tk.Tk()
        from gui.login_ui import LoginUI
        LoginUI(new_root)
        new_root.mainloop()