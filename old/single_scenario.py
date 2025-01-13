# Code developed in previous versions. Could be still usefull for future develompments if interested in 
# variations of the DSOS or RSOS algorithms

########################### CHECK arrival with fixed time steps: #######################

import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from bisect import insort_left,insort_right
from tabulate import tabulate
import random
from random import randint
import os
from job_class import Job,Job_b
from run_one import assigment_both,check_arrival_time

Printing=False

def assigment(RANDOM_assigment,job,m,machines):
    ########################################################################################
    ##########################INPUT:#######################################################
    #job               = element of the class job_b
    #RANDOM_assigment  = TRUE if random assigment, FALSE if assignment to first free machine
    #m                 = numbere machines considered
    #machines          = list containing the times machine will be free for the first time 

    ##########################OUTPUT:########################################################
    # complition time job
    #########################################################################################
    #select machine
    if RANDOM_assigment: machine=randint(0,m-1)
    else: 
        firts_free=np.min(machines)
        machine=np.min(np.where(machines==firts_free)) #assign to machine that is freed before

    if machines[machine]>=job.ta: #machine is free after alpha-point--> need to wait for machine to be free
        machines[machine]=machines[machine]+job.processing
    else: #machine is free berore alpha-point--> need to wait for job to reach alpha point
        machines[machine]=job.ta+job.processing
    complition=machines[machine]
    return complition

def run_one(jobs, m,RANDOM_alpha,RANDOM_assigment,alpha,time_step):
    ###############################################################################################################################
    ####################################################INPUT:#####################################################################
    #jobs              = list containing the Jobs, each job is an element of the class job_b
    #m                 = numbers machines in the simulation
    #time_step         = time between checks new arrival
    #RANDOM_alpha      = TRUE if alpha point are drawn at random, 
    #RANDOM_assigment  = TRUE if jobs are randombly assigned to the machines
    #alpha             = fixed value \alpha in the DSOS algorithm, usually golden_ratio-1, used if RANDOM_alpha =FALSE

    ####################################################OUTPUT:#####################################################################
    # objective value of the algorithm and the 2 lower bounds
    ################################################################################################################################
    

    # List to store arrived jobs
    L = []

    #Vector containig values of when a machine will be free again
    machines=np.zeros(m)

    #In case we run more algorims with the same jobs
    for job in jobs: 
        job.done_1=0
        job.MBT=0
    
    ite=0

    # Initialize last check time
    relative_current = 0
    last_check_time=0
    # Record the starting time of the algorithm
    start_time = datetime.now()
    
    # Until all the jobs are not processed in the single fast machine
    while sum(job.done_1 for job in jobs)<len(jobs):
        ite=ite+1      
        # Update current time
        relative_current = (datetime.now() - start_time).total_seconds()
        #check for new arrivals
        new_arrivals = check_arrival_time(jobs, relative_current,last_check_time)
        # Update last check time
        last_check_time=relative_current
        
        
        if Printing:
            print("\n\n NEW ITERATION")
            if not new_arrivals:   print("not new arrival")
        #Update L if new job arrived 
        for arrived_job_idx in new_arrivals:
            arrived_job = jobs[arrived_job_idx]
            
            #Assign value alpha
            if RANDOM_alpha: 
                arrived_job.alpha=np.random.uniform(0,1)
            else:
                arrived_job.alpha=alpha 

            insort_right(L, arrived_job, key=lambda x: -(x.we/x.expected)) #in order of not increasing w_j/p_j
            if Printing: print(f"One job arrived at {datetime.now(), relative_current} for {arrived_job.id}")

    
        #process first job in L if list is not empty
        if L:
            i=0
            tot=0
            remaning=(1-L[i].done_1)*L[i].expected/m 
            
            #when there is a job waiting and there is enough time to finish the next job 
            while tot+remaning<=time_step and i <len(L): 
                #update the mean busy time of the job we are processing    
                L[i].MBT=L[i].MBT+(m/L[i].expected)*(remaning*(2*(tot+relative_current) +remaning))/2 # cost*((relative_current+tot+remaing)^2-(relative_curreny+tot)^2)=# cost*((when_finish processing the job)^2-(when_started job in this interval)^2)
                
                #if we reach alpha point-->send the job to the real machines
                if L[i].done_1< L[i].alpha:
                    L[i].ta=relative_current+tot+(L[i].alpha-L[i].done_1)*L[i].expected/m #alpha-point=exact moment when it an alpha.portion of the job is processed
                    L[i].complition=assigment(RANDOM_assigment,L[i],m,machines)
                
                L[i].done_1=1 #job inside the while are finished
                i=i+1
                tot=tot+remaning
                if len(L)>i:
                    remaning=(1-L[i].done_1)*L[i].expected/m 
            #outside while--> only time to process part of the next job
            if len(L)>i: #if there is new job

                done_before=L[i].done_1    
                L[i].done_1=L[i].done_1+(time_step-tot)/(L[i].expected/m)
                if done_before< L[i].alpha<=L[i].done_1: #if alpha point reached in this interval
                    L[i].ta=relative_current+tot+(L[i].alpha-done_before)*L[i].expected/m 
                    L[i].complition=assigment(RANDOM_assigment,L[i],m,machines)
                L[i].MBT=L[i].MBT+(m/L[i].expected)*((relative_current+ time_step)**2-(relative_current+ tot)**2)/2
                L=L[i:] #eliminate jobs that are finished

            else: 
                L=[] #eliminate jobs that are finished
            

    # Print the table
        if Printing:
            table_data = [(job.id, job.release, job.done_1, (1-job.done_1)*job.expected/m, job.MBT , job.ta, job.processing, job.complition, job.alpha) for job in jobs]
            print("end",len(L),L)
            print("after iteration:", ite, "and time:", (datetime.now() - start_time).total_seconds())
            print(tabulate(table_data, headers=['Job ID','release', 'Done', 'Remaining', 'Mean busy time','alpha_point', 'processing','complition', 'alpha']))
            print(machines)


        time.sleep(time_step)  # sleep for 1 second

    
    total_complition = sum(job.we * job.complition for job in jobs)
    total_LR= sum(job.we * (job.MBT-(job.CV-1)*job.expected/2) for job in jobs)
    basic_LB= sum(job.we * job.expected for job in jobs)
    return total_complition, total_LR, basic_LB


def run_one_both(jobs, m,alpha,time_step):
    ###############################################################################################################################
    ####################################################INPUT:#####################################################################
    #jobs              = list containing the Jobs, each job is an element of the class job_b
    #m                 = numbers machines in the simulation
    #alpha             = fixed value \alpha in the DSOS algorith, usually golden_ratio-1
    #time_step         = time between checks new arrival
    ####################################################OUTPUT:#####################################################################
    # objective value of the RSOS algorith, DSOS algorithm, and the 2 lower bounds
    ################################################################################################################################
    # List to store arrived jobs
    L=[]
    #Vectors containig values of when a machine will be free again in each of the algorithms
    machines_DSOS=np.zeros(m)
    machines_RSOS=np.zeros(m)
    
    ite=0
    for job in jobs: #In case we run more algorims with the same jobs
        job.done_1=0
        job.MBT=0

    # Initialize last check time
    relative_current = 0
    last_check_time=0

    # Record the starting time of the algorithm
    start_time = datetime.now()
    #ordered_job_list = sorted(jobs, key=lambda x: x.release)
    #arrival=0
    
    # Until all the jobs are not processed in the single fast machine
    while sum(job.done_1 for job in jobs)<len(jobs):
        ite=ite+1
        #print("iteration",ite)
        if ite%10==0: print("iteration",ite)
       
        # Update current time
        relative_current = (datetime.now() - start_time).total_seconds()
        #check for new arrivals
        new_arrivals = check_arrival_time(jobs, relative_current,last_check_time)
        #new_arrivals,arrival=check_ordered(ordered_job_list, relative_current,last_check_time,arrival)
         # Update last check time
        last_check_time=relative_current
        
        if Printing:
            print("\n\n NEW ITERATION")
            if not new_arrivals:  print("not new")
        #update L if new job arrived 
        for arrived_job_idx in new_arrivals:
            arrived_job = jobs[arrived_job_idx]
            
            #assign alpha for 2 algorithms:
            arrived_job.alpha_RSOS=np.random.uniform(0,1)
            arrived_job.alpha_DSOS=alpha 
            insort_right(L, arrived_job, key=lambda x: -(x.we/x.expected)) #in order of not increasing w_j/p_j
            if Printing: print(f"One job arrived at {datetime.now()} for {arrived_job.id}")
            
    
        #process first job in L if list is not empty
        if L:
            i=0
            tot=0
            remaning=(1-L[i].done_1)*L[i].expected/m 
            
            #when there is a job waiting and there is enough time to finish the next job 
            while tot+remaning<=time_step and i <len(L):

                #update the mean busy time of the job we are processing    
                L[i].MBT=L[i].MBT+(m/L[i].expected)*(remaning*(2*(tot+relative_current) +remaning))/2 # cost*((relative_current+tot+remaing)^2-(relative_curreny+tot)^2)=# cost*((when_finish processing the job)^2-(when_started job in this interval)^2)
                
                #if we reach alpha point RSOS or DSOS-->send the job to the real machines in the correspinding algorithm
                if L[i].done_1< L[i].alpha_RSOS:
                    L[i].ta_RSOS=relative_current+tot+(L[i].alpha_RSOS-L[i].done_1)*L[i].expected/m
                    L[i].comp_RSOS=assigment_both("RSOS",L[i],m,machines_RSOS,machines_DSOS)
                if L[i].done_1< L[i].alpha_DSOS:
                    L[i].ta_DSOS=relative_current+tot+(L[i].alpha_DSOS-L[i].done_1)*L[i].expected/m
                    L[i].comp_DSOS=assigment_both("DSOS",L[i],m,machines_RSOS,machines_DSOS)

                L[i].done_1=1 #job inside the while are finished
                i=i+1
                tot=tot+remaning
                if len(L)>i:
                    remaning=(1-L[i].done_1)*L[i].expected/m 
            
            #outside while--> only time to process part of the next job
            if len(L)>i: #if there is new job
                
                done_before=L[i].done_1    
                L[i].done_1=L[i].done_1+(time_step-tot)/(L[i].expected/m)
                
                if done_before< L[i].alpha_RSOS<=L[i].done_1:
                    L[i].ta_RSOS=relative_current+tot+(L[i].alpha_RSOS-done_before)*L[i].expected/m 
                    L[i].comp_RSOS=assigment_both("RSOS",L[i],m,machines_RSOS,machines_DSOS)
                if done_before< L[i].alpha_DSOS<=L[i].done_1:
                    L[i].ta_DSOS=relative_current+tot+(L[i].alpha_DSOS-done_before)*L[i].expected/m  
                    L[i].comp_DSOS=assigment_both("DSOS",L[i],m,machines_RSOS,machines_DSOS)                  
                    
                L[i].MBT=L[i].MBT+(m/L[i].expected)*((relative_current+ time_step)**2-(relative_current+ tot)**2)/2
                
                L=L[i:] #eliminate jobs that are finished

            else: 
                L=[] #eliminate jobs that are finished
            

    # Print the table
        if Printing: 
            table_data = [(job.id, job.release, job.done_1, (1-job.done_1)*job.expected/m, job.MBT , job.expected, job.processing, job.alpha_RSOS, job.ta_RSOS, job.alpha_DSOS, job.ta_DSOS, job.comp_RSOS, job.comp_DSOS) for job in jobs]
            print("end",len(L),L)
            print("after iteration:", ite, "and time:", (datetime.now() - start_time).total_seconds())
            print(tabulate(table_data, headers=['Job ID','release', 'Done', 'Remaining', 'Mean busy time','expected','processing','alpha_R','alpha_point_R','alpha_D','alpha_point_D','complition_R', 'complition_D']))
            print("RSOS",machines_RSOS)
            print("DSOS",machines_DSOS)


        time.sleep(time_step)  # sleep for 1 second
    total_comp_RSOS = sum(job.we * job.comp_RSOS for job in jobs)
    total_comp_DSOS = sum(job.we * job.comp_DSOS for job in jobs)
    total_LR= sum(job.we * (job.MBT-(job.CV-1)*job.expected/2) for job in jobs)
    basic_LB= sum(job.we * job.expected for job in jobs)
    return total_comp_RSOS,total_comp_DSOS, total_LR,basic_LB
