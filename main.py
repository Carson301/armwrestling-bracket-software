#
#
#

import Competitor
import Division
import DoubleBracket
import SingleBracket
import tkinter as tk
import threading
import math

bracket = None
pressed = False  # Global variables to edit across entire class
button_num = 0

class Tournament:

    def __init__(self):

        self.buttons = []  # Lists to hold buttons and labels
        self.labels = []
        self.lines = []

        global bracket

        bracket = SingleBracket.SingleBracket(["levan saginashvili99", "Jerry Cadorette", "Jerry Cadorette", "Jerry Cadorette",
                                               "levan saginashvili99", "Jerry Cadorette", "Jerry Cadorette", "Jerry Cadorette",
                                               "levan saginashvili99", "Jerry Cadorette", "Jerry Cadorette", "Jerry Cadorette",
                                               "levan saginashvili99", "Jerry Cadorette", "Jerry Cadorette", "Jerry Cadorette",
                                               "levan saginashvili99", "Jerry Cadorette", "Jerry Cadorette", "Jerry Cadorette",
                                               "levan saginashvili99", "Jerry Cadorette", "Jerry Cadorette", "Jerry Cadorette",
                                               "levan saginashvili99", "Jerry Cadorette", "Jerry Cadorette", "Jerry Cadorette"])  # Create bracket

        # bracket = DoubleBracket.DoubleBracket(["Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper",
        #                                        "Collin King", "Carson King", "Bill Sinks", "Garrett Tupper"])  # Create bracket
        bracket.create_bracket()
        bracket.fill_bracket()
        bracket.account_for_bys()
        self.minimum_size1 = 75
        self.minimum_size2 = 25

        self.root = tk.Tk()
        window_width = "1000"
        window_height = "500"
        if int(window_width) > 1000:
            window_width = "1000"
        if int(window_height) > 1000:
            window_height = "1000"
        self.root.geometry(window_width + "x" + window_height)  # Sets dimensions of window
        self.root.minsize(width=1000, height=500)
        self.root.title("Arm Wrestling Tournament")  # Gives the window a title

        self.title_label = tk.Label(self.root, text="Arm Wrestling Tournament", font=('Impact', 10), fg="white") # Gives another title for the window, but inside the window
        self.title_label.pack(padx=1, pady=1)

        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="Azure")

        # Create scrollbars
        self.xscrollbar = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.yscrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.yscrollbar.pack(side="right", fill="y")
        self.xscrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="top", fill="both", expand=True)

        # Attach canvas to scrollbars
        self.canvas.configure(xscrollcommand=self.xscrollbar.set)
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)

        # Create frame inside canvas
        self.entries_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.entries_frame, anchor="nw")
        self.entries_frame.bind('<Configure>', self.set_scrollregion)


        self.entries_frame.configure(bg="Azure")
        self.root.configure(bg="SpringGreen4")
        self.title_label.configure(bg="SpringGreen4", pady=5)

        self.draw_bracket()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Calls on_closing when window is closed

        self.updates()  # Update window periodically

        self.root.mainloop()  # Keep window open

    def on_closing(self):
        self.root.destroy()  # End when closed

    def set_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def draw_bracket(self):
        level_counter1 = 0
        level_counter2 = bracket.get_num_levels() - 1
        entry_counter = 2
        node_counter = 0
        entry_multiplier = 2
        if isinstance(bracket, SingleBracket.SingleBracket):
            for i in range(bracket.get_num_levels()):  # Create grid layout to hold buttons and labels for bracket
                self.entries_frame.columnconfigure(i, minsize=150, weight=0)

            for i in range(int(bracket.get_num_nodes() / 2)):
                self.entries_frame.rowconfigure(i, minsize=20, weight=0)
            middles = [12, 36, 87, 187, 387, 787]
            draw_line = False
            count = 0

            for level in bracket.get_level_list():  # Create bracket in tkinter window using buttons and labels

                for entry in level:
                    if entry.get_value() != -1:
                        self.buttons.append(tk.Button(self.entries_frame, background="springgreen3", activebackground="springgreen4", fg="white", text=entry.get_value(), font=('Sans-Serif 8 bold'),
                                                      command=lambda node_counter1=node_counter: self.match_result(
                                                          node_counter1)))
                        self.buttons[len(self.buttons) - 1].grid(row=entry_counter, column=level_counter1,
                                                                 sticky=tk.W + tk.E, pady=0, padx=5)
                        if draw_line and entry.get_value() != -1 and bracket.find_index(entry) != bracket.get_num_nodes() - 1:
                            self.lines.append(tk.Canvas(self.entries_frame, width=150, height=20 * (entry_multiplier - 1), bg="Azure", highlightthickness=0))
                            self.lines[len(self.lines) - 1].grid(row=entry_counter - entry_multiplier + 1, rowspan=entry_multiplier - 1, sticky=tk.N+tk.S, column=level_counter1)
                            print(20 * entry_multiplier, 10 * entry_multiplier)
                            self.lines[len(self.lines) - 1].create_line(125, 0, 125, middles[count] * 3, width=5)
                            self.lines[len(self.lines) - 1].create_line(125, middles[count], 150, middles[count], width=5) # 12 35 80 173 357 / 2 - 5
                            #                                                                        24 70
                        draw_line = not draw_line
                    entry_counter += entry_multiplier
                    node_counter += 1
                entry_counter = 1 + entry_multiplier
                entry_multiplier *= 2
                level_counter1 += 1
                count += 1
        entry_counter = 0
        if isinstance(bracket, DoubleBracket.DoubleBracket):
            entry_counter = 6
            for i in range(bracket.get_num_levels()):  # Create grid layout to hold buttons and labels for bracket
                self.entries_frame.columnconfigure(i, minsize=150, weight=0)

            for i in range(int(bracket.get_num_nodes() / 2) + 5):
                self.entries_frame.rowconfigure(i, minsize=20, weight=0)
            middles = [12, 33, 78, 168, 348, 718]
            draw_line = False
            count = 0
            levels = bracket.get_level_list()

            entry_counter2 = 6
            node_counter2 = 0
            entry_multiplier2 = 2

            for i in range(len(levels) - 2):  # Create bracket in tkinter window using buttons and labels
                level = levels[i]
                for j in range(len(level)):
                    if level[j].get_value() != -1:
                        if j < int(len(level) / 4):
                            self.buttons.append(tk.Button(self.entries_frame, background="springgreen3", activebackground="springgreen4", fg="white", text=level[j].get_value(), font=('Serif-Sans 8 bold'),
                                                          command=lambda node_counter1=node_counter: self.match_result(
                                                              node_counter1)))
                            self.buttons[len(self.buttons) - 1].grid(row=entry_counter, column=level_counter1,
                                                                     sticky=tk.W + tk.E, padx=5, pady=0)
                            if draw_line and level[j].get_value() != -1 and bracket.find_index(
                                    level[j]) < bracket.get_num_nodes() - 5:
                                self.lines.append(
                                    tk.Canvas(self.entries_frame, width=150, height=20 * (entry_multiplier - 1),
                                              bg="Azure", highlightthickness=0))
                                self.lines[len(self.lines) - 1].grid(row=entry_counter - entry_multiplier + 1,
                                                                     rowspan=entry_multiplier - 1, sticky=tk.N + tk.S,
                                                                     column=level_counter1)
                                print(20 * entry_multiplier, 10 * entry_multiplier)
                                self.lines[len(self.lines) - 1].create_line(125, 0, 125, middles[count] * 3, width=5)
                                self.lines[len(self.lines) - 1].create_line(125, middles[count], 150, middles[count],
                                                                            width=5)
                            draw_line = not draw_line
                        else:
                            self.buttons.append(

                                tk.Button(self.entries_frame, background="springgreen3", activebackground="springgreen4", fg="white", text=level[j].get_value(), font=('Serif-Sans 8 bold'),
                                          command=lambda node_counter1=node_counter: self.match_result(
                                              node_counter1)))
                            self.buttons[len(self.buttons) - 1].grid(row=entry_counter2, column=level_counter2,
                                                                     sticky=tk.W + tk.E, padx=5, pady=0)
                            if draw_line and level[j].get_value() != -1 and bracket.find_index(
                                    level[j]) < bracket.get_num_nodes() - 6:
                                self.lines.append(
                                    tk.Canvas(self.entries_frame, width=150, height=20 * (entry_multiplier2 - 1),
                                              bg="Azure", highlightthickness=0))
                                self.lines[len(self.lines) - 1].grid(row=entry_counter2 - entry_multiplier2 + 1,
                                                                     rowspan=entry_multiplier2 - 1, sticky=tk.N + tk.S,
                                                                     column=level_counter2)
                                print(20 * entry_multiplier, 10 * entry_multiplier)
                                self.lines[len(self.lines) - 1].create_line(25, 0, 25, middles[count] * 3, width=5)
                                self.lines[len(self.lines) - 1].create_line(25, middles[count], 0, middles[count],
                                                                            width=5)
                            draw_line = not draw_line
                    if j < int(len(level) / 4):
                        entry_counter += entry_multiplier
                    else:
                        entry_counter2 += entry_multiplier2
                    node_counter += 1
                entry_counter = 5 + entry_multiplier
                entry_multiplier *= 2
                entry_counter2 = 5 + entry_multiplier2
                entry_multiplier2 *= 2
                level_counter1 += 1
                level_counter2 -= 1
                count += 1

            self.buttons.append(
                tk.Button(self.entries_frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][0].get_value(), font=('Serif-Sans 8 bold'),
                          command=lambda node_counter1=bracket.get_num_nodes() - 3: self.match_result(
                              node_counter1)))
            self.buttons[len(self.buttons) - 1].grid(row=4, column=math.floor(bracket.get_num_levels() / 2) - 1,
                                                     sticky=tk.W + tk.E, padx=5, pady=0)

            self.buttons.append(
                tk.Button(self.entries_frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][1].get_value(), font=('Serif-Sans 8 bold'),
                          command=lambda node_counter1=bracket.get_num_nodes() - 2: self.match_result(
                              node_counter1)))
            self.buttons[len(self.buttons) - 1].grid(row=4, column=math.floor(bracket.get_num_levels() / 2) + 1,
                                                     sticky=tk.W + tk.E, padx=5, pady=0)

            self.buttons.append(
                tk.Button(self.entries_frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 1][0].get_value(), font=('Serif-Sans 8 bold'),
                          command=lambda node_counter1=bracket.get_num_nodes() - 1: self.match_result(
                              node_counter1)))
            self.buttons[len(self.buttons) - 1].grid(row=2, column=math.floor(bracket.get_num_levels() / 2),
                                                     sticky=tk.W + tk.E, padx=5, pady=0)
    def updates(self):
        global pressed
        global button_num  # Access global variables
        global bracket
        if pressed and button_num < bracket.get_num_nodes():  # When a button is pressed that is not the final button/node
            self.buttons.clear()  # Reset button list
            self.draw_bracket()
            pressed = False  # Reset pressed

        self.root.after(100, self.updates)  # Update every 250ms

    def match_result(self, entry):
        global pressed
        global button_num  # Access global variables
        global bracket
        button_num = entry
        if button_num < bracket.get_num_nodes() - 1 and bracket.check_if_pair(button_num):  # Call bracket functions to produce a result to a match given the button pressed
            if bracket.get_bracket()[button_num].get_value() == bracket.find_default_next(button_num).get_value():
                bracket.match_undo(entry)
            else:
                bracket.match_winner(entry)
            pressed = True


tour_thread = threading.Thread(target=Tournament)  # Thread for tournament class
tour_thread.start()

