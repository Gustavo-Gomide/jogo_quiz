# README - Jogo de Quiz em Python com SQLite

## 📌 Visão Geral
Um jogo de quiz interativo para terminal, desenvolvido em Python, que utiliza SQLite para armazenamento de dados. O jogo inclui:
- Sistema de cadastro de usuários
- Banco de questões com dicas
- Mecânica de pontuação baseada em acertos e vidas
- Ranking de jogadores
- Efeitos sonoros e música de fundo

## 🛠️ Tecnologias Utilizadas
- Python 3.x
- SQLite (banco de dados embutido)
- Biblioteca Pygame (para áudio)
- Biblioteca Tabulate (para exibição de tabelas formatadas)

## 🎮 Funcionalidades Principais

### 🗃️ Sistema de Banco de Dados
- **Tabela `quiz`**:
  - Armazena perguntas do jogo
  - Campos: resposta (obrigatória), tipo (obrigatório), dica1, dica2 (opcionais)
  
- **Tabela `usuario`**:
  - Armazena jogadores e seus recordes
  - Campos: nome (obrigatório), recorde (obrigatório)

### 🎲 Mecânicas de Jogo
- Sistema de vidas (5 vidas iniciais)
- Pontuação baseada em acertos e vidas restantes
- Dicas progressivas para cada pergunta
- Seleção aleatória de perguntas

### 🎵 Sistema de Áudio
- Música de fundo em loop
- Efeitos sonoros para:
  - Acertos/erros
  - Vitória/derrota
  - Ações do menu

## 🖥️ Como Executar

1. **Pré-requisitos**:
   - Python 3.x instalado
   - Bibliotecas: `pygame`, `tabulate`

2. **Instalação das dependências**:
   ```bash
   pip install pygame tabulate
   ```

3. **Execução**:
   ```bash
   python nome_do_arquivo.py
   ```

## 🗂️ Estrutura de Arquivos
O jogo espera encontrar os seguintes arquivos de áudio na pasta `musicas`:
```
musicas/
├── fundo/
│   └── Galactic_Rap.mp3 (música de fundo)
└── efeitos/
    ├── correto.wav
    ├── incorreto.wav
    ├── venceu.wav
    ├── perdeu.wav
    └── sair.wav
```

## 🎨 Interface
- Menu interativo com opções numeradas
- Tabelas formatadas para exibição de dados
- Cores diferenciadas para diferentes tipos de informação
- Design ASCII personalizado para cabeçalhos

## ⚙️ Funções Principais
- `main()`: Menu principal do jogo
- `jogar()`: Lógica principal do jogo
- `placar()`: Exibe ranking de jogadores
- `adicionar_quiz()`: Adiciona novas perguntas
- `cadastrar()`: Cadastra novos jogadores

## 🔊 Controles de Áudio
- Música de fundo toca automaticamente
- Volume ajustável nas funções de áudio
- Efeitos sonoros são reproduzidos em canal separado

## 🚀 Melhorias Futuras
- Adicionar mais categorias de perguntas
- Implementar dificuldades variáveis
- Adicionar sistema de temas/skins
- Desenvolver interface gráfica

## 📝 Notas
- O banco de dados (`jogo_quiz.db`) é criado automaticamente na primeira execução
- Todos os dados são persistidos entre sessões
- O jogo foi projetado para funcionar tanto em Windows quanto em Linux/Mac

Divirta-se jogando! 🎮
