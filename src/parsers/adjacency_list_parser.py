import pandas as pd
import networkx as nx
from .base_parser import BaseParser


class AdjacencyListParser(BaseParser):
    """Parser para arquivos CSV no formato de lista de adjacência"""

    def validate(self, df: pd.DataFrame) -> None:
        """Validar estrutura da lista de adjacência"""
        super().validate(df)
        if len(df.columns) < 1:
            raise ValueError("Lista de adjacência deve ter pelo menos 1 coluna (identificador do nó)")

    def parse(self, df: pd.DataFrame) -> nx.Graph:
        """
        Processar CSV de lista de adjacência em grafo NetworkX

        Formato esperado:
        - Coluna 0: identificador do nó
        - Colunas 1+: nós vizinhos (pode ter número variável de colunas)
        - Células vazias são ignoradas

        Exemplo:
        nó,vizinho1,vizinho2,vizinho3
        A,B,D,
        B,A,C,
        C,B,D,
        D,A,C,
        """
        self.validate(df)

        G = nx.Graph()

        node_col = df.columns[0]

        for _, row in df.iterrows():
            node = row[node_col]

            if pd.notna(node):
                # Adicionar nó mesmo que não tenha vizinhos
                G.add_node(node)

                # Processar todas as colunas de vizinhos
                for col in df.columns[1:]:
                    neighbor = row[col]

                    # Adicionar aresta se vizinho não estiver vazio
                    if pd.notna(neighbor) and neighbor != '':
                        # Converter para string e remover espaços
                        neighbor = str(neighbor).strip()
                        if neighbor:
                            G.add_edge(node, neighbor)

        if len(G.nodes()) == 0:
            raise ValueError("Nenhum nó válido encontrado na lista de adjacência")

        return G
