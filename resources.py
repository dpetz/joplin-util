# https://github.com/marph91/joppy

from joppy.api import Api
from joppy import tools
import sys
import requests
from os import listdir
from os.path import isfile, join
import json
import re
from collections import Counter
import argparse
from functools import cached_property

def error(msg):
	print(msg, file=sys.stderr)
	exit(1)

class Database:

	# @cached_property -- only works well for simple immutable types
	def api(self):
		token = None
		try:
			with open('.token','r') as f:
    				# avoid readline() which appends \n to each line
				token = f.read().splitlines()[0]
		except FileNotFoundError:
			error("Missing `.token` file.")
		# new API instance returned and cached
		return Api(token)

	def id_list(self):
        	data = self.api().get_all_resources()
        	return [res.id for res in data]

	# https://joplinapp.org/help/api/references/rest_api/#resources
	def put_file(self, file_path, id_optional):
		print("Putting",file_path, "...")
		#resource_id = self.api().add_resource(filename="path/to/image.png", title="My first resource")

class Examples:
	ressource_displayed = "4df90691567d42efb93772717e9c56c7"
	db_ressource_not_displayed = "8d48085ce54c4543bcd700fbe3de206c"
	api_data_example = """ ResourceData(type_=None, id='467e9cc0983c4dd6bce42bcb9f967cc8', title='0f0a2d54285f6fda0da938248de92feb_6c6a8b96f9e94b5cb50ef983a6bc9c2c.jpg', mime=None, filename=None, created_time=None, updated_time=None, user_created_time=None, user_updated_time=None, file_extension=None, encryption_cipher_text=None, encryption_applied=None, encryption_blob_encrypted=None, size=None, is_shared=None, share_id=None, master_key_id=None)"""


class Directory:

	def __init__(self,resoure_directory="/Users/dirk/.config/joplin-desktop/resources"):
		self.resource_directory = resoure_directory

	def filename_list(self, extension_blacklist=None):
		fnames =  [f for f in listdir(self.resource_directory)
                	if isfile(join(self.resource_directory, f))]
		if (extension_blacklist):
			fnames = [f for f in fnames if not f.split('.')[-1] in extension_blacklist]
		return fnames

	def extensions_counter(self, print_to_stream=None):
		files = self.filename_list()
		endings = Counter( [f.split('.')[-1] for f in files if '.' in f] )

		if (print_to_stream):
			print(len(files), "total", sep='\t', file=print_to_stream)
			for c in endings.most_common():
				print(c[1],c[0], sep='\t', file=print_to_stream)
		return endings


def diff_db_dir():
	""" Returns set of IDs only in database and set of IDs only in directory """
	ids_db = set(Database().id_list())
	files = Directory().filename_list(extension_blacklist=['crypted'])
	ids_files = dict([(f.split('.')[0], f) for f in files])
	ids_dir = set( ids_files.keys() )
	return ids_db.difference(ids_dir), [ids_files[id] for id in ids_dir.difference(ids_db)]


command = None
commands = {
	"db-all": "list all database resources"
	,"dir-all": "list all directory resources"
	,"dir-extensions": "summarize directory files by type" 
	,"db-misses": "directory resources missing in database"
	,"dir-misses": "database resources missing in directory"
	,"put-file": "add or update file "
}


def parse_arguments():
	commands_help = "Supported Commands:\n" + "\n".join( k+"\t"+v for k, v in commands.items() )
	argp = argparse.ArgumentParser(description='Explore and modify Joplin resources',
		epilog=commands_help, formatter_class=argparse.RawDescriptionHelpFormatter)
	argp.add_argument("command", choices=commands.keys())
	return argp.parse_args(sys.argv[1:])


def output_list(l, stream=sys.stdout):
	print(*l, sep = '\n', file=stream)


def run_command(cmd):
	try:
		match cmd:
			case "db-all":
				output_list(Database().id_list())
			case "dir-all":
				output_list(Directory().filename_list())
			case "dir-extensions":
				Directory().extensions_counter(sys.stdout)
			case "dir-misses":
				output_list(diff_db_dir()[0])
			case "db-misses":
				output_list(diff_db_dir()[1])
	except requests.exceptions.HTTPError as err:
		# err = json.loads(err.response._content.decode("utf-8"))["error"]	
		msg = json.loads(err.response._content)["error"]
		end = re.search("[\n:]", msg).start()
		error(msg[0:end])


if __name__ == "__main__":
        args = parse_arguments()
        run_command(args.command)	
