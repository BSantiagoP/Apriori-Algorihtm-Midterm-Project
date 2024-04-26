#!/usr/bin/env python
# coding: utf-8

# # Reading File

# In[23]:


import csv
import time
import pandas as pd
import itertools


# In[24]:


def load_data(filename):
    full_transaction_list= []
    with open(filename, encoding = 'utf-8-sig') as data:
        transaction_data = csv.reader(data, delimiter = ',')
        for  row in transaction_data:
            filtered_rows = [value for value in row if value != '']
            full_transaction_list.append(filtered_rows)
        return full_transaction_list


# In[25]:


#Asking the user to input the file
new_list = load_data(input('please enter file name\n'))


# # Asking user for min support and confidence

# In[26]:


try:
    user_input_minsupport =int(input('Please enter the minimum support value in percentage ex: 25 is 25%:\n\n'))
    user_input_minConfidence = int(input('\nPlease enter the min confidence value n percentage ex: 50 is 50%:\n\n'))
except:
    if user_input_minsupport == int(user_input_minsupport) or user_input_minConfidence == int(user_input_minConfidence):
        print('please enter a numerical value') 


# # Transaction 2

# ### Apriori Algorithm

# In[27]:


start_time = time.time()

#function to find all the unique values with their counts
def Uniquevalues(Transactions):
    unique_items = {}
    for rows in Transactions:
        for items in rows:
            if items not in unique_items:
                unique_items[items] = 1
            else:
                unique_items[items] = unique_items[items] + 1
    uniqueitemlist = []
    for value in unique_items:
        Valuelist = []
        Valuelist.append(value)
        uniqueitemlist.append(Valuelist)
        uniqueitemlist.append(unique_items[value])
    return uniqueitemlist


# In[28]:


One_UniqueItems = Uniquevalues(new_list)
print('These are the unique items for Transaction 1:\n\n', One_UniqueItems)


# In[29]:


#function used to remove the items that do not meet the threshold
def remove_lessthansupportone(Candidates, transactions):
    Firstcandidate_list= []
    for i in range(len(Candidates)):
        if i%2 != 0:
            if (Candidates[i] / len(new_list))*100 >= user_input_minsupport:
                Firstcandidate_list.append(Candidates[i-1])
                Firstcandidate_list.append(Candidates[i]) 
    candidatesforcombo = []
    for i in range(len(Firstcandidate_list)):
        if i%2 == 0:
            candidatesforcombo.append(Firstcandidate_list[i])
    return candidatesforcombo


# In[30]:


removed_first = remove_lessthansupportone(One_UniqueItems, new_list)
print('\nThese are the candidates after the first pass\n\n',removed_first )


# In[31]:


#function used to output all possible combinations (k itemsets)
def Allpossiblecombinations(candidatesforcombo):
    if not candidatesforcombo:
        return [[]]
    first= candidatesforcombo[0]
    Allothers = candidatesforcombo[1:]
    Withoutfirst = Allpossiblecombinations(Allothers)
    Withfirst = [combo + [first] for combo in Withoutfirst]
    Combinedlist=Withoutfirst + Withfirst
    return Combinedlist


# In[32]:


All_combos = Allpossiblecombinations(removed_first)


# In[33]:


#function used to add the number of counts to the list provided before
def allcombosunique(Combination, dataset):
    from collections import Counter
    Count = Counter()
    for row in Combination:
        for s in dataset:
            if all(item in s for item in sum(row, [])):
                Count[tuple(map(tuple, row))] += 1     
    listcount = [[list(subset), count] for subset, count in Count.items()]
    return(listcount)


# In[34]:


All_uniquecombos = allcombosunique(All_combos, new_list)
print('\nAll unique possible combinations\n',All_uniquecombos )


# In[35]:


#Second function to remove the items that do not meet the threshold
def remove_lessthansupporttwo(Candidates, dataset):
    list1 = []
    for outlist in Candidates:
        if len(outlist) >= 2:
            second_object = outlist[1]
            if (second_object / len(new_list))*100  >= user_input_minsupport:
                list1.append(outlist[0])
                list1.append(outlist[1])  
    return list1


# In[36]:


removed_second = remove_lessthansupporttwo(All_uniquecombos, new_list)
print('\nThese are the candidates after the next pass\n',removed_second )


# In[37]:


def Rules(CandidateSet):
    CandidateRule = []
    for candidates in CandidateSet:
        if isinstance(candidates, list):
            if len(candidates) != 0:
                length_candidates = len(candidates) - 1
                while length_candidates > 0:
                    combos = list(itertools.combinations(candidates, length_candidates))
                    combolist = []
                    Left = []
                    for Right in combos:
                        Left = set(candidates) - set(Right)
                        combolist.append(list(Left))
                        combolist.append(list(Right))
                        CandidateRule.append(combolist)
                        combolist = []
                    length_candidates = length_candidates - 1
                    
    return CandidateRule


# In[38]:


Associationrules = Rules(removed_second)
print('\nThese are the association rules\n\n',Associationrules )


# In[39]:


def Apriori(Associationrules, new_list, user_input_minConfidence):
    AAlgorithm = []
    for rule in Associationrules:
        first = set(item[0] for item in rule[0])
        Asupport = 0
        ABsupport = 0
        for transaction in new_list:
            if first.issubset(set(transaction)):
                Asupport += 1
            if all(set(item) <= set(transaction) for each in rule for item in each):
                ABsupport += 1
        CalculateASupport = (Asupport * 1.0 / len(new_list)) * 100
        CalculateABSupport = (ABsupport * 1.0 / len(new_list)) * 100
        confidence = (CalculateABSupport / CalculateASupport) * 100
        if confidence >= user_input_minConfidence:
            OutputASupport = "A Support is: " + str(round(CalculateASupport,2))
            OutputABSupport = "\nA&B support is: " + str(CalculateABSupport)
            OutputConfidence = "\nConfidence is: " + str(round(confidence))
            AAlgorithm.append(OutputASupport)
            AAlgorithm.append(OutputABSupport)
            AAlgorithm.append(OutputConfidence)
            AAlgorithm.append(rule)
    return AAlgorithm
     


# In[40]:


Apriori = Apriori(Associationrules, new_list, user_input_minConfidence)
print('\nApriori algorithm\n', Apriori )


# In[41]:


counter = 1
for i in Apriori:
    if counter == 4:
        print("\n"+str(i[0]) + "------->" + str(i[1])+"\n")
        counter = 0
    else:
        print(i, end='  ')
    counter = counter + 1
elapsed_time = time.time() - start_time
print("--- %s seconds ---" % (elapsed_time))


# ### Brute Force

# In[42]:


import pandas as pd
import time
from itertools import combinations


# In[43]:


Transactiondata = input("Enter the file name: ")
minsupport = float(input('Please enter the minimum support value'))


# In[44]:


start_time = time.time()
transaction = pd.read_csv(Transactiondata, header =None)
TransactionforSum = pd.get_dummies(transaction.unstack().dropna()).groupby(level=1).sum()
UniqueItems = TransactionforSum.sum()  


# In[45]:


print('\nThese are all unique one item sets:\n\n', UniqueItems)


# In[46]:


OneItemSets = pd.DataFrame((UniqueItems / len(transaction) * 100), columns = ['support'])
OneFrequentItems = OneItemSets[OneItemSets['support'] >= minsupport]
print('These are the Frequent One Item sets:\n', OneFrequentItems)


# In[47]:


import itertools
items = UniqueItems.index
combos = list(itertools.combinations(items, 2))
combinations = []
for combo in combos:
    combinations.append(combo)


# In[48]:


combo_counts = {}  
for i in range(len(combinations)):
    combo = combinations[i]
    count = 0 
    for index, row in transaction.iterrows():
        if set(combo).issubset(row):
            count += 1
    combo_counts[i+1] = count   
print('Thesea are all the two possible combinations:\n\n')
for combo_num, count in combo_counts.items():
    print(f"({combinations[combo_num-1]})  , Number of repetitions {count}.")


# In[49]:


print('These are the 2 frequent itemsets:\n\n')
for combo_num, count in combo_counts.items():
    if (count / len(transaction) * 100) >= minsupport:
        print(f" ({combinations[combo_num-1]})   number of repetition: {count}.")


# In[50]:


combinations = []
for r in range(3,4):  
    combos = list(itertools.combinations(items, r))
    combinations.extend(combos)

# Filter out empty tuples
combinations = [combo for combo in combinations if combo]


# In[51]:


combo_counts = {}  
for i in range(len(combinations)):
    combo = combinations[i]
    count = 0 
    for index, row in transaction.iterrows():
        if set(combo).issubset(row):
            count += 1
    combo_counts[i+1] = count 
print('These are the 3 possible combinations\n\n')
for combo_num, count in combo_counts.items():
    print(f"({combinations[combo_num-1]}) number of repetitions {count}\n")


# In[52]:


print('These are the 3 Frequent item set:\n\n')
for combo_num, count in combo_counts.items():
    if (count / len(transaction) * 100) >= minsupport:
        print(f"({combinations[combo_num-1]}) number of repetitions {count}\n")


# In[53]:


combinations = []
for r in range(4,20):  
    combos = list(itertools.combinations(items, r))
    combinations.extend(combos)

# Filter out empty tuples
combinations = [combo for combo in combinations if combo]


# In[54]:


combo_counts = {}  
for i in range(len(combinations)):
    combo = combinations[i]
    count = 0 
    for index, row in transaction.iterrows():
        if set(combo).issubset(row):
            count += 1
            #print(f"Combo {i+1} ({combo}) is a subset of row {index} in the DataFrame.")
    combo_counts[i+1] = count
print('These are the 4 and 4+ Frequent item sets:\n\n')
for combo_num, count in combo_counts.items():
    print(f"({combinations[combo_num-1]}) number of repetitions {count}.\n\n")


# In[55]:


print('These are all the other frequent item sets:\n')
for combo_num, count in combo_counts.items():
    if (count / len(transaction) * 100) >= minsupport:
        print(f"({combinations[combo_num-1]}) number of repetitions: {count} .")


# In[56]:


elapsed_time = time.time() - start_time
print("--- %s seconds ---" % (elapsed_time))


# ### Aplying Apriori Library 

# In[57]:


import csv
import pandas as pd
import time
from itertools import combinations
from apyori import apriori
from mlxtend.frequent_patterns import apriori, fpmax
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder


# In[58]:


#The below will allow us to read the file
def load_data(filename):
    full_transaction_list= []
    with open(filename, encoding = 'utf-8-sig') as data:
        transaction_data = csv.reader(data, delimiter = ',')
        for  row in transaction_data:
            filtered_rows = [value for value in row if value != '']
            full_transaction_list.append(filtered_rows)
        return full_transaction_list


# In[59]:


new_list = load_data(input('please enter file name\n\n'))


# In[60]:


new_list


# In[61]:


TranEn = TransactionEncoder()
TranEn_ary=TranEn.fit(new_list).transform(new_list)


# In[62]:


Dataframe = pd.DataFrame(TranEn_ary, columns=TranEn.columns_)
Dataframe


# In[63]:


frequentItemsets = apriori(Dataframe, min_support = 0.35, use_colnames=True)
frequentItemsets


# In[64]:


Rules = association_rules(frequentItemsets, metric="confidence", min_threshold=0.75)
Rules

