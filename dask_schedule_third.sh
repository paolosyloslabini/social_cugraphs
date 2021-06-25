#!/usr/bin/env bash
#SBATCH -J dask-client
#SBATCH -n 1
#SBATCH -t 00:10:00
#SBATCH --error=cuda.err


module load cuda-11.0
module load anaconda3

CONDA_ROOT=$(conda info --base)
source $CONDA_ROOT/etc/profile.d/conda.sh

conda activate rapids-0.19

LOCAL_DIRECTORY=/nfs/dask-local-directory

cat <<EOF >>/tmp/dask-cudf-example.py
import cudf
import dask.dataframe as dd
from dask.distributed import Client

client = Client(scheduler_file="$LOCAL_DIRECTORY/scheduler.json")
cdf = cudf.datasets.timeseries()

ddf = dd.from_pandas(cdf, npartitions=10)
res = ddf.groupby(['id', 'name']).agg(['mean', 'sum', 'count']).compute()
print(res)
EOF

python3 /tmp/dask-cudf-example.py

