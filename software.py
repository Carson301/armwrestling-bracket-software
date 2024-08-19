#
#
#

import tkinter as tk
import SingleBracket
import DoubleBracket


def main():
    global root
    root = tk.Tk()
    window_width = "1000"
    window_height = "500"
    root.geometry(window_width + "x" + window_height)  # Sets dimensions of window
    root.title("Arm Wrestling Tournament")  # Gives the window a title

    title_label = tk.Label(root, text="Arm Wrestling Tournament", font=('Impact', 10), fg="white")  # Gives another title for the window, but inside the window
    title_label.pack(padx=1, pady=1)

    global canvas

    canvas = tk.Canvas(root, highlightthickness=0, bg="Azure")

    # Create scrollbars
    xscrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    yscrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    yscrollbar.pack(side="right", fill="y")
    xscrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="top", fill="both", expand=True)

    # Attach canvas to scrollbars
    canvas.configure(xscrollcommand=xscrollbar.set)
    canvas.configure(yscrollcommand=yscrollbar.set)

    # Create frame inside canvas
    entries_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=entries_frame, anchor="nw")
    entries_frame.bind('<Configure>', set_scrollregion)

    entries_frame.configure(bg="Azure")
    root.configure(bg="SpringGreen4")
    title_label.configure(bg="SpringGreen4", pady=5)


    root.protocol("WM_DELETE_WINDOW", on_closing)  # Calls on_closing when window is closed

    updates()  # Update window periodically

    root.mainloop()  # Keep window open

def match_result():
    pass
def draw_bracket_window(bracket, frame):
    global buttons
    buttons = []
    lines = []
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
                    buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[i].get_value(), font=('Sans-Serif 8 bold'), command=lambda node_counter1=node_counter: match_result(node_counter1)))

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
                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[j].get_value(), font=('Sans-Serif 8 bold'), command=lambda node_counter1=node_counter: match_result(node_counter1)))

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
                        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="black", text=level[j].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=node_counter: match_result(node_counter1)))
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
        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][0].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=bracket.get_num_nodes() - 3: match_result(node_counter1)))
        buttons[len(buttons) - 1].grid(row=4, column=int(bracket.get_num_levels() / 2) - 1, sticky=tk.W + tk.E, padx=5, pady=0)

        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 2][1].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=bracket.get_num_nodes() - 2: match_result(node_counter1)))
        buttons[len(buttons) - 1].grid(row=4, column=int(bracket.get_num_levels() / 2) + 1, sticky=tk.W + tk.E, padx=5, pady=0)

        buttons.append(tk.Button(frame, background="springgreen3", activebackground="springgreen4", fg="white", text=levels[len(levels) - 1][0].get_value(), font=('Serif-Sans 8 bold'), command=lambda node_counter1=bracket.get_num_nodes() - 1: match_result(node_counter1)))
        buttons[len(buttons) - 1].grid(row=2, column=int(bracket.get_num_levels() / 2), sticky=tk.W + tk.E, padx=5, pady=0)


def updates():
        root.after(100, updates)  # Update every 250ms

def on_closing():
    root.destroy()  # End when closed

def set_scrollregion( event):
    global canvas
    canvas.configure(scrollregion=canvas.bbox('all'))





if __name__ == '__main__':
    main()