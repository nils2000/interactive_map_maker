import tkinter as tk
import argparse
from PIL import Image

areas_of_interest = dict()

def smaller(x,y):
	return x if x <= y else y

def bigger(x,y):
	return y if x <= y else x

def rect_koords(x1,y1,x2,y2):
	return (smaller(x1,x2),smaller(y1,y2),bigger(x1,x2),bigger(y1,y2))

def second_callback(event,first_koords):
	print("Test",event.x,event.y)
	rect_koords_2 = (event.x,event.y)
	event.widget.bind("<Button-1>",first_callback,add='')
	event.widget.config(cursor="arrow")
	print(first_koords,rect_koords_2)
	(x1,y1,x2,y2) = rect_koords(*first_koords,*rect_koords_2)
	print(x1,y1,x2,y2)
	event.widget.create_rectangle(x1,y1,x2,y2,outline="red")
	create_text_input((x1,y1),(x2,y2))

def first_callback(event):
	if clicked_inside_existing_area_of_interest(event):
		print("inside generated rect")
	rect_koords_1 = (event.x,event.y)
	print("clicked at", event.x, event.y, event.widget)
	#https://stackoverflow.com/questions/3296893/how-to-pass-an-argument-to-event-handler-in-tkinter
	event.widget.bind("<Button-1>",lambda event,koords=rect_koords_1: second_callback(event,koords),add='')
	event.widget.config(cursor="cross")

def strg_w_pressed(event,koord_1,koord_2):
	print(event.widget.winfo_parent())
	parent = event.widget.master
	#print(koord_1,koord_2,event.widget.get("0.0",tk.END))
	description = event.widget.get("0.0",tk.END)
	global areas_of_interest
	areas_of_interest[(koord_1,koord_2)] = description
	print(areas_of_interest)
	parent.destroy()

def create_text_input(koord_1,koord_2):
	top = tk.Toplevel()
	text = tk.Text(top)
	text.insert(tk.END,"Hello")
	top.bind("<Control-w>",lambda event,k1=koord_1,k2=koord_2:strg_w_pressed(event,k1,k2))
	text.focus_set()
	#top.protocol("WM_DELETE_WINDOW",text_window_closed(top))
	text.pack()
	#top.destroy()
	
def quit_prog(event):
	event.widget.destroy()

def is_in_rect(rect_koords,koords):
	upper_left,lower_right = rect_koords
	x1,y1 = upper_left
	x2,y2 = lower_right
	x,y = koords
	return (x1 <= x and x <= x2) and (y1 <= y and y <= y2)

def clicked_inside_existing_area_of_interest(event):
	global areas_of_interest
	return any([is_in_rect(k,(event.x,event.y)) for k in areas_of_interest.keys()])
		

parser = argparse.ArgumentParser(description='Create an interactive map')
parser.add_argument('file_name', help='image file to create meap from')
args = parser.parse_args()
print(args.file_name)

im = Image.open(args.file_name)
print(im.size)

(image_width,image_height) = im.size

#You should only create one root widget for each program, and it must be created before any other widgets.
root = tk.Tk()

#w = tk.Label(root, text = "Hello world")
c = tk.Canvas(root,width=image_width,height=image_height)
c.bind("<Button-1>",first_callback)
c.pack()

img=tk.PhotoImage(file=args.file_name)
c.create_image(image_width/2,image_height/2,image=img)

root.bind("<Control-q>",quit_prog)

root.mainloop()


