import os
import tkinter as tk
import argparse
from tkinter.filedialog import askopenfilename
from typing import Tuple, Dict

from PIL import Image

areas_of_interest = dict()


def smaller(x, y):
    return x if x <= y else y


def bigger(x, y):
    return y if x <= y else x


def rect_koords(x1, y1, x2, y2):
    return (smaller(x1, x2), smaller(y1, y2), bigger(x1, x2), bigger(y1, y2))


def second_callback(event, first_koords):
    print("Test", event.x, event.y)
    rect_koords_2 = (event.x, event.y)
    event.widget.bind("<Button-1>", first_callback, add='')
    event.widget.config(cursor="arrow")
    print(first_koords, rect_koords_2)
    (x1, y1, x2, y2) = rect_koords(*first_koords, *rect_koords_2)
    print(x1, y1, x2, y2)
    event.widget.create_rectangle(x1, y1, x2, y2, outline="red")
    create_text_input((x1, y1), (x2, y2))


def clicked_inside_existing_area_of_interest(event):
    global areas_of_interest
    return any([is_in_rect(k, (event.x, event.y)) for k in areas_of_interest.keys()])


def first_callback(event):
    rect_koords_1 = (event.x, event.y)
    if clicked_inside_existing_area_of_interest(event):
        print("inside generated rect")
        rectangle = coords_of_containing_existing_rect(rect_koords_1,areas_of_interest)
        create_text_input(*rectangle,areas_of_interest[rectangle])
        return True
    print("clicked at", event.x, event.y, event.widget)
    # https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
    event.widget.bind("<Button-1>", lambda event, koords=rect_koords_1: second_callback(event, koords), add='')
    event.widget.config(cursor="cross")


def strg_w_pressed(event, koord_1, koord_2):
    print(event.widget.winfo_parent())
    parent = event.widget.master
    # print(koord_1,koord_2,event.widget.get("0.0",tk.END))
    description = event.widget.get("0.0", tk.END)
    global areas_of_interest
    areas_of_interest[(koord_1, koord_2)] = description[0:-1]
    print(areas_of_interest)
    parent.destroy()


def create_text_input(koord_1, koord_2, content="hello"):
    top = tk.Toplevel()
    text = tk.Text(top)
    text.insert(tk.END, content)
    top.bind("<Control-w>", lambda event, k1=koord_1, k2=koord_2: strg_w_pressed(event, k1, k2))
    text.focus_set()
    # top.protocol("WM_DELETE_WINDOW",text_window_closed(top))
    text.pack()


# top.destroy()

def quit_prog(event):
    event.widget.destroy()


def is_in_rect(rect_koords: Tuple[int, int, int, int], koords: Tuple[int, int]) -> bool:
    upper_left, lower_right = rect_koords
    x1, y1 = upper_left
    x2, y2 = lower_right
    x, y = koords
    return (x1 <= x and x <= x2) and (y1 <= y and y <= y2)


def coords_of_containing_existing_rect(click_coords: Tuple[int, int],
                                       coords_dict: Dict[Tuple[int, int, int, int], str]):
    print(click_coords)
    ret = [k for k in coords_dict.keys() if is_in_rect(k, click_coords)]
    return ret[0]


parser = argparse.ArgumentParser(description='Create an interactive map')
parser.add_argument('--filename', help='image file to create map from', default=None)
args = parser.parse_args()
print(args.filename)

root = tk.Tk()

if args.filename is None:
    filename = "ZentarimVersteckLagerhaus.png"
else:
    filename = args.filename

print(filename)

im = Image.open(filename)
print(im.size)

(image_width, image_height) = im.size

# You should only create one root widget for each program, and it must be created before any other widgets.


# w = tk.Label(root, text = "Hello world")
c = tk.Canvas(root, width=image_width, height=image_height)
c.bind("<Button-1>", first_callback)
c.pack()

img = tk.PhotoImage(file=filename)
c.create_image(image_width / 2, image_height / 2, image=img)

root.bind("<Control-q>", quit_prog)

root.mainloop()


#TODO: save to html
