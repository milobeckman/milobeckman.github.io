from milobeckman import Post
from milobeckman import xml_path
from milobeckman import update_tag_page
import argparse
import xml.etree.cElementTree as ET
import os


# read arguments from command line
def parse_args():
    parser = argparse.ArgumentParser("Regenerate all posts in the provided xml (regenerates all posts if no xml inputted).")
    
    parser.add_argument("--xml", metavar='X', type=str, help="Xml from which to retrieve the post list.")
    
    args = argparse.Namespace()
    parser.parse_args(namespace=args)
    
    if not args.xml:
        args.xml = "../tags/all.xml"
    
    return args


# regenerate the post with this internal filename
def regen_post(filename):
    
    # populate the Post from the filename
    post = Post()
    post.populate_from_xml(xml_path(filename))
    
    # clear the existing xml and html
    post.sweep(post.content_dir_local)
    
    # regenerate the xml and html
    post.write_xml(post.content_dir_local)
    post.write_html(post.content_dir_local)


def main():
    
    # read arguments from command line
    args = parse_args()
    
    # open the post list xml
    tree = ET.parse(args.xml)
    info = tree.getroot()
    
    # iterate through provided xml, regen each post
    for child in info:
        regen_post(child.text)
    
    # open the tag list xml
    tree = ET.parse("../lookups/display_tag_lookup.xml")
    info = tree.getroot()
    
    # iterate through tags, regen each tag page
    for child in info:
        update_tag_page(child.attrib["internal"])
    
    

if __name__ == '__main__':
    main()