import unittest
from profiling import Profiling
import pandas_profiling as pp
import matplotlib


class TestProfiling(unittest.TestCase):

	def setUp(self):
		self.path = 'Datasources/Acc.csv'

	def pObj(self, show_report=False, subset=5):
		self.p = Profiling(file_path=self.path, show_report=show_report, subset=subset)
		return self.p.read_csv()

	def test_read_csv_without_file(self):
		p = Profiling(data=[[]])
		t = p.read_csv()
		self.assertEqual(None, t)

	def test_read_csv_with_path(self):
		self.pObj()
		self.assertEqual(list(self.p.columns)[0], 'Accident_Index')
		self.assertEqual(len(list(self.p.columns)), 32)

	def test_read_csv_with_show_report(self):
		t = self.pObj(show_report=True)
		self.assertEqual(type(t), pp.__init__.ProfileReport)

	def test_psubset(self):
		self.pObj()
		df = self.p.psubset(cols=['Day_of_Week', 'Number_of_Casualties'])
		self.assertEqual(len(df.columns), 2)
		self.assertEqual(df.shape[0], 20)

	def test_details(self):
		self.pObj()
		t = self.p.details(cols=['Number_of_Casualties', 'Number_of_Vehicles'])
		self.assertEqual(t['Number_of_Casualties']['count'], 129982.0)
		self.assertEqual(t['Number_of_Vehicles']['max'], 23.0)

	def test_plot_timeseries(self):
		self.pObj()
		t = self.p.plot_timeseries('Date', ['Number_of_Casualties'])
		self.assertEqual(t.__class__.__name__, 'AxesSubplot')

	def test_to_datetime(self):
		self.pObj()
		self.p.to_datetime('Date')
		self.assertEqual(self.p.dtypes['Date'], 'datetime64[ns]')

	def test_plot(self):
		self.pObj()
		t = self.p.plot(x='Day_of_Week', y=['Number_of_Casualties', 'Number_of_Vehicles'])
		self.assertEqual(t.__class__.__name__, 'AxesSubplot')

	def test_v_type(self):
		self.pObj()
		t = self.p.v_type(self.p[['Number_of_Casualties', 'Did_Police_Officer_Attend_Scene_of_Accident']])
		self.assertEqual(t['Number_of_Casualties']['type'].value, 'NUM')
		self.assertEqual(t['Did_Police_Officer_Attend_Scene_of_Accident']['type'].value, 'CAT')

	def test_profile(self):
		self.pObj()
		t = self.p.profile(cols=['Number_of_Casualties'])
		self.assertEqual(type(t), pp.__init__.ProfileReport)

	def test_correlation(self):
		self.pObj()
		t = self.p.correlation(subset=['Number_of_Casualties', 'Day_of_Week'])
		self.assertEqual(t['Number_of_Casualties']['Day_of_Week'], -0.0046139671238656565)

if __name__ == '__main__':
	unittest.main()


	