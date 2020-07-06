#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
import sys
from survivaltool import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

class Survivaltool_gss_interface(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Survivaltool GSS interface for Python 3.x")
        self.minsize(height = 400, width = 400)
        self.resizable(height = False, width = False)
        self.use_font_title = ""
        self.use_font_rests = ""

        if sys.platform == "linux":
            self.use_font_title = "DejaVu Sans"
            self.use_font_rests = "DejaVu Sans Light"
        elif sys.platform == "win":
            self.use_font_title = "Arial Black"
            self.use_font_rests = "Arial"

        lbl_source = Label(self, text = "Source file  : ")
        lbl_source.grid(row = 1, column = 1)
        lbl_out_fl = Label(self, text = "Destination  : ")
        lbl_out_fl.grid(row = 2, column = 1)
        lbl_use_tp = Label(self, text = "Use template : ")
        lbl_use_tp.grid(row = 3, column = 1)
        lbl_title = Label(self, text = "Project title : ")
        lbl_title.grid(row = 4, column = 1)
        lbl_header = Label(self, text = "Project header : ")
        lbl_header.grid(row = 5, column = 1)
        lbl_footer = Label(self, text = "Project footer : ")
        lbl_footer.grid(row = 6, column = 1)

        self.source_entry = Entry(self, width = 20)
        self.source_entry.grid(row = 1, column = 2)
        self.out_file_entry = Entry(self, width = 20)
        self.out_file_entry.grid(row = 2, column = 2)
        self.out_file_entry.insert(1, "basic_gen.html")
        self.use_tp_entry = Entry(self, width = 20)
        self.use_tp_entry.grid(row = 3, column = 2)
        self.use_tp_entry.insert(1, "basic_page.html")
        self.title_entry = Entry(self, width = 20)
        self.title_entry.grid(row = 4, column = 2)
        self.title_entry.insert(1, "Survivaltool Page")
        self.header_entry = Entry(self, width = 20)
        self.header_entry.grid(row = 5, column = 2)
        self.header_entry.insert(1, "Generated by Survivaltool")
        self.footer_entry = Entry(self, width = 20)
        self.footer_entry.grid(row = 6, column = 2)
        self.footer_entry.insert(1, "Program under license")

        self.source_button = Button(self, text = "open", command = lambda x = "source" : self.open_file(x))
        self.source_button.grid(row = 1, column = 3)
        self.out_file_button = Button(self, text = "open", command = lambda x = "destination" : self.open_file(x))
        self.out_file_button.grid(row = 2, column = 3)
        self.use_tp_button = Button(self, text = "open", command = lambda x = "template" : self.open_file(x))
        self.use_tp_button.grid(row = 3, column = 3)
        self.title_button = Button(self, text = "clean", command = lambda x = "title" : self.cleaner(x))
        self.title_button.grid(row = 4, column = 3)
        self.header_button = Button(self, text = "clean", command = lambda x = "header" : self.cleaner(x))
        self.header_button.grid(row = 5, column = 3)
        self.footer_button = Button(self, text = "clean", command = lambda x = "footer" : self.cleaner(x))
        self.footer_button.grid(row = 6, column = 3)

        self.generation_button = Button(self, text = "Generate !", command = self.generating)
        self.generation_button.grid(row = 20, column = 1, columnspan = 2)
        self.byebye_button = Button(self, text = "Exit...", command = self.quit)
        self.byebye_button.grid(row = 20, column = 2, columnspan = 2)
        
        self.mainloop()
        try:
            self.destroy()
        except TclError:
            sys.exit()

    def open_file(self, selection):
        source = askopenfilename(filetypes = [("text", ".txt"), ("markdown", ".md"), ("html", ".html")])
        if selection == "source":
            self.source_entry.delete(0, 10000)
            self.source_entry.insert(0, source)
        elif selection == "destination":
            self.out_file_entry.delete(0, 10000)
            self.out_file_entry.insert(0, source)
        elif selection == "template":
            self.use_tp_entry.delete(0, 10000)
            self.use_tp_entry.insert(0, source)

    def cleaner(self, selection):
        if selection == "title":
            self.title_entry.delete(0, 10000)
        elif selection == "header":
            self.header_entry.delete(0, 10000)
        elif selection == "footer":
            self.footer_entry.delete(0, 10000)

    def generating(self):
        srv = Survivaltool_gss()
        srv.file = self.source_entry.get()
        srv.feedback = 0
        srv.out_file = self.out_file_entry.get()
        srv.use_template = self.use_tp_entry.get()
        srv.project_title = self.title_entry.get()
        srv.project_header = self.header_entry.get()
        srv.project_footer = self.footer_entry.get()
        try:
            srv.generate()
            showinfo("okay !", "the job is done !")
        except:
            showwarning("no no no...", "cannot do the job, something is missing somewhere !")
            
run = Survivaltool_gss_interface()
run