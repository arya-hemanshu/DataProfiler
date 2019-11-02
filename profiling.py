import pandas as pd
import pandas_profiling as pp
from pandas_profiling.model.describe import multiprocess_1d as md
from datetime import datetime
import os
import sys
import itertools
import matplotlib

# Combined data frame and read_csv into a single class
# Adding datatype checks before doing the calculations
# Improved memory management

class Profiling(pd.DataFrame):

	def __init__(self, data=None, subset=20, show_report=False, file_path=None):
		if data is None and file_path is None:
			raise ValueError('File path or data is required')

		super().__init__(data)

		self.file_path = file_path
		self.subset = subset
		self.show_report = show_report

	def __getitem__(self, col):
		if isinstance(col, list):
			return Profiling(super().__getitem__(col))
		else:
			return super().__getitem__(col)


	def read_csv(self) -> None or pp.__init__.ProfileReport:

		if self.file_path is None:
			print('File path is required')
			return

		file_exists = os.path.exists(os.getcwd() + '/' + self.file_path)

		if file_exists:
			self.__init__(pd.read_csv(self.file_path, low_memory=False), self.subset, self.show_report, self.file_path)
			if self.show_report:
				return self.profile(subset=self.subset)
		else:
			print(self.file_path, "doesn't exists")
			return

	def head(self, rows: int):
		return Profiling(super().head(rows))

	def tail(self, rows: int):
		return Profiling(super().tail(rows))

	def psubset(self, cols=[], rows=20):
		df = self
		if len(cols) != 0:
			df = self[cols]

		return df.head(rows)

	# Type checking before sending details
	def details(self, cols=[], use_pandas=False) -> dict or pd.Series:

		if self.empty:
			print('Data frame is required')
			return

		if len(cols) == 0:
			cols = list(self.columns)

		return self.compute(cols, use_pandas)

	def compute(self, cols, use_pandas=False) -> dict or pd.Series:
		if use_pandas:
			print('Use pandas would not check for types')
			return self[cols].describe()

		describe = {}
		for col in cols:
			dt = str(self.dtypes[col])
			if dt == 'int64':
				print(col, '-->')
				describe[col] = self[col].describe() 
				print(describe[col])
			elif dt == 'object':
				print(col, '--> has object datatype thus grouping by values')
				describe[col] = self[col].value_counts(dropna=False)
				print(describe[col])
			elif dt == 'datetime64[ns]':
				print(col, '--> has object datatype thus grouping by values')
				describe[col] = self[col].value_counts(dropna=False)
				print(describe[col])
			elif dt == 'float64':
				lat = self.loc[(self[col] > 90) & (self[col] < -90)]
				lon = self.loc[(self[col] > 180) & (self[col] < -180)]
				if lat.empty and lon.empty:
					print('It looks like a geometry column, aggregating it would produce inappropriate results')

				print(col, '-->')
				describe[col] = self[col].describe()
				print(describe[col])

			else:
				print('Unknown datatype of column', col)
		return describe

	# convert the date column to a format that pandas accept, currently it user who needs to process it
	# pd.to_datetime when passed with any column tries to convert it into date, even if they are latitude or longitude
	# currently only supports one more could be introduced to format different kind of datasets
	def plot_timeseries(self, date_col: str, cols=[], plot_on='date', figsize=(10,5), kind='line') -> None or matplotlib.axes._subplots:

		if len(cols) == 0:
			print('At least one column is required')
			return

		self.to_datetime(date_col)
		

		if plot_on == 'date':
			return super().plot(x=date_col, y=cols, figsize=figsize, kind=kind)
		elif plot_on == 'month':
			self['month'] = self[date_col].map(lambda m: m.month)
			return self.groupby(['month']).sum()[cols].plot(figsize=figsize, kind=kind)
		elif plot_on == 'year':
			self['year'] = self[date_col].map(lambda y: y.year)
			return self.groupby(['year']).sum()[cols].plot(figsize=figsize, kind=kind)
		else:
			print(plot_on, 'is an invalid value for plot_on')
			return

	def to_datetime(self, col: str):
		try:
			self[col] = self[col].map(lambda d: datetime.strptime(d, '%d/%m/%Y') if not isinstance(d, pd._libs.tslibs.timestamps.Timestamp) else d)
		except TypeError as e:
			print(col, "isn't a string column or doesn't contain date")

	def plot(self, x: str, y: list, kind='line', figsize=(10, 5)) -> matplotlib.axes._subplots:
		s_d = self.v_type(self[[x]])

		if (s_d[x]['type']).value == 'CAT' or (s_d[x]['type']).value == 'NUM':
			return self.groupby([x]).sum()[y].plot(kind=kind, figsize=figsize)

		return super().plot(x, y, kind=kind, figsize=figsize)

	def v_type(self, df) -> dict:
		a = [(c, s) for c, s in df.iteritems()]
		s_d = {c: s for c, s in itertools.starmap(md, a)}
		return s_d

	def profile(self, subset=0, cols=[], title='Report', pool_size=0, minify_html=False, output=None) -> pp.__init__.ProfileReport:
		df = self
		report = None

		if subset > 0:
			df = self.head(subset)

		if len(cols) > 0:
			df = df[cols]

		report = df.profile_report(title=title, pool_size=pool_size, minify_html=minify_html)

		if output is not None:
			report.to_file(output)

		return report

	def correlation(self, subset=[], method='pearson'):
		if len(subset) == 0:
			return self.corr(method=method)

		return Profiling(self[subset].corr(method=method))









