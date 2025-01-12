from customtkinter import *
from tkinter import *


def MenuButtonTemplate(root, font, color=['#5c6d77', '#23a8f2', '#1c86c1']):
    return lambda text, onClick, selected=None: MenuButton(root, text, font, onClick, color, selected)


def MenuButton(root, text, font, onClick, color=['#5c6d77', '#23a8f2','#1c86c1'], selected=False):
    label = Label(root, text=text, font=(font))
    isSelected = selected
    label.config(foreground=color[0], background='#212325')

    def onSelect(e):
        nonlocal isSelected
        isSelected = True
        label.config(foreground=color[1])

    def onDeSelect(e):
        nonlocal isSelected
        isSelected = False
        label.config(foreground=color[0])

    # On creation
    if selected:
        onSelect(None)

    # Bind the Enter and Leave Events to the Button
    label.bind('<ButtonRelease-1>', lambda e: onClick())
    label.bind('<Leave>', lambda e: label.config(
        foreground=color[0]) if not isSelected else label.config(foreground=color[1])) 
    label.bind('<Enter>', lambda e: label.config(
        foreground=color[2]))

    label.bind("<<MenuSelect>>", onSelect)
    label.bind("<<MenuDeSelect>>", onDeSelect)

    return label


def NotebookPage(root, width, height):
    page_frame = CTkFrame(master=root, width=width, height=height,
                          corner_radius=10)

    # Create a canvas for the scrollbar
    scrollbar_canvas = CTkCanvas(
        page_frame, width=page_frame["width"]-70, height=page_frame["height"])
    scrollbar_canvas.grid(column=0, row=0, sticky="news", padx=10, pady=10)

    # Add a scrollbar to the canvas
    scrollbar = CTkScrollbar(
        page_frame, command=scrollbar_canvas.yview)
    scrollbar.grid(column=0, row=0, sticky="nes")

    # Configure canvas
    scrollbar_canvas.configure(
        yscrollcommand=scrollbar.set, bg='#2a2d2e', highlightthickness=0)
    scrollbar_canvas.bind('<Configure>', lambda e: scrollbar_canvas.configure(
        scrollregion=scrollbar_canvas.bbox("all")))

    content_frame = CTkFrame(
        scrollbar_canvas)

    scrollbar_canvas.create_window(
        (0, 0), window=content_frame, anchor="nw", width=page_frame["width"]-80)

    def _on_mousewheel(event):
        scrollbar_canvas.yview_scroll(round(-1*(event.delta/120)), "units")

    # let's handle this on the thing that lets select things.
    # TODO: unspahget this part
    #content_frame.bind_all("<MouseWheel>", _on_mousewheel)

    return (page_frame, content_frame, _on_mousewheel)


def SettingsLabel(master, text):
    label = CTkLabel(master=master, text=text,
                     text_font=('Ariel', 18, 'bold'), bg_color='#2a2d2e', text_color='#a8d6f2', anchor='w', justify=LEFT)
    return label


def SettingsDesc(master, text):
    label = CTkLabel(master=master, text=text,
                     text_font=('Ariel', 12), bg_color='#2a2d2e', text_color='#a8d6f2', anchor='w', wraplength=600, justify=LEFT)
    return label


def NumberSetting(master, placeholder_text, title, desc, order):
    SettingsLabel(master=master, text=title).grid(
        column=0, row=order*2, sticky='w')
    SettingsDesc(master=master, text=desc).grid(
        column=0, row=order*2+1, sticky='w', pady=(0, 10))
    entry = CTkEntry(master=master, justify=RIGHT,
                     width=100, placeholder_text=placeholder_text)
    entry.grid(column=1, row=order*2, sticky="e")
    return entry


def OptionMenuSetting(master, title, desc, order, options):
    # TODO: make sure this works.
    SettingsLabel(master=master, text=title).grid(
        column=0, row=order*2, sticky='w')
    SettingsDesc(master=master, text=desc).grid(
        column=0, row=order*2+1, sticky='w', pady=(0, 10))
    combo_box = CTkComboBox(master=master,
                            values=options)
    combo_box.grid(column=1, row=order*2, sticky="e")

    return combo_box
