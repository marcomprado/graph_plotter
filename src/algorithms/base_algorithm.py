from abc import ABC, abstractmethod
from typing import Generator
import networkx as nx
from src.models.graph_state import GraphState


class BaseAlgorithm(ABC):

    @abstractmethod
    def traverse(self, graph: nx.Graph, start_node) -> Generator[GraphState, None, None]:
        pass
