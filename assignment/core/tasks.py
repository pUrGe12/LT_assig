from assignment.core.utils.huey_config import huey

@huey.task(retries=3, retry_delay=2)
def new_upload_task(save_file):
	print(f"this is the savefile path: {save_file}")

	# This is where the processing logic should be
	return []