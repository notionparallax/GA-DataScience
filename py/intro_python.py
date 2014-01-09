# Some data types
#Numbers: Integer,  Float,  Complex Numbers,  Booleans (these can be used in arithmetics)

#%%
#Lists
x = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
x[0]
x[-1]
x[1:-1]
x[:2]
x[3:]

#%%
#Dictionary
dic_name = {'item_1':1, 'item_2':2, 'item_3':3}
dic_name['item_1']
len(dic_name)
len(dic_name['item_1'])
len(str(dic_name['item_1']))

#%%
#Tuples - are immutable
tup = (1, 2, 3, 4, 5)

#%%
#Numpy arrays
import numpy as np
a = np.array([1, 2, 3, 4])
a.mean
a.mean()
a.std()
np.std(a)
np.mean(a)
a.append(6)
c = np.array([1, 2,  np.NAN, 3, 4])
c.ndim
c.shape
c[~np.nan(c)]
c[~np.isnan(c)]
np.mean(c)
np.mean(c[~np.isnan(c)])

#%%
#Fibonacci sequence
def fib(n):
    '''Print a Fibonacci series up to n'''
    a, b = 0, 1
    while a < n:
        print a, 
        a, b = b,  a+b     
fib(1000)

#%%
#Example prompt for input and if-elif-else statement
original = raw_input()
if len(original) > 0:
    print (original)
elif original.isalpha() == True:
    print (original)
else:
    print ("empty")
    
#%%
# Example read JSON file 
import json
path = '~/Book-files/pydata-book-master/ch02/usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]
records[0]
len(records)
print records[0]['r']
print records[0]['tz']
#%%
timezone = [rec['tz'] for rec in records]
timezone = [rec['tz'] for rec in records if 'tz' in records]
len(timezone)
#%%
timezone[:0]
timezone[:1]
timezone[:5]
timezone[:10]
#%%
def get_counts(sequence):
    counts={}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

counts = get_counts(timezone)

counts

#%%
num_list = [1, 2, 3, 4, 5]
for x in num_list:
    print x**2
    
x_square=[]
for x in num_list:
    x_square.append(x**2)
    
x_square