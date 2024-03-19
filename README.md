# *Stochastic Online Scheduling on Identical Parallel Machines* 


## Description
Master project on "Stochastic Online Scheduling on Parallel Machines: Theory and Simulations".

This repository contains the simulation code for testing the theoretical performance guarantee stated in "Stochastic online scheduling revisited"[1] and proved in the Master project.


## Setup

```bash

git clone git@github.com:MartaPip/Stochastic-Online-Scheduling.git

cd Stochastic-Online-Scheduling

conda env create -f environment.yml

conda activate Tesi_env

```

## Running the experiments

To run the experiments, adjust the following parameters in the *experiments.py* file and execute it:

### Usually fixed:

- **N=[10,20,50,100,200,500,1000]** array specifying the number of jobs to consider in the simulations.

- **M=[1,2,5,10]** array specifying the number of machines to consider in the simulations.

- **Distributions=["d_uniform","exponential","log_normal","deterministic"]** list specifying the distributions to consider in the simulations.

- **alpha_DSOS** the alpha considered in the $DSOS$ algorithm, by default it is *golden ratio* $-1$.

- **upper_mean** upper bound on the expected value of the processing times. 

- **upper_we** upper bound on the weights of the jobs.

- **instances** number of instances simulated for each scenario. 

- **realizations_p** number of realizations of the processing times simulated for each instance.

- **Delta_try** The upper bound on the coefficient of variation that is considered when running simulations with the log-normal distribution. The default value is 10.

### Select release time conditions:

- **fixed_release_par** A Boolean parameter (True or False) indicating whether the upper bound of the job's release time depends on the number of jobs considered.

- **Tigth_analysis**  A Boolean parameter (True or False) indicating whether the upper bound of the release time of the jobs depends on the number of machines considered.

- **upper_release_par**  If *Tigth_analysis* is True, the upper bound on the release time is calculated as upper_release_par $\times$ upper_we $\times \frac{n}{2m}$.  If *Tigth_analysis* is Fasle and *fixed_release_par* is True, *upper_release_par* specifies the upper bound on the release time. Otherwise, the upper bound is calculated as $n \times$ upper_release_par.

### Modify summary tables and plot characteristics:

- **Summary $\in$ {"Worst", "Average", "Both"}** A string indicating if the summary table of the scenario contains the worst results among the instances, the average one, or both.

- **Plot_Worst** A Boolean parameter (True or False) indicating whether the plot illustrates the highest ratio among the instances. When it is False, the average ratio across the instances is considered.


## Outputs

- **run_experiment**: Runs a simulation for a specific combination of parameters, creating a table containing the results of the DSOS and RSOS algorithms, as well as two lower bounds on the optimal solutions for each scenario and realization. The table's dimensions are (*instances* , *realizations_p* ).
  
- **convert_all_both**: Takes the tables created by *run_experiment* and outputs a summary table for each distribution and algorithm. In every table cell, corresponding to different combinations of the values in N and M, the average or the worst-case ratios among the instances are represented.
  
- **make_plot**: Takes a summary table created by convert_all_both to generate plots of the worts-case or the average ratio against the number of jobs for each number of machines setting.



## Source
[1] Schulz, Andreas S. "Stochastic online scheduling revisited." International Conference on Combinatorial Optimization and Applications. Berlin, Heidelberg: Springer Berlin Heidelberg, 2008.



