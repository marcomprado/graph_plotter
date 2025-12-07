from abc import ABC, abstractmethod
import pandas as pd
import networkx as nx


class BaseParser(ABC):

    @abstractmethod
    def parse(self, df: pd.DataFrame) -> nx.Graph:
        pass

    def validate(self, df: pd.DataFrame) -> None:
        if df.empty:
            raise ValueError("Arquivo CSV está vazio")
