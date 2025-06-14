import ply.lex as lex

# SILVIA SAQUISILI - INICIO

# PALABRAS RESERVADAS EN RUBY
# -----------------------------

reserved = {
    "alias": "ALIAS",
    "and": "AND",
    "begin": "BEGIN",
    "break": "BREAK",
    "case": "CASE",
    "class": "CLASS",
    "def": "DEF",
    "defined?": "DEFINEDQ",
    "do": "DO",
    "else": "ELSE",
    "elsif": "ELSIF",
    "end": "END",
    "ensure": "ENSURE",
    "false": "FALSE",
    "for": "FOR",
    "if": "IF",
    "in": "IN",
    "module": "MODULE",
    "next": "NEXT",
    "nil": "NIL",
    "not": "NOT",
    "or": "OR",
    "redo": "REDO",
    "rescue": "RESCUE",
    "retry": "RETRY",
    "return": "RETURN",
    "self": "SELF",
    "super": "SUPER",
    "then": "THEN",
    "true": "TRUE",
    "undef": "UNDEF",
    "unless": "UNLESS",
    "until": "UNTIL",
    "when": "WHEN",
    "while": "WHILE",
    "yield": "YIELD"
}

# SILVIA SAQUISILI - FIN

# SILVIA SAQUISILI - INICIO

# LISTA DE TOKENS
# -----------------------------

tokens = [
    # IDENTIFICADORES Y VARIABLES
    'IDENTIFIER', 'GLOBAL_VAR', 'INSTANCE_VAR', 'CLASS_VAR', 'CONSTANT',

    # TIPOS DE DATOS
    'INTEGER', 'FLOAT', 'STRING',

    # OPERADORES ARITMÉTICOS Y LÓGICOS
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'POWER',
    'EQUAL_EQUAL', 'NOT_EQUAL',
    'GREATER_THAN', 'LESS_THAN', 'GREATER_EQUAL', 'LESS_EQUAL',
    'LOGICAL_AND', 'LOGICAL_OR', 'LOGICAL_NOT',

    # ASIGNACIONES
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN',
    'OR_ASSIGN', 'AND_ASSIGN',

    # OTROS OPERADORES
    'RANGE_INCLUSIVE', 'RANGE_EXCLUSIVE', 'MATCH_REGEX', 'NOT_MATCH_REGEX',

    # DELIMITADORES
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'COMMA', 'SEMICOLON',

    #PUNTO
    'DOT'
] + list(reserved.values())

# SILVIA SAQUISILI - FIN

# LISTA DE TOKENS
# -----------------------------

# STEVEN LINO - INICIO

t_LOGICAL_AND     = r'&&'
t_LOGICAL_OR      = r'\|\|'
t_LOGICAL_NOT     = r'!'

t_ASSIGN          = r'='
t_PLUS_ASSIGN     = r'\+='
t_MINUS_ASSIGN    = r'-='
t_TIMES_ASSIGN    = r'\*='
t_DIVIDE_ASSIGN   = r'/='
t_OR_ASSIGN       = r'\|\|='
t_AND_ASSIGN      = r'&&='

# STEVEN LINO - FIN

# SILVIA SAQUISILI - INICIO

t_MATCH_REGEX     = r'=~'
t_NOT_MATCH_REGEX = r'!~'

t_RANGE_EXCLUSIVE = r'\.\.\.'
t_RANGE_INCLUSIVE = r'\.\.'

t_LPAREN          = r'\('
t_RPAREN          = r'\)'
t_LBRACE          = r'\{'
t_RBRACE          = r'\}'
t_LBRACKET        = r'\['
t_RBRACKET        = r'\]'
t_COMMA           = r','
t_SEMICOLON       = r';'

# SILVIA SAQUISILI - FIN

# STEVEN LINO - INICIO
# Cadenas
def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]  # quitar comillas
    return t

# Flotantes
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Enteros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_GLOBAL_VAR(t):
    r'\$[a-zA-Z_]\w*'
    return t

# STEVEN LINO - FIN

# -----------------------------

# SILVIA SAQUISILI - INICIO

# COMENTARIOS
def t_COMMENT(t):
    r'\#.*'
    pass

def t_MULTILINE_COMMENT(t):
    r'=begin[\s\S]*?=end'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ESPACIOS Y TABS
t_ignore = ' \t'

#PUNTO
t_DOT = r'\.'

# ERRORES
def t_error(t):
    print(f"[Error Léxico] Carácter ilegal: {t.value[0]!r} en la línea {t.lineno}")
    t.lexer.skip(1)

# SILVIA SAQUISILI - FIN