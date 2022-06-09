# -*- coding: utf-8 -*-
"""MAT012 - c1996821.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IZSfUyPY0z_uy0PNVI9sEIkvkOd2pTuW
"""

!pip install category_encoders

!pip install bayesian-optimization

#PART B

import pandas as pd
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import random
import matplotlib.pyplot as plt 
import matplotlib.mlab as mlab
import seaborn as sns
import pickle
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
import category_encoders as ce
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split, RepeatedStratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, precision_recall_curve, auc
from sklearn.feature_selection import f_classif
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from scipy.stats import chi2_contingency
from sklearn.linear_model import LinearRegression
from itertools import cycle
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier

gcd = pd.read_excel("GermanCreditData.xlsx", sheet_name="Sheet1")
gcd = gcd.replace('X',10)
gcd['Score']=0
print(gcd.columns)

##1

subset1_bs = gcd[gcd['Duration'] <=12]
subset2_bs = gcd[gcd['Duration'] >12]

##The Question 2 is under the Question 3. 
#Sorry my code is a bit messy. 
#I also have a version in excel.

"""The Question 2 is under the Question 3."""

##3

#Credit history(have credit and no credit:1(012),0(34)/delay and no delay:1(3),0(0124))
#age(0-30,31-40,41-50,51-60,61-)
#own house(have house 1, no house 234)
#skilled(no 0, have 1)

#subset1
data1=[]
subset1 = pd.DataFrame(data1,columns=['History012','HistoryDelay','Age0-30','Age31-40','Age41-50','Age51-60','Age61-','Property(House)','Skilled','Good','Score'])
subset1['History012'] = subset1_bs['History']
subset1['HistoryDelay'] = subset1_bs['History']
subset1['Age0-30'] = subset1_bs['Age']
subset1['Age31-40'] = subset1_bs['Age']
subset1['Age41-50'] = subset1_bs['Age']
subset1['Age51-60'] = subset1_bs['Age']
subset1['Age61-'] = subset1_bs['Age']
subset1['Property(House)'] = subset1_bs['Property']
subset1['Skilled'] = subset1_bs['Job']
subset1['Good'] = subset1_bs['Good']
subset1['Score'] = 0

subset1['History012'] = subset1['History012'].replace(0,1)
subset1['History012'] = subset1['History012'].replace(2,1)
subset1['History012'] = subset1['History012'].replace(3,0)
subset1['History012'] = subset1['History012'].replace(4,0)

subset1['HistoryDelay'] = subset1['HistoryDelay'].replace(1,0)
subset1['HistoryDelay'] = subset1['HistoryDelay'].replace(2,0)
subset1['HistoryDelay'] = subset1['HistoryDelay'].replace(4,0)
subset1['HistoryDelay'] = subset1['HistoryDelay'].replace(3,1)

subset1.loc[subset1['Age0-30']<=30,'Age0-30'] = 1
subset1.loc[subset1['Age0-30']>30,'Age0-30'] = 0

subset1.loc[(subset1['Age31-40']<=30) | (subset1['Age31-40']>40),'Age31-40'] = 0
subset1.loc[(subset1['Age31-40']<=40) & (subset1['Age31-40']>30),'Age31-40'] = 1

subset1.loc[(subset1['Age41-50']<=40) | (subset1['Age41-50']>50),'Age41-50'] = 0
subset1.loc[(subset1['Age41-50']<=50) & (subset1['Age41-50']>40),'Age41-50'] = 1

subset1.loc[(subset1['Age51-60']<=50) | (subset1['Age51-60']>60),'Age51-60'] = 0
subset1.loc[(subset1['Age51-60']<=60) & (subset1['Age51-60']>50),'Age51-60'] = 1

subset1.loc[subset1['Age61-']<=60,'Age61-'] = 0
subset1.loc[subset1['Age61-']>60,'Age61-'] = 1

subset1['Property(House)'] = subset1['Property(House)'].replace(2,0)
subset1['Property(House)'] = subset1['Property(House)'].replace(3,0)
subset1['Property(House)'] = subset1['Property(House)'].replace(4,0)

subset1['Skilled'] = subset1['Skilled'].replace(1,0)
subset1['Skilled'] = subset1['Skilled'].replace(2,0)
subset1['Skilled'] = subset1['Skilled'].replace(3,1)
subset1['Skilled'] = subset1['Skilled'].replace(4,1)

#subset2
data2=[]
subset2 = pd.DataFrame(data2,columns=['History012','HistoryDelay','Age0-30','Age31-40','Age41-50','Age51-60','Age61-','Property(House)','Skilled','Good','Score'])
subset2['History012'] = subset2_bs['History']
subset2['HistoryDelay'] = subset2_bs['History']
subset2['Age0-30'] = subset2_bs['Age']
subset2['Age31-40'] = subset2_bs['Age']
subset2['Age41-50'] = subset2_bs['Age']
subset2['Age51-60'] = subset2_bs['Age']
subset2['Age61-'] = subset2_bs['Age']
subset2['Property(House)'] = subset2_bs['Property']
subset2['Skilled'] = subset2_bs['Job']
subset2['Good'] = subset2_bs['Good']
subset2['Score'] = 0

subset2['History012'] = subset2['History012'].replace(0,1)
subset2['History012'] = subset2['History012'].replace(2,1)
subset2['History012'] = subset2['History012'].replace(3,0)
subset2['History012'] = subset2['History012'].replace(4,0)

subset2['HistoryDelay'] = subset2['HistoryDelay'].replace(1,0)
subset2['HistoryDelay'] = subset2['HistoryDelay'].replace(2,0)
subset2['HistoryDelay'] = subset2['HistoryDelay'].replace(4,0)
subset2['HistoryDelay'] = subset2['HistoryDelay'].replace(3,1)

subset2.loc[subset2['Age0-30']<=30,'Age0-30'] = 1
subset2.loc[subset2['Age0-30']>30,'Age0-30'] = 0

subset2.loc[(subset2['Age31-40']<=30) | (subset2['Age31-40']>40),'Age31-40'] = 0
subset2.loc[(subset2['Age31-40']<=40) & (subset2['Age31-40']>30),'Age31-40'] = 1

subset2.loc[(subset2['Age41-50']<=40) | (subset2['Age41-50']>50),'Age41-50'] = 0
subset2.loc[(subset2['Age41-50']<=50) & (subset2['Age41-50']>40),'Age41-50'] = 1

subset2.loc[(subset2['Age51-60']<=50) | (subset2['Age51-60']>60),'Age51-60'] = 0
subset2.loc[(subset2['Age51-60']<=60) & (subset2['Age51-60']>50),'Age51-60'] = 1

subset2.loc[subset2['Age61-']<=60,'Age61-'] = 0
subset2.loc[subset2['Age61-']>60,'Age61-'] = 1

subset2['Property(House)'] = subset2['Property(House)'].replace(2,0)
subset2['Property(House)'] = subset2['Property(House)'].replace(3,0)
subset2['Property(House)'] = subset2['Property(House)'].replace(4,0)

subset2['Skilled'] = subset2['Skilled'].replace(1,0)
subset2['Skilled'] = subset2['Skilled'].replace(2,0)
subset2['Skilled'] = subset2['Skilled'].replace(3,1)
subset2['Skilled'] = subset2['Skilled'].replace(4,1)

##2

#For subset1
features = ['History012','HistoryDelay','Age0-30','Age31-40','Age41-50','Age51-60','Age61-','Property(House)','Skilled']
X = subset1[features]
y = subset1['Good']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

##4

#Linear Regression

model = LinearRegression() # Constructing linear models
model.fit(X_train, y_train) # Independent variable in front, dependent variable in back
predicts = model.predict(X_test) # Predicted value
R2 = model.score(X_test, y_test) # Degree of fit R2
print('R2 = %.3f' % R2) # Output R2
coef = model.coef_ # Slope
intercept = model.intercept_ # intercept distance
print(model.coef_, model.intercept_) # Output slope and intercept

##4,5

##LogisticRegression

clf = LogisticRegression(C=1,penalty='l2', solver='newton-cg')

# Printing all the parameters of logistic regression
# print(clf)

# Creating the model on Training Data
LOG=clf.fit(X_train,y_train)
prediction=LOG.predict(X_test)

# Measuring accuracy on Testing Data
from sklearn import metrics
print(metrics.classification_report(y_test, prediction))
print(metrics.confusion_matrix(y_test, prediction))

# Printing the Overall Accuracy of the model
F1_Score=metrics.f1_score(y_test, prediction, average='weighted')
print('Accuracy of the model on Testing Sample Data:', round(F1_Score,2))

# Importing cross validation function from sklearn
from sklearn.model_selection import cross_val_score

# Running 10-Fold Cross validation on a given algorithmd
# Passing full data X and y because the K-fold will split the data and automatically choose train/test
Accuracy_Values=cross_val_score(LOG, X , y, cv=10, scoring='f1_weighted')
print('\nAccuracy values for 10-fold Cross Validation:\n',Accuracy_Values)
print('\nFinal Average Accuracy of the model:', round(Accuracy_Values.mean(),2))

# make preditions on our test set
y_hat_test = xmodel.predict(X_test)
# get the predicted probabilities
y_hat_test_proba = xmodel.predict_proba(X_test)
# select the probabilities of only the positive class (class 1 - default) 
y_hat_test_proba = y_hat_test_proba[:][: , 1]

# we will now create a new DF with actual classes and the predicted probabilities
# create a temp y_test DF to reset its index to allow proper concaternation with y_hat_test_proba
y_test_temp = y_test.copy()
y_test_temp.reset_index(drop = True, inplace = True)
y_test_proba = pd.concat([y_test_temp, pd.DataFrame(y_hat_test_proba)], axis = 1)
# Rename the columns
y_test_proba.columns = ['y_test_class_actual', 'y_hat_test_proba']
# Makes the index of one dataframe equal to the index of another dataframe.
y_test_proba.index = X_test.index

# get the values required to plot a ROC curve
fpr, tpr, thresholds = roc_curve(y_test_proba['y_test_class_actual'], y_test_proba['y_hat_test_proba'])
# plot the ROC curve
plt.plot(fpr, tpr)
# plot a secondary diagonal line, with dashed line style and black color to represent a no-skill classifier
plt.plot(fpr, fpr, linestyle = '--', color = 'k')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve')

##4,5

ns_probs = [0 for _ in range(len(y_test))]
# fit a model
model = LogisticRegression(solver='lbfgs')
model.fit(X_train, y_train)
# predict probabilities
lr_probs = model.predict_proba(X_test)
# keep probabilities for the positive outcome only
lr_probs = lr_probs[:, 1]
# calculate scores
ns_auc = roc_auc_score(y_test, ns_probs)
lr_auc = roc_auc_score(y_test, lr_probs)
# summarize scores
print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('Logistic: ROC AUC=%.3f' % (lr_auc))
GINI = (2 * lr_auc) - 1
print('GINI:',GINI)
# calculate roc curves
ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
# plot the roc curve for the model
plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
plt.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')
# axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()

##2

#For subset2

features = ['History012','HistoryDelay','Age0-30','Age31-40','Age41-50','Age51-60','Age61-','Property(House)','Skilled']
X = subset2[features]
y = subset2['Good']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

##4

#Linear Regression

model = LinearRegression() # Constructing linear models
model.fit(X_train, y_train) # Independent variable in front, dependent variable in back
predicts = model.predict(X_test) # Predicted value
R2 = model.score(X_test, y_test) # Degree of fit R2
print('R2 = %.3f' % R2) # Output R2
coef = model.coef_ # Slope
intercept = model.intercept_ # intercept distance
print(model.coef_, model.intercept_) # Output slope and intercept

##4,5

##LogisticRegression

clf = LogisticRegression(C=1,penalty='l2', solver='newton-cg')

# Printing all the parameters of logistic regression
# print(clf)

# Creating the model on Training Data
LOG=clf.fit(X_train,y_train)
prediction=LOG.predict(X_test)

# Measuring accuracy on Testing Data
from sklearn import metrics
print(metrics.classification_report(y_test, prediction))
print(metrics.confusion_matrix(y_test, prediction))

# Printing the Overall Accuracy of the model
F1_Score=metrics.f1_score(y_test, prediction, average='weighted')
print('Accuracy of the model on Testing Sample Data:', round(F1_Score,2))

# Importing cross validation function from sklearn
from sklearn.model_selection import cross_val_score

# Running 10-Fold Cross validation on a given algorithmd
# Passing full data X and y because the K-fold will split the data and automatically choose train/test
Accuracy_Values=cross_val_score(LOG, X , y, cv=10, scoring='f1_weighted')
print('\nAccuracy values for 10-fold Cross Validation:\n',Accuracy_Values)
print('\nFinal Average Accuracy of the model:', round(Accuracy_Values.mean(),2))

# make preditions on our test set
y_hat_test = xmodel.predict(X_test)
# get the predicted probabilities
y_hat_test_proba = xmodel.predict_proba(X_test)
# select the probabilities of only the positive class (class 1 - default) 
y_hat_test_proba = y_hat_test_proba[:][: , 1]

# we will now create a new DF with actual classes and the predicted probabilities
# create a temp y_test DF to reset its index to allow proper concaternation with y_hat_test_proba
y_test_temp = y_test.copy()
y_test_temp.reset_index(drop = True, inplace = True)
y_test_proba = pd.concat([y_test_temp, pd.DataFrame(y_hat_test_proba)], axis = 1)
# Rename the columns
y_test_proba.columns = ['y_test_class_actual', 'y_hat_test_proba']
# Makes the index of one dataframe equal to the index of another dataframe.
y_test_proba.index = X_test.index

# get the values required to plot a ROC curve
fpr, tpr, thresholds = roc_curve(y_test_proba['y_test_class_actual'], y_test_proba['y_hat_test_proba'])
# plot the ROC curve
plt.plot(fpr, tpr)
# plot a secondary diagonal line, with dashed line style and black color to represent a no-skill classifier
plt.plot(fpr, fpr, linestyle = '--', color = 'k')
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve')

##4,5

ns_probs = [0 for _ in range(len(y_test))]
# fit a model
model = LogisticRegression(solver='lbfgs')
model.fit(X_train, y_train)
# predict probabilities
lr_probs = model.predict_proba(X_test)
# keep probabilities for the positive outcome only
lr_probs = lr_probs[:, 1]
# calculate scores
ns_auc = roc_auc_score(y_test, ns_probs)
lr_auc = roc_auc_score(y_test, lr_probs)
# summarize scores
print('No Skill: ROC AUC=%.3f' % (ns_auc))
print('Logistic: ROC AUC=%.3f' % (lr_auc))
GINI = (2 * lr_auc) - 1
print('GINI:',GINI)
# calculate roc curves
ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
# plot the roc curve for the model
plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
plt.plot(lr_fpr, lr_tpr, marker='.', label='Logistic')
# axis labels
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
# show the legend
plt.legend()
# show the plot
plt.show()