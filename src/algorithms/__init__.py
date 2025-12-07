from .bfs import BFSAlgorithm
from .dfs import DFSAlgorithm
from .dijkstra import DijkstraAlgorithm
from .mst_prim import PrimMSTAlgorithm


class AlgorithmFactory:

    @staticmethod
    def create_algorithm(algo_type: str):
        algorithms = {
            "BFS": BFSAlgorithm(),
            "DFS": DFSAlgorithm(),
            "Dijkstra": DijkstraAlgorithm(),
            "MST (Prim)": PrimMSTAlgorithm()
        }
        if algo_type not in algorithms:
            raise ValueError(f"Algoritmo desconhecido: {algo_type}")
        return algorithms[algo_type]


__all__ = ['AlgorithmFactory', 'BFSAlgorithm', 'DFSAlgorithm', 'DijkstraAlgorithm', 'PrimMSTAlgorithm']
