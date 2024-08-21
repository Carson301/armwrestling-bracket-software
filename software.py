#
#
#

import tkinter as tk
import SingleBracket
import DoubleBracket
import Tournament

pressed = True
check_buttons = []
classes = ["0-154 R    ", "0-154 L    ", "155-176 R", "155-176 L", "177-198 R", "177-198 L", "199-220 R", "199-220 L", "221-240 R", "221-240 L", "241+ R     ", "241+ L     "]
brackets = []
checkers = []
buttons = []
lines = []
button_num = 0
menu_string = "main"
root = tk.Tk()
start_frame = tk.Frame(root, bg="white")


def main():
    global root
    global start_frame
    window_width = "1000"
    window_height = "500"
    root.geometry(window_width + "x" + window_height)  # Sets dimensions of window
    root.title("Arm Wrestling Tournament")  # Gives the window a title
    start_frame.pack(fill="both", expand=True)
    title_label = tk.Label(start_frame, text="Arm Wrestling Tournament", font=('Impact', 10), fg="white")  # Gives another title for the window, but inside the window
    title_label.pack(padx=1, pady=1)


    root.protocol("WM_DELETE_WINDOW", on_closing)  # Calls on_closing when window is closed

    updates()  # Update window periodically

    root.mainloop()  # Keep window open

def reset_start_frame():
    global start_frame
    for widgets in start_frame.winfo_children():
        widgets.destroy()
    start_frame.pack(fill="both", expand=True)
    title_label = tk.Label(start_frame, text="Arm Wrestling Tournament", font=('Impact', 10),
                           fg="white")  # Gives another title for the window, but inside the window
    title_label.pack(padx=1, pady=1)
    start_frame.configure(bg="SpringGreen4")
    title_label.configure(bg="SpringGreen4", pady=5)

def create_tournament():
    global brackets
    brackets = Tournament.Tournament()


def draw_scrollbar():
    global canvas
    global start_frame

    canvas = tk.Canvas(start_frame, highlightthickness=0, bg="Azure")

    # Create scrollbars
    xscrollbar = tk.Scrollbar(start_frame, orient="horizontal", command=canvas.xview)
    yscrollbar = tk.Scrollbar(start_frame, orient="vertical", command=canvas.yview)
    yscrollbar.pack(side="right", fill="y")
    xscrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="top", fill="both", expand=True)

    # Attach canvas to scrollbars
    canvas.configure(xscrollcommand=xscrollbar.set)
    canvas.configure(yscrollcommand=yscrollbar.set)

    # Create frame inside canvas
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind('<Configure>', set_scrollregion)

    return frame

def draw_bracket_window(bracket, frame):
    global buttons
    global lines
    level_counter1 = 0
    entry_counter = 2
    node_counter = 0
    entry_multiplier = 2
    levels = bracket.get_level_list()
    if isinstance(bracket, SingleBracket.SingleBracket):
        # Create rows and columns based on bracket size
        for i in range(int(bracket.get_num_nodes() / 2) + 32):
            if i < bracket.get_num_levels():
                frame.columnconfigure(i, minsize=150, weight=0)
            frame.rowconfigure(i, minsize=25, weight=0)

        for level in levels:  # Create bracket in tkinter window using buttons and labels

            for i in range(len(level)):
                if level[i].get_value() != -1:
                    # Create a button that represents a node in the bracket, append it to a list that stores buttons
                    buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[i].get_value(), font=('Sans-Serif 8 bold'), command=lambda node_counter1=node_counter: match_result(node_counter1, bracket)))

                    # Place the button that was just created in the tkinter grid
                    buttons[len(buttons) - 1].grid(row=entry_counter, column=level_counter1, sticky=tk.W + tk.E, pady=0, padx=5)

                    # If statement to draw lines connecting buttons properly
                    if i % 2 == 0 and bracket.find_index(level[i]) != bracket.get_num_nodes() - 1:

                        # Create the canvas to draw lines onto
                        lines.append(tk.Canvas(frame, highlightthickness=0, width=150, height=int(buttons[0].winfo_reqheight()) * (entry_multiplier - 1), bg="Azure"))

                        # Place the canvas into the tkinter grid
                        lines[len(lines) - 1].grid(row=entry_counter - entry_multiplier + 1, rowspan=entry_multiplier - 1, column=level_counter1)

                        # Draw two lines on the canvas to show that two nodes point to another
                        lines[len(lines) - 1].create_line(125, 0, 125, int(buttons[0].winfo_reqheight()) * (entry_multiplier - 1), width=5)
                        lines[len(lines) - 1].create_line(125, lines[len(lines) - 1].winfo_reqheight() // 2, 150, lines[len(lines) - 1].winfo_reqheight() // 2, width=5)

                # The following lines are variables that keep the bracket spaced properly
                entry_counter += entry_multiplier
                node_counter += 1
            entry_counter = 1 + entry_multiplier
            entry_multiplier *= 2
            level_counter1 += 1
    if isinstance(bracket, DoubleBracket.DoubleBracket):
        # Separate level counter for losers bracket
        level_counter2 = bracket.get_num_levels() - 1
        # Double bracket has different starting entry counter, to allow room for finals at the top
        entry_counter = 6
        entry_counter2 = 6
        entry_multiplier2 = 2
        count = 0

        # Create rows and columns based on bracket size
        for i in range(int(bracket.get_num_nodes() / 2) + 5):
            if i < bracket.get_num_levels():
                frame.columnconfigure(i, minsize=150, weight=0)
            frame.rowconfigure(i, minsize=25, weight=0)

        for i in range(len(levels) - 2):  # Create bracket in tkinter window using buttons and labels
            level = levels[i]
            for j in range(len(level)):
                if level[j].get_value() != -1:
                    # Separates the top half of nodes from the bottom, top=winner and loser=bottom
                    if j < int(len(level) / 4):
                        # Create a button that represents a node in the bracket, append it to a list that stores buttons
                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[j].get_value(), font=('Sans-Serif 8 bold'), command=lambda node_counter1=node_counter: match_result(node_counter1, bracket)))

                        # Place the button that was just created in the tkinter grid
                        buttons[len(buttons) - 1].grid(row=entry_counter, column=level_counter1, sticky=tk.W + tk.E, pady=0, padx=5)

                        # If statement to draw lines connecting buttons properly
                        if (i + count) % 2 == 0 and bracket.find_index(level[j]) != bracket.get_num_nodes() - 1:
                            # Create the canvas to draw lines onto
                            lines.append(tk.Canvas(frame, highlightthickness=0, width=150, height=int(buttons[0].winfo_reqheight()) * (entry_multiplier - 1), bg="Azure"))

                            # Place the canvas into the tkinter grid
                            lines[len(lines) - 1].grid(row=entry_counter - entry_multiplier + 1, rowspan=entry_multiplier - 1, column=level_counter1)

                            # Draw two lines on the canvas to show that two nodes point to another
                            lines[len(lines) - 1].create_line(125, 0, 125, int(buttons[0].winfo_reqheight()) * (entry_multiplier - 1), width=5)
                            lines[len(lines) - 1].create_line(125, lines[len(lines) - 1].winfo_reqheight() // 2, 150, lines[len(lines) - 1].winfo_reqheight() // 2, width=5)
                        count += 1
                    else:
                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[j].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=node_counter: match_result(node_counter1, bracket)))
                        buttons[len(buttons) - 1].grid(row=entry_counter2, column=level_counter2, sticky=tk.W + tk.E, padx=5, pady=0)
                        if (i + count) % 2 == 0 and level[j].get_value() != -1 and bracket.find_index(level[j]) < bracket.get_num_nodes() - 6:
                            lines.append(tk.Canvas(frame, width=150, height=int(buttons[0].winfo_reqheight()) * (entry_multiplier2 - 1), bg="Azure", highlightthickness=0))
                            lines[len(lines) - 1].grid(row=entry_counter2 - entry_multiplier2 + 1, rowspan=entry_multiplier2 - 1, column=level_counter2)
                            lines[len(lines) - 1].create_line(25, 0, 25, int(lines[len(lines) - 1].winfo_reqheight()), width=5)
                            lines[len(lines) - 1].create_line(25, int(lines[len(lines) - 1].winfo_reqheight()) // 2, 0, int(lines[len(lines) - 1].winfo_reqheight()) // 2, width=5)
                        count += 1
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

        # Add the finals buttons
        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][0].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=bracket.get_num_nodes() - 3: match_result(node_counter1, bracket)))
        buttons[len(buttons) - 1].grid(row=4, column=int(bracket.get_num_levels() / 2) - 1, sticky=tk.W + tk.E, padx=5, pady=0)

        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][1].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=bracket.get_num_nodes() - 2: match_result(node_counter1, bracket)))
        buttons[len(buttons) - 1].grid(row=4, column=int(bracket.get_num_levels() / 2) + 1, sticky=tk.W + tk.E, padx=5, pady=0)

        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 1][0].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=bracket.get_num_nodes() - 1: match_result(node_counter1, bracket)))
        buttons[len(buttons) - 1].grid(row=2, column=int(bracket.get_num_levels() / 2), sticky=tk.W + tk.E, padx=5, pady=0)

def switch_screen(string):
    global menu_string
    global pressed
    pressed = True
    menu_string = string

def draw_brackets_window(frame):
    global buttons
    global check_buttons
    global checkers
    for i in range(len(check_buttons)):
        if checkers[i][0].get() == 1:
            buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=checkers[i][1], font=('Serif-Sans 8 bold'), command=lambda screen_name="bracket": switch_screen(screen_name)))
    frame.columnconfigure(0, minsize=10, weight=0)
    frame.columnconfigure(1, minsize=10, weight=0)
    frame.columnconfigure(2, minsize=10, weight=0)
    col_counter = 0
    row_counter = -1
    for i in range(len(buttons)):
        if i % 2 == 0:
            frame.rowconfigure(i, minsize=20, weight=0)
            row_counter += 1
        buttons[i].grid(row=row_counter, column=col_counter, padx=0, pady=0)
        if col_counter == 0:
            col_counter += 2
        else:
            col_counter = 0


def draw_menu_window(frame):
    global check_buttons
    global checkers
    frame.columnconfigure(0, minsize=10, weight=0)
    frame.columnconfigure(1, minsize=10, weight=0)
    frame.columnconfigure(2, minsize=10, weight=0)
    col_counter = 0
    row_counter = -1
    for i in range(len(classes)):
        if i % 2 == 0:
            frame.rowconfigure(i, minsize=20, weight=0)
            row_counter += 1
        var = tk.IntVar()
        check_buttons.append(tk.Checkbutton(frame, text=classes[i], variable=var,
                onvalue=1,
                offvalue=0,
                height=2,
                width=20))
        checkers.append([var, classes[i]])
        check_buttons[i].grid(row=row_counter, column=col_counter, padx=0, pady=0)
        if col_counter == 0:
            col_counter += 2
        else:
            col_counter = 0

    frame.rowconfigure(len(classes), minsize=20, weight=0)
    submit = tk.Button(frame, text="Submit", command=lambda screen_name="brackets": switch_screen(screen_name))
    submit.grid(row=len(classes), column=1)


def updates():
    global buttons
    global pressed
    global start_frame
    if pressed:
        reset_start_frame()
        if menu_string == "main":
            frame = draw_scrollbar()
            draw_menu_window(frame)
        if menu_string == "bracket":
            frame = draw_scrollbar()
            buttons.clear()  # Reset button list
            draw_bracket_window(brackets[button_num], frame)
        if menu_string == "brackets":
            frame = draw_scrollbar()
            buttons.clear()  # Reset button list
            draw_brackets_window(frame)
        pressed = False

    root.after(100, updates)  # Update every 250ms


def match_result(entry, bracket):
    global pressed
    global button_num
    button_num = entry
    if button_num < bracket.get_num_nodes() - 1 and bracket.check_if_pair(
            button_num):  # Call bracket functions to produce a result to a match given the button pressed
        if bracket.get_bracket()[button_num].get_value() == bracket.find_default_next(button_num).get_value():
            bracket.match_undo(entry)
        else:
            bracket.match_winner(entry)
        pressed = True

def on_closing():
    root.destroy()  # End when closed

def set_scrollregion(event):
    global canvas
    canvas.configure(scrollregion=canvas.bbox('all'))





if __name__ == '__main__':
    main()