# Graph Plotter

## 📖 Sobre o Projeto

**Graph Plotter** é um visualizador educacional interativo de algoritmos de grafos. O projeto permite carregar grafos em diferentes formatos CSV e observar, em tempo real, como algoritmos clássicos exploram e processam a estrutura do grafo através de animações passo a passo.

---

## 🛠️ Como Funciona

### Algoritmos Implementados

O projeto oferece **4 algoritmos fundamentais** de grafos:

1. **BFS (Busca em Largura)** - Explora o grafo nível por nível
2. **DFS (Busca em Profundidade)** - Explora em profundidade ao longo dos ramos
3. **Dijkstra** - Encontra caminhos de custo mínimo em grafos ponderados
4. **MST (Prim)** - Constrói a Árvore Geradora Mínima

### Formatos de Entrada

Suporta **3 formatos CSV** diferentes:

- **Lista de Arestas** - `origem,destino,peso`
- **Matriz de Adjacência** - Matriz quadrada com valores como pesos
- **Lista de Adjacência** - `nó,vizinho1,peso1,vizinho2,peso2,...`

Exemplos de arquivos estão disponíveis em `/examples/`.

### Bibliotecas Utilizadas

| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| **Streamlit** | 1.29.0 | Interface web interativa |
| **NetworkX** | 3.2.1 | Manipulação de grafos |
| **Matplotlib** | 3.8.2 | Visualização gráfica |
| **Pandas** | 2.1.4 | Processamento de CSV |
| **Watchdog** | 6.0.0 | Auto-reload durante desenvolvimento |

### Componentes Principais

```
src/
├── algorithms/      # BFS, DFS, Dijkstra, MST (Prim)
├── parsers/         # EdgeList, AdjacencyMatrix, AdjacencyList
├── models/          # GraphState (estado da travessia)
└── visualization/   # GraphVisualizer (renderização)
```

### Como Executar

#### 1. Verificar se Python está instalado

Antes de começar, verifique se você tem Python instalado:

```bash
python --version
```
ou (se o sistema for mac ou linux)
```bash
python3 --version 
```

Se o comando retornar uma versão (ex: `Python 3.9.0` ou superior), pule para a etapa 3.

#### 2. Instalar Python (se necessário)

**Windows:**
1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Baixe o instalador mais recente do Python 3
3. Execute o instalador
4. **IMPORTANTE:** Marque a opção "Add Python to PATH" durante a instalação
5. Clique em "Install Now"

**macOS:**
- **Opção 1 - Site oficial:**
  1. Acesse [python.org/downloads](https://www.python.org/downloads/)
  2. Baixe e execute o instalador para macOS

- **Opção 2 - Homebrew (recomendado):**
  ```bash
  brew install python
  ```

**Linux:**
- **Ubuntu/Debian:**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

#### 3. Verificar instalação do Python e pip

Após instalar, confirme que Python e pip estão funcionando: (Se `python` não funcionar, tente `python3` e `pip3`.)

```bash
python --version
pip --version
```

#### 4. Instalar dependências do projeto

No diretório do projeto, execute:

```bash
pip install -r requirements.txt
```

#### 5. Executar a aplicação

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

#### 6. Usar a interface

- Selecione o formato do grafo
- Carregue um arquivo CSV (ou use os exemplos em `/examples/`)
- Escolha o algoritmo
- Ajuste a velocidade da animação
- Clique 2 vezes em "Carregar e Executar"
- Selecione o nó inicial e inicie a animação

---

## 🎯 Features

- ✅ Visualização animada em tempo real
- ✅ Suporte a grafos ponderados
- ✅ 3 formatos de entrada diferentes
- ✅ 4 algoritmos clássicos
- ✅ Estatísticas detalhadas (nós visitados, custo total, etc.)
- ✅ Detecção de grafos desconectados
- ✅ Controle de velocidade de animação

---

## 📁 Estrutura do Projeto

```
graph_plotter/
├── app.py                  # Ponto de entrada (Streamlit)
├── requirements.txt        # Dependências
├── src/
│   ├── algorithms/        # Implementação dos algoritmos
│   ├── parsers/           # Parsers para CSV
│   ├── models/            # GraphState
│   └── visualization/     # GraphVisualizer
└── examples/              # Arquivos CSV de exemplo
```

---

## 🚀 Exemplo de Uso

```python
# O projeto é executado via Streamlit, não requer código Python direto
# Toda interação é feita pela interface web
```

1. Carregue `examples/lista_de_arestas_ponderada.csv`
2. Selecione algoritmo **Dijkstra**
3. Observe o caminho de menor custo sendo construído
4. Veja estatísticas: custo total, arestas percorridas, etc.

---

## 📊 Informações Exibidas

Após cada execução, o projeto mostra:

- **Ordem de travessia** - Sequência de nós visitados
- **Nós visitados** - Total e percentual de cobertura
- **Arestas percorridas** - Número de arestas usadas
- **Custo total** - Soma dos pesos (Dijkstra/MST)
- **Detalhes das arestas** - Lista expansível com pesos
- **Alerta de desconexão** - Nós não alcançáveis

---

## 🎓 Propósito Educacional

Trabalho desenvolvido para a disciplina de **Algoritmos em Grafos** do **4º período** do curso de **Sistemas de Informação** da **PUC Minas - Betim**.

### Alunos:
- Marco Martinelli
- Vitor Lucas Resende
- João Mateus Gomes
- Stefano Gennaro

---

## 📝 Licença

Projeto desenvolvido para fins educacionais.
