import os
import inspect

import handlers.utils as utils_module

log_file_path = "logs/skyenet.log"

LOG_SETUP = 0
LOG_INFO = 1
LOG_DETAIL = 2
LOG_EXTRA_DETAIL = 3

debug_level = LOG_EXTRA_DETAIL

def set_log_file(path:str):
	global log_file_path
	log_file_path = path

	log_dir = os.path.dirname(log_file_path)
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)

def set_debug_level(level:int):
	global debug_level
	debug_level = level

def log(level:int, message):
	if level > debug_level:
		return
	now = utils_module.get_timestamp_now_ymd_hms()
	function_name = inspect.currentframe().f_back.f_code.co_name
	with open(log_file_path, "a") as log_file:
		log_file.write(f"{now} - [{level}] {function_name}: {message}\n")