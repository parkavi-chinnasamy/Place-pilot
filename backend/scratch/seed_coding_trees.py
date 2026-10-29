import sqlite3
import uuid

DB_PATH = 'placepilot.db'

# Format: (topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation)
tree_questions = [
    # ==================== TREES & GRAPHS - Easy (12) ====================
    ("Trees & Graphs", "easy", "Which tree traversal visits the root node first, then the left subtree, and finally the right subtree?", "Inorder", "Preorder", "Postorder", "Level-order", "B", "Preorder traversal follows Root -> Left -> Right order."),
    ("Trees & Graphs", "easy", "Which tree traversal visits nodes level by level from top to bottom?", "Inorder", "Preorder", "Breadth-First Search (Level-Order)", "Depth-First Search", "C", "Level-order traversal uses a queue to visit all nodes at depth d before depth d+1."),
    ("Trees & Graphs", "easy", "What is the maximum number of children a node can have in a Binary Tree?", "1", "2", "3", "Unlimited", "B", "A binary tree is defined as a tree in which no node has more than two child nodes."),
    ("Trees & Graphs", "easy", "In a Binary Search Tree (BST), where are keys smaller than the root node stored?", "In the right subtree", "In the left subtree", "At leaf nodes only", "In any child node", "B", "By definition of BST, all values in the left subtree must be strictly less than the node's key."),
    ("Trees & Graphs", "easy", "What data structure is typically used to implement Breadth-First Search (BFS) in a graph?", "Stack", "Queue", "Priority Queue", "Hash Set", "B", "BFS explores vertices in order of discovery (FIFO), implemented using a Queue."),
    ("Trees & Graphs", "easy", "What data structure is typically used for the iterative implementation of Depth-First Search (DFS)?", "Queue", "Stack", "Heap", "Linked List", "B", "DFS dives deep along branches before backtracking (LIFO), implemented using a Stack."),
    ("Trees & Graphs", "easy", "What is a leaf node in a tree?", "The top-most node", "A node with no children", "A node with exactly two children", "The root node", "B", "A leaf (terminal) node is a node that has degree 0 (no child nodes)."),
    ("Trees & Graphs", "easy", "What is the degree of a vertex in an undirected graph?", "The number of edges incident to the vertex", "The total number of vertices in the graph", "The length of the shortest path to root", "The weight of its heaviest edge", "A", "In an undirected graph, degree is the count of edges connected to the vertex."),
    ("Trees & Graphs", "easy", "What is a tree with N vertices guaranteed to have in terms of edges?", "N edges", "N - 1 edges", "N + 1 edges", "2 * N edges", "B", "A connected undirected graph with N vertices is a tree if and only if it has exactly N - 1 edges and no cycles."),
    ("Trees & Graphs", "easy", "What does post-order traversal order look like for a binary tree?", "Root -> Left -> Right", "Left -> Root -> Right", "Left -> Right -> Root", "Right -> Root -> Left", "C", "Post-order processes both subtrees before processing the current root node (Left -> Right -> Root)."),
    ("Trees & Graphs", "easy", "How do you detect if an undirected graph has a cycle during DFS?", "If a visited node is encountered that is NOT the parent of the current node", "If all nodes have degree 2", "If there are more vertices than edges", "If DFS finishes in O(V) time", "A", "In an undirected graph, finding a visited neighbor other than the immediate parent indicates a back-edge (cycle)."),
    ("Trees & Graphs", "easy", "What is the height of a binary tree with only a root node?", "0 (or 1 depending on 0/1-based convention)", "-1", "2", "Infinity", "A", "A single-node tree has height 0 (measuring edges) or 1 (measuring nodes)."),

    # ==================== TREES & GRAPHS - Medium (14) ====================
    ("Trees & Graphs", "medium", "What is the average time complexity of search, insertion, and deletion in an AVL Tree with N nodes?", "O(N)", "O(log N)", "O(N log N)", "O(1)", "B", "An AVL tree maintains height balance where height <= 1.44 * log2(N), guaranteeing O(log N) for basic operations."),
    ("Trees & Graphs", "medium", "What is the balance factor of a node in an AVL tree?", "Height(left subtree) - Height(right subtree)", "Depth of node / Total nodes", "Number of left children - Number of right children", "Degree of left child - Degree of right child", "A", "Balance factor is defined as the height of the left subtree minus the height of the right subtree, must be in {-1, 0, 1}."),
    ("Trees & Graphs", "medium", "What is the time complexity of Breadth-First Search (BFS) on a graph with V vertices and E edges represented as an adjacency list?", "O(V * E)", "O(V + E)", "O(V^2)", "O(E log V)", "B", "BFS visits each vertex once and traverses each edge once in an adjacency list, giving O(V + E) time."),
    ("Trees & Graphs", "medium", "What is the time complexity of Dijkstra's algorithm using a Min-Heap (priority queue) with V vertices and E edges?", "O(V^2)", "O((V + E) log V)", "O(V * E)", "O(E log E)", "B", "Each vertex extraction takes O(log V) and each edge relaxation takes O(log V), yielding O((V + E) log V)."),
    ("Trees & Graphs", "medium", "When does Dijkstra's algorithm fail to find the shortest path?", "When the graph has cycles", "When the graph contains negative edge weights", "When the graph is disconnected", "When the graph is a DAG", "B", "Dijkstra assumes that adding an edge to a path cannot decrease its total length, which fails with negative weights."),
    ("Trees & Graphs", "medium", "Which algorithm is used to find single-source shortest paths in a graph that may contain NEGATIVE edge weights?", "Dijkstra's Algorithm", "Bellman-Ford Algorithm", "Kruskal's Algorithm", "Prim's Algorithm", "B", "Bellman-Ford relaxes all edges V-1 times and detects negative weight cycles in O(V * E) time."),
    ("Trees & Graphs", "medium", "What is a Topological Sort of a Directed Acyclic Graph (DAG)?", "Sorting vertices by degree", "A linear ordering of vertices such that for every directed edge u -> v, u comes before v", "A pre-order traversal of the DFS tree", "Sorting edges by weight", "B", "Topological sort orders tasks/vertices respecting all directional dependencies."),
    ("Trees & Graphs", "medium", "Which algorithm finds the Minimum Spanning Tree (MST) by sorting edges and greedily adding them using Disjoint Set Union (DSU)?", "Prim's Algorithm", "Kruskal's Algorithm", "Floyd-Warshall", "Tarjan's Algorithm", "B", "Kruskal's algorithm sorts all E edges and uses Union-Find (DSU) to prevent cycles in O(E log E) time."),
    ("Trees & Graphs", "medium", "What is the time complexity of Kruskal's algorithm with E edges and V vertices?", "O(V^2)", "O(E log E)", "O(V * E)", "O(V + E)", "B", "Sorting E edges takes O(E log E), while DSU operations take near-linear O(E * alpha(V)), dominated by O(E log E)."),
    ("Trees & Graphs", "medium", "Which algorithm finds the Lowest Common Ancestor (LCA) in a tree in O(1) query time after O(N log N) preprocessing?", "Binary Lifting", "Kruskal's", "Dijkstra's", "Floyd-Warshall", "A", "Binary lifting builds an up-table up[node][i] = 2^i-th ancestor, answering LCA in O(log N) or O(1) via RMQ."),
    ("Trees & Graphs", "medium", "What is the time complexity of the Floyd-Warshall algorithm for All-Pairs Shortest Paths on a graph with V vertices?", "O(V^2)", "O(V^3)", "O(V * E)", "O(E log V)", "B", "Floyd-Warshall uses three nested loops over V vertices, taking strictly O(V^3) time."),
    ("Trees & Graphs", "medium", "How can you check if an undirected graph is Bipartite?", "Check if all vertices have even degree", "Run 2-coloring using BFS/DFS; graph is bipartite if and only if no two adjacent vertices share the same color", "Check if V = E - 1", "Compute the minimum spanning tree", "B", "A graph is bipartite if and only if it contains no odd-length cycles, verifiable via 2-coloring in O(V + E)."),
    ("Trees & Graphs", "medium", "What does Kahn's algorithm compute using in-degrees of vertices?", "Eulerian Path", "Topological Sort", "Shortest Path", "Biconnected Components", "B", "Kahn's algorithm repeatedly removes vertices with in-degree 0 to produce a topological sort in O(V + E)."),
    ("Trees & Graphs", "medium", "What is the maximum number of edges in a simple undirected graph with V vertices?", "V", "V * (V - 1) / 2", "V^2", "2^V", "B", "Each pair of distinct vertices can have at most one undirected edge, giving V*(V-1)/2 edges.")
]

tree_hard_questions = [
    # ==================== TREES & GRAPHS - Hard (12) ====================
    ("Trees & Graphs", "hard", "What is the time complexity of Tarjan's strongly connected components (SCC) algorithm on a directed graph?", "O(V^2)", "O(V * E)", "O(V + E)", "O((V + E) log V)", "C", "Tarjan's algorithm uses DFS with discovery times and low-link values in a single pass taking O(V + E) time."),
    ("Trees & Graphs", "hard", "Which algorithm finds Bridges and Articulation Points in an undirected graph in O(V + E) time?", "Dijkstra's algorithm", "Tarjan's DFS Low-Link algorithm", "Kruskal's algorithm", "Edmonds-Karp", "B", "Maintaining discovery time tin[] and lowest reachable time low[] identifies bridges (low[v] > tin[u]) in O(V + E)."),
    ("Trees & Graphs", "hard", "What is the time complexity of Dinic's algorithm for finding Maximum Flow in a general network with V vertices and E edges?", "O(V * E^2)", "O(V^2 * E)", "O(E * max_flow)", "O(V^3)", "B", "Dinic's algorithm uses layered networks with blocking flows, running in O(V^2 * E) on general graphs and O(E * sqrt(V)) on unit networks."),
    ("Trees & Graphs", "hard", "What is Heavy-Light Decomposition (HLD) used for in tree data structures?", "Decomposing tree into vertex-disjoint paths to answer path queries in O(log^2 N) using Segment Trees", "Finding minimum weight cycle", "Converting general tree into binary tree", "Computing tree centers in O(1)", "A", "HLD breaks a tree into heavy and light edges such that any path from root to node crosses at most log N light edges."),
    ("Trees & Graphs", "hard", "What is the time complexity of Centroid Decomposition on a tree of N nodes?", "O(N^2)", "O(N log N)", "O(N^3)", "O(log N)", "B", "Dividing the tree at its centroid into components of size at most N/2 creates a recursion tree of depth log N, taking O(N log N) total."),
    ("Trees & Graphs", "hard", "What is the time complexity of Johnson's algorithm for All-Pairs Shortest Paths on sparse graphs?", "O(V^3)", "O(V^2 log V + V * E)", "O(V * E^2)", "O(V + E)", "B", "Johnson's uses Bellman-Ford once to reweight edges, then runs Dijkstra V times with Fibonacci heap in O(V^2 log V + V * E)."),
    ("Trees & Graphs", "hard", "In a flow network, what does the Max-Flow Min-Cut Theorem state?", "Maximum flow is strictly less than minimum cut capacity", "The maximum amount of flow passing from source to sink equals the total capacity of the minimum s-t cut", "Every minimum cut must contain an odd number of edges", "Max flow cannot be computed in polynomial time", "B", "The Max-Flow Min-Cut theorem establishes that the maximum value of an s-t flow is equal to the minimum capacity over all s-t cuts."),
    ("Trees & Graphs", "hard", "What is the time complexity of the Edmonds-Karp algorithm for Maximum Flow?", "O(V * E^2)", "O(V^2 * E)", "O(E^3)", "O(V * E)", "A", "Edmonds-Karp implements Ford-Fulkerson using BFS for shortest augmenting paths, terminating in O(V * E^2) time."),
    ("Trees & Graphs", "hard", "What is the time complexity to find an Eulerian Path in a graph with V vertices and E edges using Hierholzer's algorithm?", "O(V^2)", "O(V + E)", "O(E log V)", "O(V * E)", "B", "Hierholzer's algorithm maintains a current tour and spliced sub-tours, traversing each edge exactly once in O(V + E) time."),
    ("Trees & Graphs", "hard", "What is the time complexity to find the maximum matching in a general (non-bipartite) graph using Edmonds' Blossom algorithm?", "O(V^3)", "O(2^V)", "O(V + E)", "O(V! * E)", "A", "Edmonds' Blossom algorithm shrinks odd-length cycles (blossoms) to find augmenting paths in O(V^3) time."),
    ("Trees & Graphs", "hard", "In 2-SAT (2-Satisfiability), how is a boolean formula in 2-CNF solved in linear time O(V + E)?", "By constructing an implication graph and finding Strongly Connected Components (SCCs)", "By testing all 2^N truth assignments", "Using Simplex algorithm", "Using Gaussian Elimination", "A", "A 2-SAT instance is satisfiable if and only if no variable x and its negation ~x belong to the same SCC in the implication graph."),
    ("Trees & Graphs", "hard", "What is the time complexity of Kosaraju's algorithm for finding Strongly Connected Components?", "O(V^2)", "O(V + E)", "O(E log V)", "O(V * E)", "B", "Kosaraju runs two DFS passes (one on the original graph, one on the transpose graph), taking O(V + E) time.")
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

inserted = 0
for topic, diff, qtext, oa, ob, oc, od, ans, exp in tree_questions + tree_hard_questions:
    c.execute("SELECT id FROM assessment_questions WHERE assessment_type='coding' AND question_text=?", (qtext,))
    if c.fetchone() is None:
        c.execute("""
            INSERT INTO assessment_questions (id, assessment_type, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation, is_active)
            VALUES (?, 'coding', ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (str(uuid.uuid4()), topic, diff, qtext, oa, ob, oc, od, ans, exp))
        inserted += 1

conn.commit()
conn.close()
print(f"Inserted {inserted} Trees & Graphs questions for Coding.")
