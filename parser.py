# PARSER für DINKEL <=> HTML

import sys
import bs4
from bs4 import BeautifulSoup

def parse(inp):
    xml = ""
    lines = [line.replace("(DINKEL PUNKT BEFREIUNGS ZEICHEN)", ".") for line in inp.split(".")]
    has_open = False
    for l in lines:
        l = l.strip()
        if not l.startswith("setze") and has_open:
            has_open = False
            xml += ">"
        if l.startswith("beginne"):
            keyword = l.split(" ")[-1]
            xml += "<" + keyword
            has_open = True
        elif l.startswith("beende"):
            keyword = l.split(" ")[-1]
            xml += "</" + keyword + ">"
        elif l.startswith("literarisch"):
            xml += " ".join(l.split(" ")[1:])
        elif l.startswith("setze"):
            if not has_open:
                print("Hey bro falsch: " + l)
                sys.exit(420)
            words = l.split(" ")
            keyword = words[1]
            value = " ".join(words[3:])
            xml += " " + keyword + "=\"" + value + "\""
    return xml

def backparse(inp):
    soup = BeautifulSoup(inp.replace(".", "(DINKEL PUNKT BEFREIUNGS ZEICHEN)"), features="lxml")
    return rec_backparse(soup.html)
        
def rec_backparse(tag):
    if tag.name == "script":
        return ""
    string = ""
    string += "beginne " + tag.name + ". "

    for key in tag.attrs:
        if isinstance(tag.attrs[key], list):
            tag.attrs[key] = " ".join(tag.attrs[key]) 
        string += "setze " + key + " auf " + tag.attrs[key] + ". "
    for child in tag.children:
        if isinstance(child, bs4.element.Tag):
            string += rec_backparse(child)
        elif isinstance(child, bs4.element.NavigableString):
            s = child.string
            s = s.replace("\n", "").strip()
            if s == "":
                continue
            string += "literarisch " + s + ". "
    string += "beende " + tag.name + ". "
    return string

def dinkelhtml(inp):
    content = backparse(inp)
    html = ""
    html += "<DINKELKASTEN>\n"
    html += content + "\n"
    html += "</DINKELKASTEN>\n"
    html += "<NODINKEL> <!-- Manche Brauser unterstützen leider noch kein DINKEL. Daher dieses Skript, das das Dinkel im Dinkelkasten in den inferioren Standard \"HTML\" übersetzt !--> <SCRIPT src=\"parse.js\"></SCRIPT></NODINKEL>"
    return html
        

def main():
    if len(sys.argv) > 4:
        print("Usage: python parser.py [method=parse|backparse|dinkelhtml] [file] [outfile]")
    inp = ""
    if len(sys.argv) <= 2:
        inp = input()
    else:
        f = sys.argv[2]
        handle = open(f)
        inp = handle.read()
        handle.close()

    save_out = len(sys.argv) > 3
    
    output = None
    if sys.argv[1] == "parse":
        output = parse(inp)
    elif sys.argv[1] == "backparse":
        output = backparse(inp)
    elif sys.argv[1] == "dinkelhtml":
        output = dinkelhtml(inp)

    if save_out:
        save_results(output, sys.argv[3])
    else:
        save_results(output, sys.argv[2])
        # print(output)

def print_results(res):
    print(res)

def save_results(res, f):
    handle = open(f, "w")
    handle.write(res)
    handle.close()


if __name__ == "__main__":
    main()
