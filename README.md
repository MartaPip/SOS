# Stochastic Online Scheduling
**Work in progress**: 

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


- *N=[10,20,50,100,200,500,1000]* array specifying the number of jobs to consider in the simulations.

- *M=[1,2,5,10]* array specifying the number of machines to consider in the simulations.

- *Distributions=["d_uniform","exponential","log_normal","deterministic"]* array specifying the distributions to consider in the simulations.

- *fixed_release_par* A Boolean parameter (True or False) indicating whether the upper bound of the release time of the jobs depends on the number of jobs considered.

- *upper_release_par* If fixed_release_par is True, it specifies the upper bound on the release time. Otherwise, the upper bound is calculated as $n \times$ upper_release_par.

- *upper_release_we* upperbound on the weigths of the jobs.

- *alpha_DSOS* the alpha considered in the $DSOS$ algorithm, by default it is *golden ratio* $-1$.

- *Delta_try* The upper bound on the coefficient of variation considered when running simulations with the log-normal distribution. The default value is 10.

*NOTE:* Additional parameters can be modified to adapt the plots or the type of comparison between our solution and the lower bound on the optimal solution.
## Outputs

- **run_experiment**: Runs a simulation for a specific combination of parameters, creating a table containing the results of the DSOS and RSOS algorithms, as well as two lower bounds on the optimal solutions for each scenario and realization.
  
- **convert_all**: Takes the tables created by *run_experiment* and creates a summary table with the ratio evaluated for different combinations of the values in N and M.
  
- **make_plot**: Takes the table created by convert_all to generate the final plots.







## Source
[1] Schulz, Andreas S. "Stochastic online scheduling revisited." International Conference on Combinatorial Optimization and Applications. Berlin, Heidelberg: Springer Berlin Heidelberg, 2008.

[2]


