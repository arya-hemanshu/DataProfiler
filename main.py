from profiling import Profiling
import argparse
import sys
from sys import platform
import os

def arguments(arg: list = []):
	"""
	List of options that could be passed through console
	"""

	parser = argparse.ArgumentParser(description='Bespoke profiler')

	parser.add_argument(
			'--dataset', 
			'-d', 
			type=str,
			required=True,
			help="Provide the dataset file path")

	parser.add_argument(
			'--columns',
			'-c',
			action='append',
			type=str,
			help='Provide column name from dataset')

	parser.add_argument(
			'--rows',
			'-r',
			type=int,
			help='Provide number of rows to consider from dataset')

	parser.add_argument(
			'--operation',
			'-o',
			type=str,
			default='profile',
			help='Options allowed (describe, plot, profile, corr)')

	parser.add_argument(
			'--no',
			'-n',
			type=bool,
			default=False,
			help='Provide in case you dont want any operation to run')

	parser.add_argument(
			'--timeseries',
			'-t',
			type=bool,
			default=False,
			help='Adding the flag will treat the x axis as timeseries')

	parser.add_argument(
			'--ploton',
			'-po',
			type=str,
			default='date',
			help='Options allowed (date, month, year)')

	parser.add_argument(
			'--xaxis',
			'-x',
			type=str,
			help='Provide column name for x axis')

	parser.add_argument(
			'--output',
			'-ot',
			type=str,
			default='report.html',
			help='Provide the filename of output file')

	parser.add_argument(
			'--vtype',
			'-vt',
			action='append',
			type=str,
			help='Pass variable for which type needs to be determined')

	parser.add_argument(
			'--corr',
			'-co',
			action='append',
			type=str,
			help='Provide list of variables for which correlation matrix is required')

	return parser.parse_args(arg)

def plot(ar, profile):
	if ar.columns is None or ar.xaxis is None:
		print('For plotting columns and x axis col name is required')
		sys.exit()

	fig = None
	if ar.timeseries:
		fig = profile.plot_timeseries(ar.xaxis, ar.columns, ar.ploton)
	else:
		fig = profile.plot(ar.xaxis, ar.columns)

	(fig.get_figure()).savefig(ar.output)

	if platform == 'darwin':
		os.system('open ' + ar.output)
	else:
		print('Please visit', ar.output, 'to open image')

def profile_data(ar, profile):
	cols = ar.columns
	rows = ar.rows
	if cols is not None and rows is not None:
		profile.profile(subset=rows, cols=cols, output=ar.output)
	elif rows is not None:
		profile.profile(rows=rows, output=ar.output)
	elif cols is not None:
		profile.profile(cols=cols, output=ar.output)
	else:
		print('It may take longer to profile on whole dataset')
		profile.profile(output=ar.output)

def describe(ar, profile):
	cl = []
	if ar.columns is not None:
		cl = ar.columns
	
	profile.details(cols=cl)

def variable_type(ar, profile):
	df = profile.psubset(cols=ar.vtype, rows=profile.shape[0])
	vt = df.v_type(df)

	for k, v in vt.items():
		print(k, '\t', (vt[k]['type']).value)

def corr(ar, profile):
	return profile.correlation(subset=ar.corr)
	

if __name__ == '__main__':
	args = sys.argv
	if len(args) <= 1:
		print('--dataset argument is mandatory')
		sys.exit()

	ar = arguments(args[1:])

	profile = Profiling(file_path=ar.dataset)
	profile.read_csv()

	if not ar.no:
		if ar.operation == 'plot':
			plot(ar, profile)

		elif ar.operation == 'profile':
			profile_data(ar, profile)

		elif ar.operation == 'describe':
			describe(ar, profile)

		else:
			print('Invalid operation selected')
			sys.exit()

	if ar.vtype is not None:
		variable_type(ar, profile)

	if ar.corr is not None:
		print(corr(ar, profile))






	


















