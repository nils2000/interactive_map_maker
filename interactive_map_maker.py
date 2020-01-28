import os
import tkinter as tk
import argparse
from tkinter.filedialog import askopenfilename
from typing import Tuple, Dict

from PIL import Image

areas_of_interest = dict()

template = """<!DOCTYPE html>
<html>
<!--https://www.mediaevent.de/tutorial/svg-image.html-->

<head>
    <script>
    	var window_height = window.innerHeight;
    	var window_width = window.innerWidth;
    	var my_image = new Image();
		my_image.src = 'INSERT_IMAGE_FILE_NAME';
        var image_height = my_image.height;
        var image_width = my_image.width;
    </script>
    <meta charset='utf-8'>
    <title>INSERT_TITLE</title>
    <style>
  
        @media (min-width: 500px) {
            .svgbg {
                background-image: url('INSERT_IMAGE_FILE_NAME');
                background-size: contain;
                background-repeat: no-repeat;
            
            }
                .descr_link {
            fill-opacity: 0.3;
            color: white;
        }
        }
    </style>
</head>

<body>
	<div style="width: 100%" onclick="dragged(event)">
			<button draggable="true" style="margin-left: 70%" ondrag="dragged(event)">Test</button>
	</div>
    <div style="float:right; background-color: lightgrey; width:50%;height:50%;">
        <div id="description" style="float:right; background-color: lightgrey; width:100%;height:50%;">
        Hier kommt die Beschreibung hin ...
        </div>
            <div id="monster" style="float:right; background-color: lightpink; width:100%;height:50%;">
        Hier die Monsterwerte .....
        </div> 
    </div>
    <svg id="map" class="svgbg" width="50%" height="800">
    </svg>

    <script>
        function describe(num) {
            let descr_div = document.getElementById("description");
            descr_div.innerHTML = beschreibung[num];
        }
        let beschreibung = Object();
        beschreibung[""] = ``;
        beschreibung[""] = ``;
        beschreibung[""] = ``;
        beschreibung[""] = ``;
        beschreibung[""] = ``;
        beschreibung[""] = ``;
        beschreibung[""] = ``;

        
           function rect_elem(x1, y1, x2, y2) {
            //var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            //svg.setAttributeNS(null, "id", "map");
            //svg.setAttributeNS(null, "class", "svgbg");
            //svg.setAttributeNS(null, "height", "100%");
            //svg.setAttributeNS(null, "width", "50%");
            //svg.setAttributeNS(null, "viewBox", "0 0 452 828");

            //document.getElementsByTagName('body')[0].appendChild(svg);
            

            //var txtElem = document.createElementNS("http://www.w3.org/2000/svg", "text");
            //txtElem.setAttributeNS(null, "x", 20);
            //txtElem.setAttributeNS(null, "y", 40);
            var canvas = document.getElementById("map");
            var conv_fact = 800/image_height;
            var rectElem = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            rectElem.setAttributeNS(null, "x", x1 * conv_fact);
            rectElem.setAttributeNS(null, "y", y1 * conv_fact);
            rectElem.setAttributeNS(null, "width", (x2 - x1) * conv_fact);
            rectElem.setAttributeNS(null, "height", (y2 - y1) * conv_fact);
            rectElem.setAttributeNS(null, "class", "descr_link");
            return rectElem;

        }
        
        function add_description_link(room, x1, y1, x2, y2){
            var rectElem = rect_elem(x1, y1, x2, y2);
            rectElem.setAttributeNS(null, "onclick", "describe('" + room + "')");


            //var theText = "Hello World! This is SVG Text created with JavaScript.";
            //var theMSG = document.createTextNode(theText);
            //txtElem.appendChild(theMSG);
            var svgDoc = document.getElementById('map');
            svgDoc.appendChild(rectElem);
            }
            
            function add_svg_anchor(target, x1, y1, x2, y2){
            var rectElem = rect_elem(x1, y1, x2, y2);
            rectElem.setAttributeNS(null,"onclick", "change_location('"+target+"')");
            var svgDoc = document.getElementById('map');
            svgDoc.appendChild(rectElem);
            }
        function change_location(target){
            window.location.href = target;
            }
            
            add_description_link("38",594,999,1517,1775);
            
            add_svg_anchor("Gewölbe1.html",33,569,336,777);

        sample = a=>{return a[Math.floor(Math.random()*a.length)];}

        function dragged(ev){
        	console.log(ev);
        }
            
    </script>
        }
</body>

</html>
"""

#print(template)

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
    
basename = os.path.splitext(os.path.basename(filename))[0]

file_1_contents = (template.replace("INSERT_IMAGE_FILE_NAME",filename)).replace("INSERT_TITLE",basename)

print(file_1_contents)

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
