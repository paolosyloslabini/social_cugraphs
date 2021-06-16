import cugraph
import cudf as cudf
import argparse


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect results for approximate algorithms into a csv")
	parser.add_argument("--input-file", default="/", 
		    help="the input csv of a graph to be analyzed")
    	args = parser.parse_args()

 	input_file = args.input_file;

# read data into a cuDF DataFrame using read_csv
gdf = cudf.read_csv(, names=["src", "dst"], dtype=["int32", "int32"])

# We now have data as edge pairs
# create a Graph using the source (src) and destination (dst) vertex pairs
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst')

# Centrality scores
df_page = cugraph.pagerank(G)
vertex_bc = cugraph.betweenness_centrality(G)
edge_bc = cugraph.edge_betweenness_centrality(G)

# Communities
gdf["data"] = 1.0
G = cugraph.Graph()
G.from_cudf_edgelist(gdf, source='src', destination='dst', edge_attr='data', renumber=True)
df_louv, mod_louv = cugraph.louvain(G)
df_ecg = cugraph.ecg(G)
