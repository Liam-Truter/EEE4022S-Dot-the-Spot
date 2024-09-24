from opentrons import robot, instruments, containers
import tkinter as tk

class Calibrator:
    def __init__(self):
        pass
    
    def start(self):
        self.root = tk.Tk()
        self.root.title("Opentrons Calibrator GUI")

        # Step sizes
        self.step_sizes = [0.1, 0.5, 1, 5, 10, 50]
        self.step_size_idx = 2
        self.step_size = self.step_sizes[self.step_size_idx]
        
        # Variable for radio button
        self.step_var = tk.IntVar()
        self.step_var.set(self.step_size_idx) # Default to starting step size

        # Key bindings
        self.root.bind('<Shift_L>', lambda event: self.increase_step())
        self.root.bind('<Control_L>', lambda event: self.decrease_step())
        self.root.bind('<w>', lambda event: self.move_forward())
        self.root.bind('<s>', lambda event: self.move_backward())
        self.root.bind('<a>', lambda event: self.move_left())
        self.root.bind('<d>', lambda event: self.move_right())
        self.root.bind('<e>', lambda event: self.move_up())
        self.root.bind('<q>', lambda event: self.move_down())

        # Step size radio button list
        self.step_selection = tk.Frame(self.root)
        self.step_selection.pack(pady=10)

        # Iterate through each step size
        for i in range(len(self.step_sizes)):
            # Step size label
            step_label = tk.Label(self.step_selection, text=str(self.step_sizes[i]))
            step_label.grid(row=0, column=i, padx=5)

            # Step size radio button
            step_radio = tk.Radiobutton(self.step_selection, variable=self.step_var, value=i, command=self.step_size_selected)
            step_radio.grid(row=1, column=i, padx=5)


        # Button dimensions
        btn_width = 5
        btn_height = 2

        # First set of arrow buttons (forward, backward, left, right)
        frame_fblr = tk.Frame(self.root)
        frame_fblr.pack(pady=10)

        btn_fwd = tk.Button(frame_fblr, text="↑", command=self.move_forward, width=btn_width, height=btn_height)
        btn_fwd.grid(row=0, column=1)

        btn_left = tk.Button(frame_fblr, text="←", command=self.move_left, width=btn_width, height=btn_height)
        btn_left.grid(row=1, column=0)

        btn_back = tk.Button(frame_fblr, text="↓", command=self.move_backward, width=btn_width, height=btn_height)
        btn_back.grid(row=1, column=1)

        btn_right = tk.Button(frame_fblr, text="→", command=self.move_right, width=btn_width, height=btn_height)
        btn_right.grid(row=1, column=2)

        # Second set of buttons (up and down)
        frame_ud = tk.Frame(self.root)
        frame_ud.pack(pady=10)

        btn_up = tk.Button(frame_ud, text="↑", command=self.move_up, width=btn_width, height=btn_height)
        btn_up.grid(row=0, column=0)

        btn_down = tk.Button(frame_ud, text="↓", command=self.move_down, width=btn_width, height=btn_height)
        btn_down.grid(row=1, column=0)

        self.root.mainloop()
    
    def increase_step(self):
        self.step_size_idx = min(len(self.step_sizes)-1,self.step_size_idx+1)
        self.step_size = self.step_sizes[self.step_size_idx]
        self.step_var.set(self.step_size_idx)

    def decrease_step(self):
        self.step_size_idx = max(0,self.step_size_idx-1)
        self.step_size = self.step_sizes[self.step_size_idx]
        self.step_var.set(self.step_size_idx)

    def step_size_selected(self):
        self.step_size_idx = self.step_var.get()
        self.step_size = self.step_sizes[self.step_size_idx]
    
    def move_forward(self):
        bot_pos = robot._driver.get_head_position()['current']['y']
        robot.move_head(y=bot_pos+self.step_size)
    
    def move_backward(self):
        bot_pos = robot._driver.get_head_position()['current']['y']
        robot.move_head(y=bot_pos-self.step_size)
    
    def move_left(self):
        bot_pos = robot._driver.get_head_position()['current']['x']
        robot.move_head(x=bot_pos-self.step_size)

    def move_right(self):
        bot_pos = robot._driver.get_head_position()['current']['x']
        robot.move_head(x=bot_pos+self.step_size)

    def move_up(self):
        bot_pos = robot._driver.get_head_position()['current']['z']
        robot.move_head(z=bot_pos+self.step_size)

    def move_down(self):
        bot_pos = robot._driver.get_head_position()['current']['z']
        robot.move_head(z=bot_pos-self.step_size)

def main():
    calibrator = Calibrator()
    robot.connect(robot.get_serial_ports_list()[0])
    robot.home()
    print(robot._driver.get_position())
    calibrator.start()
    print("Restarting calibrator")
    calibrator.start()
    

if __name__ == '__main__':
    main()