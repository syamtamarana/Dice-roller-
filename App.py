# Dice-roller-
import tkinter as tk
import random
import time

# --- Config ---
SIZE = 200          # canvas size
MARGIN = 20         # margin around die
DIE_SIZE = SIZE - 2 * MARGIN
PIP = 18            # pip diameter

# Precomputed normalized pip positions (as fractions of DIE_SIZE)
POS = {
    "top_left": (0.25, 0.25),
    "top_center": (0.5, 0.25),
    "top_right": (0.75, 0.25),
    "middle_left": (0.25, 0.5),
    "center": (0.5, 0.5),
    "middle_right": (0.75, 0.5),
    "bottom_left": (0.25, 0.75),
    "bottom_center": (0.5, 0.75),
    "bottom_right": (0.75, 0.75),
}

# Mapping die face -> which positions to draw
FACE_MAP = {
    1: ["center"],
    2: ["top_left", "bottom_right"],
    3: ["top_left", "center", "bottom_right"],
    4: ["top_left", "top_right", "bottom_left", "bottom_right"],
    5: ["top_left", "top_right", "center", "bottom_left", "bottom_right"],
    6: ["top_left", "middle_left", "bottom_left", "top_right", "middle_right", "bottom_right"],
}

# --- Tkinter UI ---
root = tk.Tk()
root.title("Dice Roller")

canvas = tk.Canvas(root, width=SIZE, height=SIZE, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=8)

num_label = tk.Label(root, text="Roll the die!", font=("Helvetica", 16))
num_label.grid(row=1, column=0, sticky="w", padx=12)

def draw_die(n):
    """Draw the die square and the pips for face n (1..6)."""
    canvas.delete("all")
    # Draw background / die rectangle
    x0, y0 = MARGIN, MARGIN
    x1, y1 = MARGIN + DIE_SIZE, MARGIN + DIE_SIZE
    # Slightly rounded appearance using a rectangle with thicker border
    canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", width=4)
    # Draw pips
    for pos_key in FACE_MAP[n]:
        fx, fy = POS[pos_key]
        cx = x0 + fx * DIE_SIZE
        cy = y0 + fy * DIE_SIZE
        r = PIP / 2
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="black")

def roll_animation(final_callback=None):
    """Animate rolling and call final_callback(last_number) when done (optional)."""
    last = None
    # Quick animation: show a few random faces
    for _ in range(12):
        n = random.randint(1, 6)
        draw_die(n)
        num_label.config(text=str(n))
        root.update_idletasks()
        time.sleep(0.04)  # short pause for animation
        last = n
    # Final face
    final = random.randint(1, 6)
    draw_die(final)
    num_label.config(text=f"Result: {final}")
    if final_callback:
        final_callback(final)
    return final

def on_roll():
    roll_animation()

roll_btn = tk.Button(root, text="Roll", command=on_roll, font=("Helvetica", 12), width=10)
roll_btn.grid(row=1, column=1, sticky="e", padx=12)

# Bind Spacebar to roll
root.bind("<space>", lambda e: on_roll())

# Draw initial face (1)
draw_die(1)

root.mainloop()
