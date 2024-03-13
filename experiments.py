#TO DO: try machine depdendent release dates U(1,tigness_par*n*job_par/m) done
#TO DO maybe: try comoparing different policies
#TO DO: improve efficiency for the virtual single machine

import pandas as pd
import numpy as np
import math
from convert import  convert_all_both
from analysis import make_plot
from run_experiment import run_experiment


instances=50
realizations_p=50
Distributions=["d_uniform","exponential","log_normal","deterministic"]
NP=[10,20,50,100,200,500,1000] #for plot
MP=[1,2,5,10]                  #for plot
N=[10,20,50,100,200,500,1000]
M=[1,2,5,10]
golden_ratio=( 1 + math.sqrt(5) ) / 2
upper_mean=50
upper_we=30
time_step=1
Printing=False



################################################ adapt parameters for simulations################################################à

alpha_DSOS=golden_ratio-1
Delta_try=10

#Upper release parameters
upper_release_par=3
fixed_release_par=False
Tigth_analysis=False

#Type of summary and plots
Plot_Worst=False
Summary="Both" #"Average", "Worst"

#Modyfy to consider subset scenarios:
#Distributions=["log_normal"]
#simulation parametrs
#N=[1000]
#M=[1,2,5,10]
#plot parameters
MP=M
NP=N
#NP=[10,20,50,100,200,500,1000]
#MP=[1,2,5,10]

################################################################################################################################################

for distribution in Distributions:                
    for m in M:
        for n in N:
            run_experiment(m,n,distribution,upper_mean,alpha_DSOS,Tigth_analysis,fixed_release_par,upper_release_par,upper_we,instances,realizations_p,Delta_try)
            print(f"finished for distribution {distribution} withe {m} machines and {n} jobs")
    convert_all_both(Summary,Tigth_analysis,fixed_release_par,upper_release_par,upper_we,NP,MP,[distribution],upper_mean,Delta_try)
    for method in ["DSOS","RSOS"]:
        make_plot(NP,MP,distribution,upper_mean,method, Tigth_analysis,fixed_release_par,upper_release_par,upper_we,Plot_Worst,alpha_DSOS, Delta_try)
