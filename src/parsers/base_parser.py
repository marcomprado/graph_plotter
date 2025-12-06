from abc import ABC, abstractmethod
import pandas as pd
import networkx as nx


class BaseParser(ABC):
    """Classe base abstrata para parsers de CSV"""

    @abstractmethod
    def parse(self, df: pd.DataFrame) -> nx.Graph:
        """Converter DataFrame para Grafo NetworkX"""
        pass

    def validate(self, df: pd.DataFrame) -> None:
        """Validar estrutura do DataFrame (sobrescrever em subclasses)"""
        if df.empty:
            raise ValueError("Arquivo CSV está vazio")
