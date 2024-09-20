import tkinter as tk

# Callback functions
def increase_step():
    global step_size_idx
    global step_size
    step_size_idx = min(len(step_sizes)-1,step_size_idx+1)
    step_size = step_sizes[step_size_idx]

def decrease_step():
    global step_size_idx
    global step_size
    step_size_idx = max(0,step_size_idx-1)
    step_size = step_sizes[step_size_idx]

def step_scaled(step):
    global step_size_idx
    global step_size
    step_size_idx = int(step)
    step_size = step_sizes[step_size_idx]

def move_forward():
    print(f"Moving forward {step_size} mm")

def move_backward():
    print(f"Moving backward {step_size} mm")

def move_left():
    print(f"Moving left {step_size} mm")

def move_right():
    print(f"Moving right {step_size} mm")

def move_up():
    print(f"Moving up {step_size} mm")

def move_down():
    print(f"Moving down {step_size} mm")

def bind_keys():
    root.bind('<Shift_L>', lambda event: increase_step())
    root.bind('<Control_L>', lambda event: decrease_step())
    root.bind('<w>', lambda event: move_forward())
    root.bind('<s>', lambda event: move_backward())
    root.bind('<a>', lambda event: move_left())
    root.bind('<d>', lambda event: move_right())
    root.bind('<e>', lambda event: move_up())
    root.bind('<q>', lambda event: move_down())

# Create the main window
root = tk.Tk()
root.title("Test Calibration Interface")

# Step sizes
step_sizes = [0.1, 0.5, 1, 5, 10, 50]
step_size_idx = 2
step_size = step_sizes[step_size_idx]

# Bind keys
bind_keys()

step_scale = tk.Scale(root, from_=0, to=len(step_sizes)-1, orient=tk.HORIZONTAL, command=step_scaled)
step_scale.pack(pady=20)

# Button dimensions
btn_width = 5
btn_height = 2

# First set of arrow buttons (forward, backward, left, right)
frame_fblr = tk.Frame(root)
frame_fblr.pack(pady=10)

btn_fwd = tk.Button(frame_fblr, text="↑", command=move_forward, width=btn_width, height=btn_height)
btn_fwd.grid(row=0, column=1)

btn_left = tk.Button(frame_fblr, text="←", command=move_left, width=btn_width, height=btn_height)
btn_left.grid(row=1, column=0)

btn_back = tk.Button(frame_fblr, text="↓", command=move_backward, width=btn_width, height=btn_height)
btn_back.grid(row=1, column=1)

btn_right = tk.Button(frame_fblr, text="→", command=move_right, width=btn_width, height=btn_height)
btn_right.grid(row=1, column=2)

# Second set of buttons (up and down)
frame_ud = tk.Frame(root)
frame_ud.pack(pady=10)

btn_up = tk.Button(frame_ud, text="↑", command=move_up, width=btn_width, height=btn_height)
btn_up.grid(row=0, column=0)

btn_down = tk.Button(frame_ud, text="↓", command=move_down, width=btn_width, height=btn_height)
btn_down.grid(row=1, column=0)

# Start the GUI loop
root.mainloop()