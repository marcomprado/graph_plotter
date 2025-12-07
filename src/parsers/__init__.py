from .edge_list_parser import EdgeListParser
from .adjacency_matrix_parser import AdjacencyMatrixParser
from .adjacency_list_parser import AdjacencyListParser


class ParserFactory:

    @staticmethod
    def create_parser(format_type: str):

        format_mapping = {
            "Lista de Arestas": "Edge List",
            "Matriz de Adjacência": "Adjacency Matrix",
            "Lista de Adjacência": "Adjacency List"
        }

        format_key = format_mapping.get(format_type, format_type)

        parsers = {
            "Edge List": EdgeListParser(),
            "Adjacency Matrix": AdjacencyMatrixParser(),
            "Adjacency List": AdjacencyListParser()
        }
        if format_key not in parsers:
            raise ValueError(f"Formato desconhecido: {format_type}")
        return parsers[format_key]


__all__ = ['ParserFactory', 'EdgeListParser', 'AdjacencyMatrixParser', 'AdjacencyListParser']
