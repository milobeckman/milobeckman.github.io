import milobeckman
import argparse
import os


# read arguments from the command line
def parse_args():
    parser = argparse.ArgumentParser("Fully integrate a new post.")
    
    parser.add_argument("filename", metavar='F', type=str, help="Plaintext file containing the post's content.")
    
    args = argparse.Namespace()
    parser.parse_args(namespace=args)
    return args

# move files for this post to the appropriate content directory
def move_to_content_dir(post):
    
    # gen filepaths for workspace and content directories
    workspace_dir = milobeckman.home_dir_local + "/workspace"
    content_dir = milobeckman.home_dir_local + post.content_dir_rel
    
    # create content directory if it doesn't exist
    if not os.path.exists(milobeckman.home_dir_local + post.content_dir_rel):
        os.makedirs(milobeckman.home_dir_local + post.content_dir_rel)
    
    # move txt and xml files to content directory (html is preview and will be swept)
    for suffix in [".txt", ".xml"]:
        old_path = workspace_dir + "/" + post.filename + suffix
        new_path = content_dir + "/" + post.filename + suffix
        
        os.rename(old_path, new_path)


def main():
    # read arguments from command line
    args = parse_args()
    
    # create a Post object for this post
    post = milobeckman.Post()
    post.populate_from_xml(args.filename[:-3] + "xml")
    
    # move the three files to the appropriate content directory
    move_to_content_dir(post)
    
    # sweep preview html, gen web-ready html
    post.sweep(os.getcwd())
    post.write_html(milobeckman.home_dir_local + post.content_dir_rel)


if __name__ == '__main__':
    main()