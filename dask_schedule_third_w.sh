#!/usr/bin/env bash
#SBATCH -J dask-client
#SBATCH -t 48:00:00
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

python3 /home/clusterusers/pasyloslabini/social_cugraphs/analyse_weighted_graph.py --input-file ${1} --output-folder ${2} --threshold 1500 --name g_1500
python3 /home/clusterusers/pasyloslabini/social_cugraphs/analyse_weighted_graph.py --input-file ${1} --output-folder ${2} --threshold 1000 --name g_1000
python3 /home/clusterusers/pasyloslabini/social_cugraphs/analyse_weighted_graph.py --input-file ${1} --output-folder ${2} --threshold 500 --name g_500
