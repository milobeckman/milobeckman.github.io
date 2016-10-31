import datetime
import calendar
import xml.etree.cElementTree as ET
import os

now = datetime.datetime.now()

# filepath roots
home_dir_local = "/users/milo/Desktop/Dropbox/Code/milobeckman"
home_dir_online = "http://milobeckman.github.io"

# filepaths referenced inside html code
stylesheet_from_preview = "../style/default.css"
stylesheet_from_live = "../../../style/default.css"
stylesheet_from_tag = "../style/default.css"

favicon_from_preview = "../style/favicon.png"
favicon_from_live = "../../../style/favicon.png"
favicon_from_tag = "../style/favicon.png"


# filepaths referenced inside python code (all relative to home_dir_local)
display_tag_lookup = "/lookups/display_tag_lookup.xml"
template_post = "/style/post.html"
template_tag = "/style/tag.html"
template_tag_slice = "/style/tag_slice.html"
template_next_page = "/style/next_page.html"
template_end_of_results = "/style/end_of_results.html"
template_continue_reading = "/style/continue_reading.html"


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
            self.datestring += " AM" if now.hour < 12 else " PM"
            self.datestring += " on " + calendar.month_abbr[now.month] + " " + str(now.day) + ", " + str(now.year)
        
        # save year and month
        self.year = str(args.year if args.year else now.year)
        self.month = str(args.month if args.month else now.month)
        
        # save tags as list
        self.tags = [x.strip() for x in args.tags.split(",")]
        
        # save content filename
        self.filename = args.filename
        
        # save the relative content filepath
        self.content_dir_rel = "/content/" + self.year + "/" + self.month
        self.content_dir_local = home_dir_local + self.content_dir_rel
        
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
        self.content_dir_local = home_dir_local + self.content_dir_rel
        
        # this Post is now populated
        self.populated = True
    
    
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
            stylesheet = stylesheet_from_preview
            favicon = favicon_from_preview
        else:
            html_filename = home_dir_local + self.content_dir_rel + "/" + self.filename + ".html"
            txt_filename = home_dir_local + self.content_dir_rel + "/" + self.filename + ".txt"
            stylesheet = stylesheet_from_live
            favicon = favicon_from_live
        
        # open a new html file for writing
        html = open(html_filename, "w+")
        
        # read template html into string
        template_filename = home_dir_local + template_post
        template = open(template_filename, "r")
        html_str = template.read()
        
        # insert text
        txt = open(txt_filename, "r")
        text = txt.read()
        html_str = html_str.replace("[[TEXT]]", text)
        
        # replace placeholders with content
        html_str = html_str.replace("[[STYLESHEET]]", stylesheet)
        html_str = html_str.replace("[[FAVICON]]", favicon)
        html_str = html_str.replace("[[HOMELINK]]", home_dir_online)
        html_str = html_str.replace("[[FOLD]]", "")
        
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
    
    
    # erase generated content from provided directory
    def sweep(self, dir_path):
        rm_if_exists(dir_path + "/" + self.filename + ".html")
        rm_if_exists(dir_path + "/" + self.filename + ".xml")
    
    
    # move files for this post to the appropriate content directory
    def move_to_content_dir(self):
        
        # gen filepaths for workspace and content directories
        workspace_dir = home_dir_local + "/workspace"
        content_dir = home_dir_local + self.content_dir_rel
        
        # create content directory if it doesn't exist
        if not os.path.exists(home_dir_local + self.content_dir_rel):
            os.makedirs(home_dir_local + self.content_dir_rel)
        
        # move txt and xml files to content directory (html is preview and will be swept)
        for suffix in [".txt", ".xml"]:
            old_path = workspace_dir + "/" + self.filename + suffix
            new_path = content_dir + "/" + self.filename + suffix
            os.rename(old_path, new_path)
        
        # store the xml path in xml_path_lookup
        tree = ET.parse(home_dir_local + "/lookups/xml_path_lookup.xml")
        info = tree.getroot()
        new_node = ET.SubElement(info, "post")
        new_node.attrib["filename"] = self.filename
        new_node.text = self.content_dir_local + "/" + self.filename + ".xml"
        tree = ET.ElementTree(info)
        tree.write(home_dir_local + "/lookups/xml_path_lookup.xml")
    
    
    # add ref to this post in the provided tag list
    def add_to_list(self, tag):
        
        # create the tag list xml if it doesn't exist
        xml_filename = home_dir_local + "/tags/" + tag + ".xml"
        if not os.path.isfile(xml_filename):
            f = open(xml_filename, 'a')
            f.write("<info></info>")
            f.close()
        
        # open the tag list xml
        tree = ET.parse(xml_filename)
        info = tree.getroot()
        
        # add this new post
        ET.SubElement(info, "post").text = self.filename
        
        # make tree and write to xml file
        tree = ET.ElementTree(info)
        tree.write(xml_filename)
    
    
    # return an html code block to be inserted into a tag page
    def preview_block(self):
        
        # read template html into string
        template_filename = home_dir_local + template_tag_slice
        template = open(template_filename, "r")
        html_str = template.read()
        
        # insert text, replacing everything "under the fold" with a "continue reading" button
        txt = open(self.content_dir_local + "/" + self.filename + ".txt", "r")
        text = txt.read()        
        if "[[FOLD]]" in text:
            i = text.find("[[FOLD]]")
            text = text[:i] + open(home_dir_local + template_continue_reading).read()
        html_str = html_str.replace("[[TEXT]]", text)
        
        # replace placeholders with content
        permalink = home_dir_online + self.content_dir_rel + "/" + self.filename + ".html"
        html_str = html_str.replace("[[PERMALINK]]", permalink)
        
        html_str = html_str.replace("[[TITLE]]", self.title)
        html_str = html_str.replace("[[DATESTRING]]", self.datestring)
        
        tags = ""
        for tag in self.tags:
            tags += "<a href=" + home_dir_online + "/tags/" + tag + ".html>" + display_tag(tag) + "</a>, "
        html_str = html_str.replace("[[TAGS]]", tags[:-2])
        
        # return the html string
        return html_str


# use /tags/display_tag_lookup.xml to return the appropriate display tag
def display_tag(tag):
    
    # open display tag lookup as ET
    tree = ET.parse(home_dir_local + "/lookups/display_tag_lookup.xml")
    info = tree.getroot()
    
    # go through the tags until you find this one
    for child in info:
        if child.attrib["internal"] == tag:
            return child.text
    
    # if not found, ask user to add tag
    return add_tag(tag)


# ask user to input display tag, then store in /lookups/display_tag_lookup.xml
def add_tag(tag):
    
    # ask user for input
    disp = raw_input("Input a display version for " + tag + ": ")
    
    # open the tag lookup file
    tree = ET.parse(home_dir_local + display_tag_lookup)
    info = tree.getroot()
    
    # add this new tag
    new_node = ET.SubElement(info, "tag")
    new_node.attrib["internal"] = tag
    new_node.text = disp
    
    # save the tag lookup file
    tree = ET.ElementTree(info)
    tree.write(home_dir_local + display_tag_lookup)
    
    # return the inputted display tag
    return disp


# rewrite this tag's html page to include all tagged posts, or create it if it doesn't exist
def update_tag_page(tag):
    
    # open template html for reading into strings
    template_filename = home_dir_local + template_tag
    template = open(template_filename, "r")
    template_str = template.read()
    
    # open xml file containing all tagged posts
    xml_filename = home_dir_local + "/tags/" + tag + ".xml"
    tree = ET.parse(xml_filename)
    info = tree.getroot()
    
    # make a list of filenames with this tag, flip to reverse chron
    results = []
    for child in info:
        results += [child.text]
    results = results[::-1]
    
    # prepare for multiple pages of results
    page_no = 0
    
    while len(results) > 0:
        
        html_str = template_str
        slots_left_on_page = 3
        
        # replace placeholders with content
        html_str = html_str.replace("[[STYLESHEET]]", stylesheet_from_tag)
        html_str = html_str.replace("[[FAVICON]]", favicon_from_tag)
        html_str = html_str.replace("[[HOMELINK]]", home_dir_online)
        html_str = html_str.replace("[[YEAR]]", str(now.year))
        html_str = html_str.replace("[[DISPLAY]]", display_tag(tag))
        
        ### generate and sub in the list of results
        
        results_str = ""
        
        # add result previews to this page until we run out of slots or results
        while slots_left_on_page > 0 and len(results) > 0:
            post = Post()
            post.populate_from_xml(xml_path(results[0]))
            results_str += post.preview_block()
            
            slots_left_on_page -= 1
            results = results[1:]
        
        # sub in these results
        html_str = html_str.replace("[[RESULTS]]", results_str)
        
        # add a next button if there are more results
        if len(results) > 0:
            next_page = open(home_dir_local + template_next_page).read()
            link = home_dir_online + "/tags/" + tag + "_" + str(page_no + 1) + ".html"
            next_page = next_page.replace("[[LINK]]", link)
        else:
            next_page = open(home_dir_local + template_end_of_results).read()
        html_str = html_str.replace("[[NEXT]]", next_page)
        
        # write to file
        html_filename = home_dir_local + "/tags/" + tag + (("_" + str(page_no)) if page_no > 0 else "") + ".html"
        rm_if_exists(html_filename)
        html = open(html_filename, "w+")
        html.write(html_str)
        
        # add a new page if there are results remaining
        page_no += 1
    


# returns a path to the xml file for this internal post name
def xml_path(filename):
    
    # open xml path lookup as ET
    tree = ET.parse(home_dir_local + "/lookups/xml_path_lookup.xml")
    info = tree.getroot()
    
    # go through the tags until you find this one
    for child in info:
        if child.attrib["filename"] == filename:
            return child.text
    
    # if not found, return False
    return False


# remove the specified file if it exists
def rm_if_exists(filepath):
    try:
        os.remove(filepath)
    except OSError:
        pass
    