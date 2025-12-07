import pandas as pd
import networkx as nx
from .base_parser import BaseParser


class AdjacencyListParser(BaseParser):

    def validate(self, df: pd.DataFrame) -> None:
        super().validate(df)
        if len(df.columns) < 1:
            raise ValueError("Lista de adjacência deve ter pelo menos 1 coluna (identificador do nó)")

    def parse(self, df: pd.DataFrame) -> nx.Graph:
        self.validate(df)

        G = nx.Graph()

        node_col = df.columns[0]

        neighbor_cols = df.columns[1:]
        has_weights = (len(neighbor_cols) % 2 == 0) and len(neighbor_cols) > 0

        for _, row in df.iterrows():
            node = row[node_col]

            if pd.notna(node):
                G.add_node(node)

                if has_weights:
                    # Formato com pesos: vizinho1,peso1,vizinho2,peso2,...
                    for i in range(0, len(neighbor_cols), 2):
                        neighbor_col = neighbor_cols[i]
                        weight_col = neighbor_cols[i + 1] if i + 1 < len(neighbor_cols) else None

                        neighbor = row[neighbor_col]

                        if pd.notna(neighbor) and neighbor != '':
                            neighbor = str(neighbor).strip()

                            if weight_col:
                                weight = row[weight_col]
                                try:
                                    weight = float(weight) if pd.notna(weight) else 1.0
                                except (ValueError, TypeError):
                                    weight = 1.0
                            else:
                                weight = 1.0

                            if neighbor:
                                G.add_edge(node, neighbor, weight=weight)
                else:
                    # Formato SEM pesos
                    for col in neighbor_cols:
                        neighbor = row[col]

                        if pd.notna(neighbor) and neighbor != '':
                            neighbor = str(neighbor).strip()
                            if neighbor:
                                G.add_edge(node, neighbor, weight=1.0)

        if len(G.nodes()) == 0:
            raise ValueError("Nenhum nó válido encontrado na lista de adjacência")

        return G
