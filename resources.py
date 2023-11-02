# https://github.com/marph91/joppy

from joppy.api import Api
from joppy import tools
import sys

from os import listdir
from os.path import isfile, join

from collections import Counter

import argparse

with open('.token','r') as f:
    token = f.read().splitlines()[0] # avoid readline() which appends \n to each line

# Create a new Api instance.
api = Api(token)

# resource_id = api.add_resource(filename="path/to/image.png", title="My first resource")
res_missed = "4df90691567d42efb93772717e9c56c7"
res_exists = "8d48085ce54c4543bcd700fbe3de206c"
res_data_example = """ResourceData(type_=None, id='467e9cc0983c4dd6bce42bcb9f967cc8', title='0f0a2d54285f6fda0da938248de92feb_6c6a8b96f9e94b5cb50ef983a6bc9c2c.jpg', mime=None, filename=None, created_time=None, updated_time=None, user_created_time=None, user_updated_time=None, file_extension=None, encryption_cipher_text=None, encryption_applied=None, encryption_blob_encrypted=None, size=None, is_shared=None, share_id=None, master_key_id=None)"""

# Prints name
# code = api.get_resource(res_exists)
# print("\n\nData: " + code.title)

# Throws exception
# code = api.get_resource(res_missed)
# print("\n\nData: " + code)

def all():
	data = api.get_all_resources()
	ids = [res.id for res in data] 
	return ids

def resource_directory_as_map(resource_directory="/Users/dirk/.config/joplin-desktop/resources"):
	files = [f for f in listdir(resource_directory)
		if isfile(join(resource_directory, f))]

	print("Total\t", len(files))

	endings = [f.split('.')[-1] for f in files if '.' in f]
		
	for c in Counter(endings).most_common():
		print(c[0],"\t",c[1])

command = None
commands = {
	"db":"list all resources in database",
	"dir": "list all resources in directory"
}

def parse_arguments():
	commands = { "db":"list all in database", "dir": "list all in directory" }
	commands_help = "Supported Commands:\n" + "\n".join( k + "\t" + v for k, v in commands.items() )
	argp = argparse.ArgumentParser(description='Explore and modify Joplin resources',
		epilog=commands_help, formatter_class=argparse.RawDescriptionHelpFormatter)
	argp.add_argument("command", choices=commands.keys())
	return argp.parse_args(sys.argv[1:])

args = parse_arguments()

match args.command:
	case "db":
		print(*all(), sep = '\n')
	case "dir":
		resource_directory_as_map()
