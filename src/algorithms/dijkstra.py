import heapq
from typing import Generator
import networkx as nx
from .base_algorithm import BaseAlgorithm
from src.models.graph_state import GraphState


class DijkstraAlgorithm(BaseAlgorithm):
    # Implementação do algoritmo de Dijkstra para caminho mínimo

    def traverse(self, graph: nx.Graph, start_node) -> Generator[GraphState, None, None]:

        if start_node not in graph.nodes():
            raise ValueError(f"Nó inicial '{start_node}' não encontrado no grafo")

        # Estruturas de dados do Dijkstra
        distances = {node: float('inf') for node in graph.nodes()}
        distances[start_node] = 0
        previous = {start_node: None}

        visited_set = set()  # Para verificação O(1)
        visited_order = []   # Para manter ordem cronológica
        visited_edges = []

        # Fila de prioridade: (distância, nó)
        pq = [(0, start_node)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            # Pular se já visitado
            if current in visited_set:
                continue

            visited_set.add(current)
            visited_order.append(current)  # Adicionar na lista (ordem garantida)

            # Adicionar aresta visitada
            if previous.get(current) is not None:
                edge = tuple(sorted([previous[current], current], key=str))
                if edge not in visited_edges:
                    visited_edges.append(edge)

            # Criar estrutura de dados para exibição da fila
            queue_display = [node for _, node in sorted(pq)]

            # Yield estado atual
            yield GraphState(
                visited=list(visited_order),  # Usar lista ordenada
                current=current,
                queue_or_stack=queue_display,
                graph=graph,
                previous=previous.get(current),
                visited_edges=list(visited_edges)
            )

            # Relaxar arestas dos vizinhos
            for neighbor in graph.neighbors(current):
                if neighbor not in visited_set:
                    # Obter peso da aresta
                    weight = graph[current][neighbor].get('weight', 1.0)
                    new_dist = current_dist + weight

                    # Atualizar distância se for menor
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        previous[neighbor] = current
                        heapq.heappush(pq, (new_dist, neighbor))
