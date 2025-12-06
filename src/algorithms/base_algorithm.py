from abc import ABC, abstractmethod
from typing import Generator
import networkx as nx
from src.models.graph_state import GraphState


class BaseAlgorithm(ABC):
    """Classe base abstrata para algoritmos de travessia de grafos"""

    @abstractmethod
    def traverse(self, graph: nx.Graph, start_node) -> Generator[GraphState, None, None]:
        """
        Executar algoritmo e produzir estado a cada passo

        Args:
            graph: Grafo NetworkX para percorrer
            start_node: Nó inicial para travessia

        Yields:
            Objetos GraphState representando cada passo
        """
        pass
