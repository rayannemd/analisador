import sys

avisos = []
erros  = []


# ANÁLISE LÉXICA

def tokenizar(codigo):
    # percorre o código caractere a caractere e gera a lista de tokens
    # cada token é uma tupla: (tipo, valor, linha)
    tokens = []
    i      = 0
    linha  = 1

    while i < len(codigo):
        c = codigo[i]

        # espaços em branco
        if c in ' \t\r':
            i += 1
            continue

        # nova linha
        if c == '\n':
            linha += 1
            i += 1
            continue

        # comentário
        if c == '#':
            while i < len(codigo) and codigo[i] != '\n':
                i += 1
            continue

        # string
        if c in ('"', "'"):
            delim = c
            i += 1
            buf = ''
            while i < len(codigo) and codigo[i] != delim:
                if codigo[i] == '\\':
                    i += 1
                buf += codigo[i]
                i += 1
            i += 1  # fecha a aspa
            tokens.append(('STRING', buf, linha))
            continue

        # digitos
        if c.isdigit() or (c == '-' and i+1 < len(codigo) and codigo[i+1].isdigit()):
            buf = c
            i += 1
            while i < len(codigo) and (codigo[i].isdigit() or codigo[i] == '.'):
                buf += codigo[i]
                i += 1
            tipo = 'REAL' if '.' in buf else 'INTEIRO'
            tokens.append((tipo, buf, linha))
            continue

        # identificador
        if c.isalpha() or c == '_':
            buf = ''
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                buf += codigo[i]
                i += 1
            if buf in ('True', 'False'):
                tokens.append(('BOOLEANO', buf, linha))
            elif buf == 'None':
                tokens.append(('NULO', buf, linha))
            else:
                tokens.append(('VARIAVEL', buf, linha))
            continue

        # símbolo
        if c in '={}:,':
            tokens.append(('SIMBOLO', c, linha))
            i += 1
            continue

        # erro léxico
        parar('lexico', f"linha {linha}: caractere inválido '{c}'")

    tokens.append(('EOF', '', linha))
    return tokens


# ANÁLISE SINTÁTICA  (Top-Down)

pos    = 0
tokens = []

def parar(fase, msg):
    # registra o erro e encerra o programa imediatamente
    erros.append(f"Erro — {msg}")
    print(f"\n  Erro {fase} | {msg}")
    print("  Execução interrompida no primeiro erro encontrado.")
    print("=" * 52)
    sys.exit(1)

def atual():
    # retorna o token na posição atual sem avançar
    return tokens[pos]

def consumir(tipo=None, val=None):
    # verifica se o token atual é o esperado
    global pos
    tok = tokens[pos]
    if tipo and tok[0] != tipo:
        parar('sintático', f"linha {tok[2]}: esperava {tipo} mas veio '{tok[1]}'")
    if val and tok[1] != val:
        parar('sintático', f"linha {tok[2]}: esperava '{val}' mas veio '{tok[1]}'")
    pos += 1
    return tok

def verificar(tipo=None, val=None):
    # olha o token atual sem consumir
    tok = tokens[pos]
    if tipo and tok[0] != tipo: return False
    if val  and tok[1] != val:  return False
    return True

def programa():
    
    decls = []
    while not verificar('EOF'):
        decls.append(declaracao())
    return decls

def declaracao():
    # declaracao -> VARIAVEL '=' dicionario
    tok = atual()
    if tok[0] != 'VARIAVEL':
        parar('sintático', f"linha {tok[2]}: nome de variável inválido '{tok[1]}'")
    nome = consumir('VARIAVEL')
    consumir('SIMBOLO', '=')
    dic  = dicionario()
    return ('decl', nome[1], dic, nome[2])

def dicionario():
    # dicionario -> '{' pares '}'
    consumir('SIMBOLO', '{')
    ps = pares() if not verificar('SIMBOLO', '}') else []
    consumir('SIMBOLO', '}')
    return ('dict', ps)

def pares():
    # pares -> par (',' par)*
    lista = [par()]
    while verificar('SIMBOLO', ','):
        consumir('SIMBOLO', ',')
        if verificar('SIMBOLO', '}'):
            break
        lista.append(par())
    return lista

def par():
    
    tok = atual()
    if tok[0] != 'STRING':
        parar('sintático', f"linha {tok[2]}: chave deve ser string, não '{tok[1]}' ({tok[0]})")
    chave = consumir('STRING')
    consumir('SIMBOLO', ':')
    val   = valor()
    return ('par', chave[1], val)

def valor():
    
    tok = atual()
    if tok[0] not in ('STRING', 'INTEIRO', 'REAL', 'BOOLEANO', 'NULO'):
        parar('sintático', f"linha {tok[2]}: valor inválido '{tok[1]}' — use string, inteiro, real, True, False ou None")
    consumir()
    return (tok[0], tok[1])


# ANÁLISE SEMÂNTICA

def checar(decls):
    
    vars_vistas = {} 

    for _, nome, dic, linha in decls:

        if nome in vars_vistas: # variáveis duplicadas
            avisos.append(f"linha {linha}: variável '{nome}' já declarada na linha {vars_vistas[nome]}")
        vars_vistas[nome] = linha

        chaves_vistas = {} # chaves duplicadas
        for _, chave, _ in dic[1]:
            if chave in chaves_vistas:
                avisos.append(f"linha {linha}: chave '{chave}' duplicada em '{nome}'")
            else:
                chaves_vistas[chave] = linha


# EXECUÇÃO

if len(sys.argv) < 2:
    print("Uso: python analisador.py entrada.txt")
    sys.exit(1)

with open(sys.argv[1], encoding='utf-8') as f:
    codigo = f.read()

print("=" * 52)
print(f"  Arquivo: {sys.argv[1]}")
print("=" * 52)

print("\nAnálise Léxica")
print("-" * 52)
tokens = tokenizar(codigo)
for tok in tokens:
    if tok[0] != 'EOF':
        print(f"  {tok[0]:<10} {repr(tok[1]):<25} linha {tok[2]}")
total = len([t for t in tokens if t[0] != 'EOF'])
print(f"\n  OK — {total} tokens gerados")

print("\nAnálise Sintática")
print("-" * 52)
pos = 0
ast = programa()
print(f"  OK — {len(ast)} declaração(ões) reconhecida(s)")
for _, nome, dic, linha in ast:
    print(f"\n  {nome} (linha {linha}) — {len(dic[1])} par(es):")
    for _, chave, val in dic[1]:
        print(f"    {chave!r:<20} : {val[1]!r} ({val[0].lower()})")

print("\nAnálise Semântica")
print("-" * 52)
checar(ast)
if avisos:
    for a in avisos:
        print(f"  Aviso | {a}")
else:
    print("  OK — sem problemas")

# resultado
print("\n" + "=" * 52)
if erros:
    print(f"  RESULTADO: CÓDIGO INVÁLIDO — {len(erros)} erro(s)")
elif avisos:
    print(f"  RESULTADO: CÓDIGO VÁLIDO COM {len(avisos)} AVISO(S)")
else:
    print("  RESULTADO: CÓDIGO VÁLIDO")
print("=" * 52)