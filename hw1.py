#Michael Fosco
#4-3-16

import numpy as np 
import pandas as pd 
import requests

'''
Problem A

 

The first task is to load the file and generate summary statistics for each field
 as well as probability distributions or histograms. 
 The summary statistics should include mean, median, mode, standard deviation, 
 as well as the number of missing values for each field.
 DONE

You will notice that a lot of students are missing gender values . 
Your task is to infer the gender of the student based on their name. 
Please use the API at www.genderize.io to infer the gender of each student and 
generate a new data file.

You will also notice that some of the other attributes are missing. Your task is 
to fill in the missing values for Age, GPA, and Days_missed using the following 
approaches:
Fill in missing values with the mean of the values for that attribute
Fill in missing values with a class-conditional mean (where the class is 
	whether they graduated or not).
Is there a better, more appropriate method for filling in the missing values? 
If yes, describe and implement it. 
You should create 2 new files with the missing values filled, one for each approach
 A, B, and C and submit those along with your code. 

Please submit the Python code for each of these tasks as well as the new data files for this assignment.
'''

# First part
data = pd.read_csv("mock_student_data.csv")
data.describe()
print "Note the median is the 50%"
dt = pd.DataFrame(data)
missingVals = len(data.index) - data.count()
data.mode()

z = data.hist(layout=(2,2))
z[0][1].get_figure().savefig('hists.pdf')


def getGender(name):
	r = requests.get('https://api.genderize.io/?name=' + name)
	s = r.text

	beg = s.index('gender')+9
	en = s[beg:].index('"') + beg
	gender = s[beg:en]

	if gender == 'male':
		return "Male"
	return "Female"

def addGenders(dat):
	df = dat
	temp = data['Gender']

	for i in df.index:
		print str(i)
		if type(temp[i]) != str and np.isnan(temp[i]):
			df.set_value(i, 'Gender', getGender(df.get_value(i, 'First_name')))
	return df




#part ii
dfGender = addGenders(data)
dfGender.to_csv('genderAdded.csv')

#part iii
def wayA(dat):
	aMean = dat.Age.mean()
	gpaMean = dat.GPA.mean()
	dmMean = dat.Days_missed.mean()
	df = dat

	df['Age'] = df['Age'].fillna(aMean)
	df['GPA'] = df['GPA'].fillna(gpaMean)
	df['Days_missed'] = df['Days_missed'].fillna(dmMean)

	return df

dfA = wayA(dfGender)

dfA.to_csv("wayA.csv")

def wayB(dat):
	df = dat
	means = df.groupby(['Graduated'])['Age'].mean()
	df = df.set_index(['Graduated'])
	df['Age'] = df['Age'].fillna(means)
	df = df.reset_index()

	means = df.groupby(['Graduated'])['GPA'].mean()
	df = df.set_index(['Graduated'])
	df['GPA'] = df['GPA'].fillna(means)
	df = df.reset_index()

	means = df.groupby(['Graduated'])['Days_missed'].mean()
	df = df.set_index(['Graduated'])
	df['Days_missed'] = df['Days_missed'].fillna(means)
	df = df.reset_index()

	return df

dfB = wayB(dfGender)
dfB.to_csv("wayB.csv")

'''
Instead of just taking the means of the values (conditional or nonconditional)
it should be better to interpolate what the values should be based
on a prediction from our data where we do have full information.
Thus, we can fit a linear model to predict what the value should be, using
the data points with no missing values to inform our prediction.
'''
def wayC(dat):
	df = dat
	df['Age'] = df['Age'].fillna(df.Age.interpolate())
	df['GPA'] = df['GPA'].fillna(df.GPA.interpolate())
	df['Days_missed'] = df['Days_missed'].fillna(df.Days_missed.interpolate())	
	return df	

dfC = wayC(dfGender)
dfC.to_csv("wayC.csv")











