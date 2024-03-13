
import pandas as pd
import numpy as np
import os
import ast
import math

# Function to calculate the average of a dataframe
def calculate_ratio_max(df,method):
    ##################################################################################################################################################
    ####################################################INPUT:#########################################################################################
    #df        = Data frame containing the the objective value of the "RSOS", "DSOS" and two lower bounds for each instance (row) and ralizartions (columns)
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
    #df        = Data frame containing the the objective value of the "RSOS", "DSOS" and two lower bounds for each instance (row) and ralizartions (columns)
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
    #df        = Data frame containing the the objective value of the "RSOS", "DSOS" and two lower bounds for each instance (row) and ralizartions (columns)
    #method    = Algorithm considered "RSOS", "DSOS"
    
    ####################################################OUTPUT:#########################################################################################
    # Highesy ratio, between the objective value of the algorithm and the maximum lower bound across all the instance in df
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
    #upper_release_par = Parameter influencing upper bound on release time
    #upper_we          = upper bound on jobs' weigths
    #N                 = List with numbers of jobs 
    #M                 = List with numbers of machines 
    #Distribution      = List of string corresponding  to the distrubution of processing data
    #mean              = Upper bound on mean of the processing time distribution
    #Delta_try=10      = Parameter influencing the coefficint of varition for the log-normal distribution
    
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

        #Cretae Data frame to store summary results
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
             
            


    '''
def calculate_ratio_asymptotic(df,method): #not good idea
    if method=="DSOS":
        col=1
    else: col=0
    ratio=0
    for i in range(df.shape[0]):
        for k in range(df.shape[1]):
            value_as_str = df.iat[i,k]
            value_as_list = ast.literal_eval(value_as_str)
            results= [float(number) for number in value_as_list]
            ratio=ratio+((results[col]-results[2])/(results[col]))
    return ratio/(df.shape[0] * df.shape[1])
'''
'''
def calculate_ratio_step(df,method,CV,alpha):
    if method=="DSOS":
        col=1
        bound=1+((2+alpha)*(CV+1)/2)
    else: 
         col=0
         bound=2+CV
    ratio=0
    for i in range(df.shape[0]):
        ratio_istance=0
        for k in range(df.shape[1]):
            value_as_str = df.iat[i,k]
            value_as_list = ast.literal_eval(value_as_str)
            results= [float(number) for number in value_as_list]
            ratio_istance=ratio_istance+(results[col]/results[2])
        ratio_istance=ratio_istance/df.shape[1] 
        if(ratio_istance>bound): print("problem in istances:",i)
        ratio=ratio+ratio_istance
    return ratio/df.shape[0] 
'''
'''
def convert_all(Tigth_analysis,fixed_release_par,upper_release_par,upper_we,N,M,Distributions,mean,type,ratio,alpha,Delta_try=10):
    MA=[1,2,5,10]
    NU=[10,20,50,100,200,500,1000]
    #Distributions=["d_uniform","exponential","log_normal","deterministic"]
    #Delta_try=10

    # Get a list of folders (m_1, m_2, m_3, m_4) in the repository
    #folders = [f for f in os.listdir(repository_path) if os.path.isdir(os.path.join(repository_path, f))]
    fix="n"
    if fixed_release_par: fix="fix"
    if Tigth_analysis: fix="mn_dependent_"
    path_save=os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","summary")
    
    if not os.path.exists(path_save):
            # Create the directory if it doesn't exist
            os.makedirs(path_save)

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
        #print(CV)
        repository_path = os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}",distribution)


        #for each algorithm:
        #plot for each m in different colors ration  on y axis and n on x axis

        folders_paths=[os.path.join(repository_path,"m_"+str(x)) for x in M]

        #files = [f for f in os.listdir(folders_paths[0]) if f.endswith(".csv")]
        #name_files=[]
        result_RSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        result_DSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        #print("folders:",folders_paths)


        # Iterate through each folder
        for m,folder in enumerate(folders_paths):
            ma=M[m]
            #folder_path = os.path.join(repository_path, folder)

            # Get a list of CSV files in the folder
            #files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
            files=[os.path.join(folder,f"results_m_{M[m]}_n_"+str(x)+f"_{distribution}_{round(CV, 2)}.csv") for x in N]
            #print(files)
            #files = [f for f in os.listdir(folder) if f.endswith(".csv")]

            # Iterate through each CSV file
            for n,file in enumerate(files):
                nu=N[n]
                #file_path = os.path.join(folder, file)

                # Read the CSV file into a dataframe
                df = pd.read_csv(file)
                
                if ratio=="M_LP":
                    result_DSOS.loc[ma,nu]=calculate_ratio_LP(df,"DSOS")
                    result_RSOS.loc[ma,nu]=calculate_ratio_LP(df,"RSOS")
                else: 
                    result_DSOS.loc[ma,nu]=calculate_ratio_max(df,"DSOS")
                    result_RSOS.loc[ma,nu]=calculate_ratio_max(df,"RSOS")
                
            
        #save summary results
        if type=="asymptotic":
            name_DSOS=f"{distribution}_DSOS_{round(CV,2)}_asymptotic.csv"
            name_RSOS=f"{distribution}_RSOS_{round(CV,2)}_asymptotic.csv"
        else:
            name_DSOS=f"{distribution}_DSOS_{round(CV,2)}.csv"
            name_RSOS=f"{distribution}_RSOS_{round(CV,2)}.csv"
             
        result_DSOS.to_csv(os.path.join(path_save,name_DSOS))
        result_RSOS.to_csv(os.path.join(path_save,name_RSOS))


def convert_all_WC(Tigth_analysis,fixed_release_par,upper_release_par,upper_we,N,M,Distributions,mean,type,ratio,alpha,Delta_try=10):
    MA=[1,2,5,10]
    NU=[10,20,50,100,200,500,1000]
    #Distributions=["d_uniform","exponential","log_normal","deterministic"]
    #Delta_try=10

    # Get a list of folders (m_1, m_2, m_3, m_4) in the repository
    #folders = [f for f in os.listdir(repository_path) if os.path.isdir(os.path.join(repository_path, f))]
    fix="n"
    if fixed_release_par: fix="fix"
    if Tigth_analysis: fix="mn_dependent_"
    path_save=os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","summary","WORST")
    
    if not os.path.exists(path_save):
            # Create the directory if it doesn't exist
            os.makedirs(path_save)

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
        #print(CV)
        repository_path = os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}",distribution)


        #for each algorithm:
        #plot for each m in different colors ration  on y axis and n on x axis

        folders_paths=[os.path.join(repository_path,"m_"+str(x)) for x in M]

        #files = [f for f in os.listdir(folders_paths[0]) if f.endswith(".csv")]
        #name_files=[]
        result_RSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        result_DSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        #print("folders:",folders_paths)


        # Iterate through each folder
        for m,folder in enumerate(folders_paths):
            ma=M[m]
            #folder_path = os.path.join(repository_path, folder)

            # Get a list of CSV files in the folder
            #files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
            files=[os.path.join(folder,f"results_m_{M[m]}_n_"+str(x)+f"_{distribution}_{round(CV, 2)}.csv") for x in N]
            #print(files)
            #files = [f for f in os.listdir(folder) if f.endswith(".csv")]

            # Iterate through each CSV file
            for n,file in enumerate(files):
                nu=N[n]
                #file_path = os.path.join(folder, file)

                # Read the CSV file into a dataframe
                df = pd.read_csv(file)
                result_DSOS.loc[ma,nu]=calculate_ratio_worst(df,"DSOS")
                result_RSOS.loc[ma,nu]=calculate_ratio_worst(df,"RSOS")
            
            
        #save summary results
        
        name_DSOS=f"{distribution}_DSOS_{round(CV,2)}_Worst.csv"
        name_RSOS=f"{distribution}_RSOS_{round(CV,2)}_Worst.csv"
             
        result_DSOS.to_csv(os.path.join(path_save,name_DSOS))
        result_RSOS.to_csv(os.path.join(path_save,name_RSOS))


def convert_all(Tigth_analysis,fixed_release_par,upper_release_par,upper_we,N,M,Distributions,mean,type,ratio,alpha,Delta_try=10):
    MA=[1,2,5,10]
    NU=[10,20,50,100,200,500,1000]
    #Distributions=["d_uniform","exponential","log_normal","deterministic"]
    #Delta_try=10

    # Get a list of folders (m_1, m_2, m_3, m_4) in the repository
    #folders = [f for f in os.listdir(repository_path) if os.path.isdir(os.path.join(repository_path, f))]
    fix="n"
    if fixed_release_par: fix="fix"
    if Tigth_analysis: fix="mn_dependent_"
    path_save=os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","summary")
    
    if not os.path.exists(path_save):
            # Create the directory if it doesn't exist
            os.makedirs(path_save)

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
        #print(CV)
        repository_path = os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}",distribution)


        #for each algorithm:
        #plot for each m in different colors ration  on y axis and n on x axis

        folders_paths=[os.path.join(repository_path,"m_"+str(x)) for x in M]

        #files = [f for f in os.listdir(folders_paths[0]) if f.endswith(".csv")]
        #name_files=[]
        result_RSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        result_DSOS= pd.DataFrame(np.nan,index=MA,columns=NU)
        #print("folders:",folders_paths)


        # Iterate through each folder
        for m,folder in enumerate(folders_paths):
            ma=M[m]
            #folder_path = os.path.join(repository_path, folder)

            # Get a list of CSV files in the folder
            #files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
            files=[os.path.join(folder,f"results_m_{M[m]}_n_"+str(x)+f"_{distribution}_{round(CV, 2)}.csv") for x in N]
            #print(files)
            #files = [f for f in os.listdir(folder) if f.endswith(".csv")]

            # Iterate through each CSV file
            for n,file in enumerate(files):
                nu=N[n]
                #file_path = os.path.join(folder, file)

                # Read the CSV file into a dataframe
                df = pd.read_csv(file)
                if type=="asymptotic":
                    result_DSOS.loc[ma,nu]=calculate_ratio_asymptotic(df,"DSOS")
                    result_RSOS.loc[ma,nu]=calculate_ratio_asymptotic(df,"RSOS")

                elif ratio=="M_LP":
                    result_DSOS.loc[ma,nu]=calculate_ratio_LP(df,"DSOS")
                    result_RSOS.loc[ma,nu]=calculate_ratio_LP(df,"RSOS")
                else: 
                    result_DSOS.loc[ma,nu]=calculate_ratio_max(df,"DSOS")
                    result_RSOS.loc[ma,nu]=calculate_ratio_max(df,"RSOS")
            
        #save summary results
        if type=="asymptotic":
            name_DSOS=f"{distribution}_DSOS_{round(CV,2)}_asymptotic.csv"
            name_RSOS=f"{distribution}_RSOS_{round(CV,2)}_asymptotic.csv"
        else:
            name_DSOS=f"{distribution}_DSOS_{round(CV,2)}.csv"
            name_RSOS=f"{distribution}_RSOS_{round(CV,2)}.csv"
             
        result_DSOS.to_csv(os.path.join(path_save,name_DSOS))
        result_RSOS.to_csv(os.path.join(path_save,name_RSOS))

    # Print the resulting dataframe
    #print(result_RSOS)

    #directory_path= os.path.join('results',distribution,'m_'+str(m))
        #name=f"results_m_{m}_n_{n}_{distribution}_{round(CV,2)}.csv"
        #file_path = os.path.join(directory_path, name)
        
        
        #df=pd.DataFrame(results)
        #df.to_csv(file_path,index=False)
'''