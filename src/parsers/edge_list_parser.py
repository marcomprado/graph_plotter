import pandas as pd
import networkx as nx
from .base_parser import BaseParser


class EdgeListParser(BaseParser):
    """Parser para arquivos CSV no formato de lista de arestas"""

    def validate(self, df: pd.DataFrame) -> None:
        """Validar estrutura da lista de arestas"""
        super().validate(df)
        if len(df.columns) < 2:
            raise ValueError("Lista de arestas deve ter pelo menos 2 colunas (origem, destino)")

    def parse(self, df: pd.DataFrame) -> nx.Graph:
        """
        Processar CSV de lista de arestas em grafo NetworkX

        Formato esperado:
        - Coluna 0: nó de origem
        - Coluna 1: nó de destino
        - Colunas adicionais são ignoradas
        """
        self.validate(df)

        G = nx.Graph()

        # Usar as duas primeiras colunas independentemente dos nomes dos cabeçalhos
        source_col = df.columns[0]
        target_col = df.columns[1]

        for _, row in df.iterrows():
            source = row[source_col]
            target = row[target_col]

            # Pular linhas com valores ausentes
            if pd.notna(source) and pd.notna(target):
                G.add_edge(source, target)

        if len(G.nodes()) == 0:
            raise ValueError("Nenhuma aresta válida encontrada no arquivo CSV")

        return G
