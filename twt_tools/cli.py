from thread import Thread
from twt_tools.lib.lib import get_media
import argparse
import os

parser = argparse.ArgumentParser("")
parser.add_argument("link", help="Last tweet in the thread link or ID")
parser.add_argument("thread_name", help="Name for the archive")
parser.add_argument("--output_folder", "-o", default=os.getcwd(), help="If not provided, outputs to current directory.")
parser.add_argument("-s", "--keep_source_files", default=False, action="store_true", help="If provided, keeps a folder with the full size images and Markdown of thread")
parser.add_argument("-m", "--media", default=False, action="store_true", help="If provided, scrapes a SINGLE tweet for media files and saves them in current directory")
args = parser.parse_args()

thread = Thread(args.link, args.thread_name, args.output_folder)
if args.media:
    get_media(args.link, args.thread_name)

else:
    thread.build_markdown()
    thread.build_pdf()
    if not args.keep_source_files:
        thread.cleanup()
