import psutil

from .. import logger

def readable(size_bytes:int):
	'''
		Convert bytes to a human-readable string (B, KB, MB, GB, TB).
	'''
	if size_bytes == 0:
		return "0B"
	
	units = ["B", "KB", "MB", "GB", "TB"]

	for i in range(len(units) - 1):
		if size_bytes < 1024:
			break
		size_bytes /= 1024
		
	return f"{size_bytes:.2f}{units[i]}"

def get_cpu_usage():
	logger.log(logger.LOG_EXTRA_DETAIL, "Getting CPU usage")
	current_usage_per_cpu = psutil.cpu_percent(percpu=True)

	if isinstance(current_usage_per_cpu, float):
		current_usage_per_cpu = [current_usage_per_cpu]

	per_cpu_items = [f"{x}%" for x in current_usage_per_cpu]
	per_cpu_usages = ", ".join(per_cpu_items) if per_cpu_items else "n/a"

	current_usage_total = sum(current_usage_per_cpu) / len(current_usage_per_cpu) if current_usage_per_cpu else 0
	return f"{per_cpu_usages} ({len(current_usage_per_cpu)} cores, {current_usage_total}% total)"

def get_memory_usage():
	logger.log(logger.LOG_EXTRA_DETAIL, "Getting MEM usage")
	mem = psutil.virtual_memory()
	return f"{readable(mem.used)} / {readable(mem.total)} ({mem.percent}%) - {readable(mem.free)} free"

def get_swap_memory_usage():
	logger.log(logger.LOG_EXTRA_DETAIL, "Getting Swap usage")
	swap = psutil.swap_memory()
	return f"{readable(swap.used)} / {readable(swap.total)} ({swap.percent}%) - {readable(swap.free)} free"

def get_disk_usage():
	logger.log(logger.LOG_EXTRA_DETAIL, "Getting Disk usage")
	partitions = psutil.disk_partitions(all=False)
	seen_devices = set()
	lines = []
	drive_num = 1

	# Filesystem types and mountpoints to ignore
	excluded_fstypes = {"tmpfs", "devtmpfs", "squashfs", "overlay", "aufs", "ramfs", "iso9660"}
	excluded_mount_prefixes = ("/dev", "/run", "/proc", "/sys")

	# Aggregates for Total
	total_total = 0
	total_used = 0
	total_free = 0

	logger.log(logger.LOG_EXTRA_DETAIL, f"Checking {len(partitions)} partitions")
	for part in partitions:
		device_key = part.device or f"mount:{part.mountpoint}"

		# skip obvious pseudo or loop devices
		if "loop" in device_key:
			continue
		# skip common pseudo filesystems
		fstype = (part.fstype or "").lower()
		if fstype in excluded_fstypes:
			continue
		# skip system mountpoints (root, tmp, proc, sys, dev, run)
		if part.mountpoint == "/" or part.mountpoint.startswith(excluded_mount_prefixes):
			continue
		if device_key in seen_devices:
			continue

		try:
			usage = psutil.disk_usage(part.mountpoint)
		except (PermissionError, FileNotFoundError):
			continue

		seen_devices.add(device_key)

		# accumulate totals
		total_total += usage.total
		total_used += usage.used
		total_free += usage.free

		line = (
			f"Drive {drive_num}: "
			f"{readable(usage.used)} / {readable(usage.total)} "
			f"({usage.percent}%) - {readable(usage.free)} free"
		)
		lines.append(line)
		drive_num += 1

	if not lines:
		logger.log(logger.LOG_EXTRA_DETAIL, "Couldn't get info on any drives")
		return "No drives found or accessible."

	result = "\n".join(lines)
	if len(lines) > 1 and total_total > 0:
		total_percent = (total_used / total_total) * 100
		result += f"\n\nTotal: {readable(total_used)} / {readable(total_total)} ({total_percent:0.2f}%) - {readable(total_free)} free"

	return result