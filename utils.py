import os
import configparser
import gitme_lib

def repo_path(repo, *path):
	"""Compute path under repo's gitdir."""
	return os.path.join(repo.gitdir, *path)

def repo_dir(repo, *path, mkdir=False):
	"""Same as repo_path, but mkdir *path if absent if mkdir."""

	path = repo_path(repo, *path)

	if os.path.exists(path):
		if os.path.isdir(path):
			return path
		else:
			raise Exception(f'Not a directory {path}')

	if mkdir:
		os.makedirs(path)
		return path
	else:
		return None


def repo_file(repo, *path, mkdir=False):
	if repo_dir(repo, *path[:-1], mkdir=mkdir):
		return repo_path(repo, *path)


def repo_default_config():
	ret = configparser.ConfigParser()

	ret.add_section("core")
	ret.set("core", "repositoryformatversion", "0")
	ret.set("core", "filemode", "false")
	ret.set("core", "bare", "false")

	return ret


def repo_find(path='.', required=True):
	path = os.path.realpath(path)

	if os.path.isdir(os.path.join(path, ".git")):
		return gitme_lib.GitRepository(path)

	parent = os.path.realpath(os.path.join(path,".."))

	if parent == path:
		# if parent == path, then it is root
		
		if required:
			raise Exception("No git directory")
		else:
			return None


	return repo_path(parent, required)