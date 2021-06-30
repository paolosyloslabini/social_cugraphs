#!/usr/bin/env bash
#SBATCH -J dask-cuda-workers
#SBATCH -t 48:00:00
#SBATCH --job-name=dask_schedule_start
#SBATCH --error=workers-%j.err
#SBATCH --output=workers-%j.out
#SBATCH --partition gpu
#SBATCH --gres=gpu
#SBATCH --nodes 2
module load cuda-11.0
module load anaconda3

CONDA_ROOT=$(conda info --base)
source $CONDA_ROOT/etc/profile.d/conda.sh
conda activate rapids-21.06
LOCAL_DIRECTORY=/home/clusterusers/pasyloslabini/dask-local-directory

dask-cuda-worker \
	    --rmm-pool-size 32GB \
	        --scheduler-file "$LOCAL_DIRECTORY/dask-scheduler.json"

