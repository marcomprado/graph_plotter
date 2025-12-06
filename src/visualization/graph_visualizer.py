import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from src.models.graph_state import GraphState


class GraphVisualizer:
    """Gerencia renderização de grafos baseada em matplotlib com layout fixo"""

    def __init__(self):
        self.layout = None  # Cachear layout para consistência
        self.node_colors = {
            'unvisited': '#D3D3D3',   # Cinza claro
            'visited': '#87CEEB',     # Azul céu
            'current': '#FF4500'      # Vermelho alaranjado
        }
        self.edge_colors = {
            'unvisited': '#CCCCCC',   # Cinza claro
            'visited': '#87CEEB',     # Azul céu (combinando com nós visitados)
            'current': '#00FF00'      # Verde brilhante
        }

    def render(self, graph: nx.Graph, state: GraphState) -> Figure:
        """
        Renderizar grafo com cores de nós e arestas baseadas no estado

        Args:
            graph: Grafo NetworkX para renderizar
            state: Estado atual da travessia

        Returns:
            Objeto figura do Matplotlib
        """
        # Calcular layout uma vez e cachear
        if self.layout is None:
            self.layout = nx.spring_layout(graph, seed=42)

        # Mapear nós para cores baseado no estado
        node_colors = []
        for node in graph.nodes():
            if node == state.current:
                node_colors.append(self.node_colors['current'])
            elif node in state.visited:
                node_colors.append(self.node_colors['visited'])
            else:
                node_colors.append(self.node_colors['unvisited'])

        # Criar figura
        fig, ax = plt.subplots(figsize=(10, 9))

        # Mapear arestas para cores e espessuras baseado no estado
        edge_colors = []
        edge_widths = []

        for edge in graph.edges():
            edge_normalized = tuple(sorted(edge, key=str))  # Normalizar para grafo não direcionado

            # Verificar se esta é a aresta atual sendo percorrida
            if state.previous is not None:
                current_edge = tuple(sorted([state.previous, state.current], key=str))
                if edge_normalized == current_edge:
                    edge_colors.append(self.edge_colors['current'])  # Verde para aresta atual
                    edge_widths.append(4.0)  # Mais espessa
                    continue

            # Verificar se a aresta foi visitada
            if state.visited_edges and edge_normalized in [tuple(sorted(e, key=str)) for e in state.visited_edges]:
                edge_colors.append(self.edge_colors['visited'])  # Azul para arestas visitadas
                edge_widths.append(2.5)
            else:
                edge_colors.append(self.edge_colors['unvisited'])  # Cinza para arestas não visitadas
                edge_widths.append(1.5)

        # Desenhar arestas primeiro (para ficarem atrás dos nós)
        nx.draw_networkx_edges(
            graph,
            self.layout,
            edge_color=edge_colors,
            width=edge_widths,
            ax=ax
        )

        # Desenhar nós
        nx.draw_networkx_nodes(
            graph,
            self.layout,
            node_color=node_colors,
            node_size=700,
            ax=ax
        )

        # Desenhar rótulos de nós
        nx.draw_networkx_labels(
            graph,
            self.layout,
            font_size=12,
            font_weight='bold',
            ax=ax
        )

        # Desenhar labels de peso nas arestas
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        if edge_labels:
            # Formatar pesos: 2 casas decimais, ocultar peso=1
            edge_labels_formatted = {
                edge: f"{weight:.2f}" if weight != 1.0 else ""
                for edge, weight in edge_labels.items()
            }
            # Remover labels vazios (peso = 1)
            edge_labels_formatted = {k: v for k, v in edge_labels_formatted.items() if v}

            # Desenhar labels nas arestas
            if edge_labels_formatted:
                nx.draw_networkx_edge_labels(
                    graph,
                    self.layout,
                    edge_labels=edge_labels_formatted,
                    font_size=9,
                    font_color='red',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="red", alpha=0.8),
                    ax=ax
                )

        # Atualizar título para mostrar aresta atual
        if state.previous is not None:
            ax.set_title(
                f"Aresta Atual: {state.previous} → {state.current} | "
                f"Visitados: {len(state.visited)}/{len(graph.nodes())}"
            )
        else:
            ax.set_title(f"Nó Atual: {state.current} | Visitados: {len(state.visited)}/{len(graph.nodes())}")

        return fig

    def reset_layout(self):
        """Resetar layout cacheado (chamar quando novo grafo for carregado)"""
        self.layout = None
