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

count3 = 0
count4 = 0

# A frame to place all other widgets within
start_frame = tk.Frame(root, bg="white")
# A frame for buttons at the top of the screen
buttons_frame = tk.Frame(start_frame, bg="red")
# A frame for all adding to brackets widgets
frame2 = tk.Frame(start_frame, bg="red")
# Canvas for scrollbars
canvas = tk.Canvas(start_frame)
canvas2 = tk.Canvas(frame2)

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
# To know which bracket button was pressed
brackets_button_num = 0
# To know which node button was pressed
node_button_num = 0


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
    canvas = tk.Canvas(start_frame, highlightthickness=0, bg="Azure", relief="solid")

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
    global count4
    canvas.configure(scrollregion=canvas.bbox('all'))
    if count4 < 4:
        count4 += 1
        canvas.yview_moveto(0)

def set_scrollregion1(event):
    global canvas2
    global count3
    canvas2.configure(scrollregion=canvas2.bbox('all'))
    if count3 < 4:
        count3 += 1
        canvas2.yview_moveto(0)



def del_competitor(bracket, competitor_name):
    global pressed
    # Call bracket method to delete competitor from bracket
    bracket.del_competitor(competitor_name)
    # Begin bracket again
    bracket.begin_bracket()
    pressed = True


def add_competitor(bracket, competitor_name):
    global pressed
    # Make sure competitor name isn't nothing
    if competitor_name.get().strip() != "":
        # Make sure competitor name is shorter than 20 characters
        if len(competitor_name.get().strip()) > 20:
            messagebox.showerror('Error', 'Error: Competitor name cannot be longer than 20 characters')
        else:
            # If all other checks satisfied begin checking for if the competitor is within the bracket already
            already_in_bracket = False
            # Go through each competitor and check
            for i in range(bracket.num_competitors):
                if bracket.get_competitor_list()[i] == competitor_name.get().strip():
                    already_in_bracket = True
            # The competitor does already exist in the bracket
            if already_in_bracket:
                messagebox.showerror('Error', 'Error: Competitor is already in the ' + bracket.get_bracket_name() + ' bracket')
            # Competitor doesn't already exist in bracket
            # Add them to bracket
            else:
                bracket.add_competitor(competitor_name.get().strip())
                bracket.begin_bracket()
                pressed = True
    else:
        messagebox.showerror('Error', 'Error: Competitor name cannot be nothing')


def draw_bracket_window(bracket, frame):
    global buttons, lines, start_frame, buttons_frame
    # Variables that keep track of where nodes of a bracket should be places in the frame grid
    winner_lvl_count = 0
    winner_entry_count = 2
    node_count = 0
    winner_entry_mult = 2
    levels = bracket.get_level_list()
    # If the bracket being drawn is of the form SingleBracket
    if isinstance(bracket, SingleBracket.SingleBracket):
        # Create an entry field to take in the input of a competitor name to add to bracket
        input_var = tk.StringVar()
        competitor_entry = tk.Entry(frame2, textvariable=input_var, width=15)
        # Create an add button to add the competitor to the bracket
        add_button = tk.Button(frame2, background="springgreen3", activebackground="springgreen4", fg="black",
                             text="Add", font=('Sans-Serif 8 bold'),
                             command=lambda bracket_ref=bracket, competitor_ref=input_var: add_competitor(bracket_ref, competitor_ref))
        add_button.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        competitor_entry.grid(row=0, column=0, pady=5)

        # Variable to keep track of current row in frame2
        row_count = 2
        # Label for competitor list of bracket
        tk.Label(frame2, text="Competitor List", font='sans-serif 10', bg="seashell4").grid(row=1, column=0,                                                                                columnspan=2, sticky='ew')
        # For each competitor
        for entry in bracket.get_competitor_list():
            # Create both a label and a button that may be pressed to remove the competitor from the bracket
            competitor_label = tk.Label(frame2, text=entry, bg="seashell3")
            competitor_label.grid(row=row_count, column=0)
            remove_button = tk.Button(frame2, text="X", bg="red", font='Arial 5',
                      command=lambda comp1=entry: del_competitor(bracket, comp1))
            remove_button.grid(row=row_count, column=1)
            row_count += 1

        # If the bracket doesn't have enough competitors
        if bracket.get_num_competitors() < 2:
            tk.Label(frame, text='Attention! Bracket Requires at least 2 competitors before it is drawn.', font='20', bg='yellow').grid(row=2, column=0, sticky="e")
        # Once the bracket does have at least 2 competitors
        else:
            # Create enough rows and columns for the grid
            for i in range(int(bracket.get_num_nodes())):
                if i < bracket.get_num_levels() + 1:
                    frame.columnconfigure(i, minsize=150, weight=0)
                frame.rowconfigure(i, minsize=25, weight=0)
            # For each level in the bracket. A Level being the columns of the bracket
            for level in levels:
                for i in range(len(level)):
                    # Only draw nodes that have valid values
                    # -1 means don't draw this entry as it is not needed
                    if level[i].get_value() != -1:
                        # Create a button that represents a node in the bracket, append it to a list that stores buttons
                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[i].get_value(), font=('Sans-Serif 8 bold'), command=lambda node_count_ref=node_count: match_result(node_count_ref, bracket)))
                        buttons[len(buttons) - 1].grid(row=winner_entry_count, column=winner_lvl_count, sticky=tk.W + tk.E, pady=0, padx=5)

                        # If statement to draw lines connecting buttons properly
                        if i % 2 != 0 and bracket.find_index(level[i]) != bracket.get_num_nodes() - 1:

                            # Create the canvas to draw lines onto
                            lines.append(tk.Canvas(frame, highlightthickness=0, width=150, height=int(buttons[0].winfo_reqheight()) * (winner_entry_mult - 1), bg="Azure"))
                            lines[len(lines) - 1].grid(row=winner_entry_count - winner_entry_mult + 1, rowspan=winner_entry_mult - 1, column=winner_lvl_count)

                            # Draw two lines on the canvas to show that two nodes point to another
                            lines[len(lines) - 1].create_line(125, 0, 125, int(buttons[0].winfo_reqheight()) * (winner_entry_mult - 1), width=5)
                            lines[len(lines) - 1].create_line(125, lines[len(lines) - 1].winfo_reqheight() // 2, 150, lines[len(lines) - 1].winfo_reqheight() // 2, width=5)

                    # The following lines are variables that keep the bracket spaced properly
                    winner_entry_count += winner_entry_mult
                    node_count += 1
                winner_entry_count = 1 + winner_entry_mult
                winner_entry_mult *= 2
                winner_lvl_count += 1
    if isinstance(bracket, DoubleBracket.DoubleBracket):
        # Separate level counter for losers bracket
        level_counter2 = bracket.get_num_levels() - 1
        # Double bracket has different starting entry counter, to allow room for finals at the top
        winner_entry_count = 6
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
                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[j].get_value(), font=('Sans-Serif 8 bold'), command=lambda node_count_ref=node_count: match_result(node_count_ref, bracket)))

                        # Place the button that was just created in the tkinter grid
                        buttons[len(buttons) - 1].grid(row=winner_entry_count, column=winner_lvl_count, sticky=tk.W + tk.E, pady=0, padx=5)

                        # If statement to draw lines connecting buttons properly
                        if (i + count) % 2 == 0 and bracket.find_index(level[j]) != bracket.get_num_nodes() - 1:
                            # Create the canvas to draw lines onto
                            lines.append(tk.Canvas(frame, highlightthickness=0, width=150, height=int(buttons[0].winfo_reqheight()) * (winner_entry_mult - 1), bg="Azure"))

                            # Place the canvas into the tkinter grid
                            lines[len(lines) - 1].grid(row=winner_entry_count - winner_entry_mult + 1, rowspan=winner_entry_mult - 1, column=winner_lvl_count)

                            # Draw two lines on the canvas to show that two nodes point to another
                            lines[len(lines) - 1].create_line(125, 0, 125, int(buttons[0].winfo_reqheight()) * (winner_entry_mult - 1), width=5)
                            lines[len(lines) - 1].create_line(125, lines[len(lines) - 1].winfo_reqheight() // 2, 150, lines[len(lines) - 1].winfo_reqheight() // 2, width=5)
                        count += 1
                    else:
                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[j].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_count_ref=node_count: match_result(node_count_ref, bracket)))
                        buttons[len(buttons) - 1].grid(row=entry_counter2, column=level_counter2, sticky=tk.W + tk.E, padx=5, pady=0)
                        if (i + count) % 2 == 0 and level[j].get_value() != -1 and bracket.find_index(level[j]) < bracket.get_num_nodes() - 6:
                            lines.append(tk.Canvas(frame, width=150, height=int(buttons[0].winfo_reqheight()) * (entry_multiplier2 - 1), bg="Azure", highlightthickness=0))
                            lines[len(lines) - 1].grid(row=entry_counter2 - entry_multiplier2 + 1, rowspan=entry_multiplier2 - 1, column=level_counter2)
                            lines[len(lines) - 1].create_line(25, 0, 25, int(lines[len(lines) - 1].winfo_reqheight()), width=5)
                            lines[len(lines) - 1].create_line(25, int(lines[len(lines) - 1].winfo_reqheight()) // 2, 0, int(lines[len(lines) - 1].winfo_reqheight()) // 2, width=5)
                        count += 1
                if j < int(len(level) / 4):
                    winner_entry_count += winner_entry_mult
                else:
                    entry_counter2 += entry_multiplier2
                node_count += 1
            winner_entry_count = 5 + winner_entry_mult
            winner_entry_mult *= 2
            entry_counter2 = 5 + entry_multiplier2
            entry_multiplier2 *= 2
            winner_lvl_count += 1
            level_counter2 -= 1

        # Add the finals buttons
        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][0].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_count_ref=bracket.get_num_nodes() - 3: match_result(node_count_ref, bracket)))
        buttons[len(buttons) - 1].grid(row=4, column=int(bracket.get_num_levels() / 2) - 1, sticky=tk.W + tk.E, padx=5, pady=0)

        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][1].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_count_ref=bracket.get_num_nodes() - 2: match_result(node_count_ref, bracket)))
        buttons[len(buttons) - 1].grid(row=4, column=int(bracket.get_num_levels() / 2) + 1, sticky=tk.W + tk.E, padx=5, pady=0)

        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 1][0].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_count_ref=bracket.get_num_nodes() - 1: match_result(node_count_ref, bracket)))
        buttons[len(buttons) - 1].grid(row=2, column=int(bracket.get_num_levels() / 2), sticky=tk.W + tk.E, padx=5, pady=0)


def switch_screen(string, bracket_name=None, brackets_button_num_ref=None):
    global menu_string, brackets_button_num, pressed, title, prev_menu_string
    # Depending on the menu_string alter the screen variables to fit that screen
    if string == "main":
        title = "Arm Wrestling Tournament"
        brackets_button_num = 0
    if string == "pick":
        prev_menu_string = "main"
    if string == "brackets":
        if menu_string != "bracket":
            create_tournament()
        title = "Arm Wrestling Tournament"
        brackets_button_num = 0
        prev_menu_string = "pick"
    if string == "bracket":
        title = bracket_name
        brackets_button_num = brackets_button_num_ref
        prev_menu_string = "brackets"
    # Set menu_string to the new screen name
    menu_string = string
    pressed = True


def add_to_brackets(name):
    global brackets, pressed, check_button
    # Index of button that references the current bracket
    button_count = -1
    brackets_within = "Error: Competitor is already in the following brackets:\n"
    if name.get().strip() != "":
        if len(name.get().strip()) > 20:
            messagebox.showerror('Error', 'Error: Competitor name cannot be longer than 20 characters')
        else:
            # Boolean to check if competitor is already in the bracket
            already_in_bracket = False
            # For each weight class/bracket
            for key in check_button:
                # Checkers for the weight classes for both checkbox areas of the program
                weight_class_checkers = check_button[key][1][1]
                weight_class_checkers_2 = check_button[key][1][2]
                for i in range(len(weight_class_checkers)):
                    # Increment button count if the box was checked with the first checkboxes
                    if weight_class_checkers[i].get() == 1:
                        button_count += 1
                    # Add the competitor to the bracket if the box was checked
                    if weight_class_checkers_2[i].get() == 1:
                        current_bracket = brackets.get_tournament()[button_count]
                        for j in range(current_bracket.num_competitors):
                            # If the competitor is already in the bracket set boolean and add the name of the bracket
                            # to the brackets_within string
                            if current_bracket.get_competitor_list()[j] == name.get().strip():
                                already_in_bracket = True
                                brackets_within += current_bracket.get_bracket_name() + "\n"
            # Show the user what brackets the competitor is already in
            if already_in_bracket:
                messagebox.showerror('Error', brackets_within)
            # If no other errors
            else:
                button_count = -1
                for key in check_button:
                    # Checkers for the weight classes for both checkbox areas of the program
                    weight_class_checkers = check_button[key][1][1]
                    weight_class_checkers_2 = check_button[key][1][2]
                    for j in range(len(weight_class_checkers)):
                        if weight_class_checkers[j].get() == 1:
                            button_count += 1
                        if weight_class_checkers_2[j].get() == 1:
                            current_bracket = brackets.get_tournament()[button_count]
                            current_bracket.add_competitor(name.get().strip())
                            current_bracket.begin_bracket()
                            pressed = True
    else:
        messagebox.showerror('Error', 'Error: Competitor name cannot be nothing')


def draw_brackets_window(frame):
    global buttons, frame2, check_button
    button_names = []
    frames = []
    # Create two frames to break up the window
    frame_one = tk.Frame(frame, relief='solid', borderwidth=2)
    frame_two = tk.Frame(frame, relief='solid', borderwidth=2)
    frame_one.grid(row=0, column=0)
    frame_two.grid(row=1, column=0)
    row_counter = 0
    column_counter = -1
    # Create columns and rows for those frames
    for i in range(6):
        frame_one.columnconfigure(i, minsize=10, weight=0)
        frame_two.columnconfigure(i, minsize=10, weight=0)
    frame_one.rowconfigure(0, minsize=10, weight=0)
    frame_two.rowconfigure(0, minsize=10, weight=0)
    # Create 6 frames within each of the frames above to separate out the window even more
    for i in range(12):
        if i < 6:
            column_counter += 1
            frames.append(tk.Frame(frame_one, relief='solid', borderwidth=2, bg="springgreen3"))
            frames[i].grid(row=row_counter, column=column_counter, sticky='news')
            if i == 5:
                column_counter = -1
        else:
            column_counter += 1
            frames.append(tk.Frame(frame_two, relief='solid', borderwidth=2, bg="springgreen3"))
            frames[i].grid(row=row_counter, column=column_counter, sticky='news')
    frame_count = -1
    buttons = []
    for key in check_button:
        frame_count += 1
        # Create a label for each frame, that is the current brackets title
        label = tk.Label(frames[frame_count], text=key, width=15, font='bold', bg="springgreen3")
        label.grid(row=0, column=0)
        weight_class_checkers = check_button[key][1][1]
        weight_class_names = check_button[key][1][0]
        # For each weight_class_checker create a corresponding check button
        for i in range(len(weight_class_checkers)):
            # If the check button was checked create a button for that weight class/bracket
            if weight_class_checkers[i].get() == 1:
                buttons.append(
                    tk.Button(frames[frame_count], background="springgreen3", width=8, activebackground="springgreen4",
                              fg="white",
                              text=weight_class_names[i], font=('Serif-Sans 15 bold'),
                              command=lambda screen_name="bracket", bracket_name=weight_class_names[i],
                                             button_num_ref=len(buttons): switch_screen(screen_name, bracket_name,
                                                                                     button_num_ref)))
                buttons[len(buttons) - 1].grid(row=i + 1, column=0, pady=4)

# Begin making check box in this window

    global canvas2
    canvas2 = tk.Canvas(frame2, highlightthickness=0, bg="Azure", relief="solid")
    yscrollbar = tk.Scrollbar(frame2, orient="vertical", command=canvas2.yview)
    yscrollbar.pack(side="right", fill="y")
    canvas2.pack(side="top", fill="both", expand=True)
    canvas2.configure(yscrollcommand=yscrollbar.set, bg='seashell3', width=150)
    frame_new = tk.Frame(canvas2, bg="seashell3")
    canvas2.create_window((0, 0), window=frame_new, anchor="center")
    frame_new.bind('<Configure>', set_scrollregion1)
    # Make columns for frame2
    for i in range(3):
        frame_new.columnconfigure(i, minsize=0, weight=0)
    # Create an entry field to take in the input of a competitor name to add to bracket
    input_var = tk.StringVar()
    competitor_entry = tk.Entry(frame_new, textvariable=input_var, width=15)
    competitor_entry.grid(row=0, column=0, pady=5)
    frame_count = -1
    frames = []
    for key in check_button:
        button_count = -1
        check_button[key][0].clear()
        weight_class_checkers = check_button[key][1][1]
        weight_class_checkers_2 = check_button[key][1][2]
        check_buttons = check_button[key][0]
        weight_class_names = check_button[key][1][0]
        for i in range(len(weight_class_checkers_2)):
            if weight_class_checkers[i].get() == 1:
                if button_count == -1:
                    frames.append(tk.Frame(frame_new, borderwidth=2, relief='solid'))
                    frames[len(frames) - 1].grid(row=len(frames) + 1, column=0, sticky='ns')
                    label = tk.Label(frames[len(frames) - 1], text=key, font='bold', bg="seashell4")
                    label.grid(row=0, column=0, sticky='ew')
                    frame_count += 1
                button_count += 1

                # For each weight_class_checker create a corresponding check button
                var = tk.IntVar()
                check_buttons.append(
                    tk.Checkbutton(frames[frame_count], bg="seashell3", font='Arial 10 bold', text=weight_class_names[i],
                                   variable=var,
                                   onvalue=1,
                                   offvalue=0,
                                   height=1,
                                   width=15))
                weight_class_checkers_2[i] = var
                check_buttons[button_count].grid(row=i + 1, column=0)
            else:
                weight_class_checkers_2[i] = tk.IntVar()
    submit = tk.Button(frame_new, text="Submit", bg='seashell4',
                       command=lambda name=input_var: add_to_brackets(name))
    submit.grid(row=len(frames) + 2, column=0)


def draw_menu_window(frame):
    global check_button
    frames = []
    # Create two frames to break up the window
    frame_one = tk.Frame(frame, relief='solid', borderwidth=2)
    frame_two = tk.Frame(frame, relief='solid', borderwidth=2)
    frame_one.grid(row=0, column=0)
    frame_two.grid(row=1, column=0)
    row_counter = 0
    column_counter = -1
    # Create columns and rows for those frames
    for i in range(6):
        frame_one.columnconfigure(i, minsize=10, weight=0)
        frame_two.columnconfigure(i, minsize=10, weight=0)
    frame_one.rowconfigure(0, minsize=10, weight=0)
    frame_two.rowconfigure(0, minsize=10, weight=0)
    # Create 6 frames within each of the frames above to separate out the window even more
    for i in range(12):
        if i < 6:
            column_counter += 1
            frames.append(tk.Frame(frame_one, relief='solid', borderwidth=2, bg="springgreen3"))
            frames[i].grid(row=row_counter, column=column_counter, sticky='ns')
            if i == 5:
                column_counter = -1
        else:
            column_counter += 1
            frames.append(tk.Frame(frame_two, relief='solid', borderwidth=2, bg="springgreen3"))
            frames[i].grid(row=row_counter, column=column_counter, sticky='ns')

    count = -1
    for key in check_button:
        count += 1
        # Create a label for each frame, that is the current brackets title
        label = tk.Label(frames[count], text=key, font='bold', bg="springgreen3")
        label.grid(row=0, column=0)
        weight_class_checkers = check_button[key][1][1]
        check_buttons = check_button[key][0]
        weight_class_names = check_button[key][1][0]
        # For each weight_class_checker create a corresponding check button
        for i in range(len(weight_class_checkers)):
            var = tk.IntVar()
            check_buttons.append(tk.Checkbutton(frames[count], bg="springgreen3", font='Arial 10 bold', text=weight_class_names[i], variable=var,
                                                onvalue=1,
                                                offvalue=0,
                                                height=1,
                                                width=15))
            weight_class_checkers[i] = var
            check_buttons[i].grid(row=i + 1, column=0)
    # Create a button for submitting the check buttons
    submit = tk.Button(frame, text="Submit", command=lambda screen_name="brackets": switch_screen(screen_name))
    submit.grid(row=2, column=0)


def draw_main_window(frame):
    global buttons
    # Create 3 buttons for main window
    tk.Button(frame, bg='springgreen3', text="Start", font=('Impact', 25), width=25, command=lambda screen_name="pick": switch_screen(screen_name)).grid(row=0, column=0, pady=10)
    tk.Button(frame, bg='springgreen3', text="Options", font=('Impact', 25), width=25, command=lambda screen_name="options": switch_screen(screen_name)).grid(row=1, column=0, pady=10)
    tk.Button(frame, bg='springgreen3', text="Help", font=('Impact', 25), width=25, command=lambda screen_name="help": switch_screen(screen_name)).grid(row=2, column=0, pady=10)


def updates():
    global buttons, lines, pressed, start_frame, node_button_num, brackets_button_num, menu_string, count3, count4
    if pressed:
        count3 = 0
        count4 = 0
        reset_start_frame()
        frame = draw_scrollbar()
        if menu_string == "main":
            count3 = 10
            count4 = 10
            draw_main_window(frame)
        if menu_string == "pick":
            count3 = 10
            count4 = 10
            # Reset check_button
            for key in check_button:
                check_button[key][0].clear()
                for var in check_button[key][1][1]:
                    var = 0
            draw_menu_window(frame)
        if menu_string == "bracket":
            # Reset buttons and lines
            buttons.clear()
            lines.clear()
            draw_bracket_window(brackets.get_tournament()[brackets_button_num], frame)
        if menu_string == "brackets":
            # Reset check_button
            for key in check_button:
                check_button[key][0].clear()
                for var in check_button[key][1][1]:
                    var = 0
            # Reset buttons
            buttons.clear()
            draw_brackets_window(frame)
        pressed = False

    root.after(100, updates)  # Update every 250ms


def match_result(entry, bracket):
    global pressed, node_button_num
    node_button_num = entry
    if node_button_num < bracket.get_num_nodes() - 1 and bracket.check_if_pair(
            node_button_num):  # Call bracket functions to produce a result to a match given the button pressed
        if bracket.get_bracket()[node_button_num].get_value() == bracket.find_default_next(node_button_num).get_value():
            bracket.match_undo(entry)
        else:
            bracket.match_winner(entry)
        pressed = True


def on_closing():
    root.destroy()  # End when closed


if __name__ == '__main__':
    main()
