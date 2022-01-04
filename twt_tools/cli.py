from thread import Thread
import argparse
import os

parser = argparse.ArgumentParser("")
parser.add_argument("link")
parser.add_argument("thread_name")
parser.add_argument("--output_folder", "-o", default=os.getcwd())
parser.add_argument("-s", "--keep_source_files", default=False, action="store_true")
args = parser.parse_args()

thread = Thread(args.link, args.thread_name, args.output_folder)
thread.build_markdown()
thread.build_pdf()
if not args.keep_source_files:
    thread.cleanup()
