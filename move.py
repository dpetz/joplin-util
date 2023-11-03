# python3 move.py sample-db-misses /Users/dirk/.config/joplin-desktop/resources /Users/dirk/git/joplin-util/stage

import os
import sys

def move_files(file_with_filenames, source_directory, target_directory, log=None):

	files = []

	with open(file_with_filenames,'r') as f:
		# avoid readline() which appends \n to each line
		files = f.read().splitlines()

	for f in files:
		src = os.path.join(source_directory,f)
		trg = os.path.join(target_directory,f)
		if (log):
                        print("Moving",src,"to",trg, file=log)
		try:
			os.rename(src, trg)
		except FileNotFoundError as err:
			print(err, file=sys.stderr)

if(len(sys.argv)!=4):
	print("Usage: python3 move.py <file_with_filenames> <source_directory> <target_directory>")

move_files(sys.argv[1], sys.argv[2], sys.argv[3], log=sys.stdout)

