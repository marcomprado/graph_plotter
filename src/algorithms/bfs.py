from collections import deque
from typing import Generator
import networkx as nx
from .base_algorithm import BaseAlgorithm
from src.models.graph_state import GraphState


class BFSAlgorithm(BaseAlgorithm):
    """Implementação do algoritmo de Busca em Largura (BFS)"""

    def traverse(self, graph: nx.Graph, start_node) -> Generator[GraphState, None, None]:
        """
        Executar travessia BFS e produzir estado a cada passo

        Args:
            graph: Grafo NetworkX para percorrer
            start_node: Nó inicial para travessia

        Yields:
            Objetos GraphState representando cada passo do BFS
        """
        if start_node not in graph.nodes():
            raise ValueError(f"Nó inicial '{start_node}' não encontrado no grafo")

        visited = set()
        queue = deque([start_node])
        visited_edges = []  # Rastrear arestas visitadas
        parent = {start_node: None}  # Rastrear pai de cada nó

        while queue:
            current = queue.popleft()

            if current not in visited:
                visited.add(current)

                # Obter nó anterior
                previous = parent[current]

                # Adicionar aresta às visitadas se houver nó anterior
                if previous is not None:
                    edge = tuple(sorted([previous, current], key=str))  # Aresta não direcionada
                    if edge not in visited_edges:
                        visited_edges.append(edge)

                # Produzir estado com informações da aresta
                yield GraphState(
                    visited=list(visited),
                    current=current,
                    queue_or_stack=list(queue),
                    graph=graph,
                    previous=previous,
                    visited_edges=list(visited_edges)
                )

                # Adicionar vizinhos não visitados à fila
                for neighbor in graph.neighbors(current):
                    if neighbor not in visited and neighbor not in queue:
                        queue.append(neighbor)
                        parent[neighbor] = current  # Rastrear pai
