import pandas as pd, matplotlib.pyplot as plt, numpy as np, seaborn as sns, movies
import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv("nonvoters_data.csv")

#Processing

columns_keep = ['RespId','Q20','Q21','Q22','Q26','Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5', 'Q27_6', 
                'Q30', 'Q31', 'Q32','ppage', 'educ', 'race', 'gender', 'income_cat','voter_category']

for i in ['Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5', 'Q27_6']:
    dummy.drop(dummy[dummy[i] == -1].index, inplace = True)
for i in ['race']:
    dummy.drop(dummy[dummy[i] == "White"].index, inplace = True)
for i in ['Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5', 'Q27_6']:
    dummy[i] = dummy[i].apply(lambda x: 'Yes' if x == 1 else 'No')
count = []
for i in range(len(dummy)):
    a = dummy.iloc[i].value_counts()
    if 'Yes' in a:
        b = a.loc['Yes']
        count.append(b)
    else:
        count.append(0)
dummy['count'] = count

dummy['income_cat'] = dummy['income_cat'].replace(['$75-125k', '$125k or more', '$40-75k', 'Less than $40k'], [((75+125)/2), 125, ((40+75)/2), ((0+40)/2)])
dummy2 = dummy[['RespId','ppage','educ','race','gender','income_cat', 'count','voter_category']]
dummy2 = dummy2.rename(columns={"count": "times_voted","ppage" : "age","RespId" : "Id"})

# First Visualization

table = pd.crosstab(dummy2['times_voted'], dummy2['gender'],normalize='index')

counts =dummy2['times_voted'].value_counts() 
counts = counts.sort_index(ascending=True)
counts = np.array(counts)
movies.mult_stacked_bar(table,['deeppink','cornflowerblue']
                ,counts=counts,legend_title='Gender',filename='Viz1.png',
                 title= 'In the past six elections being a consistent voter does \n not seem to depend too much on gender in minority groups',xlabel='Times Voted')

# Second Visualization

dummy2 = dummy2.loc[(dummy2.times_voted >= 5)]
table = pd.crosstab(dummy2['times_voted'], dummy2['gender'],normalize='index')

counts =dummy2['times_voted'].value_counts() 
counts = counts.sort_index(ascending=True)
counts = np.array(counts)

a = dummy2.gender.value_counts()
ax = a.plot.bar(stacked = False, rot = 0, fontsize = 16,
                    figsize = [16,5], color = ['cornflowerblue','deeppink'])
#remove top and right spines
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
[ax.spines[i].set_visible(False) for i in ax.spines]
#remove x tick marks
ax.tick_params(axis = 'x', length = 0)

for patch in ax.patches:
    x,y,height = patch.get_x(), patch.get_y(), patch.get_height()
    ax.text(x + 0.25,height+10,('n = ' + str(height)), fontsize=16,
            horizontalalignment='center')

plt.title('For eligible respondents who voted in all or all but one election in the \n last six elections, males are a larger share'
           , fontsize = 20, y = 1.07)
plt.savefig('Viz2.png',bbox_inches = 'tight')
plt.show()

# Third Visualization Code and more processing

import warnings
warnings.filterwarnings('ignore')
import pandas as pd, matplotlib.pyplot as plt, numpy as np, seaborn as sns, movies
data = pd.read_csv("nonvoters_data.csv")
columns_keep = ['RespId','Q20','Q21','Q22','Q26','Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5', 'Q27_6', 
                'Q30', 'Q31', 'Q32','ppage', 'educ', 'race', 'gender', 'income_cat','voter_category']
dummy = data[columns_keep]
for i in ['Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5', 'Q27_6']:
    dummy.drop(dummy[dummy[i] == -1].index, inplace = True)
for i in ['race']:
    dummy.drop(dummy[dummy[i] == "White"].index, inplace = True)
for i in ['Q27_1', 'Q27_2', 'Q27_3', 'Q27_4', 'Q27_5', 'Q27_6']:
    dummy[i] = dummy[i].apply(lambda x: 'Yes' if x == 1 else 'No')
count = []
for i in range(len(dummy)):
    a = dummy.iloc[i].value_counts()
    if 'Yes' in a:
        b = a.loc['Yes']
        count.append(b)
    else:
        count.append(0)
dummy['count'] = count
#dummy['income_cat'] = dummy['income_cat'].replace(['$75-125k', '$125k or more', '$40-75k', 'Less than $40k'], [((75+125)/2), 125, ((40+75)/2), ((0+40)/2)])
dummy['income_cat'] = dummy['income_cat'].replace(['$75-125k', '$125k or more', '$40-75k', 'Less than $40k'],
                                                  [(124_999), 125000, (75_000), ((39_999))])
dummy2 = dummy[['RespId','ppage','educ','race','gender','income_cat', 'count','voter_category']]
dummy2 = dummy2.rename(columns={"count": "times_voted","ppage" : "age","RespId" : "Id"})

df = dummy2
df = df[['voter_category','income_cat','gender']]

#select less 40 

less_40 = df[(df['voter_category'] == 'always') & (df['income_cat']  < 40_000)]

# select 40 - 75
between_40_75 = df[(df['voter_category'] == 'always')]
between_40_75 = between_40_75[(df['income_cat'] >= 40_000)]
between_40_75 = between_40_75[(df['income_cat'] <= 75_000)]

#select 75 - 125
between_75_125 = df[(df['voter_category'] == 'always')]
between_75_125 = between_75_125[(df['income_cat'] > 75_000)]
between_75_125 = between_75_125[(df['income_cat'] <= 124_999)]

# select > 125
more_125 = df[(df['voter_category'] == 'always') & (df['income_cat']  >= 125_000)]
more_125

gender_vals_female = [less_40.gender.value_counts()[0], between_40_75.gender.value_counts()[0],
                      between_75_125.gender.value_counts()[0], more_125.gender.value_counts()[1]]
gender_vals_male = [less_40.gender.value_counts()[1], between_40_75.gender.value_counts()[1],
                      between_75_125.gender.value_counts()[1], more_125.gender.value_counts()[0]]

# Visualization 3 Here

# set bar width
width = 0.25
fig,ax = plt.subplots(figsize =(12, 8))
barWidth = 0.25 
# set position of bar on X axis
females = np.arange(len(gender_vals_female))
males = [x + barWidth for x in females]
 
# make the plot
plt.bar(females, gender_vals_female, color ='deeppink', width = width,
        edgecolor ='grey', label ='Female')
plt.bar(males, gender_vals_male, color ='cornflowerblue', width = width,
        edgecolor ='grey', label ='Male')
# add data labels above bars 
for patch in ax.patches:
    x,y,height = patch.get_x(), patch.get_y(), patch.get_height()
    ax.text(x+0.13,height+1,(str(height)), fontsize=16,
            horizontalalignment='center')
# add Xticks
plt.title('Across all income groups, there are more females \n than males who indicate that they always vote when they are eligible',
          fontsize = 18, y = 1.01)
plt.yticks(np.linspace(0,100,11),fontsize = 15)
plt.xticks([r + 0.14 for r in range(len(gender_vals_female))],
        ['Less than $40k','$40-75k','$75-125k','$125k or more' ],fontsize = 18)
plt.tick_params(bottom = False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
plt.legend(fontsize=16)
plt.savefig('Viz3.png',bbox_inches = 'tight')
plt.show()

# Visualization 4

df = dummy2
df = df[['voter_category','income_cat','gender']]
df = df[df.gender == 'Male']
#df = df[df.voter_category == 'rarely/never']
df = df[df.income_cat == 39_999]
table = pd.crosstab(df['income_cat'], df['voter_category'],normalize='index')

df = dummy2
df = df[['voter_category','income_cat','gender']]
df = df[df.gender == 'Female']
#df = df[df.voter_category == 'rarely/never']
df = df[df.income_cat == 39_999]
table = pd.crosstab(df['income_cat'], df['voter_category'],normalize='index')

df = dummy2
df = df[['voter_category','income_cat','gender']]
# MALES
df1 = df[df.gender == 'Male']
df1 = df1[df1.income_cat == 39_999]
table1 = pd.crosstab(df1['income_cat'], df1['voter_category'],normalize='index')

df2 = df[df.gender == 'Male']
df2 = df2[df2.income_cat == 75_000]
table2 = pd.crosstab(df2['income_cat'], df2['voter_category'],normalize='index')

df3 = df[df.gender == 'Male']
df3 = df3[df3.income_cat == 124_999]
table3 = pd.crosstab(df3['income_cat'], df3['voter_category'],normalize='index')

df4 = df[df.gender == 'Male']
df4 = df4[df4.income_cat == 125_000]
table4 = pd.crosstab(df4['income_cat'], df4['voter_category'],normalize='index')

# FEMALES
df5 = df[df.gender == 'Female']
df5 = df5[df5.income_cat == 39_999]
table5 = pd.crosstab(df5['income_cat'], df5['voter_category'],normalize='index')

df6 = df[df.gender == 'Female']
df6 = df6[df6.income_cat == 75_000]
table6 = pd.crosstab(df6['income_cat'], df6['voter_category'],normalize='index')

df7 = df[df.gender == 'Female']
df7 = df7[df7.income_cat == 124_999]
table7 = pd.crosstab(df7['income_cat'], df7['voter_category'],normalize='index')

df8 = df[df.gender == 'Female']
df8 = df8[df8.income_cat == 125_000]
table8 = pd.crosstab(df8['income_cat'], df8['voter_category'],normalize='index')

less_40 = [table1,table5]
less_75 = [table2,table6]
less_124999 = [table3,table7]
more_125 = [table4,table8]

figure, [[ax1, ax2], [ax3, ax4], [ax5,ax6], [ax7,ax8]] = plt.subplots(4, 2, figsize=(12, 24),sharey = True)
axes = [ax1, ax2, ax3, ax4, ax5,ax6, ax7,ax8]
axes2 = [ax2, ax3, ax4, ax5,ax6, ax7,ax8] # all but the first plot
table1.plot(ax=ax1, kind='bar')
table5.plot(ax=ax2, kind='bar')
table2.plot(ax=ax3, kind='bar')
table6.plot(ax=ax4, kind='bar')
table3.plot(ax=ax5, kind='bar')
table7.plot(ax=ax6, kind='bar')
table4.plot(ax=ax7, kind='bar')
table8.plot(ax=ax8, kind='bar')
ax1.set_title("Less than $40k income males",fontsize=16), ax2.set_title("Less than $40k income females",fontsize=16)
ax3.set_title("Between \$40k to $75k income males",fontsize=16), ax4.set_title("Between \$40k to $75k income females",fontsize=16)
ax5.set_title("Between \$75k to $125k income males",fontsize=16), ax6.set_title("Between \$75k to $125k income males",fontsize=16)
ax7.set_title("\$125k or more income males",fontsize=16), ax8.set_title("\$125k or more income females",fontsize=16)

for i in axes:
    i.set_xticks([])
for i in axes:
    i.set_yticklabels([(str(0)+'%'),(str(10)+'%'),(str(20)+'%'),(str(30)+'%'),(str(40)+'%'),(str(50)+'%')],fontsize=20)
for i in axes2:
    i.legend([])
for i in axes:
    i.grid()
    
ax1.legend(bbox_to_anchor = [2.75,1.031],fontsize=16)
#ax1.set_xticks([])
plt.savefig('Viz4',bbox_inches = 'tight')
plt.show()