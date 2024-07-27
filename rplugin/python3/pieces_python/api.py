from typing import Optional
from ._pieces_lib import pieces_os_client as pos_client
from ._pieces_lib import semver
from .settings import Settings
import time
import subprocess
from ._version import __version__

PIECES_OS_MIN_VERSION = "9.0.0"  # Minium version (10.0.0)
PIECES_OS_MAX_VERSION = "10.0.0" # Maxium version (11.0.0)

def get_version() -> Optional[str]:
	"""Get pieces os version return None if there is a problem"""
	try:
		version = pos_client.WellKnownApi(Settings.api_client).get_well_known_version()
		return version
	except: # There is a problem in the startup
		return None


def open_pieces_os() -> Optional[str]:
	"""Open pieces os and return its version"""
	version = get_version()
	if version:
		return version
	pl = Settings.os
	if pl == "WINDOWS":
		subprocess.run(["start", "pieces://launch"], shell=True)
	elif pl == "MACOS":
		subprocess.run(["open","pieces://launch"])
	elif pl == "LINUX":
		subprocess.run(["xdg-open","pieces://launch"])

	for _ in range(2):
		version = get_version()
		if version:
			return version
		time.sleep(2) # wait for the server to open
	return get_version() # pieces os version


def get_user():
	api_instance = pos_client.UserApi(Settings.api_client)
	user = api_instance.user_snapshot().user
	return user

def version_check():
	"""Check the version of the pieces os in the within range"""
	pieces_os_version = get_version()

	# Parse version numbers
	os_version_parsed = semver.VersionInfo.parse(pieces_os_version)
	min_version_parsed = semver.VersionInfo.parse(PIECES_OS_MIN_VERSION)
	max_version_parsed = semver.VersionInfo.parse(PIECES_OS_MAX_VERSION)


	# Check compatibility
	if os_version_parsed >= max_version_parsed:
		return False,"the Pieces Neovim Plugin"
	elif os_version_parsed < min_version_parsed:
		return False,"Pieces OS"
	return True,None


def is_pieces_opened(func):
	def wrapper(*args, **kwargs):
		if Settings.is_loaded:
			return func(*args, **kwargs)
		else:
			return Settings.nvim.err_write("Please make sure Pieces OS is running and updated\n")
	return wrapper

