import heapq
from typing import Generator
import networkx as nx
from .base_algorithm import BaseAlgorithm
from src.models.graph_state import GraphState


class PrimMSTAlgorithm(BaseAlgorithm):
    # Implementação do algoritmo de Prim para Árvore Geradora Mínima (MST)

    def traverse(self, graph: nx.Graph, start_node) -> Generator[GraphState, None, None]:
        
        if start_node not in graph.nodes():
            raise ValueError(f"Nó inicial '{start_node}' não encontrado no grafo")

        # Estruturas do Prim
        visited = set()
        visited_edges = []  # Arestas da MST
        parent = {start_node: None}

        # Fila de prioridade: (peso, nó_destino, nó_origem)
        pq = [(0, start_node, None)]

        while pq and len(visited) < len(graph.nodes()):
            weight, current, prev = heapq.heappop(pq)

            # Pular se já visitado
            if current in visited:
                continue

            visited.add(current)

            # Adicionar aresta à MST (exceto primeiro nó)
            if prev is not None:
                edge = tuple(sorted([prev, current], key=str))
                if edge not in visited_edges:
                    visited_edges.append(edge)
                    parent[current] = prev

            # Criar display da fila
            queue_display = [node for _, node, _ in sorted(pq)]

            # Yield estado
            yield GraphState(
                visited=list(visited),
                current=current,
                queue_or_stack=queue_display,
                graph=graph,
                previous=prev,
                visited_edges=list(visited_edges)
            )

            # Adicionar arestas dos vizinhos não visitados
            for neighbor in graph.neighbors(current):
                if neighbor not in visited:
                    edge_weight = graph[current][neighbor].get('weight', 1.0)
                    heapq.heappush(pq, (edge_weight, neighbor, current))
