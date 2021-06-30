import cugraph
import cudf as cudf
from dask.distributed import Client
import argparse

schedulerjson = "/home/clusterusers/pasyloslabini/dask-local-directory/dask-scheduler.json"
client = Client(scheduler_file=schedulerjson)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect results for approximate algorithms into a csv")
	parser.add_argument("--input-file", default="/", help="the input csv of a graph to be analyzed")
	parser.add_argument("--output-folder", default="/", help="the where to save results")
	args = parser.parse_args()
	input_file = args.input_file
	output_folder = args.output_folder

# read data into a cuDF DataFrame using read_csv
print("reading csv")
gdf = cudf.read_csv(input_file, names=["src", "dst"], dtype=["int32", "int32"])
print("csv read")

# We now have data as edge pairs
# create a Graph using the source (src) and destination (dst) vertex pairs
print("Making graph")
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst')
print("Graph created")

# Centrality scores
#print("evaluating centrality scores")
#df_page = cugraph.pagerank(G)
#df_page.to_csv(output_folder + "/pagerank.csv")
#print("pagerank done")

#vertex_bc = cugraph.betweenness_centrality(G)
#vertex_bc.to_csv(output_folder + "/vertex_bc.csv")
#print("BC done")

#Communities
gdf["data"] = 1
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst', edge_attr='data')
df_louv, mod_louv = cugraph.louvain(G)
df_louv.to_csv(output_folder + "/df_louv.csv")
print("Louvain done")

df_ecg = cugraph.ecg(G)
df_ecg.to_csv(output_folder + "/df_ecg.csv")
print("ECG done");

print("sanity check: printing the first 5 pagerank score")
for i in range(5):
	print("vertex " + str(df_page['vertex'].iloc[i]) +
		" PageRank is " + str(df_page['pagerank'].iloc[i]))
