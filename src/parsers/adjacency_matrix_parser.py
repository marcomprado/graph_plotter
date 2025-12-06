import pandas as pd
import networkx as nx
from .base_parser import BaseParser


class AdjacencyMatrixParser(BaseParser):
    """Parser para arquivos CSV no formato de matriz de adjacência"""

    def validate(self, df: pd.DataFrame) -> None:
        """Validar estrutura da matriz de adjacência"""
        super().validate(df)

        # Verificar se a matriz é quadrada
        num_rows = len(df)
        num_cols = len(df.columns)

        # A primeira coluna pode ser rótulos de nós, então verificar ambos os casos
        if num_cols != num_rows and num_cols != num_rows + 1:
            raise ValueError(
                f"Matriz de adjacência deve ser quadrada. Recebido {num_rows} linhas e {num_cols} colunas. "
                "A matriz deve ter rótulos de nós como índice de linha e cabeçalhos de coluna."
            )

    def parse(self, df: pd.DataFrame) -> nx.Graph:
        """
        Processar CSV de matriz de adjacência em grafo NetworkX

        Formato esperado:
        - Primeira linha: cabeçalhos de coluna (rótulos dos nós)
        - Primeira coluna: rótulos de linha (rótulos dos nós) - opcional
        - Células da matriz: 0 (sem aresta) ou valor numérico (peso da aresta)

        Exemplo:
        ,A,B,C
        A,0,1,0
        B,1,0,1
        C,0,1,0

        Exemplo com pesos:
        ,A,B,C
        A,0,2.5,0
        B,2.5,0,1.0
        C,0,1.0,0
        """
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

                        # Adicionar aresta se não-zero (valor da célula = peso)
                        if cell_value != 0:
                            # Para grafo não direcionado, adicionar aresta apenas uma vez (triângulo superior)
                            if i <= j:
                                G.add_edge(row_node, col_node, weight=cell_value)
                except (IndexError, KeyError):
                    continue

        if len(G.nodes()) == 0:
            raise ValueError("Nenhuma aresta válida encontrada na matriz de adjacência")

        return G
