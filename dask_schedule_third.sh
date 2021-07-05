#!/usr/bin/env bash
#SBATCH -J dask-client
#SBATCH -t 48:00:00
#SBATCH --error=client-%j.err
#SBATCH --output=client-%j.out
#SBATCH --partition gpu
#SBATCH --gres=gpu
#SBATCH --nodes 2
module load cuda-11.0
module load anaconda3
CONDA_ROOT=$(conda info --base)
source $CONDA_ROOT/etc/profile.d/conda.sh
conda activate rapids-21.06

python3 /home/clusterusers/pasyloslabini/social_cugraphs/centrality_tests.py --input-file /home/clusterusers/pasyloslabini/social_cugraphs/YT_BIG_relabeled.csv --output-folder /home/clusterusers/pasyloslabini/social_cugraphs/big_test/
