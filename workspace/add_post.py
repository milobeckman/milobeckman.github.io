from milobeckman import Post
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
    
    # add reference to this post in appropriate tag/all xmls
    post.add_to_list("all")
    
    ### stuff to move back to there
    # move the three files to the appropriate content directory
    post.move_to_content_dir()
    
    # sweep preview html, gen web-ready html
    post.sweep(os.getcwd())
    post.write_html(post.content_dir_local)
    ### end of stuff
    

if __name__ == '__main__':
    main()