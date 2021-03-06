import os
import sys
import tkinter as tk
import argparse
from tkinter.filedialog import askopenfilename
from typing import Tuple, Dict
import json

import interactive_map_maker_helper_functions

from PIL import Image

areas_of_interest = dict()


def smaller(x, y):
    return x if x <= y else y


def bigger(x, y):
    return y if x <= y else x


def rect_koords(x1, y1, x2, y2):
    return (smaller(x1, x2), smaller(y1, y2), bigger(x1, x2), bigger(y1, y2))


def draw_rectangle(widget, x1, y1, x2, y2):
    (x1, y1, x2, y2) = rect_koords(x1, y1, x2, y2)
    #print(x1, y1, x2, y2)
    widget.create_rectangle(x1, y1, x2, y2, outline="red")


def second_callback(event, first_koords):
    print("Test", event.x, event.y)
    rect_koords_2 = (event.x, event.y)
    event.widget.bind("<Button-1>", first_callback, add='')
    event.widget.config(cursor="arrow")
    x1, y1, x2, y2 = *first_koords, *rect_koords_2
    #print(first_koords, rect_koords_2)
    draw_rectangle(event.widget, x1, y1, x2, y2)
    create_text_input((x1, y1), (x2, y2))


def clicked_inside_existing_area_of_interest(event):
    global areas_of_interest
    return any([is_in_rect(k, (event.x, event.y)) for k in areas_of_interest.keys()])


def first_callback(event):
    rect_koords_1 = (event.x, event.y)
    if clicked_inside_existing_area_of_interest(event):
        print("inside generated rect")
        rectangle = coords_of_containing_existing_rect(
            rect_koords_1, areas_of_interest)
        create_text_input(*rectangle, areas_of_interest[rectangle])
        return True
    print("clicked at", event.x, event.y, event.widget)
    # https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
    event.widget.bind("<Button-1>", lambda event,
                      koords=rect_koords_1: second_callback(event, koords), add='')
    event.widget.config(cursor="cross")


def strg_w_pressed(event, koord_1, koord_2):
    print(event.widget.winfo_parent())
    parent = event.widget.master.master
    # print(koord_1,koord_2,event.widget.get("0.0",tk.END))
    description = event.widget.get("0.0", tk.END)
    global areas_of_interest
    areas_of_interest[(koord_1, koord_2)] = description[0:-
                                                        1].replace('\n', ' ')
    # print(areas_of_interest,areas_of_interest_keys_as_values())
    parent.destroy()


def link_file(event):
    f_name = askopenfilename()
    print(f_name)
    surround_selection_with(
        event, '<a href="'+os.path.relpath(f_name, filename)+'">', "</a>")


def surround_selection_with(event, tag_start, tag_end):
    #selection_start = event.widget.SEL_FIRST
    #selection_end = event.widget.SEL_LAST
    try:
        event.widget.insert(tk.SEL_FIRST, tag_start)
        event.widget.insert(tk.SEL_LAST, tag_end)
    except:
        pass


def create_text_input(koord_1, koord_2, content=""):
    top = tk.Toplevel()
    main_frame = tk.Frame(top)
    button_frame = tk.Frame(main_frame)
    # shortcuts and buttons for <b>selection</b>,<br>,<i>selection</i>, <a> extern und intern
    tk.Label(button_frame,
             text="str-b:bold;\tstr-j:italic;\tstr-r:<br>;\tstr-l:<a href ...").pack()
    button_frame.pack()
    text = tk.Text(main_frame)
    text.insert(tk.END, content)
    text.bind("<Control-b>", lambda event, start="<b>",
              end="</b>": surround_selection_with(event, start, end))
    text.bind("<Control-j>", lambda event, start="<i>",
              end="</i>": surround_selection_with(event, start, end))

#    text.bind("<Control-l>", link_file)
    text.bind("<Control-l>", lambda event, start='<a href="">',
              end="</a>": surround_selection_with(event, start, end))
    text.bind("<Control-r>", lambda event: text.insert(tk.INSERT, "<br>"))
    top.bind("<Control-w>", lambda event, k1=koord_1,
             k2=koord_2: strg_w_pressed(event, k1, k2))
    text.focus_set()
    # top.protocol("WM_DELETE_WINDOW",text_window_closed(top))
    text.pack()
    main_frame.pack()

# top.destroy()


def quit_prog(event):
    print("tSCHÜSS", areas_of_interest)
    global basename
    # save to disk
    # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
    #print(json.dumps(areas_of_interest_keys_as_values(), ensure_ascii=False,indent=4))
    with open(basename+".js", 'w', encoding='utf8') as json_file:
        json_file.write("var rooms = ")
        json.dump(areas_of_interest_keys_as_values(),
                  json_file, ensure_ascii=False)
    event.widget.destroy()


def is_in_rect(rect_koords: Tuple[int, int, int, int], koords: Tuple[int, int]) -> bool:
    upper_left, lower_right = rect_koords
    x1, y1 = upper_left
    x2, y2 = lower_right
    x, y = koords
    return (x1 <= x and x <= x2) and (y1 <= y and y <= y2)


def coords_of_containing_existing_rect(click_coords: Tuple[int, int],coords_dict: Dict[Tuple[int, int, int, int], str]):
    print(click_coords)
    ret = [k for k in coords_dict.keys() if is_in_rect(k, click_coords)]
    return ret[0]


def areas_of_interest_keys_as_values():
    global reduction_factor
    ret = dict()
    for key in areas_of_interest.keys():
        tmp = areas_of_interest[key]
        # print(tmp)
        p1, p2 = key
        x1, y1 = p1
        x2, y2 = p2
        val = [x * reduction_factor for x in [x1, y1, x2, y2]]
        ret[tmp] = val
    return ret


parser = argparse.ArgumentParser(description='Create an interactive map')
parser.add_argument(
    '--filename', help='image file to create map from', default=None)
args = parser.parse_args()
print(args.filename)
print(sys.argv)


root = tk.Tk()
# https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(screen_width, screen_height)

template_dir = os.path.dirname(sys.argv[0])
# print(template_dir)

if args.filename is None:
    quit()
else:
    filename = args.filename


# You should only create one root widget for each program, and it must be created before any other widgets.


# w = tk.Label(root, text = "Hello world")


displ = tk.PhotoImage(file=filename)
# not working: https://stackoverflow.com/questions/24745857/python-pillow-how-to-scale-an-image
#maxsize = (screen_width, screen_height)
#im.thumbnail(maxsize, Image.ANTIALIAS)

# https://stackoverflow.com/questions/6582387/image-resize-under-photoimage

reduction_factor = 1

while (screen_width < displ.width() or screen_height < displ.height()):
    displ = displ.subsample(2)
    reduction_factor *= 2

c = tk.Canvas(root, width=displ.width(), height=displ.height())
c.bind("<Button-1>", first_callback)
c.pack()
c.create_image(displ.width() / 2, displ.height() / 2, image=displ)

basename = os.path.splitext(os.path.basename(filename))[0]

if not os.path.isfile(basename+".html"):
    with open(os.path.join(template_dir, 'Vorlage.html')) as f:
        template = f.read()

    file_1_contents = (template.replace("INSERT_IMAGE_FILE_NAME",
                                        filename)).replace("INSERT_TITLE", basename)

    with open(basename+".html", 'w', encoding='utf8') as html_file:
        html_file.write(file_1_contents)
else:
    areas_of_interest = interactive_map_maker_helper_functions.load_areas_of_interest_from_file(
        basename + ".js", reduction_factor)
    for k in areas_of_interest.keys():
        p1, p2 = k
        x1, y1, x2, y2 = *p1, *p2
        draw_rectangle(c, x1, y1, x2, y2)


root.bind("<Control-q>", quit_prog)

root.mainloop()
