import argparse
import datetime
import calendar
import xml.etree.cElementTree as ET
import os

now = datetime.datetime.now()

template_post = "template-post.html"
template_tags = "template-tags.html"
stylesheet = "default.css"

# filepaths
home_dir_local = "/users/milo/Desktop/Dropbox/Code/milobeckman"
home_dir_online = "http://milobeckman.github.io"
content_dir_rel = "/content/" + str(now.year) + "/" + str(now.month)


class Post:
    
    def __init__(self, args):
        
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
    
    
    # move this post's txt file to the appropriate content subdir
    def move_txt_to_content(self):
        if not os.path.exists(home_dir_local + self.content_dir_rel):
            os.makedirs(home_dir_local + self.content_dir_rel)
        
        old_path = home_dir_local + "/workspace/" + self.filename + ".txt"
        new_path = home_dir_local + self.content_dir_rel + "/" + self.filename + ".txt"
        
        print old_path
        print new_path
        
        os.rename(old_path, new_path)
    
    
    # write an xml file with metadata on this post using ElementTree
    def create_xml(self):
        
        # write header, title, and date info
        info = ET.Element("info")
        ET.SubElement(info, "title").text = self.title
        ET.SubElement(info, "datestring").text = self.datestring
        ET.SubElement(info, "year").text = self.year
        ET.SubElement(info, "month").text = self.month
        
        # write tags
        tags = ET.SubElement(info, "tags")
        for tag in self.tags:
            ET.SubElement(tags, "internal").text = tag
            ET.SubElement(tags, "display").text = display_tag(tag)
        
        # write content filename
        ET.SubElement(info, "filename").text = self.filename
        
        # make tree and write to xml file
        xml_filename = home_dir_local + self.content_dir_rel + "/" + self.filename + ".xml"
        tree = ET.ElementTree(info)
        tree.write(xml_filename)
    
    
    # write an html file to display this post
    def create_html(self):
        
        # open a new html file for writing
        html_filename = home_dir_local + self.content_dir_rel + "/" + self.filename + ".html"
        html = open(html_filename, "w+")
        
        # read template html into string
        template_filename = home_dir_local + "/style/" + template_post
        template = open(template_filename, "r")
        html_str = template.read()
        
        # insert text
        txt_filename = home_dir_local + self.content_dir_rel + "/" + self.filename + ".txt"
        txt = open(txt_filename, "r")
        text = txt.read()
        html_str = html_str.replace("[[TEXT]]", text)
        
        # replace placeholders with content
        html_str = html_str.replace("[[STYLESHEET]]", home_dir_online + "/style/" + stylesheet)
        html_str = html_str.replace("[[HOMELINK]]", home_dir_online)
        
        permalink = home_dir_online + self.content_dir_rel + "/" + self.filename + ".html"
        html_str = html_str.replace("[[PERMALINK]]", permalink)
        
        html_str = html_str.replace("[[TITLE]]", self.title)
        html_str = html_str.replace("[[DATESTRING]]", self.datestring)
        
        tags = ""
        for tag in self.tags:
            tags += "<a href=" + home_dir_online + "/tags/" + tag + ".html>" + display_tag(tag) + "</a>, "
        html_str = html_str.replace("[[TAGS]]", tags[:-2])
        
        # write to html file
        html.write(html_str)


# read arguments from the command line
def parse_args():
    parser = argparse.ArgumentParser("Integrate a new post into milobeckman.com")
    
    parser.add_argument("filename", metavar='F', type=str, help="Plaintext file containing the post's content.")
    parser.add_argument("title", metavar='T', type=str, help="Display title for post.")
    parser.add_argument("tags", metavar='t', type=str, help="Comma-separated list of tags for this post (internal format).")
    parser.add_argument("--datestring", metavar="S", type=str, help="Optionally override the date string.")
    parser.add_argument("--year", metavar="Y", type=int, help="Optionally override the year.")
    parser.add_argument("--month", metavar="M", type=int, help="Optionally override the month.")
    
    args = argparse.Namespace()
    parser.parse_args(namespace=args)
    
    if args.year or args.month:
        global content_dir_rel
        content_dir_rel = "/content/" + str(args.year if args.year else now.year) + "/" + str(args.month if args.month else now.month)
    
    return args



# return the display version of the given internal tag [MAKE THIS]
def display_tag(tag):
    return "display tag"


def main():
    args = parse_args()
    new_post = Post(args)
    
    new_post.move_txt_to_content()
    new_post.create_xml()
    new_post.create_html()


if __name__ == '__main__':
    main()