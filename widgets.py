import tkinter as tk


def label(root, text, x=0, y=0, **kwargs):
    widget = tk.Label(root, text=text)
    widget.place(x=x, y=y)

    if kwargs: widget.config(**kwargs)

    return widget


def button(root, text, x=0, y=0, command=None, **kwargs):
    widget = tk.Button(root, text=text, command=command)
    widget.place(x=x, y=y)

    if kwargs: widget.config(**kwargs)

    return widget


def entry(root, x=0, y=0, **kwargs):
    widget = tk.Entry(root)
    widget.place(x=x, y=y)

    if kwargs: widget.config(**kwargs)

    return widget


def listbox(root, x=0, y=0, **kwargs):
    widget = tk.Listbox(root, selectmode=tk.SINGLE)
    widget.place(x=x, y=y)

    if kwargs: widget.config(**kwargs)

    return widget