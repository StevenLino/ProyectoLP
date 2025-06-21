import ply.yacc as yacc
from lexico import tokens  # Tu lexer actualizado que incluye GETS y demás
import os
from datetime import datetime
import subprocess

errores_sintacticos = []

# Indicar la regla inicial del parser:
#start = 'statement'

# Silvia Saquisili - Inicio
# Regla inicial
start = 'program'

# Regla para representar el programa completo
def p_program(p):
    '''program : statement_list'''
    p[0] = ('program', p[1])

# Regla para permitir múltiples declaraciones
def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Silvia Saquisili - Final

#Steven Lino - Inicio
#--------------------

def p_statement(p):
    '''statement : print
                 | input
                 | assignment
                 | expression
                 | if_statement'''
    p[0] = p[1]

def p_print(p):
    'print : PUTS expression'
    p[0] = ('print', p[2])

def p_input(p):
    'input : IDENTIFIER ASSIGN GETS DOT IDENTIFIER'
    p[0] = ('input', p[1], 'gets', p[5])

def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

def p_assignment_composed(p):
    '''assignment : IDENTIFIER PLUS_ASSIGN expression
                  | IDENTIFIER MINUS_ASSIGN expression
                  | IDENTIFIER TIMES_ASSIGN expression
                  | IDENTIFIER DIVIDE_ASSIGN expression'''
    p[0] = ('assign_op', p[2], p[1], p[3])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression MODULO expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_number(p):
    '''expression : INTEGER
                  | FLOAT'''
    p[0] = p[1]

def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('var', p[1])

def p_condition_logical(p):
    '''condition : expression LOGICAL_AND expression
                 | expression LOGICAL_OR expression'''
    p[0] = ('logical', p[2], p[1], p[3])

#Steven Lino - Fin
#--------------------

# Silvia Saquisili - Inicio
# Regla para los comparadores en condition
def p_condition_comparison(p):
    ''' condition : expression EQUAL_EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN expression
                  | expression GREATER_EQUAL expression
                  | expression LESS_EQUAL expression'''
    p[0] = ('compare', p[2], p[1], p[3])

# Reglas completas para condicionales Ruby
def p_if_statement(p):
    '''if_statement : IF condition statement_list elsif_blocks_opt else_block_opt END_KW'''
    p[0] = ('if_full', p[2], p[3], p[4] + p[5])

def p_elsif_blocks_opt(p):
    '''elsif_blocks_opt : elsif_blocks
                        | empty'''
    p[0] = p[1]

def p_elsif_blocks(p):
    '''elsif_blocks :  elsif_blocks ELSIF condition statement_list
                    | ELSIF condition statement_list'''
    if len(p) == 5:
        p[0] = p[1] + [('elsif', p[3], p[4])]
    else:
        p[0] = [('elsif', p[2], p[3])]

def p_else_block_opt(p):
    '''else_block_opt : ELSE statement_list
                      | empty'''
    if len(p) == 3:
        p[0] = [('else', p[2])]
    else:
        p[0] = []

def p_empty(p):
    'empty : '
    p[0] = []

# Silvia Saquisili - Fin


#Steven Lino - Inicio
#--------------------
def p_while_loop(p):
    '''statement : WHILE condition statement_list END_KW'''
    p[0] = ('while', p[2], p[3])


# Estructura de datos -Arreglo
def p_array(p):
    '''expression : LBRACKET elements RBRACKET'''
    p[0] = ('array', p[2])

def p_elements(p):
    '''elements : elements COMMA expression
                | expression
                | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] != []:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_error(p):
    if p:
        mensaje = f"[Error Sintáctico] Token inesperado: {p.type} ('{p.value}') en la línea {p.lineno}"
    else:
        mensaje = "[Error Sintáctico] Fin de archivo inesperado"
    print(mensaje)
    errores_sintacticos.append(mensaje)
#Steven Lino - Fin
#--------------------

if __name__ == "__main__":
    parser = yacc.yacc()

    archivo_rb = "algoritmos/algoritmo7.rb"

    with open(archivo_rb, "r", encoding="utf-8") as f:
        code = f.read()

    # Obtiene usuario git para log
    try:
        usuario_git = subprocess.getoutput("git config user.name").strip()
        if not usuario_git:
            usuario_git = "usuarioGit"
    except:
        usuario_git = "usuarioGit"

    if not os.path.exists("logs"):
        os.makedirs("logs")

    from datetime import datetime
    ahora = datetime.now()
    nombre_log = f"sintactico-{usuario_git}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    ruta_log = os.path.join("logs", nombre_log)

    resultado = parser.parse(code)

    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("=== LOG ANALIZADOR SINTÁCTICO ===\n")
        f.write(f"Fecha: {ahora.strftime('%d/%m/%Y')}\n")
        f.write(f"Hora: {ahora.strftime('%H:%M')}\n\n")
        f.write("--- ERRORES ---\n")
        if errores_sintacticos:
            for err in errores_sintacticos:
                f.write(err + '\n')
        else:
            f.write("No se encontraron errores sintácticos.\n")

    print(f"\n✅ Log guardado en: {ruta_log}")
