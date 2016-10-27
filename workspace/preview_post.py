from milobeckman import Post
import argparse
import os


# read arguments from command line
def parse_args():
    parser = argparse.ArgumentParser("Preview a new post.")
    
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

def main():
    # read arguments from command line
    args = parse_args()
    
    # create a Post object for this post
    post = Post()
    post.populate_from_args(args)
    
    # sweep previous previews, then write html and xml in the workspace directory
    post.sweep(os.getcwd())
    post.write_html(os.getcwd(), True)
    post.write_xml(os.getcwd())

    

if __name__ == '__main__':
    main()