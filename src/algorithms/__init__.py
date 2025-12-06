from .bfs import BFSAlgorithm
from .dfs import DFSAlgorithm
from .dijkstra import DijkstraAlgorithm
from .mst_prim import PrimMSTAlgorithm


class AlgorithmFactory:
    """Fábrica para criar instâncias de algoritmos"""

    @staticmethod
    def create_algorithm(algo_type: str):
        """
        Criar algoritmo baseado no tipo

        Args:
            algo_type: Tipo de algoritmo ("BFS", "DFS", "Dijkstra", "MST (Prim)")

        Returns:
            Instância de algoritmo para o tipo especificado

        Raises:
            ValueError: Se algo_type for desconhecido
        """
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
