import ply.yacc as yacc
from lexico import tokens  # Tu lexer actualizado que incluye GETS y demás
import os
from datetime import datetime
import subprocess

# Steven Lino -Inicio
# Tabla de símbolos y errores semánticos
tabla_simbolos = {
    "variables": {},
    "funciones": {},  # nombre: tipo_retorno
    "tipos_validos": ["Integer", "Float", "String", "Boolean", "Array", "Hash", "Nil"],
}
# Contexto de funciones
contexto_funcion = []


errores_semanticos = []

# Función para registrar errores
def registrar_error(mensaje):
    print(mensaje)
    errores_semanticos.append(mensaje)
# Steven Lino - Fin

# Angel Gómez - Inicio
# Reglas de precedencia
precedence = (
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'EQUAL_EQUAL', 'NOT_EQUAL', 'GREATER_THAN', 'LESS_THAN', 'GREATER_EQUAL', 'LESS_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'POWER'),  # Exponenciación es derecha-asociativa
    ('right', 'UMINUS')  # Unario negativo
)
# Angel Gómez - Final

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
                 | if_statement
                 | function_def
                 | while_statement
                 | unless_statement 
                 | case_statement
                 | class_def''' # agrego unless_statemente y case_statement - Angel Gómez
    p[0] = p[1]

def p_print(p):
    'print : PUTS expression'
    p[0] = ('print', p[2])

# Silvia Saquisili - Inicio
def p_input(p):
    'input : IDENTIFIER ASSIGN GETS DOT IDENTIFIER'
    var_name = p[1]
    tabla_simbolos["variables"][var_name] = "String"
    p[0] = ('input', var_name, "String")

# Silvia Saquisili - Fin
# -----------------------------------------

# Steven Lino - Inicio
def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression'
    var_name = p[1]
    var_type = p[3]

    if var_type not in tabla_simbolos["tipos_validos"]:
        registrar_error(f"[Error Semántico] Tipo desconocido asignado a '{var_name}': {var_type}")
    else:
        tabla_simbolos["variables"][var_name] = var_type

    p[0] = ('assign', var_name,var_type)
# Steven Lino - Fin

def p_assignment_composed(p):
    '''assignment : IDENTIFIER PLUS_ASSIGN expression
                  | IDENTIFIER MINUS_ASSIGN expression
                  | IDENTIFIER TIMES_ASSIGN expression
                  | IDENTIFIER DIVIDE_ASSIGN expression'''
    p[0] = ('assign_op', p[2], p[1], p[3])

# Angel Gómez - Inicio
def p_assignment_logical_op(p):
    '''assignment : IDENTIFIER OR_ASSIGN expression
                  | IDENTIFIER AND_ASSIGN expression'''
    p[0] = ('assign_op', p[2], p[1], p[3])

# Agrupación con parentesis
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# Nueva regla sintactico para expresiones de contengan {} - Angel Gómez
def p_expression_block(p):
    'expression : LBRACE statement_list RBRACE'
    p[0] = ('block', p[2])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('neg', p[2])

# Angel Gómez - Final

# Steven Lino - Inicio
def p_expression_binop(p):
    '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression MODULO expression
                      | expression POWER expression'''
    tipo1 = p[1]
    tipo2 = p[3]
    op = p[2]

    # Reglas simples de compatibilidad de tipos
    if tipo1 == tipo2 and tipo1 in ["Integer", "Float"]:
        p[0] = tipo1  # El resultado es del mismo tipo
    elif (tipo1, tipo2) == ("String", "String") and op == '+':
        p[0] = "String"
    else:
        registrar_error(f"[Error Semántico] Tipo inválido en operación: {tipo1} {op} {tipo2}")
        p[0] = "Error"

def p_expression_number(p):
    '''expression : INTEGER
                      | FLOAT'''
    if isinstance(p[1], int):
        p[0] = "Integer"
    else:
        p[0] = "Float"


def p_expression_string(p):
    'expression : STRING'
    p[0] = "String"

# Steven Lino - Fin

# Angel Gómez - Inicio
# Regla para la estructura de datos Symbols
def p_expression_symbol(p):
    'expression : SYMBOL_COLON'
    p[0] = ('symbol', p[1])
# Angel Gómez - Fin

# Nueva regla para identificar defined?. Esta es una consideración para evitar conflictos - Angel Gómez
def p_expression_definedq(p):
    'expression : DEFINEDQ'
    p[0] = ('definedq',)

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    var_name = p[1]
    if var_name in tabla_simbolos["variables"]:
        p[0] = tabla_simbolos["variables"][var_name]
    else:
        registrar_error(f"[Error Semántico] Variable '{var_name}' no definida")
        p[0]="Error"

#Steven Lino - Fin

# REGLAS SINTACTICA PARA VARIABLES DE INSTANCIA INICIO
def p_expression_instance_var(p):
    'expression : INSTANCE_VAR'
    p[0] = "String"  #

# Regla para considerar las asignaciones
def p_assignment_instance_var(p):
    'assignment : INSTANCE_VAR ASSIGN expression'
    p[0] = ('assign_instance', p[1], p[3])

# REGLAS SINTACTICA PARA VARIABLES DE INSTANCIA FIN

#--------------------

# Silvia Saquisili - Inicio
# Regla para los comparadores en condition

# Silvia Saquisili - Inicio
# REGLA SEMÁNTICA PARA CONDICIONES Y COMPARACIONES
def p_expression_condition(p):
    '''expression : expression LOGICAL_AND expression
                  | expression LOGICAL_OR expression
                  | expression EQUAL_EQUAL expression
                  | expression NOT_EQUAL expression
                  | expression GREATER_THAN expression
                  | expression LESS_THAN expression
                  | expression GREATER_EQUAL expression
                  | expression LESS_EQUAL expression'''
    tipo1 = p[1]
    tipo2 = p[3]
    op = p[2]

    if tipo1 == tipo2 and tipo1 in ["Integer", "Float", "String"]:
        p[0] = "Boolean"
    else:
        registrar_error(f"[Error Semántico] Comparación no válida: {tipo1} {op} {tipo2}")
        p[0] = "Error"

# Silvia Saquisili - Fin
# -----------------------------------------

# Reglas completas para condicionales Ruby

# Silvia Saquisili - Inicio
# REGLA SEMÁNTICA PARA CONDICIONES BOOLEANAS EN ESTRUCTURA DE CONTROL
def p_if_statement(p):
    '''if_statement : IF expression statement_list elsif_blocks_opt else_block_opt END_KW'''
    if p[2] != "Boolean":
        registrar_error(f"[Error Semántico] Condición no booleana en estructura de control (if).")
    p[0] = ('if', p[2])

# Silvia Saquisili - Fin
# -----------------------------------------

# Angel Gómez - Inicio
# Regla para la estructura de control unless y case
def p_unless_statement(p):
    '''unless_statement : UNLESS expression statement_list else_block_opt END_KW'''
    p[0] = ('unless', p[2], p[3], p[4])

def p_case_statement(p):
    '''case_statement : CASE expression when_blocks else_block_opt END_KW'''
    p[0] = ('case', p[2], p[3], p[4])

def p_when_blocks(p):
    '''when_blocks : when_blocks when_block
                   | when_block'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_when_block(p):
    'when_block : WHEN expression statement_list'
    p[0] = ('when', p[2], p[3])
# Angel Gómez - Fin

def p_elsif_blocks_opt(p):
    '''elsif_blocks_opt : elsif_blocks
                        | empty'''
    p[0] = p[1]

def p_elsif_blocks(p): #correciones para evitar problemas de recursion
    '''elsif_blocks : ELSIF expression statement_list elsif_blocks
                    | ELSIF expression statement_list'''
    if len(p) == 5:
        p[0] = [('elsif', p[2], p[3])] + p[4] # Correción de errores sintactico
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
    'empty :'
    p[0] = []

# Silvia Saquisili - Fin
#--------------------

# Reglas semantica para funciones y tipo de retorno INICIO - Angel Gomez
def p_function_def(p):
    '''function_def : DEF IDENTIFIER LPAREN param_list_opt RPAREN statement_list END_KW'''
    nombre = p[2]
    # Ingresar a contexto
    contexto_funcion.append(nombre)

    # CORRECION SEMANTICA PARA VARIABLE
    for param in p[4]:  # p[4] es la lista de parámetros
        if param[0] == 'param':
            tabla_simbolos["variables"][param[1]] = "String"  # o inferido

    # Si hubo una sentencia return, la función tendrá un tipo (evaluado abajo)
    tipo_retorno = None
    for stmt in p[6]:
        if isinstance(stmt, tuple) and stmt[0] == 'return':
            tipo_retorno = stmt[1]
            break

    if tipo_retorno is None:
        tipo_retorno = "Nil"  # Asumimos que no retorna nada explícitamente

    tabla_simbolos["funciones"][nombre] = tipo_retorno

    # Salir del contexto
    contexto_funcion.pop()

    p[0] = ('function', nombre, tipo_retorno)

def p_statement_return(p):
    'statement : RETURN expression'
    tipo_retorno = p[2]

    if not contexto_funcion:
        registrar_error("[Error Semántico] 'return' fuera de una función.")
    else:
        funcion_actual = contexto_funcion[-1]
        tipo_esperado = tabla_simbolos["funciones"].get(funcion_actual, "Desconocido")

        # Si ya se conoce el tipo anterior, validar que sea coherente
        if tipo_esperado != "Desconocido" and tipo_esperado != tipo_retorno:
            registrar_error(
                f"[Error Semántico] Tipo de retorno inválido en función '{funcion_actual}'. Se esperaba {tipo_esperado}, se obtuvo {tipo_retorno}")

    p[0] = ('return', tipo_retorno)

# Reglas semantica para funciones y tipo de retorno INICIO - Angel Gomez

#Angel Gómez - Inicio
# Función sin paréntesis (param_list_opt ya admite vacío)
def p_function_def_no_parens(p):
    '''function_def : DEF IDENTIFIER param_list_opt statement_list END_KW'''
    p[0] = ('function_def_no_parens', p[2], p[3], p[4])
#Angel Gómez - Fin

# Steven Lino -Inicio
#--------------------

# Métodos de clase (definidos con self. o Clase.)
def p_function_def_class_method(p):
    '''function_def : DEF SELF DOT IDENTIFIER statement_list END_KW
                    | DEF CONSTANT DOT IDENTIFIER statement_list END_KW'''
    p[0] = ('class_method_def', p[3], p[4], p[5])


def p_statement_yield(p):
    'statement : YIELD'
    p[0] = ('yield',)

# Regla para considerar la expresión yield if condition
def p_statement_yield_if(p):
    'statement : YIELD IF expression'
    p[0] = ('yield_if', p[3])

# Steven Lino - Fin
#--------------------

# Reglas de definición de Clases y Objetos INICIO - Angel Gomez
def p_class_def(p):
    '''class_def : CLASS CONSTANT statement_list END_KW'''
    p[0] = ('class_def', p[2], p[3])

def p_object_creation(p):
    '''expression : CONSTANT DOT NEW expression_list_opt'''
    p[0] = ('new_object', p[1], p[4])

def p_expression_list_opt(p):
    '''expression_list_opt : expression_list
                           | empty'''
    p[0] = p[1]

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
# Herencia
def p_class_def_inherit(p):
    '''class_def : CLASS CONSTANT LESS_THAN CONSTANT statement_list END_KW'''
    p[0] = ('class_def_inherit', p[2], p[4], p[5])

# Metodos utiles en clases
def p_attr_statement(p):
    '''statement : ATTR_ACCESSOR symbol_list
                 | ATTR_READER symbol_list
                 | ATTR_WRITER symbol_list'''
    p[0] = ('attr', p[1], p[2])

def p_symbol_list(p):
    '''symbol_list : SYMBOL_COLON
                   | symbol_list COMMA SYMBOL_COLON'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
# Reglas de definición de Clases y Objetos FIN - Angel Gomez

# Regla para mejorar el llamado de metodos
def p_expression_method_call(p):
    '''expression : IDENTIFIER DOT IDENTIFIER LPAREN arg_list RPAREN'''
    # p[1] = clase u objeto
    # p[3] = método (new, hablar, etc.)
    # p[5] = argumentos
    nombre_objeto_o_clase = p[1]
    metodo = p[3]

    if metodo == 'new':
        tipo = nombre_objeto_o_clase
    else:
        tipo = "Desconocido"

    p[0] = tipo

def p_arg_list(p):
    '''arg_list : arg_list COMMA expression
                | expression
                | empty'''
    if len(p) == 4:
        p[0] = [p[1]] + [p[3]]
    elif len(p) == 2 and p[1] != []:
        p[0] = [p[1]]
    else:
        p[0] = []

# Parámetros con valores por defecto
def p_param(p):
    '''param : IDENTIFIER
             | IDENTIFIER ASSIGN expression'''
    if len(p) == 2:
        p[0] = ('param', p[1], None)
    else:
        p[0] = ('param', p[1], p[3])

def p_param_list_opt(p):
    '''param_list_opt : param_list
                      | empty'''
    p[0] = p[1]

def p_param_list(p):
    '''param_list : param
                  | param_list COMMA param'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# Silvia Saquisili - Fin

# Reglas semantica de validación de break, next y while INICIO - Angel Gómez
nivel_bucle = 0

def p_while_statement(p):
    '''while_statement : WHILE expression statement_list END_KW'''
    global nivel_bucle
    if p[2] != "Boolean":
        registrar_error(f"[Error Semántico] Condición no booleana en bucle while.")
    nivel_bucle += 1
    nivel_bucle -= 1
    p[0] = ('while', p[2])

def p_statement_break(p):
    'statement : BREAK'
    if nivel_bucle <= 0:
        registrar_error(f"[Error Semántico] 'break' usado fuera de un bucle.")
    p[0] = ('break',)

def p_statement_next(p):
    'statement : NEXT'
    if nivel_bucle <= 0:
        registrar_error(f"[Error Semántico] 'next' usado fuera de un bucle.")
    p[0] = ('next',)
# Reglas semantica de validación de break, next y while FIN - Angel Gómez

#Steven Lino - Inicio
# Estructura de datos -Arreglo
def p_array(p):
    '''expression : LBRACKET elements RBRACKET'''
    p[0] = "Array" #modificacion

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
#Steven Lino - Fin

# Silvia Saquisili - Inicio
# Reglas corregidas para hash que evitan recursión infinita

def p_expression_hash(p):
    '''expression : LBRACE hash_content RBRACE'''
    p[0] = ('hash', p[2])

def p_hash_content(p):
    '''hash_content : hash_pair_list
                    | '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]

def p_hash_pair_list(p):
    '''hash_pair_list : hash_pair
                      | hash_pair_list COMMA hash_pair'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_hash_pair(p):
    '''hash_pair : SYMBOL_COLON ASSIGN expression'''
    p[0] = (p[1], p[3])
# Silvia Saquisili - Fin

# Rango
def p_expression_range(p):
    '''expression : expression RANGE_INCLUSIVE expression
                  | expression RANGE_EXCLUSIVE expression'''
    p[0] = ('range', p[2],p[1],p[3])

#Steven Lino - Inicio
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
    parser = yacc.yacc(debug=True, debugfile="parser.out", tabmodule='parsetab')
    archivo_rb = "algoritmos/algoritmo1.rb"

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
    nombre_log = f"semantico-{usuario_git}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    ruta_log = os.path.join("logs", nombre_log)

    resultado = parser.parse(code)

    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("=== LOG ANALIZADOR SEMANTICO ===\n")
        f.write(f"Fecha: {ahora.strftime('%d/%m/%Y')}\n")
        f.write(f"Hora: {ahora.strftime('%H:%M')}\n\n")
        f.write("--- ERRORES ---\n")
        if errores_semanticos:
            for err in errores_semanticos:
                f.write(err + '\n')
        else:
            f.write("No se encontraron errores semanticos.\n")

    print(f"\n✅ Log guardado en: {ruta_log}")