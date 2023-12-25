import pandas as pd
import numpy as np
import os
import pickle
'''''
m=2
distribution="d_uniform"
n=10
CV=1/3
directory_path= os.path.join('results',distribution,'m_'+str(m))
name_2 = f"results_m_{m}_n_{n}_{distribution}_{round(CV, 2)}.pkl"
file_path_2 = os.path.join(directory_path, name_2)
with open(file_path_2, 'rb') as f:
    results = pickle.load(f)
print(results)
'''
import pandas as pd
import numpy as np

# Assuming you already have result_RSOS DataFrame
MA = [1, 2, 5, 10]
NU = [10, 20, 50, 100, 500]
Prova = pd.DataFrame(np.nan, index=MA, columns=NU)

# Rows and column to modify
rows_to_modify = [1, 10]
column_to_modify = [20]


# New values to set
#new_values = [3.14, 2.718]  # Replace with your desired values
folders_paths=[x^2 for x in rows_to_modify]


# Update the values using loc
for m,folder in enumerate(folders_paths):
            ma=rows_to_modify[m]
            files=[x+2 for x in column_to_modify]
            # Iterate through each CSV file
            for n,file in enumerate(files):
                nu=column_to_modify[n]
                #file_path = os.path.join(folder, file)

                # Read the CSV file into a dataframe
                
                
                Prova.loc[ma,nu]=2
                

#result_RSOS.loc[rows_to_modify, column_to_modify] = new_values

# Display the modified DataFrame
print(Prova)

"""""
#159910.54112934228 133902.21407250038 115117.33403591841
#160011.06897377557 133977.35872984416 115281.6457283996

jobs_data = [
    {'job_id': '1', 'release': 4, 'processing': 5, 'expected': 4.5, 'CV':3,'weigth':4.5},
    {'job_id': '2', 'release': 1, 'processing': 3,'expected': 3, 'CV':0,'weigth':3},
    {'job_id': '3', 'release': 3, 'processing': 5,'expected': 1.5, 'CV':1,'weigth':1.5},
    {'job_id': '4', 'release': 5, 'processing': 3,'expected': 3, 'CV':1,'weigth':3},
    {'job_id': '5', 'release': 4, 'processing': 5, 'expected': 4.5, 'CV':3,'weigth':4.5},
    {'job_id': '6', 'release': 10, 'processing': 3,'expected': 3, 'CV':0,'weigth':3},
    #{'job_id': '5', 'release': 9, 'processing': 5,'expected': 1.5, 'CV':4,'weigth':1.5},
    #{'job_id': '6', 'release': 5, 'processing': 3,'expected': 3, 'CV':1,'weigth':3},
    #{'job_id': '7', 'release': 7, 'processing': 5,'expected': 1.5, 'CV':4,'weigth':1.5}


]

#convert list to list of object
jobs = [Job(**job_data) for job_data in jobs_data]
np.random.seed(10)
random.seed(10)
m=3
alpha=0.5
Printing=True
RANDOM_alpha=True
RANDOM_assigment=True
time_step=1
jobs_after=run_one(jobs, m,RANDOM_alpha,RANDOM_assigment,alpha,time_step)
Printing=True
"""





