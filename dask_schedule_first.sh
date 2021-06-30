#!/usr/bin/env bash
#SBATCH -J dask-scheduler
#SBATCH --partition gpu
#SBATCH --nodes 1
#SBATCH --ntasks=1
#SBATCH -t 48:00:00
#SBATCH --error=scheduler-%j.err
#SBATCH --output=scheduler-%j.out
module load cuda-11.0
module load anaconda3
CONDA_ROOT=$(conda info --base)
source $CONDA_ROOT/etc/profile.d/conda.sh
conda activate rapids-21.06

LOCAL_DIRECTORY=/home/clusterusers/pasyloslabini/dask-local-directory
mkdir $LOCAL_DIRECTORY
dask-scheduler --protocol tcp --scheduler-file "$LOCAL_DIRECTORY/dask-scheduler.json"
