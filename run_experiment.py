import pandas as pd
import numpy as np
import math
import time
from datetime import datetime, timedelta
from bisect import insort_left,insort_right
from tabulate import tabulate
import random
from random import randint
import os
from job_class import Job,Job_b
from run_one import run_one, run_one_both, run_one_both_fast
import pickle
from convert import convert_all 
from analysis import make_plot

def run_experiment(m,n,distribution,mean,alpha_DSOS,fixed_release_par,upper_release_par,upper_we,instances,realizations_p,Delta_try=10):
    np.random.seed(10)
    random.seed(10)
    results=[]
    if fixed_release_par: 
        upper_release=upper_release_par
        fix="fix"
    else: 
        upper_release=n*upper_release_par
        fix="n"
    problem_istances=[]
    if distribution=="deterministic": realizations_p=1
    for i in range(instances):
        #print("-------------------------------------------------------------------------------------------")
        #print("------------------------------------------------NEW istance---------------------------------")
        #print("-------------------------------------------------------------------------------------------")
        Jobs=[]
        result_istance=[]
        #for x in range(n):
        if distribution=="d_uniform":
            CV=1/3
            for x in range(n):
                expected=randint(1,mean)
                release=randint(0,upper_release)  
                we=random.uniform(0, upper_we)
                job=Job_b(x,release,expected,CV,we)
                Jobs.append(job)
        if distribution=="exponential":
            CV=1
            for x in range(n):
                expected=randint(1,mean)
                release=randint(0,upper_release)
                we=random.uniform(0, upper_we)
                job=Job_b(x,release,expected,CV,we)
                Jobs.append(job)
        if distribution=="log_normal":
            sigma2=math.log(Delta_try+1)
            CV=math.exp(sigma2)-1
            CV=round(CV)
            for x in range(n):
                expected=randint(1,mean)
                release=randint(0,upper_release)  
                we=random.uniform(0, upper_we)
                job=Job_b(x,release,expected,CV,we)
                Jobs.append(job)
            
        if distribution=="deterministic":
            CV=0
            for x in range(n):
                expected=randint(1,mean)
                release=randint(0,upper_release)  
                we=random.uniform(0, upper_we)
                job=Job_b(x,release,expected,CV,we)
                Jobs.append(job)
                
            
        for j in range(realizations_p):
            
            if distribution=="d_uniform":
                for k in range(n): Jobs[k].processing=random.uniform(0,round(2*Jobs[k].expected))
                #for k in range(n): Jobs[k].processing=randint(0,round(2*Jobs[k].expected))
            if distribution=="exponential":
                for k in range(n): Jobs[k].processing=random.expovariate(1/Jobs[k].expected)
            if distribution=="log_normal":
                for k in range(n): 
                    mu=math.log(Jobs[k].expected)-sigma2/2
                    Jobs[k].processing=random.lognormvariate(mu,math.sqrt(sigma2))
            if distribution=="deterministic":
                for k in range(n): Jobs[k].processing=Jobs[k].expected
                    
            #print("------------------------------------------------NEW Processing---------------------------------")
            #print("-------------------------------------------------------------------------------------------")
            #[print(job.we,job.release) for job in Jobs]
            total_RSOS,total_DSOS,total_LR,basic_LB=run_one_both_fast(Jobs,m,alpha_DSOS)
            '''''
            if (total_RSOS>(2+CV)*total_LR): 
                print(f"for scenario{i} realizaton {j} RSOS Not fullfiled")
                problem_istances.append(Jobs)
                precedence=sorted(Jobs, key=lambda job: (job.we/job.expected), reverse=True)
                print("precedence:")
                [print(job.id, job.we/job.expected, job.comp_RSOS,job.we, job.expected) for job in precedence]
            '''
            #print("for istance",i,"realization",j,total_RSOS,total_DSOS,total_LR)
            result_istance.append([total_RSOS,total_DSOS,total_LR,basic_LB])
        results.append(result_istance)
    
    directory_path= os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}",distribution,'m_'+str(m))
    name=f"results_m_{m}_n_{n}_{distribution}_{round(CV,2)}.csv"
    file_path = os.path.join(directory_path, name)
    if not os.path.exists(directory_path):
        # Create the directory if it doesn't exist
        os.makedirs(directory_path)
    
    df=pd.DataFrame(results)
    df.to_csv(file_path,index=False)
    #name_2 = f"results_m_{m}_n_{n}_{distribution}_{round(CV, 2)}.pkl"
    #file_path_2 = os.path.join(directory_path, name_2)

    #if not os.path.exists(directory_path):
        # Create the directory if it doesn't exist
        #os.makedirs(directory_path)
    #with open(file_path_2, 'wb') as f:
        #pickle.dump(results, f)
    
#"""

#m=2
#distribution="d_uniform"