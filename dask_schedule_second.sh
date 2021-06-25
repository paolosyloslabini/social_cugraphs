#!/usr/bin/env bash

#SBATCH -J dask-cuda-workers
#SBATCH -t 00:10:00
#SBATCH --job-name=dask_schedule_start
#SBATCH --mem=10G


module load cuda-11.0
module load anaconda3


CONDA_ROOT=$(conda info --base)
source $CONDA_ROOT/etc/profile.d/conda.sh
conda activate rapids-0.19

LOCAL_DIRECTORY=/nfs/dask-local-directory

dask-cuda-worker \
	    --rmm-pool-size 1GB \
	        --scheduler-file "$LOCAL_DIRECTORY/dask-scheduler.json"

