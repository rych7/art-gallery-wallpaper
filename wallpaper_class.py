import os
from tkinter import *
from tkinter import ttk
from PIL import Image
import requests
from selenium import webdriver
from io import BytesIO
import ctypes

categories = ["trending", "anime_manga", "illustration", "concept_art", "science_fiction", "abstract", "fantasy", "game_art"]
category = "trending"
search_url = "https://www.artstation.com/?sort_by=trending"
thumbnails = set()
s_width = 0
s_height = 0
gap_pc = 5    #gap percentage
gap = 0
rows = 4
cols = 4
max_images = rows*cols

class Gui(Frame):
    def __init__(self, master=None):
        global s_height, s_width, gap, max_images, rows, cols
        Frame.__init__(self,master)
        self.master = master
        self.rows_input = IntVar()
        self.cols_input = IntVar()
        self.gap_input = IntVar()
        self.cat_input = StringVar()

        enter_rows = Spinbox(root, from_= 1, to = 5, textvariable = self.rows_input, command=self.set_rows, wrap = False)
        enter_cols = Spinbox(root, from_= 1, to = 6, textvariable = self.cols_input, command=self.set_cols, wrap = False)
        #select category from list
        select_cat = ttk.Combobox(root, textvariable = self.cat_input)
        select_cat.bind('<<ComboboxSelected>>', self.set_cat)
        select_cat['values'] = categories
        select_cat['state'] = 'readonly'
        #labels
        cat_label = Label(text="Select a category:")
        row_label = Label(text="Rows:")
        col_label = Label(text="Columns:")
        gap_label = Label(text="Choose gap size (%)")
        #update background
        update_btn = Button(root, text="Set Background", command=update_bkgd)
        #gap slider
        gap_slider = Scale(root, from_=0, to=10, orient="horizontal", variable = self.gap_input, command=self.set_gap)
        #place items on grid
        row_label.grid(row=1, column=1)
        enter_rows.grid(row=1, column=2)
        col_label.grid(row=1, column=3)
        enter_cols.grid(row=1, column=4)
        gap_label.grid(row=2, column=1)
        gap_slider.grid(row=2,column=2)
        cat_label.grid(row=3, column=1)
        select_cat.grid(row=3, column=2)
        update_btn.grid(row = 4, column = 2)
        #######
        #get screen resolution
        s_width = root.winfo_screenwidth()  #screen width
        s_height = root.winfo_screenheight() #screen height
    def set_cat(self, master):
        global category
        category = self.cat_input.get()
        print("category="+str(category))
    def set_gap(self, master):
        global gap_pc
        gap_pc = self.gap_input.get()
        print('gap='+str(gap_pc))
    def set_rows(self):
        global rows
        rows = self.rows_input.get()
        print('rows='+str(rows))
    def set_cols(self):
        global cols
        cols = self.cols_input.get()
        print('rows='+str(cols))

def update_bkgd():
    global max_images, gap
    max_images = rows*cols
    gap = .01*gap_pc*s_height
    set_url()
    fetch_images()
    collage()
    set_backgd()
    print("Wallpaper updated.")

def set_url():
    global search_url
    if category in categories:
        if category == "trending":
            search_url = "https://www.artstation.com/?sort_by=trending"
        else:
            search_url = "https://www.artstation.com/channels/"+category+"?sort_by=trending"

def fetch_images():
    global thumbnails
    thumbnails.clear()
    #path for ChromeDriver here
    PATH = "C:/Users/rchum/source/Projects/chromedriver_win32/chromedriver"
    wd = webdriver.Chrome(executable_path=PATH)
    wd.get(search_url)
    elements = wd.find_elements_by_class_name("d-block")
    #store thumbnail urls in array
    for x in range(max_images):
        t = elements[x].get_attribute("src")
        if t:
            thumbnails.add(t)
    wd.quit()

def collage():
    #create new image
    new_image = Image.new('RGBA', (s_width, s_height), (0, 0, 0, 1))
    img_height = int(((.9-.01*gap_pc*(rows-1))*s_height)/rows)
    x_start = int((s_width-(img_height*cols+gap*(cols-1)))/2)
    y_start = int(.05*s_height)
    x = 0
    y = 0
    try:
        for url in thumbnails:
            #open url using requests
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            r_img = img.resize((img_height, img_height))
            #paste image to indexed location
            new_image.paste(r_img, (int(x_start+img_height*x+gap*x), int(y_start+img_height*y+gap*y)))
            #update index
            x += 1
            if x == cols:
                y += 1
                x = 0
    except IOError:
        print("error")
        pass
    new_image.save("C:/Users/rchum/Pictures/output_image.png")

def set_backgd():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:/Users/rchum/Pictures/output_image.png" , 0)


if __name__ == "__main__":
    root = Tk()
    window = Gui(root)
    root.mainloop()
    #set_url()
    #fetch_images()
    #collage()
    #set_backgd()


