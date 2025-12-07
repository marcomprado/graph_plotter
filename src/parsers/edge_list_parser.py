import pandas as pd
import networkx as nx
from .base_parser import BaseParser


class EdgeListParser(BaseParser):

    def validate(self, df: pd.DataFrame) -> None:
        super().validate(df)
        if len(df.columns) < 2:
            raise ValueError("Lista de arestas deve ter pelo menos 2 colunas (origem, destino)")

    def parse(self, df: pd.DataFrame) -> nx.Graph:
        self.validate(df)

        G = nx.Graph()

        source_col = df.columns[0]
        target_col = df.columns[1]

        has_weight = len(df.columns) >= 3
        weight_col = df.columns[2] if has_weight else None

        for _, row in df.iterrows():
            source = row[source_col]
            target = row[target_col]

            if pd.notna(source) and pd.notna(target):
                if has_weight:
                    weight = row[weight_col]
                    try:
                        weight = float(weight) if pd.notna(weight) else 1.0
                    except (ValueError, TypeError):
                        weight = 1.0
                else:
                    weight = 1.0

                G.add_edge(source, target, weight=weight)

        if len(G.nodes()) == 0:
            raise ValueError("Nenhuma aresta válida encontrada no arquivo CSV")

        return G
