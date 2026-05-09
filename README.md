# Analisador de Dicionário Python

Analisador léxico e sintático para declarações de dicionário da linguagem Python, desenvolvido como trabalho prático da disciplina de Compiladores.

## Descrição

O programa lê um arquivo `.txt` contendo declarações de dicionário Python e as valida em três fases:

1. **Análise Léxica** — transforma o código em tokens
2. **Análise Sintática** — verifica se a estrutura está correta (estratégia Top-Down / Descendente Recursivo)
3. **Análise Semântica** — detecta variáveis redeclaradas e chaves duplicadas

O analisador para imediatamente ao encontrar o primeiro erro, indicando a linha, a coluna e apontando o problema com uma seta.

---

## Gramática reconhecida

```
programa   -> declaracao* EOF
declaracao -> VARIAVEL '=' dicionario
dicionario -> '{' pares '}'
pares      -> par (',' par)* | vazio
par        -> STRING ':' valor
valor      -> STRING | INTEIRO | REAL | BOOLEANO | NULO
```

### Tokens reconhecidos

| Token    | Descrição                                       | Exemplo              |
|----------|-------------------------------------------------|----------------------|
| VARIAVEL | Letra ou `_` seguido de letras, dígitos ou `_`  | `dicio`, `_config`   |
| STRING   | Texto entre aspas simples ou duplas             | `'nome'`, `"valor"`  |
| INTEIRO  | Sequência de dígitos, positivo ou negativo      | `42`, `-5`           |
| REAL     | Dígitos com ponto decimal, positivo ou negativo | `3.14`, `-2.5`       |
| BOOLEANO | Valor lógico                                    | `True`, `False`      |
| NULO     | Ausência de valor                               | `None`               |

---

## Como usar

Coloque o `analisador.py` e o arquivo de entrada na mesma pasta e execute:

```bash
python analisador.py entrada.txt
```

---

## Formato do arquivo de entrada

Cada linha deve conter uma declaração de dicionário. Linhas em branco e comentários com `#` são ignorados.

```python
# entrada.txt
aluno   = {'nome': 'Carlos', 'matricula': '2024001', 'periodo': 4}
produto = {'descricao': 'Notebook', 'preco': 3299.99, 'estoque': 10}
config  = {'debug': False, 'versao': 2, 'host': 'localhost'}
vazio   = {}
```

---

## Saída

### Código válido

Exibe apenas uma linha:

```
CÓDIGO VÁLIDO
```

### Código válido com avisos semânticos

Exibe um aviso por problema encontrado, mas não encerra com erro:

```
Aviso — linha 2: variável 'dicio' já declarada na linha 1
Aviso — linha 3: chave 'email' duplicada em 'config'
```

### Código inválido

Exibe a linha com o problema, uma seta apontando a coluna exata e a mensagem de erro:

```
Erro Sintático — linha 2, coluna 12:
  produto = {42: 'valor invalido'}
             ^
  chave deve ser string, não '42' (inteiro)
```

---

## Erros detectados

| Fase      | Descrição                                             |
|-----------|-------------------------------------------------------|
| Léxica    | Caractere inválido no código                          |
| Sintática | Chave do dicionário não é string                      |
| Sintática | Valor não é um tipo primitivo Python                  |
| Sintática | Estrutura incorreta — falta `=`, `{`, `}` ou `:`     |
| Semântica | Variável declarada mais de uma vez *(aviso)*          |
| Semântica | Chave duplicada dentro do dicionário *(aviso)*        |

---

## Requisitos

- Python 3.x  
- Nenhuma biblioteca externa
