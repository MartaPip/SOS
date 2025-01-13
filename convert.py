
import pandas as pd
import numpy as np
import os
import ast
import math

# Function to calculate the average of a dataframe
def calculate_ratio_max(df,method):
    ##################################################################################################################################################
    ####################################################INPUT:#########################################################################################
    #df        = Dataframe containing the the objective value of the "RSOS", "DSOS" and two lower bounds for each instance (row) and ralizartions (columns)
    #method    = Algorithm considered "RSOS", "DSOS"
    
    ####################################################OUTPUT:#########################################################################################
    # Average ratio, between the objective value of the algorithm and the maximum lower bound across all the instance in df
    ####################################################################################################################################################
    if method=="DSOS":
        col=1
    else: col=0
    ratio=0
    #iterate over all instances and  realizations and compute average ratio
    for i in range(df.shape[0]):
        for k in range(df.shape[1]):
            value_as_str = df.iat[i,k]
            value_as_list = ast.literal_eval(value_as_str)
            results= [float(number) for number in value_as_list]
            #select maxium lower bound
            d=max(results[2],results[3]) 
            add=results[col]/d
            ratio=ratio+add
    return ratio/(df.shape[0] * df.shape[1])

def calculate_ratio_LP(df,method):
    ##################################################################################################################################################
    ####################################################INPUT:#########################################################################################
    #df        = Dataframe containing the the objective value of the "RSOS", "DSOS" and two lower bounds for each instance (row) and ralizartions (columns)
    #method    = Algorithm considered "RSOS", "DSOS"
    
    ####################################################OUTPUT:#########################################################################################
    # Average ratio, between the objective value of the algorithm and the LP lower bound across all the instance in df
    ####################################################################################################################################################
    if method=="DSOS":
        col=1
    else: col=0
    ratio=0
    #iterate over all instances and  realizations and compute average ratio
    for i in range(df.shape[0]):
        for k in range(df.shape[1]):
            value_as_str = df.iat[i,k]
            value_as_list = ast.literal_eval(value_as_str)
            results= [float(number) for number in value_as_list]
            add=results[col]/results[2]
            ratio=ratio+add
    return ratio/(df.shape[0] * df.shape[1])

    
def calculate_ratio_worst(df,method):
    ##################################################################################################################################################
    ####################################################INPUT:#########################################################################################
    #df        = Dataframe containing the the objective value of the "RSOS", "DSOS" and two lower bounds for each instance (row) and ralizartions (columns)
    #method    = Algorithm considered "RSOS", "DSOS"
    
    ####################################################OUTPUT:#########################################################################################
    # Highest ratio, between the objective value of the algorithm and the maximum lower bound across all the instance in df
    ####################################################################################################################################################
    if method=="DSOS":
        col=1
    else: col=0
    ratio=0
    #iterate over all istances and compute average ratio among realization
    for i in range(df.shape[0]):
        ratio_istance=0
        for k in range(df.shape[1]):
            value_as_str = df.iat[i,k]
            value_as_list = ast.literal_eval(value_as_str)
            results= [float(number) for number in value_as_list]
            d=max(results[2],results[3]) 
            add=results[col]/d
            ratio_istance=ratio_istance+add      
        ratio_istance=ratio_istance/df.shape[1]
        #select maximum ratio among instances
        if (ratio<ratio_istance): ratio=ratio_istance
    return ratio
    


def convert_all_both(Summary,Tigth_analysis,fixed_release_par,upper_release_par,upper_we,N,M,Distributions,mean,Delta_try=10):
    ###################################################################################################################################################
    ####################################################INPUT:#########################################################################################
    #Summary           = type ratio we want to store: "Worst", "Average", "Both"
    #Tigth_analysis    = TRUE if the upper bound on the release times depends on m
    #fixed_release_par = TRUE if the upper bound on the release times is indipendent from m and n
    #upper_release_par = parameter influencing upper bound on release time
    #upper_we          = upper bound on jobs' weigths
    #N                 = list with numbers of jobs 
    #M                 = list with numbers of machines 
    #Distributions     = list of string corresponding  to the distrubution of processing data
    #mean              = upper bound on mean of the processing time distribution
    #Delta_try=10      = parameter influencing the coefficint of varition for the log-normal distribution
    
    ####################################################OUTPUT:#########################################################################################
    # A table for each distribution with either the avreage ratio, the highest ratio or both of them, for each combination of number of machines and number of jobs
    ####################################################################################################################################################
    MA=[1,2,5,10]
    NU=[10,20,50,100,200,500,1000]

    # Find repository with data
    fix="n"
    if fixed_release_par: fix="fix"
    if Tigth_analysis: fix="mn_dependent_"
    
    # create table m x n for each distribution
    for distribution in Distributions:
        print(distribution)
        if distribution=="d_uniform": CV=1/3
        if distribution=="exponential": CV=1
        if distribution=="log_normal":
                    sigma2=math.log(Delta_try+1)
                    CV=math.exp(sigma2)-1
                    CV=round(CV)
        if distribution=="deterministic":CV=0
        repository_path = os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}",distribution)


        
        # List of paths to the folders contatining the simulation results for the different values of m in M
        folders_paths=[os.path.join(repository_path,"m_"+str(x)) for x in M]

        #Cretae Dataframe to store summary results
        result_RSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        result_DSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        result_RSOS_worst= pd.DataFrame(np.nan,index=MA,columns=NU)
        result_DSOS_worst= pd.DataFrame(np.nan,index=MA,columns=NU)
        both_RSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        both_DSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
       

        # Iterate through each folder
        for m,folder in enumerate(folders_paths):
            ma=M[m]
            
            # Get a list of CSV files in the folder
            files=[os.path.join(folder,f"results_m_{M[m]}_n_"+str(x)+f"_{distribution}_{round(CV, 2)}.csv") for x in N]
           
            # Iterate through each CSV file
            for n,file in enumerate(files):
                nu=N[n]
                df = pd.read_csv(file)

                #Store the summary result for the specif number of machine and number of jobs combinations
                if Summary=="Both" or Summary=="Average":
                    result_DSOS.loc[ma,nu]="{:.3f}".format(round(calculate_ratio_max(df,"DSOS"),3))
                    result_RSOS.loc[ma,nu]="{:.3f}".format(round(calculate_ratio_max(df,"RSOS"),3))
                if Summary=="Both" or Summary=="Worst":
                    result_DSOS_worst.loc[ma,nu]="{:.3f}".format(round(calculate_ratio_worst(df,"DSOS"),3))
                    result_RSOS_worst.loc[ma,nu]="{:.3f}".format(round(calculate_ratio_worst(df,"RSOS"),3))
                
        # Save summary data
        if Summary=="Both":   
            name_DSOS=f"{distribution}_DSOS_{round(CV,2)}_both.csv"
            name_RSOS=f"{distribution}_RSOS_{round(CV,2)}_both.csv"
            path_save=os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","summary","Both")
            both_RSOS = pd.concat([result_RSOS, result_RSOS_worst], axis=1)
            both_DSOS = pd.concat([result_DSOS, result_DSOS_worst], axis=1)

            if not os.path.exists(path_save): os.makedirs(path_save) 

            both_DSOS.to_csv(os.path.join(path_save,name_DSOS))
            both_RSOS.to_csv(os.path.join(path_save,name_RSOS))
        elif Summary=="Worst":
            name_DSOS=f"{distribution}_DSOS_{round(CV,2)}_Worst.csv"
            name_RSOS=f"{distribution}_RSOS_{round(CV,2)}_Worst.csv"
            path_save=os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","summary","WORST")
            if not os.path.exists(path_save): os.makedirs(path_save) 

            result_DSOS_worst.to_csv(os.path.join(path_save,name_DSOS))
            result_RSOS_worst.to_csv(os.path.join(path_save,name_RSOS))
        else:
            name_DSOS=f"{distribution}_DSOS_{round(CV,2)}.csv"
            name_RSOS=f"{distribution}_RSOS_{round(CV,2)}.csv"
            path_save=os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","summary")
            if not os.path.exists(path_save): os.makedirs(path_save) 
            result_DSOS.to_csv(os.path.join(path_save,name_DSOS))
            result_RSOS.to_csv(os.path.join(path_save,name_RSOS))
             
            