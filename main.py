#
#
#

import Competitor
import Division
import DoubleBracket
import SingleBracket
import tkinter as tk
import threading

bracket = None
pressed = False  # Global variables to edit across entire class
button_num = 0

class Tournament:

    def __init__(self):

        self.buttons = []  # Lists to hold buttons and labels
        self.labels = []

        global bracket

        #bracket = SingleBracket.SingleBracket(["one", "two", "three", "four"])  # Create bracket
        bracket = DoubleBracket.DoubleBracket(["Collin", "Carson", "Gabe", "Bill", "Garrett", "Glenn", "Dale"])  # Create bracket
        bracket.create_bracket()
        bracket.fill_bracket()
        bracket.account_for_bys()
        print(bracket)
        self.minimum_size1 = 70
        self.minimum_size2 = 10

        self.root = tk.Tk()
        window_width = str((self.minimum_size1 + 10) * (bracket.get_num_levels()))
        window_height = str((self.minimum_size2 + 10) * (len(bracket.get_levels()[0]) * 2))
        if int(window_width) > 1000:
            window_width = "1000"
        if int(window_height) > 1000:
            window_height = "1000"
        self.root.geometry(window_width + "x" + window_height)  # Sets dimensions of window
        self.root.title("Arm Wrestling Tournament")  # Gives the window a title

        self.title_label = tk.Label(self.root, text="Arm Wrestling Tournament", font=('Arial', 5, 'bold')) # Gives another title for the window, but inside the window
        self.title_label.pack(padx=1, pady=1)



        self.entries_frame = tk.Frame(self.root)
        self.entries_frame.pack(fill='x')  # Packs entries frame so objects fill the x axis

        self.draw_bracket()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Calls on_closing when window is closed

        self.updates()  # Update window periodically

        self.root.mainloop()  # Keep window open

    def on_closing(self):
        self.root.destroy()  # End when closed

    def draw_bracket(self):
        level_counter1 = 0
        level_counter2 = bracket.get_num_levels() - 1
        entry_counter = 1
        node_counter = 0
        entry_multiplier = 2
        if isinstance(bracket, SingleBracket.SingleBracket):
            for i in range(bracket.get_num_levels()):  # Create grid layout to hold buttons and labels for bracket
                self.entries_frame.columnconfigure(i, minsize=self.minimum_size1)

            for i in range(bracket.get_num_nodes() + 1):
                self.entries_frame.rowconfigure(i, minsize=self.minimum_size2)

            for level in bracket.get_levels():  # Create bracket in tkinter window using buttons and labels
                for entry in level:
                    if entry.get_value() != -1:
                        self.buttons.append(tk.Button(self.entries_frame, text=entry.get_value(), font=('Arial', 5),
                                                      command=lambda node_counter1=node_counter: self.match_result(
                                                          node_counter1)))
                        self.buttons[len(self.buttons) - 1].grid(row=entry_counter, column=level_counter1,
                                                                 sticky=tk.W + tk.E, padx=5, pady=5)
                    entry_counter += entry_multiplier
                    node_counter += 1
                entry_counter = 1 * entry_multiplier
                entry_multiplier *= 2
                level_counter1 += 1
        if isinstance(bracket, DoubleBracket.DoubleBracket):
            for i in range(bracket.get_num_levels()):  # Create grid layout to hold buttons and labels for bracket
                self.entries_frame.columnconfigure(i, minsize=self.minimum_size1)

            for i in range(int(bracket.get_num_nodes() + 1 / 2)):
                self.entries_frame.rowconfigure(i, minsize=self.minimum_size2)

            levels = bracket.get_levels()

            entry_counter2 = 1
            node_counter2 = 0
            entry_multiplier2 = 2

            for i in range(len(levels)):  # Create bracket in tkinter window using buttons and labels
                level = levels[i]
                for j in range(len(level)):
                    if level[j].get_value() != -1:
                        if j < int(len(level) / 2):
                            self.buttons.append(tk.Button(self.entries_frame, text=level[j].get_value(), font=('Arial', 5),
                                                          command=lambda node_counter1=node_counter: self.match_result(
                                                              node_counter1)))
                            self.buttons[len(self.buttons) - 1].grid(row=entry_counter, column=level_counter1,
                                                                     sticky=tk.W + tk.E, padx=5, pady=5)
                        else:
                            self.buttons.append(
                                tk.Button(self.entries_frame, text=level[j].get_value(), font=('Arial', 5),
                                          command=lambda node_counter1=node_counter: self.match_result(
                                              node_counter1)))
                            self.buttons[len(self.buttons) - 1].grid(row=entry_counter2, column=level_counter2,
                                                                     sticky=tk.W + tk.E, padx=5, pady=5)
                    if j < int(len(level) / 2):
                        entry_counter += entry_multiplier
                    else:
                        entry_counter2 += entry_multiplier2
                    node_counter += 1
                entry_counter = 1 * entry_multiplier
                entry_multiplier *= 2
                entry_counter2 = 1 * entry_multiplier2
                entry_multiplier2 *= 2
                level_counter1 += 1
                level_counter2 -= 1
    def updates(self):
        global pressed
        global button_num  # Access global variables
        global bracket
        if pressed and button_num < bracket.get_num_nodes():  # When a button is pressed that is not the final button/node
            self.buttons.clear()  # Reset button list
            self.draw_bracket()
            pressed = False  # Reset pressed
            if bracket.check_done():
                print("Done")

        self.root.after(100, self.updates)  # Update every 250ms

    def match_result(self, entry):
        global pressed
        global button_num  # Access global variables
        global bracket
        button_num = entry
        if button_num < bracket.get_num_nodes() - 1:  # Call bracket functions to produce a result to a match given the button pressed
            if bracket.get_bracket()[button_num].get_value() == bracket.find_next(button_num).get_value():
                bracket.match_undo(entry)
            else:
                bracket.match_winner(entry)
            pressed = True


tour_thread = threading.Thread(target=Tournament)  # Thread for tournament class
tour_thread.start()

