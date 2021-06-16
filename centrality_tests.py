import cugraph
import cudf as cudf
import argparse


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect results for approximate algorithms into a csv")
	parser.add_argument("--input-file", default="/", help="the input csv of a graph to be analyzed")
	args = parser.parse_args()
	input_file = args.input_file

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
print("evaluating centrality scores")
df_page = cugraph.pagerank(G)
print("pagerank done")
vertex_bc = cugraph.betweenness_centrality(G)
print("BC done")
edge_bc = cugraph.edge_betweenness_centrality(G)
print("EDGE BC done")

# Communities
gdf["data"] = 1.0
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst', edge_attr='data', renumber=True)
df_louv, mod_louv = cugraph.louvain(G)
df_ecg = cugraph.ecg(G)

for i in range(5):
	print("vertex " + str(df_page['vertex'].iloc[i]) +
		" PageRank is " + str(df_page['pagerank'].iloc[i]))
