from typing import Generator
import networkx as nx
from .base_algorithm import BaseAlgorithm
from src.models.graph_state import GraphState


class DFSAlgorithm(BaseAlgorithm):
    """Implementação do algoritmo de Busca em Profundidade (DFS)"""

    def traverse(self, graph: nx.Graph, start_node) -> Generator[GraphState, None, None]:
        """
        Executar travessia DFS e produzir estado a cada passo

        Args:
            graph: Grafo NetworkX para percorrer
            start_node: Nó inicial para travessia

        Yields:
            Objetos GraphState representando cada passo do DFS
        """
        if start_node not in graph.nodes():
            raise ValueError(f"Nó inicial '{start_node}' não encontrado no grafo")

        visited = set()
        stack = [start_node]
        visited_edges = []  # Rastrear arestas visitadas
        parent = {start_node: None}  # Rastrear pai de cada nó

        while stack:
            current = stack.pop()

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
                    queue_or_stack=list(stack),
                    graph=graph,
                    previous=previous,
                    visited_edges=list(visited_edges)
                )

                # Adicionar vizinhos não visitados à pilha (em ordem reversa para travessia consistente)
                neighbors = list(graph.neighbors(current))
                for neighbor in reversed(neighbors):
                    if neighbor not in visited and neighbor not in stack:
                        stack.append(neighbor)
                        parent[neighbor] = current  # Rastrear pai
