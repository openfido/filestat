"""OpenFIDO filestat pipeline

This pipeline creates a CSV file name containing the file status of the input files.

INPUTS

  The list of files to be examined.

OUTPUTS

  The CSV file containing the file status information

"""
import os, csv, datetime, pwd, grp, stat, hashlib

def main(inputs,outputs,options):
	if len(outputs) == 0:
		raise Exception("output file must be specified")
	if len(outputs) > 1:
		raise Exception("too many outputs specified")
	with open(outputs[0],"w") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["pathname","mode","size","user","group","links","accessed","modified","created","checksum"])
		for file in inputs:
			fs = os.stat(file)
			with open(file) as fh:
				md5 = hashlib.md5(fh.read().encode("utf-8"))
			writer.writerow([
				os.path.abspath(file),
				stat.filemode(fs.st_mode),
				fs.st_size,
				pwd.getpwuid(fs.st_uid).pw_name,
				grp.getgrgid(fs.st_gid).gr_name,
				fs.st_nlink,
				datetime.datetime.utcfromtimestamp(fs.st_atime),
				datetime.datetime.utcfromtimestamp(fs.st_mtime),
				datetime.datetime.utcfromtimestamp(fs.st_ctime),
				md5.hexdigest()
				])
	return outputs[0]
