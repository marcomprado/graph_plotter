from dataclasses import dataclass
from typing import List, Any
import networkx as nx


@dataclass
class GraphState:
    """Representa o estado da travessia do grafo em um passo específico"""
    visited: List[Any]          # Nós visitados até agora
    current: Any                # Nó atual sendo processado
    queue_or_stack: List[Any]   # Estado da estrutura de dados auxiliar
    graph: nx.Graph             # Referência ao grafo NetworkX
    previous: Any = None        # Nó anterior (de onde viemos)
    visited_edges: List[tuple] = None  # Lista de arestas já percorridas
