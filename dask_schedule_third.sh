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
conda activate rapids-0.19
LOCAL_DIRECTORY=/home/clusterusers/pasyloslabini/dask-local-directory


cat <<EOF >>/home/clusterusers/pasyloslabini/dask-local-directory/dask-cudf-example.py
import cudf
import dask.dataframe as dd
from dask.distributed import Client
client = Client(scheduler_file="$LOCAL_DIRECTORY/scheduler.json")
cdf = cudf.datasets.timeseries()
ddf = dd.from_pandas(cdf, npartitions=10)
res = ddf.groupby(['id', 'name']).agg(['mean', 'sum', 'count']).compute()
print(res)
EOF

 

python3 /home/clusterusers/pasyloslabini/dask-local-directory/dask-cudf-example.py 



