import collections
import configparser
import hashlib
from math import ceil
import os
import re
import zlib


from utils import *


class GitRepository():
	"""A git repository"""

	worktree = None
	gitdir = None
	conf = None

	def __init__(self, path, force=False):
		self.worktree = path
		self.gitdir = os.path.join(path,'.git')

		if not (force or os.path.isdir(self.gitdir)):
			raise Exception(f"Not a git repository {path}")

		self.conf = configparser.ConfigParser()
		cf = repo_file(self, 'config')

		if cf and os.path.exists(cf):
			self.conf.read([cf])
		elif not force:
			raise Exception("Configuration file missing")


		if not force:
			vers = int(self.conf.get("core", "repositoryformatversion"))
			if vers != 0:
				raise Exception(f"Unsupported repositoryformatversion {vers}")



def repo_create(path):
	"""Create a new repository at path"""

	repo = GitRepository(path, True)

	# make sure path either doesn't exists or is an empty dir
	if os.path.exists(repo.worktree):
		if not os.path.isdir(repo.worktree):
			raise Exception(f"{path} is not a directory!")
		if os.listdir(repo.worktree):
			raise Exception(f"{path} is not empty!")
	else:
		os.makedirs(repo.worktree)


	assert(repo_dir(repo,"branches", mkdir=True))
	assert(repo_dir(repo, "objects", mkdir=True))
	assert(repo_dir(repo, "refs", "tags", mkdir=True))
	assert(repo_dir(repo, "refs", "heads", mkdir=True))


	# .git/description
	with open(repo_file(repo, "description"), "w") as f:
		f.write("Unnamed repository; edit this file 'description' to name repository. \n")

	#.git/HEAD
	with open(repo_file(repo, "HEAD"), "w") as f:
		f.write("ref: refs/heads/master\n")

	with open(repo_file(repo, "config"), "w") as f:
		config = repo_default_config()
		config.write(f)

	return repo


def cmd_init(args):
	repo_create(args.path)




