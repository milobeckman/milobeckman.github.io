from milobeckman import Post
from milobeckman import update_tag_page
import argparse
import os


# read arguments from the command line
def parse_args():
    parser = argparse.ArgumentParser("Fully integrate a new post.")
    
    parser.add_argument("filename", metavar='F', type=str, help="Internal referent for this post (plaintext filename without extension).")
    
    args = argparse.Namespace()
    parser.parse_args(namespace=args)
    return args


def main():
    
    # read arguments from command line
    args = parse_args()
    
    # create a Post object for this post
    post = Post()
    post.populate_from_xml(args.filename + ".xml")
    
    ### move stuff back to here
        ### stuff to move back to there
    # move the three files to the appropriate content directory
    post.move_to_content_dir()
    
    # sweep preview html, gen web-ready html
    post.sweep(os.getcwd())
    post.write_html(post.content_dir_local)
    ### end of stuff
    
    # make sure no post exists with this name (filename must be unique!)
    
    
    
    # add reference to this post in appropriate tag/all xmls
    post.add_to_list("all")
    for tag in post.tags:
        post.add_to_list(tag)
        update_tag_page(tag)
    
    
    
    
    
    
    
    

    

if __name__ == '__main__':
    main()