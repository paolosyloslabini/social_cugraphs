#!/usr/bin/env bash
#SBATCH -J dask-client
#SBATCH -t 00:10:00
#SBATCH --error=client-%j.err
#SBATCH --output=client-%j.out
#SBATCH --partition gpu
#SBATCH --gres=gpu
#SBATCH --nodes 1
module load cuda-11.0
module load anaconda3
CONDA_ROOT=$(conda info --base)
source $CONDA_ROOT/etc/profile.d/conda.sh
conda activate rapids-21.06
LOCAL_DIRECTORY=/home/clusterusers/kohofer/slurm/sylos/dask-local-dir


python3 /home/clusterusers/kohofer/slurm/sylos/dask-local-dir/dask-cudf-example.py
 



