import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import seaborn as sns

Delta_try=10
distribution="d_uniform"
method="RSOS"




def make_plot(N,M,distribution,mean,method, fixed_release_par,upper_release_par,upper_we, alpha=(( 1 + math.sqrt(5) ) / 2), Delta_try=10):
    fix="n"
    if fixed_release_par: fix="fix"
    path=os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","summary")
    if distribution=="d_uniform": 
         CV=1/3
         name_distribution="Uniform"
    if distribution=="exponential":
         CV=1
         name_distribution="Exponential"
    if distribution=="log_normal":
                sigma2=math.log(Delta_try+1)
                CV=math.exp(sigma2)-1
                CV=round(CV)
                name_distribution="Log-normal"
    if distribution=="deterministic":
         CV=0
         name_distribution="Deterministic"

    if method=="DSOS":
        predicted=1+((2+alpha)*(CV+1)/2)
        name_DSOS=f"{distribution}_DSOS_{round(CV,2)}.csv"
        data=pd.read_csv(os.path.join(path,name_DSOS))

    if method=="RSOS":
        predicted=2+CV
        name_RSOS=f"{distribution}_RSOS_{round(CV,2)}.csv"
        data=pd.read_csv(os.path.join(path,name_RSOS))
    
    color_palette = sns.color_palette("colorblind")
   
    for index, row in data.iterrows():
        selected_columns = [str(n) for n in N if str(n) in row.index]
        plt.plot( pd.to_numeric(selected_columns), row[selected_columns], label=f"m= {round(row.iloc[0])}", marker='o',color=color_palette[index]) #label=f"m={row['m']}"
        #pd.to_numeric(row.index[1:])
    plt.axhline(y=predicted, color='red', linestyle='--', label='Theoretical guarantee')
    plt.legend()
    plt.xlabel('number of jobs')
    plt.ylabel('performance ratio')
    plt.title(f"Performance {method} for {name_distribution} Distribution ")

    #plt.show()

    save_folder = os.path.join("Results",f"results_{fix}{upper_release_par}_mean_{mean}_we_{upper_we}","plots")

    # Create the folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Save the plots to the specified folder
    plt.savefig(os.path.join(save_folder, f"{distribution}_{method}_{round(CV,2)}.png"))
    plt.close()


'''''
def make_plot_asymptotic(distribution,method, fixed_release_par,upper_release_par, alpha=(( 1 + math.sqrt(5) ) / 2), Delta_try=10):
    fix="n"
    if fixed_release_par: fix="fix"
    path=os.path.join("Results",f"results_{fix}{upper_release_par}","summary")
    if distribution=="d_uniform": CV=1/3
    if distribution=="exponential":CV=1
    if distribution=="log_normal":
                sigma2=math.log(Delta_try+1)
                CV=math.exp(sigma2)-1
                CV=round(CV)
    if distribution=="deterministic":CV=0

    if method=="DSOS":
        predicted=1-1/(1+((2+alpha)*(CV+1)/2))
        name_DSOS=f"{distribution}_DSOS_{round(CV,2)}_asymptotic.csv"
        data=pd.read_csv(os.path.join(path,name_DSOS))

    if method=="RSOS":
        predicted=(1+CV)/(2+CV)
        name_RSOS=f"{distribution}_RSOS_{round(CV,2)}_asymptotic.csv"
        data=pd.read_csv(os.path.join(path,name_RSOS))
    
    color_palette = sns.color_palette("colorblind")

    for index, row in data.iterrows():
        plt.scatter(row.index[1:], row.values[1:], label=f"m= {round(row.iloc[0])}", marker='o',c=color_palette[index]) #label=f"m={row['m']}"

    plt.axhline(y=predicted, color='red', linestyle='--', label='Theoretical guarantee')
    plt.legend()
    plt.xlabel('number of jobs')
    plt.ylabel('Asymmtotic performance ratio')
    plt.title(f"Performance for {method} for distribution {distribution} ")

    #plt.show()

    save_folder = os.path.join("Results",f"results_{fix}{upper_release_par}","plots")

    # Create the folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Save the plots to the specified folder
    plt.savefig(os.path.join(save_folder, f"{distribution}_{method}_{round(CV,2)}_asymptotic.png"))
    plt.close()

#for distribution in ["d_uniform","exponential","log_normal","deterministic"]:
 #       for method in ["DSOS","RSOS"]:
 #           make_plot(distribution,method,(( 1 + math.sqrt(5) ) / 2), Delta_try)
'''