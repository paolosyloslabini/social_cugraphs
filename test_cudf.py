import cudf
import dask.dataframe as dd
from dask.distributed import Client
schedulerjson = "/home/clusterusers/pasyloslabini/dask-local-directory/dask-scheduler.json"
print(schedulerjson)
client = Client(scheduler_file=schedulerjson)
cdf = cudf.datasets.timeseries()

ddf = dd.from_pandas(cdf, npartitions=10)
res = ddf.groupby(['id', 'name']).agg(['mean', 'sum', 'count']).compute()
print(res)
