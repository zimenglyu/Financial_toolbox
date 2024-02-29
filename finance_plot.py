import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

result_dir = '/Users/zimenglyu/Documents/cluster_results/finance_result'
num_repeat = 7 
maxGenome=20000
n=int(0.98*maxGenome)
stock = "DJIA"
plt.figure(figsize=(16, 12), dpi=100)
offset = 2
for lr in[0.001]:
    for dataset in ["CRSP_DJI", "CRSP_DJI_slice_25", "CRSP_DJI_window_5_25"]:
        
        generation = []
        mse = []
        for repeat in range(num_repeat):
            data = np.genfromtxt(result_dir+'/{}/lr_{}/offset_{}/max_genome_{}/island_10/{}/fitness_log.csv'.format( dataset, lr, offset,maxGenome, repeat), delimiter=',', skip_header=True, usecols=(0,4))[0:n]
            generation.append(data[:,0])
            mse.append(data[:,1])

        plt.plot(np.average(generation, axis = 0), np.average(mse, axis=0), label="{}".format(dataset))
        plt.fill_between(np.average(generation, axis = 0), np.min(mse, axis=0), np.max(mse, axis=0), alpha=.2)


plt.ylim([0.00,0.004])
    #     plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.ylabel("MSE")
plt.xlabel("Generated Genomes")
title = "{}".format(stock)
name = "{}".format(stock)
plt.title(title)
plt.savefig(name + ".png",bbox_inches='tight')  