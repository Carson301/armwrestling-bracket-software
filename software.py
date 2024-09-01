#
#
#

import tkinter as tk
import SingleBracket
import DoubleBracket
import Tournament
from tkinter import messagebox

# The root of the window
root = tk.Tk()

# A frame to place all other widgets within
start_frame = tk.Frame(root, bg="white")
# A frame for buttons at the top of the screen
buttons_frame = tk.Frame(start_frame, bg="red")
# A frame for all adding to brackets widgets
frame2 = tk.Frame(start_frame, bg="red")
# Canvas for scrollbars
canvas = tk.Canvas(start_frame)

# Title for current screen
title = "Arm Wrestling Tournament"
# Create a title_label for the current screen
title_label = tk.Label(start_frame, text=title, font=('Impact', 10), fg="white")

# Menu strings used to know what screen the program is currently on
menu_string = "main"
prev_menu_string = "main"

# The tournament
brackets = Tournament.Tournament()
# Buttons and lines for the brackets
buttons = []
lines = []

# Whether a button has been pressed
pressed = True
# To know which button was pressed
button_num = 0


# A dictionary full of information about the tournament and the check buttons used within the program
check_button = {"Pro Right": [[], [["0-154", "154-165", "166-176", "176-187", "187-198", "199-220", "221-240", "241+"], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]],
                "Semi-Pro Right": [[], [["0-154", "154-165", "166-176", "176-187", "187-198", "199-220", "221-240", "241+"], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]],
                "Amateur Right": [[], [["0-154", "176-198", "199-220", "221-240", "241+"], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]],
                "Novice Right": [[], [["0-198", "199+"], [0, 0], [0, 0]]],
                "Master Right": [[], [["0-198", "199+"], [0, 0], [0, 0]]],
                "Women Right": [[], [["0-143", "144+"], [0, 0], [0, 0]]],
                "Pro Left": [[], [["0-154", "154-165", "166-176", "176-187", "187-198", "199-220", "221-240", "241+"], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]],
                "Semi-Pro Left": [[], [["0-154", "154-165", "166-176", "176-187", "187-198", "199-220", "221-240", "241+"], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]],
                "Amateur Left": [[], [["0-154", "176-198", "199-220", "221-240", "241+"], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]],
                "Novice Left": [[], [["0-198", "199+"], [0, 0], [0, 0]]],
                "Master Left": [[], [["0-198", "199+"], [0, 0], [0, 0]]],
                "Women Left": [[], [["0-143", "144+"], [0, 0], [0, 0]]],
                }

def main():
    global root, start_frame, title_label, buttons_frame
    # Create a window that takes up the whole screen
    root.state("zoomed")
    root.resizable(False, False)
    # Gives the window a title
    root.title("Arm Wrestling Tournament")
    # Pack the start_frame into the root
    start_frame.pack(fill="both", expand=True)
    # Pack the title label for the current screen into the start_frame
    title_label.pack(padx=1, pady=1)
    # Pack the buttons_frame into the start_frame
    buttons_frame.pack()

    # If the window is closed call on_closing to finish up the program
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Update window periodically
    updates()

    # Keep window open
    root.mainloop()

def reset_start_frame():
    global start_frame, buttons_frame, frame2, prev_menu_string, title_label
    # The screen needs to be reset
    # So destroy all current widgets of the start_frame
    for widgets in start_frame.winfo_children():
        widgets.destroy()
    # Create and repack all important widgets that were destroyed
    start_frame.pack(fill="both", expand=True)
    start_frame.configure(bg="SpringGreen4")
    title_label = tk.Label(start_frame, text=title, font=('Impact', 10),
                           fg="white")
    title_label.pack(padx=1, pady=1)
    title_label.configure(bg="SpringGreen4", pady=5)
    buttons_frame = tk.Frame(start_frame, bg="Azure")
    buttons_frame.pack(fill="both")
    frame2 = tk.Frame(start_frame, bg="seashell3")
    # Only pack frame2 on these screens
    if menu_string == "bracket" or menu_string == "brackets":
        frame2.pack(fill="y", side="right")
        frame2.configure(borderwidth=3, relief="solid")
    # All screens except main should have a go back button
    if menu_string != "main":
        go_back = tk.Button(buttons_frame, background="springgreen3", activebackground="springgreen4", fg="black",
                            text="Back", font=('Sans-Serif 8 bold'),
                            command=lambda menu=prev_menu_string: switch_screen(menu))
        go_back.grid(row=0, column=0)

def create_tournament():
    global brackets, check_button
    # Create a tournament object
    brackets = Tournament.Tournament()
    # For each "key" in check_button, key being the weight class
    for key in check_button:
        weight_class_checkers = check_button[key][1][1]
        # For each weight class
        for i in range(len(weight_class_checkers)):
            # If the checker value for the corresponding weight class is on
            if weight_class_checkers[i].get() == 1:
                # Create and begin a bracket for that weight class and add it to the tournament
                weight_classes = check_button[key][1][0]
                bracket = SingleBracket.SingleBracket([], weight_classes[i])
                bracket.begin_bracket()
                brackets.get_tournament().append(bracket)

def draw_scrollbar():
    global canvas, start_frame, menu_string

    # Create a canvas
    canvas = tk.Canvas(start_frame, highlightthickness=0, bg="Azure", borderwidth=3, relief="solid")

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
    frame = tk.Frame(canvas, bg="Azure")
    x_var = frame.winfo_screenwidth() / 2
    y_var = frame.winfo_screenheight() / 2
    # Depending on menu_string use different x and y vars
    if menu_string == "main" or menu_string == "pick":
        y_var = (frame.winfo_screenheight() / 2) - 50
    if menu_string == "pick":
        frame.configure(borderwidth=3, relief="solid")
    if menu_string == "bracket" or menu_string == "brackets":
        y_var = 0
        x_var = 0
    canvas.create_window((x_var, y_var), window=frame, anchor="center")
    frame.bind('<Configure>', set_scrollregion)

    return frame

def set_scrollregion(event):
    global canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

def del_competitor(bracket1, comp):
    global pressed
    bracket1.del_competitor(comp)
    bracket1.begin_bracket()
    pressed = True

def add_competitor(bracket1, comp):
    global pressed
    if comp.get().strip() != "":
        if len(comp.get().strip()) > 20:
            messagebox.showerror('Error', 'Error: Competitor name cannot be longer than 20 characters')
        else:
            copy = False
            for i in range(bracket1.num_competitors):
                if bracket1.get_competitor_list()[i] == comp.get().strip():
                    copy = True
            if copy:
                messagebox.showerror('Error', 'Error: Competitor is already in bracket')
            else:
                bracket1.add_competitor(comp.get().strip())
                bracket1.begin_bracket()
                pressed = True
    else:
        messagebox.showerror('Error', 'Error: Competitor name cannot be nothing')


def draw_bracket_window(bracket, frame):
    global buttons
    global lines
    global start_frame
    global buttons_frame
    level_counter1 = 0
    entry_counter = 2
    node_counter = 0
    entry_multiplier = 2
    levels = bracket.get_level_list()
    if isinstance(bracket, SingleBracket.SingleBracket):
        # Create rows and columns based on bracket size
        if bracket.get_num_competitors() > 1:
            for i in range(int(bracket.get_num_nodes())):
                if i < bracket.get_num_levels() + 1:
                    frame.columnconfigure(i, minsize=150, weight=0)
                frame.rowconfigure(i, minsize=25, weight=0)
        input_add = tk.StringVar()
        add_input = tk.Entry(frame2, textvariable=input_add, width=15)
        add_comp = tk.Button(frame2, background="springgreen3", activebackground="springgreen4", fg="black",
                                     text="Add", font=('Sans-Serif 8 bold'),
                                     command=lambda bracket1=bracket, comp=input_add: add_competitor(bracket1, comp))

        add_comp.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        add_input.grid(row=0, column=0, pady=5)

        if bracket.get_num_competitors() < 2:
            tk.Label(frame, text='Attention! Bracket Requires at least 2 competitors before it is drawn.', font='20', bg='yellow').grid(row=2, column=0, sticky="e")
        else:
            for level in levels:  # Create bracket in tkinter window using buttons and labels

                for i in range(len(level)):
                    if level[i].get_value() != -1:
                        # Create a button that represents a node in the bracket, append it to a list that stores buttons


                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[i].get_value(), font=('Sans-Serif 8 bold'), command=lambda node_counter1=node_counter: match_result(node_counter1, bracket)))

                        # Place the button that was just created in the tkinter grid
                        buttons[len(buttons) - 1].grid(row=entry_counter, column=level_counter1, sticky=tk.W + tk.E, pady=0, padx=5)

                        # If statement to draw lines connecting buttons properly
                        if i % 2 != 0 and bracket.find_index(level[i]) != bracket.get_num_nodes() - 1:

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
        count = 2
        tk.Label(frame2, text="Competitor List", font='sans-serif 10', bg="seashell4").grid(row=1, column=0, columnspan=2, sticky='ew')
        for entry in bracket.get_competitor_list():
            tk.Label(frame2, text=entry, bg="seashell3").grid(row=count, column=0)
            tk.Button(frame2, text="X", bg="red", font='Arial 5', command=lambda comp1=entry: del_competitor(bracket, comp1)).grid(row=count, column=1)
            count += 1
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

def switch_screen(string, bracket_name=None, button_num2=None):
    global menu_string
    global button_num1
    global button_num
    global pressed
    global title
    global prev_menu_string
    prev_menu_string = ""
    if menu_string == "main":
        title = "Arm Wrestling Tournament"
        button_num = 0
    if menu_string == "pick":
        title = "Arm Wrestling Tournament"
        button_num = 0
        if string == "brackets":
            create_tournament()
            title = "Arm Wrestling Tournament"
            button_num = 0
    if menu_string == "brackets":
        if string == "bracket":
            title = bracket_name
            button_num1 = button_num2
    if menu_string == "bracket":
        prev_menu_string = "brackets"
    if string == "pick":
        prev_menu_string = "main"
    if string == "brackets":
        prev_menu_string = "pick"
    if string == "bracket":
        prev_menu_string = "brackets"
    menu_string = string
    pressed = True

def add_to_brackets(name, checks, button_nums1):
    global brackets
    global checkers
    global buttons
    global pressed
    button_count = -1
    button_count2 = -1
    brackets_within = "Error: Competitor is already in the following brackets:\n"
    if name.get().strip() != "":
        if len(name.get().strip()) > 20:
            messagebox.showerror('Error', 'Error: Competitor name cannot be longer than 20 characters')
        else:
            copy = False
            for key in checks:
                for i in range(len(checks[key][1][1])):
                    if checks[key][1][1][i].get() == 1:
                        button_count += 1
                    if checks[key][1][2][i].get() == 1:
                        print(button_count)
                        for j in range(brackets.get_tournament()[button_nums1[button_count]].num_competitors):
                            if brackets.get_tournament()[button_nums1[button_count]].get_competitor_list()[j] == name.get().strip():
                                copy = True
                                brackets_within += brackets.get_tournament()[button_nums1[button_count]].get_bracket_name() + "\n"
            if copy == True:
                messagebox.showerror('Error', brackets_within)
            else:
                for key in checks:
                    for j in range(len(checks[key][1][1])):
                        if checks[key][1][1][j].get() == 1:
                            button_count2 += 1
                        if checks[key][1][2][j].get() == 1:
                            brackets.get_tournament()[button_nums1[button_count2]].add_competitor(name.get().strip())
                            brackets.get_tournament()[button_nums1[button_count2]].begin_bracket()
                            pressed = True
    else:
        messagebox.showerror('Error', 'Error: Competitor name cannot be nothing')





def draw_brackets_window(frame1):
    global buttons
    global frame2
    global check_button
    global check_button2

    button_nums = []
    button_names = []
    frames = []
    frame = tk.Frame(frame1, relief='solid', borderwidth=2)
    frame3 = tk.Frame(frame1, relief='solid', borderwidth=2)
    frame.grid(row=0, column=0)
    frame3.grid(row=1, column=0)
    row_counter = 0
    column_counter = -1
    frame.columnconfigure(0, minsize=10, weight=0)
    frame.columnconfigure(1, minsize=10, weight=0)
    frame.columnconfigure(2, minsize=10, weight=0)
    frame.columnconfigure(3, minsize=10, weight=0)
    frame.columnconfigure(4, minsize=10, weight=0)
    frame.columnconfigure(5, minsize=10, weight=0)
    frame.rowconfigure(0, minsize=10, weight=0)
    frame3.columnconfigure(0, minsize=10, weight=0)
    frame3.columnconfigure(1, minsize=10, weight=0)
    frame3.columnconfigure(2, minsize=10, weight=0)
    frame3.columnconfigure(3, minsize=10, weight=0)
    frame3.columnconfigure(4, minsize=10, weight=0)
    frame3.columnconfigure(5, minsize=10, weight=0)
    frame3.rowconfigure(0, minsize=10, weight=0)
    for i in range(6):
        column_counter += 1
        frames.append(tk.Frame(frame, relief='solid', borderwidth=2, bg="springgreen3"))
        frames[i].grid(row=row_counter, column=column_counter, sticky='ns')
    column_counter = -1
    for i in range(6, 12):
        column_counter += 1
        frames.append(tk.Frame(frame3, relief='solid', borderwidth=2, bg="springgreen3"))
        frames[i].grid(row=row_counter, column=column_counter, sticky='ns')
    count = -1
    for key in check_button:
        count += 1
        label = tk.Label(frames[count], text=key, font='bold', bg="springgreen3", width=15)
        label.grid(row=0, column=0)
        for i in range(0, len(check_button[key][1][1])):
            if check_button[key][1][1][i].get() == 1:
                buttons.append(
                    tk.Button(frames[count], background="springgreen3", width=8, activebackground="springgreen4", fg="white",
                              text=check_button[key][1][0][i], font=('Serif-Sans 15 bold'),
                              command=lambda screen_name="bracket", bracket_name=check_button[key][1][0][i],
                                             button_num2=len(buttons): switch_screen(screen_name, bracket_name,
                                                                                     button_num2)))
                button_names.append(check_button[key][1][0][i])
                button_nums.append(len(buttons) - 1)
                buttons[len(buttons) - 1].grid(row=i + 1, column=0, pady=4)
    print(button_nums)
# Separator
    frame2.columnconfigure(0, minsize=10, weight=0)
    frame2.columnconfigure(1, minsize=10, weight=0)
    frame2.columnconfigure(2, minsize=10, weight=0)
    input_add = tk.StringVar()
    add_input = tk.Entry(frame2, textvariable=input_add, width=15)
    add_input.grid(row=0, column=0, pady=5)
    count = -1
    count2 = -1
    frames2 = []
    row_counter = 0
    for key in check_button:
        count = -1
        check_button[key][0].clear()
        for i in range(len(check_button[key][1][2])):
            if check_button[key][1][1][i].get() == 1:
                if count == -1:
                    frames2.append(tk.Frame(frame2, borderwidth=2, relief='solid'))
                    frames2[len(frames2) - 1].grid(row=len(frames2) + 2, column=0, sticky='ns')
                    label = tk.Label(frames2[count2], text=key, font='bold', bg="springgreen3")
                    label.grid(row=0, column=0)
                    count2 += 1
                count += 1
                var = tk.IntVar()
                check_button[key][0].append(
                    tk.Checkbutton(frames2[count2], background="springgreen3", activebackground="springgreen4", text=button_names[count],
                                   variable=var,
                                   onvalue=1,
                                   offvalue=0,
                                   height=2,
                                   width=20))
                check_button[key][1][2][i] = var
                check_button[key][0][count].grid(row=count + 1, column=0)
            else:
                check_button[key][1][2][i] = tk.IntVar()
    # frame2.rowconfigure(len(classes), minsize=20, weight=0)
    submit = tk.Button(frame2, text="Submit",
                       command=lambda name=input_add, checks=check_button, button_nums1=button_nums: add_to_brackets(name,
                                                                                                                  checks,
                                                                                                                  button_nums1))
    submit.grid(row=len(frames), column=0)
    # for i in range(len(buttons)):
    #     var = tk.IntVar()
    #     check_button.append(tk.Checkbutton(frame2, background="springgreen3", activebackground="springgreen4", text=button_names[i], variable=var,
    #             onvalue=1,
    #             offvalue=0,
    #             height=2,
    #             width=20))
    #     checkers2.append([var, classes[i]])
    # frame2.configure(bg="springgreen3")
    # row_counter = 0
    # prev_button = "NA"
    # for i in range(len(check_buttons2)):
    #     if button_names[i][:-1] == prev_button[:-1]:
    #         col_counter = 1
    #     else:
    #         frame2.rowconfigure(i, minsize=50, weight=0)
    #         row_counter += 1
    #         if "L" in button_names[i]:
    #             col_counter = 1
    #         else:
    #             col_counter = 0
    #     check_buttons2[i].grid(row=row_counter, column=col_counter, padx=5, pady=5)
    #     prev_button = button_names[i]
    #



def draw_menu_window(frame1):
    global check_button
    frames = []
    frame = tk.Frame(frame1, relief='solid', borderwidth=2)
    frame3 = tk.Frame(frame1, relief='solid', borderwidth=2)
    frame.grid(row=0, column=0)
    frame3.grid(row=1, column=0)
    row_counter = 0
    column_counter = -1
    frame.columnconfigure(0, minsize=10, weight=0)
    frame.columnconfigure(1, minsize=10, weight=0)
    frame.columnconfigure(2, minsize=10, weight=0)
    frame.columnconfigure(3, minsize=10, weight=0)
    frame.columnconfigure(4, minsize=10, weight=0)
    frame.columnconfigure(5, minsize=10, weight=0)
    frame.rowconfigure(0, minsize=10, weight=0)
    frame3.columnconfigure(0, minsize=10, weight=0)
    frame3.columnconfigure(1, minsize=10, weight=0)
    frame3.columnconfigure(2, minsize=10, weight=0)
    frame3.columnconfigure(3, minsize=10, weight=0)
    frame3.columnconfigure(4, minsize=10, weight=0)
    frame3.columnconfigure(5, minsize=10, weight=0)
    frame3.rowconfigure(0, minsize=10, weight=0)
    for i in range(6):
        column_counter += 1
        frames.append(tk.Frame(frame, relief='solid', borderwidth=2, bg="springgreen3"))
        frames[i].grid(row=row_counter, column=column_counter, sticky='ns')
    column_counter = -1
    for i in range(6, 12):
        column_counter += 1
        frames.append(tk.Frame(frame3, relief='solid', borderwidth=2, bg="springgreen3"))
        frames[i].grid(row=row_counter, column=column_counter, sticky='ns')

    count = -1
    for key in check_button:
        count += 1
        label = tk.Label(frames[count], text=key, font='bold', bg="springgreen3")
        label.grid(row=0, column=0)
        for i in range(0, len(check_button[key][1][0])):
            var = tk.IntVar()
            check_button[key][0].append(tk.Checkbutton(frames[count], bg="springgreen3", font='Arial 10 bold', text=check_button[key][1][0][i], variable=var,
                                                onvalue=1,
                                                offvalue=0,
                                                height=1,
                                                width=15))
            check_button[key][1][1][i] = var
            check_button[key][0][i].grid(row=i + 1, column=0)

    submit = tk.Button(frame1, text="Submit", command=lambda screen_name="brackets": switch_screen(screen_name))
    submit.grid(row=2, column=0)

def draw_main_window(frame):
    global buttons
    tk.Button(frame, bg='springgreen3', text="Start", font=('Impact', 25), width=25, command=lambda screen_name="pick": switch_screen(screen_name)).grid(row=0, column=0, pady=10)
    tk.Button(frame, bg='springgreen3', text="Options", font=('Impact', 25), width=25, command=lambda screen_name="options": switch_screen(screen_name)).grid(row=1, column=0, pady=10)
    tk.Button(frame, bg='springgreen3', text="Help", font=('Impact', 25), width=25, command=lambda screen_name="help": switch_screen(screen_name)).grid(row=2, column=0, pady=10)



def updates():
    global buttons
    global check_buttons
    global checkers
    global check_buttons2
    global checkers2
    global lines
    global pressed
    global start_frame
    global button_num
    global button_num1
    global menu_string
    if pressed:
        reset_start_frame()
        if menu_string == "main":
            frame = draw_scrollbar()
            draw_main_window(frame)
        if menu_string == "pick":
            for key in check_button:
                check_button[key][0].clear()
                for var in check_button[key][1][1]:
                    var = 0
            frame = draw_scrollbar()
            draw_menu_window(frame)
        if menu_string == "bracket":
            frame = draw_scrollbar()
            buttons.clear()  # Reset button list
            lines.clear()
            draw_bracket_window(brackets.get_tournament()[button_num1], frame)
        if menu_string == "brackets":
            for key in check_button:
                check_button[key][0].clear()
                for var in check_button[key][1][1]:
                    var = 0
            frame = draw_scrollbar()
            lines.clear()
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





if __name__ == '__main__':
    main()