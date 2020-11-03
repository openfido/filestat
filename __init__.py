"""OpenFIDO filestat pipeline

This pipeline creates a CSV file name containing the file status of the input files.

INPUTS

  The list of files to be examined.

OUTPUTS

  The CSV file containing the file status information

"""
import os, csv, datetime, pwd, grp, stat, hashlib

def main(inputs,outputs,options):
	if not outputs or not type(outputs) is list or not outputs[0]:
		outputs = ["/dev/stdout"]
	if len(outputs) > 1:
		raise Exception("too many outputs specified")
	with open(outputs[0],"w") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["pathname","mode","size","user","group","links","accessed","modified","created","checksum"])
		for file in inputs:
			fs = os.stat(file)
			with open(file) as fh:
				md5 = hashlib.md5(fh.read().encode("utf-8"))
			try:
				uname = pwd.getpwuid(fs.st_uid).pw_name
			except:
				uname = str(fs.st_uid)
				pass
			try:
				gname = grp.getgrgid(fs.st_gid).gr_name
			except:
				gname = str(fs.st_gid)
				pass
			writer.writerow([
				os.path.abspath(file),
				stat.filemode(fs.st_mode),
				fs.st_size,
				uname,
				gname,
				fs.st_nlink,
				datetime.datetime.utcfromtimestamp(fs.st_atime),
				datetime.datetime.utcfromtimestamp(fs.st_mtime),
				datetime.datetime.utcfromtimestamp(fs.st_ctime),
				md5.hexdigest()
				])
	return outputs[0]
