# 🎬 IMDB Actor Graph

This project builds a large graph from IMDB data.

- **Nodes**: Actors  
- **Edges**: One for each movie two actors appear in together  
- **Edge weights**: Movie rating  
- **Graph type**: Undirected, weighted, with parallel edges

Alternative model: Bipartite graph with actors and movies as nodes.

The graph has ~100,000 nodes and ~5 million edges.  
Used for testing graph algorithms like shortest path, clustering, and centrality.

## Run

```bash
python build_graph.py
