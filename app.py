import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import networkx as nx
from src.parsers import ParserFactory
from src.algorithms import AlgorithmFactory
from src.visualization.graph_visualizer import GraphVisualizer


def main():
    st.set_page_config(page_title="Visualizador de Algoritmos de Grafos", layout="wide")
    st.title("Visualizador Educacional de Algoritmos de Grafos")

    # Inicializar visualizador no estado da sessão
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = GraphVisualizer()

    # Inicializar variáveis de estado da sessão relacionadas ao grafo
    if 'graph_loaded' not in st.session_state:
        st.session_state.graph_loaded = False
    if 'graph' not in st.session_state:
        st.session_state.graph = None
    if 'algorithm_type' not in st.session_state:
        st.session_state.algorithm_type = None

    # Entradas da barra lateral
    with st.sidebar:
        st.header("Configuração")

        # Passo 1: Seleção de formato
        format_type = st.selectbox(
            "Formato do Grafo",
            ["Lista de Arestas", "Matriz de Adjacência", "Lista de Adjacência"],
            help="Selecione o formato do seu arquivo CSV"
        )

        # Passo 2: Upload de arquivo
        uploaded_file = st.file_uploader(
            "Carregar Arquivo CSV",
            type=['csv'],
            help="Carregue um arquivo CSV no formato selecionado"
        )

        # Passo 3: Seleção de algoritmo
        algorithm_type = st.selectbox(
            "Algoritmo",
            ["BFS", "DFS", "Dijkstra", "MST (Prim)"],
            help="Escolha o algoritmo de travessia para visualizar"
        )

        # Passo 4: Controle de velocidade
        speed = st.slider(
            "Velocidade da Animação",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = mais lento, 10 = mais rápido"
        )
        sleep_duration = (11 - speed) * 0.1  # Converter para segundos

        # Passo 5: Botão executar
        execute = st.button("Carregar e Executar (Clique duas vezes)", type="primary")

    # Área de conteúdo principal - Instruções (mostrar apenas quando nenhum grafo estiver carregado)
    if not st.session_state.graph_loaded:
        st.markdown("""
        ## Como Usar Esta Aplicação

        ### Passo 1: Selecionar Formato do Grafo
        Escolha o formato do seu arquivo CSV na barra lateral:
        - **Lista de Arestas**: Duas colunas (origem, destino)
        - **Matriz de Adjacência**: Matriz quadrada com rótulos dos nós
        - **Lista de Adjacência**: Primeira coluna é o nó, colunas restantes são vizinhos

        ### Passo 2: Carregar Arquivo CSV
        Carregue seus dados de grafo em formato CSV correspondente ao formato selecionado.
        Use o scroll para rolar ate o fim da pagina.

        ### Passo 3: Escolher Algoritmo
        - **BFS (Busca em Largura)**: Explora nível por nível
        - **DFS (Busca em Profundidade)**: Explora em profundidade ao longo dos ramos

        ### Passo 4: Ajustar Velocidade
        Use o controle deslizante para controlar a velocidade da animação (1 = lento, 10 = rápido).

        ### Passo 5: Clicar em "Carregar e Executar"
        Assista o algoritmo percorrer seu grafo em tempo real!

        ---

        ### Exemplos de Formato CSV

        **Lista de Arestas (sem pesos):**
        ```
        origem,destino
        A,B
        B,C
        C,D
        ```

        **Lista de Arestas (com pesos):**
        ```
        origem,destino,peso
        A,B,2.5
        B,C,1.0
        C,D,3.7
        ```

        **Matriz de Adjacência (sem pesos):**
        ```
        ,A,B,C,D
        A,0,1,0,1
        B,1,0,1,0
        C,0,1,0,1
        D,1,0,1,0
        ```

        **Matriz de Adjacência (com pesos):**
        ```
        ,A,B,C
        A,0,2.5,0
        B,2.5,0,1.0
        C,0,1.0,0
        ```

        **Lista de Adjacência (sem pesos):**
        ```
        nó,vizinho1,vizinho2
        A,B,D
        B,A,C
        C,B,D
        D,A,C
        ```

        **Lista de Adjacência (com pesos):**
        ```
        nó,vizinho1,peso1,vizinho2,peso2
        A,B,2.5,D,1.0
        B,A,2.5,C,3.0
        C,B,3.0,D,1.5
        D,A,1.0,C,1.5
        ```
        """)

    # Lógica principal de execução - Carregar grafo
    if execute:
        if uploaded_file is None:
            st.error("Por favor, carregue um arquivo CSV")
        else:
            try:
                # Processar CSV
                df = pd.read_csv(uploaded_file)

                # Mostrar dados carregados
                with st.expander("Ver Dados Carregados"):
                    st.dataframe(df)

                # Processar grafo
                parser = ParserFactory.create_parser(format_type)
                graph = parser.parse(df)

                # Resetar layout do visualizador para novo grafo
                st.session_state.visualizer.reset_layout()

                # Armazenar no estado da sessão
                st.session_state.graph = graph
                st.session_state.algorithm_type = algorithm_type
                st.session_state.graph_loaded = True

                st.success(f"Grafo carregado: {len(graph.nodes())} nós, {len(graph.edges())} arestas")

                # Verificar se grafo é ponderado
                edge_weights = nx.get_edge_attributes(graph, 'weight')
                if edge_weights:
                    weights = list(edge_weights.values())
                    all_ones = all(w == 1.0 for w in weights)
                    if not all_ones:
                        st.info(f"Grafo PONDERADO detectado. Pesos: {min(weights):.2f} a {max(weights):.2f}")
                    else:
                        st.info("Grafo NÃO ponderado (todos os pesos = 1)")

            except ValueError as e:
                st.error(f"Erro ao processar CSV: {str(e)}")
                st.info("Por favor, verifique se o formato do CSV corresponde ao tipo de formato selecionado.")
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")
                with st.expander("Mostrar Detalhes do Erro"):
                    st.exception(e)

    # Mostrar controles de animação se o grafo estiver carregado
    if st.session_state.graph_loaded and st.session_state.graph is not None:
        graph = st.session_state.graph

        st.info(f"Grafo carregado: {len(graph.nodes())} nós, {len(graph.edges())} arestas")

        # Selecionar nó inicial
        nodes = list(graph.nodes())
        if not nodes:
            st.error("O grafo não possui nós")
        else:
            start_node = st.selectbox("Selecione o Nó Inicial", nodes)

            # Botão Iniciar Animação
            if st.button("Iniciar Animação", type="primary"):
                # Loop de animação
                st.subheader(f"Executando {st.session_state.algorithm_type} a partir do nó {start_node}")
                animation_placeholder = st.empty()

                # Criar instância do algoritmo
                algorithm = AlgorithmFactory.create_algorithm(st.session_state.algorithm_type)

                # Criar barra de progresso
                progress_bar = st.progress(0)
                status_text = st.empty()

                total_nodes = len(graph.nodes())
                step = 0

                for state in algorithm.traverse(graph, start_node):
                    step += 1

                    # Atualizar status
                    status_text.text(f"Passo {step}: Visitando nó {state.current}")

                    # Renderizar estado atual
                    fig = st.session_state.visualizer.render(graph, state)
                    animation_placeholder.pyplot(fig)

                    # Atualizar progresso
                    progress = len(state.visited) / total_nodes
                    progress_bar.progress(progress)

                    # Controlar velocidade
                    time.sleep(sleep_duration)

                    # Limpar figura matplotlib
                    plt.close(fig)

                # Completar
                progress_bar.progress(1.0)
                status_text.text("")
                st.success(f"Travessia completa! Visitados {len(state.visited)} de {total_nodes} nós.")

                # Mostrar ordem de travessia
                st.write("**Ordem de Travessia:**", " → ".join(map(str, state.visited)))


if __name__ == "__main__":
    main()
