#!/usr/bin/python3
#-*- coding: Utf-8 -*-
import re
from jinja2 import *

class Ibex_gss:
    def __init__(self):
        self.file = None
        self.feedback = 0
        self.out_file = "basic_gen.html"
        self.project_title = "ibex_in_the_jinja"
        self.use_template = "basic_page.html"

    ### this class start the convertion of the markdown file ###
    ### all begins from here when using this program... ###        
    def generate(self):
        ### first trying to read the specified template ###
        try:
            with open(self.use_template, 'r') as model:
                static_page = model.read()
        except:
            print("the specified template is not present...")

        with open(self.file, 'r') as source:
            contain = source.read()
        ### analysing the document ###
        print("searching for h6 to h1 titles")
        contain = self.per_lines(contain, "######", "<h6>", "</h6> \n")
        contain = self.per_lines(contain, "#####", "<h5>", "</h5> \n")
        contain = self.per_lines(contain, "####", "<h4>", "</h4> \n")
        contain = self.per_lines(contain, "###", "<h3>", "</h3> \n")
        contain = self.per_lines(contain, "##", "<h2>", "</h2> \n")
        contain = self.per_lines(contain, "#", "<h1>", "</h1> \n")
        print("searching for separators")
        contain = self.per_lines(contain, "------", "</p><hr />", "\n<p> ")
        print("searching for paragraphs")
        contain = self.per_lines(contain, ">>>", "<p>\n", "\n</p>")
        print("searching for code examples")
        contain = self.per_coding_example(contain, "    ", " <pre><code>\n    ", " </code></pre>\n")
        print("searching for lists")
        contain = self.per_list(contain, "+ ", "<ol>\n", "</ol>")
        contain = self.per_list(contain, "- ", "<ul>\n", "</ul>")
        print("searching for triple splat bold and italic quote")
        contain = self.per_emphasis(contain, "***", "<b><i>", "</i></b>")
        print("searching for double splat bold quote")
        contain = self.per_emphasis(contain, "**", "<b>", "</b>")
        print("searching for single splat italic quote")
        contain = self.per_emphasis(contain, "*", "<i>", "</i>")
        print("searching for headers, body, div and footers delimitation")
        contain = self.per_links(contain, "[HDR+]", "<header>")
        contain = self.per_links(contain, "[+HDR]", "</header>")
        contain = self.per_links(contain, "[FTR+]", "<footer>")
        contain = self.per_links(contain, "[+FTR]", "</footer>")
        contain = self.per_links(contain, "[BDY+]", "<body>")
        contain = self.per_links(contain, "[+BDY]", "</body>")
        contain = self.per_links(contain, "[DIV+]", "<div>")
        contain = self.per_links(contain, "[+DIV]", "</div>")
        print("searching for urls")
        contain = self.per_links(contain, "[+url]", "<a href = '")
        contain = self.per_links(contain, "[+url+]", "'>")
        contain = self.per_links(contain, "[url+]", "</a> ")
        print("searching for images")
        contain = self.per_links(contain, "[+img]", "<figure><center><img src='")
        contain = self.per_links(contain, "[img+]", "'></center></figure>")
        print("indexing the document's titles")
        contain = self.indexer(contain)
        print("extracting the links to intern chapters")
        doc_chapter = self.chapter(contain)
        print("saving the output result into .html")
        ### and there comes the output, if feedback = 0, it gives a html ###
        ### other case, it return directly the result ###
        if self.feedback == 0:         
            with open(self.out_file, 'w') as output_file:
                templ = Template(static_page)
                output_file.write(
                    templ.render(
                        page_title = self.project_title,
                        page_contains = contain,
                        page_summary = doc_chapter,
                        ))
        elif self.feedback != 0:
            templ = Template(static_page)
            output_file = templ.render(page_title, page_contains = contain)
            return output_file
        ### tell the user that the job is done ###
        print("job done !")

    ####################################################    
    ### here begins the real analyse and parsing job ###
    ####################################################

    ### this function analyse lines per lines the whole markdown file ###
    ### and puts quote for titles or separators ###
    def per_lines(self, sequence, symbol_to_modify, replace_open_parse, replace_ending_parse):
        analyse = sequence.splitlines()
        new_output = ""

        for y in analyse:
            if y.startswith(symbol_to_modify) == True:
                y = y.replace(symbol_to_modify, replace_open_parse)
                y += replace_ending_parse
                new_output += y
            else:
                new_output += y
            new_output += "\n"

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and search if there is coding exemples ###
    def per_coding_example(self, sequence, number_of_spaces, opening_parse, closing_parse):
        mark_coding = 0

        analyse = sequence.splitlines()
        new_output = ""

        for x in analyse:
            if number_of_spaces in x and mark_coding == 0:
                x = x.replace(number_of_spaces, opening_parse)
                new_output += x
                mark_coding = 1
            elif number_of_spaces in x and mark_coding == 1:
                new_output += x
            elif mark_coding == 1 and x == "":
                mark_coding = 0
                x = x.replace("", closing_parse)
                new_output += x
            else:
                new_output += x
            new_output += "\n"

        return new_output

    ### this function analyse lines per lines the whole markdonw file ###
    ### and search if there is some unordered lists ###
    def per_list(self, sequence, begins, opening_parse, closing_parse):
        mark_list = 0

        analyse = sequence.splitlines()
        new_output = ""

        for w in analyse:
            if w.startswith(begins) == True and mark_list == 0:
                w = w.replace(begins, opening_parse + "\n <li> ")
                new_output += w + " </li> "
                mark_list = 1
            elif w.startswith(begins) == True and mark_list == 1:
                w = w.replace(begins, " <li> ")
                new_output += w + " </li> "
            elif mark_list == 1 and w == "":
                mark_list = 0
                w = w.replace("", closing_parse)
                new_output += w
            else:
                new_output += w
            new_output += " \n"

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and parse bold or italic symbols ###
    def per_emphasis(self, sequence, symbol_to_modify, replace_open_parse, replace_ending_parse):
        mark_emphasis = 0
        mark_code = 0

        analyse = sequence.split(" ")
        new_output = ""
                
        for z in analyse:
            if "<pre><code>" in z:
                mark_code = 1
            elif "</code></pre>" in z:
                mark_code = 0

            if z.startswith(symbol_to_modify) == True and mark_emphasis == 0 and mark_code == 0:
                if z.endswith(symbol_to_modify) == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + " "
                elif z.endswith(symbol_to_modify + ".") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + ". "
                elif z.endswith(symbol_to_modify + "?") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + "? "
                elif z.endswith(symbol_to_modify + "!") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + "! "
                elif z.endswith(symbol_to_modify + "\n") == True:
                    z = z.split(symbol_to_modify)
                    z[0] = replace_open_parse
                    z[-1] = replace_ending_parse
                    new_output += "".join(z) + "\n"
                else:    
                    z = z.replace(symbol_to_modify, replace_open_parse)
                    mark_emphasis = 1
                    new_output += z + " "
                    
            elif symbol_to_modify in z and mark_emphasis == 0 and mark_code == 0:
                z = z.replace(symbol_to_modify, replace_open_parse)
                new_output += z + " "
                mark_emphasis = 1
                
            elif symbol_to_modify in z and mark_emphasis == 1 and mark_code == 0:
                z = z.replace(symbol_to_modify, replace_ending_parse)
                new_output += z + " "
                mark_emphasis = 0
                
            elif z.endswith(symbol_to_modify) == True and mark_emphasis == 1 and mark_code == 0:
                z = z.replace(symbol_to_modify, replace_ending_parse)
                new_output += z + " "
                mark_emphasis = 0
                
            else:
                new_output += z + " "

        return new_output

    ### this function analyse lines per lines the whole markdown file ###
    ### and parse url or images symbols ###
    def per_links(self, sequence, symbol_to_modify, replace_parse):
        mark_links = 0
        mark_code = 0

        analyse = sequence.split(" ")
        new_output = ""
                
        for z in analyse:
            if "<pre><code>" in z:
                mark_code = 1
            elif "</code></pre>" in z:
                mark_code = 0

            if symbol_to_modify in z and mark_code == 0:
                z = z.replace(symbol_to_modify, replace_parse)
                new_output += z
            else:
                new_output += z + " "

        return new_output

    ### this function do an indexation of the document and add a div='x' to <hx> quotes ###
    ### but only in the 'body'. incase of absence of any sections, it still working ###
    def indexer(self, sequence):
        analyse = sequence.splitlines()
        mark_section = 0
        counter = 0
        new_output = ""
        expression_check = r"<h(?P<number>\d)>"

        section_begins = ['<head>', '<header>', '<foot>', '<footer>']
        section_ends = ['</head>', '</header>', '</foot>', '</footer>']
        
        for x in analyse:
            
            for y in section_begins:
                if y in x:
                    mark_section = 1
            for z in section_ends:
                if z in x:
                    mark_section = 0

            extract = re.search(expression_check, x)
            if extract is not None and mark_section == 0:
                opening_symbol = f"<h{extract.group('number')}>"
                z = x.split(opening_symbol)
                #y = z[1].split(ending_symbol)
                #new_open_symbol = opening_symbol.replace(">", f" div='#{y[0]}'>")
                new_open_symbol = opening_symbol.replace(">", f" id='{counter}'>")
                z[0] = new_open_symbol
                new_output += "".join(z)
                counter += 1
            else:
                new_output += x
                
            new_output += "\n"
            
        return new_output

    ### this function extract the chapters of the body section ###
    ### it returns it in the <nav> section of the basic template ###
    def chapter(self, sequence):
        analyse = sequence.splitlines()
        dict_chapter = []
        new_dict_chapter = []

        for x in analyse:
            expression = r"<h(\d) id='(\d+)'>(?P<chapter>.*)</h(\d)>"
            try:
                extract = re.search(expression, x)
                dict_chapter.append(extract.group("chapter"))
            except:
                None
        print(dict_chapter)

        for y in range(0, len(dict_chapter)):
            includer = f"<a href='#{y}'>{dict_chapter[y]}</a>"
            new_dict_chapter.append(includer)

        print(new_dict_chapter)
        return new_dict_chapter
        


