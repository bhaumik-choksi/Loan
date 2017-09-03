import pandas as pd
path = "loan_small.csv"


def intify_categories(arr):
	unique_items = list(set(arr))
	mapping = {}
	i = 0
	for unique_item in unique_items:
		mapping[unique_item] = i
		i += 1

	output = list(map((lambda x : mapping[x]),arr))
	return output

data = pd.read_csv(path, usecols = ['loan_amnt',
 	'term', 
 	'int_rate', 
	'installment',
  	'emp_length', 
	'home_ownership', 
	'annual_inc',
	'verification_status',
	'purpose', 
	'dti',
	'delinq_2yrs',
	'inq_last_6mths',
	'mths_since_last_delinq', 
	'open_acc',
	'pub_rec', 
	'revol_bal', 
	'revol_util',
	'total_acc'])

data['term'] = data['term'].apply(lambda x : int(x.replace("months","").strip()))

data['emp_length'] = intify_categories(data['emp_length'])
data['home_ownership'] = intify_categories(data['home_ownership'])
data['verification_status'] = intify_categories(data['verification_status'])
data['purpose'] = intify_categories(data['purpose'])

print(data.dtypes)