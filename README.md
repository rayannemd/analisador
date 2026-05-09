# Analisador de Dicionário Python

Analisador léxico e sintático para declarações de dicionário da linguagem Python, desenvolvido como trabalho prático da disciplina de Compiladores.

## Descrição

O programa lê um arquivo `.txt` contendo declarações de dicionário Python e as analisa em três fases:

1. **Análise Léxica** — transforma o código em tokens
2. **Análise Sintática** — verifica se a estrutura está correta (estratégia Top-Down / Descendente Recursivo)
3. **Análise Semântica** — detecta problemas de significado como variáveis redeclaradas e chaves duplicadas

O analisador para imediatamente ao encontrar o primeiro erro.

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

### Regras léxicas

| Token    | Descrição                                          | Exemplo              |
|----------|----------------------------------------------------|----------------------|
| VARIAVEL | Letra ou `_` seguido de letras, dígitos ou `_`     | `dicio`, `_config`   |
| STRING   | Texto entre aspas simples ou duplas                | `'nome'`, `"valor"`  |
| INTEIRO  | Sequência de dígitos, positivo ou negativo         | `42`, `-5`           |
| REAL     | Dígitos com ponto decimal, positivo ou negativo    | `3.14`, `-2.5`       |
| BOOLEANO | Valor lógico                                       | `True`, `False`      |
| NULO     | Ausência de valor                                  | `None`               |

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
# exemplo de entrada válida
dicio = {'chave1': 'valor', 'chave2': 'valor'}
dados = {'nome': 'Ana', 'idade': 30, 'altura': 1.68, 'ativo': True, 'apelido': None}
vazio = {}
temperatura = {'minima': -5, 'maxima': 40, 'media': -2.5}
```

---

## Exemplos de saída

### Código válido

```
====================================================
  Arquivo: entrada.txt
====================================================

Análise Léxica
----------------------------------------------------
  VARIAVEL   'dicio'                   linha 1
  SIMBOLO    '='                       linha 1
  ...
  OK — 11 tokens gerados

Análise Sintática
----------------------------------------------------
  OK — 1 declaração(ões) reconhecida(s)

  dicio (linha 1) — 2 par(es):
    'chave1'             : 'valor' (string)
    'chave2'             : 'valor' (string)

Análise Semântica
----------------------------------------------------
  OK — sem problemas

====================================================
  RESULTADO: CÓDIGO VÁLIDO
====================================================
```

### Código com avisos semânticos

```
Análise Semântica
----------------------------------------------------
  Aviso | linha 5: variável 'dicio' já declarada na linha 1
  Aviso | linha 6: chave 'host' duplicada em 'config'

====================================================
  RESULTADO: CÓDIGO VÁLIDO COM 2 AVISO(S)
====================================================
```

### Código inválido

```
Análise Sintática
----------------------------------------------------

  Erro sintático | linha 3: chave deve ser string, não '42' (INTEIRO)
  Execução interrompida no primeiro erro encontrado.
====================================================
  RESULTADO: CÓDIGO INVÁLIDO — 1 erro(s)
====================================================
```

---

## Erros detectados

| Fase      | Erro                                          |
|-----------|-----------------------------------------------|
| Léxica    | Caractere inválido no código                  |
| Sintática | Chave do dicionário não é string              |
| Sintática | Valor não é um tipo primitivo Python          |
| Sintática | Estrutura incorreta (falta `=`, `{`, `}`, `:`) |
| Semântica | Variável declarada mais de uma vez (aviso)    |
| Semântica | Chave duplicada no dicionário (aviso)         |

---

## Requisitos

- Python 3.x
- Nenhuma biblioteca externa
