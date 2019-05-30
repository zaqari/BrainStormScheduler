import pandas as pd
import numpy as np
import query.training_schedule.query_sessions as ts

w = ts.sess('alltraining.csv')

train_me = {}
for col in list(w.df)[1:]:
    s = w.df['staff'].loc[w.df[col].isin([str(1)])].values.tolist()
    if col in train_me.keys():
        train_me[col] += s
    else:
        train_me[col] = s
    train_me[col] = list(set(train_me[col]))

len_trainees = []
course_name = []

for k, v in train_me.items():
    len_trainees.append(len(v))
    course_name.append(k)

df_most_pressing = pd.DataFrame(np.array(list(zip(course_name, len_trainees))).reshape(-1, 2), columns=['topic', 'n'])
dtt = df_most_pressing.loc[~df_most_pressing['n'].isin(['0', '1', '2'])]
print(len(dtt))

true_df = w.df[['staff']+list(dtt['topic'].unique())]
from query.training_schedule.scheduler import *
sorted = sort()
con_doc, matrices = sorted.cosine_concurrency_doc(true_df)
schedule = sorted.create_schedule(n_rooms=6)
