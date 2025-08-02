# 🐦 Flappy Bird IA com Dificuldade Progressiva

Um projeto de **Inteligência Artificial** que treina uma IA para jogar Flappy Bird usando **algoritmos genéticos (NEAT)** com um sistema inovador de **dificuldade progressiva adaptativa**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![NEAT](https://img.shields.io/badge/NEAT--Python-Latest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Sobre o Projeto

Este projeto foi **inspirado no canal [Hashtag Programação](https://www.youtube.com/@HashtagProgramacao)** e expandido com funcionalidades avançadas de progressão de dificuldade adaptativa.

A IA utiliza **redes neurais evolutivas (NEAT)** para aprender a jogar Flappy Bird, mas com um twist: **a dificuldade aumenta progressivamente** conforme a IA vai dominando cada fase, criando um desafio cada vez maior.

### ✨ Principais Características

- 🧠 **IA Evolutiva**: Algoritmo NEAT para treinamento automático
- 📈 **Dificuldade Progressiva**: 6 fases de dificuldade que se acumulam
- 🎮 **Modo Manual**: Você também pode jogar!
- ⚡ **Aceleração de Treino**: Tecla 'A' para acelerar visualização
- 🔄 **Sistema Adaptativo**: IA só avança após dominar cada fase
- 🎯 **Limite por Geração**: Máximo de 40 pontos por geração

## 🎮 Fases de Dificuldade

O jogo possui **6 fases progressivas** que testam diferentes habilidades da IA:

### 🟢 Fase 1: Normal
- Jogo Flappy Bird tradicional
- IA aprende mecânicas básicas

### 🟡 Fase 2: Movimento Vertical
- Canos se movem verticalmente
- 100% dos canos têm movimento

### 🟠 Fase 3: Velocidade + Movimento
- Velocidade aumentada (1.5x)
- 65% dos canos se movem (aleatório)

### 🔴 Fase 4: Espaço Reduzido + Mix
- Espaço entre canos reduzido (160px → 120px)
- Mix aleatório das fases anteriores
- 50% chance movimento vertical
- 65% chance velocidade aumentada

### 🟣 Fase 5: Obstáculos Falsos + Mix
- Canos "fantasma" semi-transparentes
- 30% chance de obstáculos falsos
- Mix de todas as dificuldades anteriores

### ⚫ Fase 6: Canos Invisíveis + Mix Completo
- Canos completamente invisíveis
- IA navega apenas pelos sensores
- Todas as dificuldades anteriores combinadas

## 🔧 Sistema Adaptativo

A IA precisa **dominar cada fase** antes de avançar:

- ✅ **Sucesso**: Atingir 40 pontos = +1 sucesso
- ❌ **Falha**: Menos de 40 pontos = zera contador
- 🎯 **Avanço**: Precisa de **3 sucessos consecutivos**
- 🔄 **Extensão**: Fases podem durar quantas gerações precisar

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado em seu sistema.

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/flappy-bird-ia.git
cd flappy-bird-ia
```

### 2. Instale as Dependências
```bash
pip install pygame neat-python
```

### 3. Estrutura de Arquivos
Certifique-se de ter a seguinte estrutura:
```
flappy-bird-ia/
├── main.py
├── configIA.txt
├── imgs/
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png
│   ├── base.png
│   └── bg.png
└── README.md
```

### 4. Execute o Jogo
```bash
python main.py
```

## 🎮 Como Usar

### Menu Principal
Ao executar, você verá duas opções:
- **1**: Jogar manualmente (você controla o pássaro)
- **2**: IA jogando (treino automático)

### Controles

#### Modo Manual:
- `ESPAÇO`: Fazer o pássaro pular

#### Modo IA:
- `A`: Alternar aceleração (4x mais rápido)
- Apenas observe a IA aprender!

### Interface Durante o Treino
- **Geração**: Número da geração atual
- **Fase**: Fase atual e nome da dificuldade
- **Progresso**: Quantas gerações na fase e sucessos consecutivos
- **Pontuação**: Pontos da geração atual

## 📦 Dependências

### Bibliotecas Python
- **pygame**: Interface gráfica e mecânicas do jogo
- **neat-python**: Algoritmo de redes neurais evolutivas
- **random**: Geração de números aleatórios
- **os**: Manipulação de arquivos e caminhos
- **math**: Operações matemáticas

### Arquivo de Configuração (configIA.txt)
Contém todos os parâmetros do algoritmo NEAT:
- Tamanho da população: 100 indivíduos
- Inputs: 3 (posição Y, distância topo, distância base)
- Outputs: 1 (pular ou não pular)
- Função de ativação: tanh

## 🧠 Como a IA Funciona

### Algoritmo NEAT
1. **População**: 100 redes neurais aleatórias
2. **Avaliação**: Cada rede joga e recebe fitness baseado na performance
3. **Seleção**: Melhores redes sobrevivem
4. **Reprodução**: Redes geram offspring com mutações
5. **Evolução**: Processo se repete até dominar o jogo

### Inputs da IA
A IA recebe 3 informações:
- Posição Y do pássaro
- Distância do pássaro ao topo do próximo cano
- Distância do pássaro à base do próximo cano

### Sistema de Fitness
- **+0.1**: Por frame sobrevivido
- **+5**: Por cano passado
- **-1**: Por colisão

## 📊 Resultados Esperados

### Progressão Típica:
- **Fase 1**: 5-15 gerações (aprendizado básico)
- **Fase 2**: 10-25 gerações (adaptação ao movimento)
- **Fase 3**: 15-30 gerações (velocidade + coordenação)
- **Fase 4**: 20-40 gerações (precisão com espaço reduzido)
- **Fase 5**: 25-50 gerações (distinguir obstáculos falsos)
- **Fase 6**: 30-100+ gerações (navegação sem visual)

## 🛠️ Personalização

### Modificar Dificuldades
Edite a função `obter_configuracao_dificuldade()` para:
- Alterar porcentagens de cada característica
- Criar novas fases
- Modificar critérios de sucesso

### Ajustar Parâmetros NEAT
Modifique `configIA.txt` para:
- Alterar tamanho da população
- Mudar taxas de mutação
- Ajustar topologia da rede

### Limites e Performance
- Modifique o limite de pontos por geração
- Ajuste velocidade de aceleração
- Customize critérios de avanço de fase

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Créditos

- **Inspiração Original**: [Hashtag Programação](https://www.youtube.com/@HashtagProgramacao)
- **Algoritmo NEAT**: [NEAT-Python](https://neat-python.readthedocs.io/)
- **Engine de Jogo**: [Pygame](https://www.pygame.org/)

## 📞 Contato

Se você tiver dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou entrar em contato!

---

**Divirta-se assistindo a IA evoluir e dominar o Flappy Bird! 🚀🐦**