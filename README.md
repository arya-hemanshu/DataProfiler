## Data Profiler

There are good data profilers available. Profiling library doesn't aim to build everything from scratch. It tries to built on top of existing tools.

The tool is built on top of pandas.DataFrame. Profiling class inherits all the methods of pandas.DataFrame and add a few of its own to enchance the capability of pandas.DataFrame bespoke to companies use case.

The tool combines pandas.DataFrame and pandas_profiling library into one class and makes direct use of pandas_profiling methods to get information about Variables.

#### Demo

- Open ```DataProfiler.ipynb```
- For full report open ```report.html``` in a browser

#### How to set up the tool

- Clone the repo
```
git clone https://github.com/arya-hemanshu/DataProfiler.git
```
- Install dependencies from ```requirements.txt``` by
```pip3 install -r requirements.txt```
- Run tests ```python TestProfiling.py```


#### How to run the tool
- By Importing
	- Copy the ```profiling.py``` into your working directory or start working in the same directory by creating a python notebook or python file

	- Import the ```profiling.py``` file by ```from profiling import Profiling```

	- An example notebook is in the repo ```DataProfiler.ipynb```
- By Terminal
	- Get help by ```python main.py -h```
	- Get ```correlation``` between variables 
		```
			python main.py \
			-d Datasources/Acc.csv \
			-n True \
			-co Days_of_Week -co Number_of_Casualties
		```
	- Describe Variables 
		```
			python main.py \
			-d Datasources/Acc.csv \
			-o describe \
			-c Number_of_Casualties -c Day_of_Week
		```
	- Get Variable types
		```
			python main.py \
			-d Datasources/Acc.csv \
			-n True \
			-vt Day_of_Week -vt Number_of_Casualties
		```
	- Plot Variables
		```
			python main.py \
			-d Datasources/Acc.csv \
			-o plot \
			-c Number_of_Casualties -c Number_of_Vehicles \
			-x Day_of_week \
			-ot image.png
		```
	- Profile Variables
		```
			python main.py \
			-d Datasources/Cas.csv \
			-o profile
		```

#### Future Developments

Profiling library is in very early stages of its development and would continue to develop. Improvement areas are:
- Ability to pass multiple csv files
- Ability to support more file types
- Adding bespoke sections to profile report
- Supporting more date formats









