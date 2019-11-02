import pandas as pd
import pandas_profiling as pp
from pandas_profiling.model.describe import multiprocess_1d as md
from datetime import datetime
import os
import sys
import itertools
import matplotlib

class Profiling(pd.DataFrame):
	"""
	There are good data profilers available. Profiling library doesn't aim to build everything 
	from scratch. It tries to built on top of existing tools.

	The tool is built on top of pandas.DataFrame. Profiling class inherits all the methods of 
	pandas.DataFrame and add a few of its own to enchance the capability of pandas.DataFrame 
	bespoke to companies use case.

	The tool combines pandas.DataFrame and pandas_profiling library into one class and makes 
	direct use of pandas_profiling methods to get information about Variables.

	Args:
		:data: accepts a pandas dataframe or Profiling object
		:subset: number of rows to consider when showing report
		:show_report: Allows users to profile dataset while loading dataset
		:file_path: Path of csv file to create dataset from

	Profiling object would have access to all pandas.DataFrame variable

	Example:

		.. code-block:: python

			from profiling import Profiling
			p = Profiling(file_path='Datasources/Acc.csv')
			p.read_csv()

	"""

	def __init__(self, data=None, subset=20, show_report=False, file_path=None):

		if data is None and file_path is None:
			raise ValueError('File path or data is required')

		super().__init__(data)

		self.file_path = file_path
		self.subset = subset
		self.show_report = show_report

	def __getitem__(self, col):
		"""
		Subscript Profiling object

		Args:
			:col: list of column name from which new Profiling object is built

		Returns:
			:Profiling: object
			:pandas.Series: object

		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				s = p[['Number_of_Casualties', 'Number_of_Vehicles', 'Date']]	

		"""

		if isinstance(col, list):
			return Profiling(super().__getitem__(col))
		else:
			return super().__getitem__(col)


	def read_csv(self):
		"""
		Read csv file passed in the Profiling constructor with file_path

		Args:
			:None:

		Return:
			:pp.__init__.ProfileReport: Object

		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.read_csv()

		"""

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
		"""
		Return the number of specified rows from top

		Args:
			:rows: Number of rows to process

		Return:
			:profiling.Profiling: object


		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.head(20)



		"""

		return Profiling(super().head(rows))

	def tail(self, rows: int):
		"""
		Return the number of specified rows from bottom

		Args:
			:rows: Number of rows to process

		Return:
			:profiling.Profiling: object

		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.tail(20)
				
		"""

		return Profiling(super().tail(rows))

	def psubset(self, cols=[], rows=20):
		"""
		Return the number of specified rows and columns

		Args:
			:cols: List of columns
			:rows: Number of rows to consider while creating new Profiling object

		Return:
			:profiling.Profiling: object

		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.psubset(cols=['Number_of_Casualties', 'Number_of_Vehicles']))
				
		"""

		df = self
		if len(cols) != 0:
			df = self[cols]

		return df.head(rows)

	def details(self, cols=[], use_pandas=False) -> dict or pd.Series:
		"""
		Return the details of variables, like describe of pandas.DataFrame.describe()

		Args:
			:cols: List of columns to consider
			:use_pandas: bool variable indicating use of super class method or child class

		Return:
			:dict: Dictionary of Variables and its details
			:pandas.Series: object

		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.details(cols=['Number_of_Casualties', 'Number_of_Vehicles']))
				
		"""

		if self.empty:
			print('Data frame is required')
			return

		if len(cols) == 0:
			cols = list(self.columns)

		return self.compute(cols, use_pandas)

	def compute(self, cols, use_pandas=False) -> dict or pd.Series:
		"""
		Return the details of variables, like describe of pandas.DataFrame.describe()

		Args:
			:cols: List of columns to consider
			:use_pandas: bool variable indicating use of super class method or child class

		Return:
			:dict: Dictionary of Variables and its details
			:pandas.Series: object

		Example:
			.. code-block:: python
			
				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.details(cols=['Number_of_Casualties', 'Number_of_Vehicles']))
	
		"""

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

	def plot_timeseries(self, date_col: str, cols=[], plot_on='date', figsize=(10,5), kind='line') -> None or matplotlib.axes._subplots:
		"""
		Plot the dataset as timeseries

		Args:
			:date_col: Name of the column to consider as datetime
			:cols: default '[]' List of columns to consider
			:plot_on: default 'date' Ploting xaxis based on date, month or year
			:fig_size: default '(10, 5)' size of graph to save or print
			:kind: default 'line' Type of graph


		Return:
			:matplotlib.axes._subplots.AxesSubplot: object

		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.plot_timeseries('Date', ['Number_of_Casualties', 'Number_of_Vehicles'], plot_on='month', kind='bar')
	
		"""

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
		"""
		Convert column to datetime object, on inplace Profiling object

		Args:
			:col: Name of the column to consider

		Return:
			:None: Changes the object inplace


		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.to_datetime('Date')

				
		"""

		try:
			self[col] = self[col].map(lambda d: datetime.strptime(d, '%d/%m/%Y') if not isinstance(d, pd._libs.tslibs.timestamps.Timestamp) else d)
		except TypeError as e:
			print(col, "isn't a string column or doesn't contain date")

	def plot(self, x: str, y: list, kind='line', figsize=(10, 5)) -> matplotlib.axes._subplots:
		"""
		Plot dataset based on columns passed

		Args:
			:x: xaxis variable to consider
			:y: List of variable to consider for y axis
			:kind: default 'line' Type of graph
			:figsize: default '(10, 5)' size of graph to save or print

		Return:
			:matplotlib.axes._subplots.AxesSubplot: object

		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.plot(x='Day_of_Week', y=['Number_of_Casualties', 'Number_of_Vehicles'])

				
		"""

		s_d = self.v_type(self[[x]])

		if (s_d[x]['type']).value == 'CAT' or (s_d[x]['type']).value == 'NUM':
			return self.groupby([x]).sum()[y].plot(kind=kind, figsize=figsize)

		return super().plot(x, y, kind=kind, figsize=figsize)

	def v_type(self, df) -> dict:
		"""
		Provides the type variables in the dataframe

		Args:
			:df: pandas.DataFrame or profiling.Profiling

		Return:
			:dict: Variable names along its data types


		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				d = p.v_type(p.psubset(['Number_of_Casualties', 'Light_Conditions', 'Did_Police_Officer_Attend_Scene_of_Accident']))
				for k, v in d.items():
				    print(k, '\t', v['type'].value)

				
		"""

		a = [(c, s) for c, s in df.iteritems()]
		s_d = {c: s for c, s in itertools.starmap(md, a)}
		return s_d

	def profile(self, subset=0, cols=[], title='Report', pool_size=0, minify_html=False, output=None):
		"""
		Create report of the dataframe

		Args:
			:subset: default '0', Number of rows to consider while creating profile
			:cols:	default '[]' List of columns to consider while creating profile
			:title: default 'Report' Name of the report
			:pool_size: default '0' Number of cores to use
			:minify_html: default 'False' Whether to minify html or not
			:output: default 'None' Path of the output file

		Return:
			:pp.__init__.ProfileReport: object


		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.profile(cols=['Number_of_Casualties'])

				
		"""

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
		"""
		Provides correlation between of passed variables

		Args:
			:subset: List of columns to consider while finding correlations
			:method: correlation method to consider, default 'pearson'


		Return:
			:profiling.Profiling: object


		Example:
			.. code-block:: python

				from profiling import Profiling
				p = Profiling(file_path='Datasources/Acc.csv')
				p.correlation(subset=['Number_of_Casualties', 'Number_of_Vehicles', 'Light_Conditions'])

		"""

		if len(subset) == 0:
			return self.corr(method=method)

		return Profiling(self[subset].corr(method=method))









