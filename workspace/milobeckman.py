import datetime
import calendar
import xml.etree.cElementTree as ET
import os

now = datetime.datetime.now()

template_post = "post_default.html"
template_tags = "tags_default.html"

# filepaths
home_dir_local = "/users/milo/Desktop/Dropbox/Code/milobeckman"
home_dir_online = "http://milobeckman.github.io"

# stylesheets
stylesheet_local = "../style/default.css"               # relative to workspace dir
stylesheet_online = "../../../style/default.css"        # relative to content subsubdir


class Post:
    
    # create an empty Post object
    def __init__(self):
        self.populated = False
    
    
    # populate this Post object with info from command line arguments
    def populate_from_args(self, args):
        
        # save title
        self.title = args.title
        
        # save datestring
        if args.datestring:
            self.datestring = args.datestring
        else:
            self.datestring = "at " + str((now.hour-1) % 12 + 1) + ":"
            self.datestring += str(now.minute) if now.minute > 9 else "0" + str(now.minute)
            self.datestring += "am" if now.hour < 12 else "pm"
            self.datestring += " on " + calendar.month_abbr[now.month] + " " + str(now.day) + ", " + str(now.year)
        
        # save year and month
        self.year = str(args.year if args.year else now.year)
        self.month = str(args.month if args.month else now.month)
        
        # save tags as list
        self.tags = [x.strip() for x in args.tags.split(",")]
        
        # save content filename (sans txt)
        self.filename = args.filename[:-4]
        
        # save the relative content filepath
        self.content_dir_rel = "/content/" + self.year + "/" + self.month
        
        # this Post is now populated
        self.populated = True
    
    
    # populate this Post object with info from an xml file
    def populate_from_xml(self, xml_path):
        
        # open the xml file as an ET
        tree = ET.parse(xml_path)
        info = tree.getroot()
        
        # save info from xml
        self.title = info.find("title").text
        self.datestring = info.find("datestring").text
        self.year = info.find("year").text
        self.month = info.find("month").text
        self.tags = [x.find("internal").text for x in info.find("tags").findall("tag")]
        self.filename = info.find("filename").text
        
        # save the relative content filepath
        self.content_dir_rel = "/content/" + self.year + "/" + self.month
        
        # this Post is now populated
        self.populated = True
    
    
    # move this post's txt file to the appropriate content subdir
    def move_txt_to_content(self):
        if not os.path.exists(home_dir_local + self.content_dir_rel):
            os.makedirs(home_dir_local + self.content_dir_rel)
        
        old_path = home_dir_local + "/workspace/" + self.filename + ".txt"
        new_path = home_dir_local + self.content_dir_rel + "/" + self.filename + ".txt"
        
        os.rename(old_path, new_path)
    
    
    # write an xml file with metadata on this post using ElementTree
    def write_xml(self, dir_path):
        
        # write header, title, and date info
        info = ET.Element("info")
        ET.SubElement(info, "title").text = self.title
        ET.SubElement(info, "datestring").text = self.datestring
        ET.SubElement(info, "year").text = self.year
        ET.SubElement(info, "month").text = self.month
        
        # write tags
        tags = ET.SubElement(info, "tags")
        for tag in self.tags:
            tag_elt = ET.SubElement(tags, "tag")
            ET.SubElement(tag_elt, "internal").text = tag
            ET.SubElement(tag_elt, "display").text = display_tag(tag)
        
        # write content filename
        ET.SubElement(info, "filename").text = self.filename
        
        # make tree and write to xml file
        xml_filename = dir_path + "/" + self.filename + ".xml"
        tree = ET.ElementTree(info)
        tree.write(xml_filename)
    
    
    # write an html file to display this post
    def write_html(self, dir_path, preview=False):
        
        # set filepaths (diff for preview and live post)
        if preview:
            html_filename = self.filename + ".html"
            txt_filename = self.filename + ".txt"
            stylesheet = stylesheet_local
        else:
            html_filename = home_dir_local + self.content_dir_rel + "/" + self.filename + ".html"
            txt_filename = home_dir_local + self.content_dir_rel + "/" + self.filename + ".txt"
            stylesheet = stylesheet_online
        
        # open a new html file for writing
        html = open(html_filename, "w+")
        
        # read template html into string
        template_filename = home_dir_local + "/style/" + template_post
        template = open(template_filename, "r")
        html_str = template.read()
        
        # insert text
        txt = open(txt_filename, "r")
        text = txt.read()
        html_str = html_str.replace("[[TEXT]]", text)
        
        # replace placeholders with content
        html_str = html_str.replace("[[STYLESHEET]]", stylesheet)
        html_str = html_str.replace("[[HOMELINK]]", home_dir_online)
        
        permalink = home_dir_online + self.content_dir_rel + "/" + self.filename + ".html"
        html_str = html_str.replace("[[PERMALINK]]", permalink)
        
        html_str = html_str.replace("[[TITLE]]", self.title)
        html_str = html_str.replace("[[DATESTRING]]", self.datestring)
        html_str = html_str.replace("[[YEAR]]", self.year)
        
        tags = ""
        for tag in self.tags:
            tags += "<a href=" + home_dir_online + "/tags/" + tag + ".html>" + display_tag(tag) + "</a>, "
        html_str = html_str.replace("[[TAGS]]", tags[:-2])
        
        # write to html file
        html.write(html_str)
    
    # erase preview html from provided directory
    def sweep(self, dir_path):
        rm_if_exists(dir_path + "/" + self.filename + ".html")
        rm_if_exists(dir_path + "/" + self.filename + ".xml")
    
    
    
# TEMPORARY
def display_tag(tag):
    return "display tag"

# remove the specified file if it exists
def rm_if_exists(filepath):
    try:
        os.remove(filepath)
    except OSError:
        pass
    