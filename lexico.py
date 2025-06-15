import ply.lex as lex
import os
from datetime import datetime
import subprocess

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

# EXPRESIONES REGULARES
# -----------------------------

# ANGEL GÓMEZ - INICIO

t_POWER           = r'\*\*'
t_PLUS            = r'\+'
t_MINUS           = r'-'
t_TIMES           = r'\*'
t_DIVIDE          = r'/'
t_MODULO          = r'%'

t_GREATER_EQUAL   = r'>='
t_LESS_EQUAL      = r'<='
t_EQUAL_EQUAL     = r'=='
t_NOT_EQUAL       = r'!='
t_GREATER_THAN    = r'>'
t_LESS_THAN       = r'<'

# ANGEL GÓMEZ - FIN

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

# -----------------------------

# STEVEN LINO - INICIO
# CADENAS
def t_STRING(t):
    r'"([^\\"]|\\.)*"'
    t.value = t.value[1:-1]  # quitar comillas
    return t

# FLOTANTES
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# ENTEROS
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_GLOBAL_VAR(t):
    r'\$[a-zA-Z_]\w*'
    return t

# STEVEN LINO - FIN

# ANGEL GÓMEZ - INICIO

def t_INSTANCE_VAR(t):
    r'@[a-zA-Z_]\w*'
    return t

def t_CLASS_VAR(t):
    r'@@[a-zA-Z_]\w*'
    return t

def t_CONSTANT(t):
    r'[A-Z][a-zA-Z_0-9]*'
    return t

def t_IDENTIFIER(t):
    r'[a-z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# ANGEL GÓMEZ - FIN

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

errores_lexicos = []

def t_error(t):
    mensaje = f"[Error Léxico] Carácter ilegal: {t.value[0]!r} en la línea {t.lineno}"
    print(mensaje)
    errores_lexicos.append(mensaje)
    t.lexer.skip(1)

# SILVIA SAQUISILI - FIN

# ANGEL GÓMEZ - INICIO

# CONSTRUCCIÓN DEL LÉXICO
# -----------------------------

lexer = lex.lex()

if __name__ == "__main__":
    code = '''
    =begin
    Este programa define una clase base Persona,
    y una subclase Estudiante que hereda sus
    propiedades.
    =end
    
    class Persona
      attr_accessor :nombre, :edad
    
      def initialize(nombre, edad)
        @nombre = nombre
        @edad = edad
      end
    
      def presentarse
        puts "Hola, soy #{@nombre} y tengo #{@edad}
    años."
      end
    end
    
    class Estudiante < Persona
      attr_accessor :curso
    
      def initialize(nombre, edad, curso)
        super(nombre, edad)
        @curso = curso
      end
    
      def presentarse
        super
        puts "Estudio en el curso #{@curso}."
      end
    end
    
    alumno = Estudiante.new("Carlos", 20, "Ruby101")
    alumno.presentarse
    '''

    # MECÁNICA DE LOS LOGS

    # OBTENCIÓN DEL USUARIO GIT
    try:
        usuario_git = subprocess.getoutput("git config user.name").strip()
        if not usuario_git:
            usuario_git = "usuarioGit"
    except:
        usuario_git = "usuarioGit"

    # CREACIÓN DE LA CARPETA DE LOS LOGS
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # OBTENCIÓN DE LA FECHA Y NOMBRE DEL ARCHIVO
    ahora = datetime.now()
    nombre_archivo = f"lexico-{usuario_git}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    ruta_archivo = os.path.join("logs", nombre_archivo)

    lexer.input(code)

    # MODIFICACIÓN DEL ARCHIVO PARA ESCRIBIR EL LOG
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        f.write("=== LOG ANALIZADOR LÉXICO ===\n")
        f.write(f"Fecha: {ahora.strftime('%d/%m/%Y')}\n")
        f.write(f"Hora: {ahora.strftime('%H:%M')}\n\n")

        f.write("--- TOKENS RECONOCIDOS ---\n")
        token_count = 0
        while True:
            tok = lexer.token()
            if not tok:
                break
            token_count += 1
            f.write(f"[Línea {tok.lineno}] Tipo: {tok.type}, Valor: {tok.value}\n")

        f.write(f"\nTotal de tokens: {token_count}\n")

        f.write("\n--- ERRORES ---\n")
        if not errores_lexicos:
            f.write("No se encontraron errores léxicos.\n")
        else:
            for error in errores_lexicos:
                f.write(error + "\n")
        f.write(f"\nTotal de errores: {len(errores_lexicos)}\n")

    print(f"\nLog guardado en: {ruta_archivo}")