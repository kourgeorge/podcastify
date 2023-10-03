import datetime


def get_timestamp():
	return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")