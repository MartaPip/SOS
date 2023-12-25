# Stochastic Online Scheduling
**Work in progress**: 

## Description
Master project on "Stochastic Online Scheduling on Parallel Machines".

This reposotory contains the simulation code for testing the thoretical bound stated in "Stochastic online scheduling revisited"[1] and proved in the Master project.

## Installation
git clone git@github.com:MartaPip/Stochastic-Online-Scheduling.git
cd Stochastic-Online-Scheduling
conda env create -f environment.yml
conda activate Tesi_env

## Usuage
**TO DO**: after having the main results--> modify code to use  *argparse* ()

To run the experiments adapt the following parameters in the *experiments.py* file:\\
- *N=[10,20,50,100,200,500,1000]* array containing the number of jobs to consider in the simulations.

- *M=[1,2,5,10]* array containing the number of machine to consider in the simulations.

- *Distributions=["d_uniform","exponential","log_normal","deterministic"]* array contating the name of the distribution to consider in the simulations.


- *fixed_release_par $\in [True,False]$*  True if the upper bound of the release time of the jobs does not depend on the number of job considered

- *upper_release_par* If fixed_release_par is True it gives the upper bound on the release time. Otherwise the upperbound is give by $n*upper_release_pa$

- *upper_release_par* upperbound on the weigths of the jobs.

- *alpha_DSOS* the alpha considered in the $DSOS$ algorithm, by default it is $golden ratio-1$.

- *Delta_try* the $\Delta$ (upper_bound on the coefficient of variation) that is considered when running simulations wuth the log-normal distribution.  By defauly it is 10.




## Source
[1] Schulz, Andreas S. "Stochastic online scheduling revisited." International Conference on Combinatorial Optimization and Applications. Berlin, Heidelberg: Springer Berlin Heidelberg, 2008.
[2]


