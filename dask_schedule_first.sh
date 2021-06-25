#!/usr/bin/env bash

#SBATCH -J dask-scheduler
#SBATCH -n 1
#SBATCH -t 00:10:00

module load cuda-11.0
module load anaconda3

CONDA_ROOT=$(conda info --base)
source $CONDA_ROOT/etc/profile.d/conda.sh
conda activate rapids-0.19


LOCAL_DIRECTORY=/home/clusterusers/pasyloslabini/dask-local-directory
mkdir $LOCAL_DIRECTORY
dask-scheduler --protocol tcp --scheduler-file "$LOCAL_DIRECTORY/dask-scheduler.json"
