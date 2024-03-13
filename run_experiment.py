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

def run_experiment(m,n,distribution,mean,alpha_DSOS,Tigth_analysis,fixed_release_par,upper_release_par,upper_we,instances,realizations_p,Delta_try=10):
    ###############################################################################################################################
    ####################################################INPUT:#####################################################################
    #m,n               = numbers machines and jobs in the simulation
    #distribution      = processing time distribution  in the simulation 
    #mean              = Upper bound on mean of the processing time distribution
    #alpha_DSOS        = fixed value \alpha in the DSOS algorith, usually golden_ratio-1

    #Tigth_analysis    = TRUE if the upper bound on the release times depends on m
    #fixed_release_par = TRUE if the upper bound on the release times is indipendent from m and n
    #upper_release_par = Parameter influencing upper bound on release time
    #upper_we          = uppe bound on jobs' weigths

    #instances         = number of istance considere in the simulation
    #realizations_p    = number realizations of processing times considered for each istance
    #Delta_try=10      = Parameter influencing the coefficint of varition for the log-normal distribution


    ####################################################OUTPUT:#####################################################################
    #Data frame stored in the Result folder containg the objective value of the RSOS algorith, DSOS algorithm, and the 2 lower bounds for all the instances and realizations
    ################################################################################################################################
    np.random.seed(10)
    random.seed(10)
    results=[]

    #Define upper bound on release time:
    if fixed_release_par: 
        upper_release=upper_release_par
        fix="fix"
    else: 
        upper_release=n*upper_release_par
        fix="n"
    if Tigth_analysis:
        upper_release=round(n*upper_release_par*(mean/2)/m) 
        fix="mn_dependent_"

    #Generate data and run the algorithm
    for i in range(instances):
        Jobs=[] #list contsining the jobs
        result_istance=[]
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
                
        # simulate realization processing times    
        for j in range(realizations_p):
            
            if distribution=="d_uniform":
                for k in range(n): Jobs[k].processing=random.uniform(0,round(2*Jobs[k].expected))
            if distribution=="exponential":
                for k in range(n): Jobs[k].processing=random.expovariate(1/Jobs[k].expected)
            if distribution=="log_normal":
                for k in range(n): 
                    mu=math.log(Jobs[k].expected)-sigma2/2
                    Jobs[k].processing=random.lognormvariate(mu,math.sqrt(sigma2))
            if distribution=="deterministic":
                for k in range(n): Jobs[k].processing=Jobs[k].expected
                    
            #Run RSOS and DSOS on simulated data
            #NOTE: For every realization of the same istance we compute the same lower bounds since the data necessary to construct the LP schedule is the same. 
            total_RSOS,total_DSOS,total_LR,basic_LB=run_one_both_fast(Jobs,m,alpha_DSOS)
            result_istance.append([total_RSOS,total_DSOS,total_LR,basic_LB])
        results.append(result_istance)

    #Store results:
    directory_path= os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}",distribution,'m_'+str(m))
    name=f"results_m_{m}_n_{n}_{distribution}_{round(CV,2)}.csv"
    file_path = os.path.join(directory_path, name)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    df=pd.DataFrame(results)
    df.to_csv(file_path,index=False)

    