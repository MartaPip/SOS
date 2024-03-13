#  Work in progress: *Stochastic Online Scheduling on Identical Parallel Machines* 


## Description
Master project on "Stochastic Online Scheduling on Parallel Machines".

This reposotory contains the simulation code for testing the thoretical bound stated in "Stochastic online scheduling revisited"[1] and proved in the Master project.

## Setup

```bash

git clone git@github.com:MartaPip/Stochastic-Online-Scheduling.git

cd Stochastic-Online-Scheduling

conda env create -f environment.yml

conda activate Tesi_env

```

## Running the exoeriments
**TO DO**: After obtaining the main results, modify the code to incorporate *argparse* for more flexible parameter handling.

To run the experiments, adjust the following parameters in the *experiments.py* file and execute it:

### Usually fixed:

- **N=[10,20,50,100,200,500,1000]** array specifying the number of jobs to consider in the simulations.

- **M=[1,2,5,10]** array specifying the number of machines to consider in the simulations.

- **Distributions=["d_uniform","exponential","log_normal","deterministic"]** list specifying the distributions to consider in the simulations.

- **upper_mean** upper bound on the expected value of the processing times

- **upper_we** upperbound on the weigths of the jobs.

- **alpha_DSOS** the alpha considered in the $DSOS$ algorithm, by default it is *golden ratio* $-1$.

- **instances** number of istances simulated for each scenario.

- **realizations_p** number of realization of the processing times simulatated for each instance

- **Delta_try** The upper bound on the coefficient of variation considered when running simulations with the log-normal distribution. The default value is 10.

### Select  release time conditions:

- **fixed_release_par** A Boolean parameter (True or False) indicating whether the upper bound of the release time of the jobs depends on the number of jobs considered.

- **Tigth_analysis**  A Boolean parameter (True or False) indicating whether the upper bound of the release time of the jobs depends on the number of machines considered.

- **upper_release_par** If Tigth_analysis is True the the upper bound on the release time is calculated as upper_release_par $\times$ upper_we $\times \frac{n}{2m}$. If fixed_release_par is True, it specifies the upper bound on the release time. Otherwise, the upper bound is calculated as $n \times$ upper_release_par.

### Modify summary tables and plot sharacteristics:

- **Summary $\in$ {"Worst", "Average", "Both"}** A string indicating if the summery table of the scenario contains worst results among the instances, the average one or both.

- **Plot_Worst** A Boolean parameter (True or False) indicating whether the plot illustrate the highes ratio among the istances. When it is False, the average ratio is considered

.
## Outputs

- **run_experiment**: Runs a simulation for a specific combination of parameters, creating a table containing the results of the DSOS and RSOS algorithms, as well as two lower bounds on the optimal solutions for each scenario and realization.
  
- **convert_all_both**: Takes the tables created by *run_experiment* and, for each distribution and algorithm, outputs a summary table. In every cell of the table, corresponding to a different combinations of the values in N and M, the average or the worst-case ratios among the instance is represented.
  
- **make_plot**: Takes a table created by convert_all_both to generate the plots.







## Source
[1] Schulz, Andreas S. "Stochastic online scheduling revisited." International Conference on Combinatorial Optimization and Applications. Berlin, Heidelberg: Springer Berlin Heidelberg, 2008.

[2]


