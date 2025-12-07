import pandas as pd
import networkx as nx
from .base_parser import BaseParser


class AdjacencyMatrixParser(BaseParser):

    def validate(self, df: pd.DataFrame) -> None:
        super().validate(df)

        num_rows = len(df)
        num_cols = len(df.columns)

        if num_cols != num_rows and num_cols != num_rows + 1:
            raise ValueError(
                f"Matriz de adjacência deve ser quadrada. Recebido {num_rows} linhas e {num_cols} colunas. "
                "A matriz deve ter rótulos de nós como índice de linha e cabeçalhos de coluna."
            )

    def parse(self, df: pd.DataFrame) -> nx.Graph:

        self.validate(df)

        G = nx.Graph()

        # Verificar se a primeira coluna parece conter rótulos de linha
        first_col = df.columns[0]
        has_row_labels = (
            df[first_col].dtype == 'object' or
            str(first_col).startswith('Unnamed')
        )

        if has_row_labels:
            # Usar primeira coluna como rótulos de linha
            row_labels = df.iloc[:, 0].tolist()
            col_labels = df.columns[1:].tolist()
            matrix_data = df.iloc[:, 1:]
        else:
            # Usar cabeçalhos de coluna como rótulos de linha e coluna
            row_labels = df.columns.tolist()
            col_labels = df.columns.tolist()
            matrix_data = df

        # Validar matriz quadrada após extrair rótulos
        if len(row_labels) != len(col_labels):
            raise ValueError(
                f"Matriz deve ser quadrada. Recebido {len(row_labels)} rótulos de linha "
                f"e {len(col_labels)} rótulos de coluna"
            )

        # Criar arestas a partir da matriz
        for i, row_node in enumerate(row_labels):
            for j, col_node in enumerate(col_labels):
                try:
                    cell_value = matrix_data.iloc[i, j]

                    # Converter para numérico se possível
                    if pd.notna(cell_value):
                        try:
                            cell_value = float(cell_value)
                        except (ValueError, TypeError):
                            cell_value = 0

                        # Adicionar aresta se não-zero
                        if cell_value != 0:
                            # Para grafo não direcionado
                            if i <= j:
                                G.add_edge(row_node, col_node, weight=cell_value)
                except (IndexError, KeyError):
                    continue

        if len(G.nodes()) == 0:
            raise ValueError("Nenhuma aresta válida encontrada na matriz de adjacência")

        return G
