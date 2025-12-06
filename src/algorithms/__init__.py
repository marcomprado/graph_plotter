from .bfs import BFSAlgorithm
from .dfs import DFSAlgorithm


class AlgorithmFactory:
    """Fábrica para criar instâncias de algoritmos"""

    @staticmethod
    def create_algorithm(algo_type: str):
        """
        Criar algoritmo baseado no tipo

        Args:
            algo_type: Tipo de algoritmo ("BFS", "DFS")

        Returns:
            Instância de algoritmo para o tipo especificado

        Raises:
            ValueError: Se algo_type for desconhecido
        """
        algorithms = {
            "BFS": BFSAlgorithm(),
            "DFS": DFSAlgorithm()
        }
        if algo_type not in algorithms:
            raise ValueError(f"Algoritmo desconhecido: {algo_type}")
        return algorithms[algo_type]


__all__ = ['AlgorithmFactory', 'BFSAlgorithm', 'DFSAlgorithm']
