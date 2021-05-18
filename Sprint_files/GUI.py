import tkinter as tk
# import serial

# from move_car_auto import car_move_auto
from move_car_auto import car_move_auto, car_move ,terminate
STOP = '0'
# from move_car import car_move

LEFT = 'a'
RIGHT = 'd'
FORWARD = 'w'
BACKWARD = 's'
ERROR = 'e'
O_UP = (0, -1)
O_DOWN = (0, 1)
O_LEFT = (-1, 0)
O_RIGHT = (1, 0)
SIZE = 8
START = (0, SIZE - 1)
DIRS = [O_UP, O_LEFT, O_DOWN, O_RIGHT]
TIMES = {LEFT: 0.9, RIGHT: 1.1, FORWARD: 0.5, BACKWARD: 0.5, ERROR: 0.05}
ROUTES = {'1':[('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05)]
            ,'2':[('d', 1.1), ('w', 0.6), ('d', 0.05), ('w', 0.6), ('d', 0.05), ('w', 0.6), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05)]
            ,'3':[('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05)]
          ,'4':[('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05)]
            ,'5':[('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.6), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05), ('d', 1.1), ('w', 0.5), ('d', 0.05)]
            ,'6':[('d', 1.2), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('a', 0.9), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05), ('w', 0.5), ('d', 0.05)]

          }

class GUI:
    def __init__(self):
        self.last_place = START
        self.orientation = O_UP
        self.move_list = []
        self.root = tk.Tk()
        self.root.title("Kaplan's Killing Machine")
        self.reset = tk.Button(master=self.root, text="Reset Path", command=self.reset_press)
        self.reset.pack()
        self.move_label = tk.Label(master=self.root, text="")
        self.move_label.pack()
        self.grid_frame = tk.Frame(master=self.root, background="red")
        self.grid_frame.pack()
        self.send = tk.Button(master=self.root, text="GO!", command=self.send)
        self.send.pack()
        self.terminate = tk.Button(master=self.root,text="STOP",foreground="red",command=self.terminate_pressed)
        self.terminate.pack()
        l = SIZE
        for i in range(l):
            for j in range(l):
                button = tk.Button(master=self.grid_frame, text=i * l + j, background="lightgrey")
                y = 5 * int(int(l / 2) == i)
                x = 5 * int(int(l / 2) == j)
                button.grid(column=j, row=i, sticky=tk.NSEW, pady=(y, 0), padx=(x, 0))
                button.config(font=("Courier", 28))
                button.bind("<Button-1>", self.left_click(button))
                button.bind("<Button-3>", self.right_click(button))
                if (j, i) == START:
                    button.config(background="purple")

        self.root.mainloop()

    def terminate_pressed(self):
        terminate()
        self.root.destroy()

    def reset_press(self):
        self.last_place = START
        self.move_list = []
        self.move_label["text"] = "PATH HAS BEEN RESET"
        for widget in self.grid_frame.winfo_children():
            if widget["background"] != "purple":
                widget.config(background="lightgrey")

    def send(self):
        ins = [(item, TIMES[item]) for item in self.move_list]
        # print(ins)
        i = 0
        while i < len(ins):
            if ins[i][0] == FORWARD:
                ins.insert(i + 1, (RIGHT, TIMES[ERROR]))
            i += 1
        print(ins)
        # ins = [('w', 1)] + ins
        car_move_auto(ins)  # TODO: uncomment this :)

    def left_click(self, button):
        def inner(e):
            bg = button["background"]
            if bg == "lightgrey":
                button.config(background="green")
            elif bg == "red":
                button.config(background="lightgrey")
            # elif bg == "blue":
            #     button.config(background="green")
            elif bg == "green":
                button.config(background="red")

        return inner

    def right_click(self, button):
        def inner(e):
            x = int(button["text"]) % SIZE
            y = int(button["text"]) // SIZE
            dir = (x - self.last_place[0], y - self.last_place[1])
            if dir[0] ** 2 + dir[1] ** 2 == 1:
                button.config(background="blue")
                while dir != self.orientation:
                    self.move_list.append(LEFT)
                    ind = DIRS.index(self.orientation)
                    self.orientation = DIRS[(ind + 1) % len(DIRS)]
                    self.last_place = (x, y)
                self.last_place = (x, y)
                if len(self.move_list) >= 3 and self.move_list[-1] == self.move_list[-2] == self.move_list[-3] == LEFT:
                    self.move_list.pop()
                    self.move_list.pop()
                    self.move_list.pop()
                    self.move_list.append(RIGHT)
                    self.move_list.append(FORWARD)
                elif len(self.move_list) >= 2 and self.move_list[-1] == self.move_list[-2] == LEFT:
                    self.move_list.pop()
                    self.move_list.pop()
                    self.move_list.append(BACKWARD)
                    self.orientation = (-self.orientation[0], -self.orientation[1])
                else:
                    self.move_list.append(FORWARD)
                self.move_label["text"] = str(self.move_list)
            return

        return inner


if __name__ == '__main__':
    #gui = GUI()
    idx=input()
    car_move_auto(ROUTES[idx])
    car_move()
