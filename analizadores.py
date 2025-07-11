# analizadores.py

from lexico import lexer, errores_lexicos
from sintactico import parser_sintactico, errores_sintacticos
from semantico import parser_semantico, errores_semanticos

# ---------- Análisis Léxico ----------
def analizar_lexico(codigo: str) -> str:
    lexer.lineno = 1
    errores_lexicos.clear()
    lexer.input(codigo)

    resultado = ["=== ANÁLISIS LÉXICO ==="]
    while True:
        token = lexer.token()
        if not token:
            break
        resultado.append(f"[Línea {token.lineno}] {token.type}: {token.value}")

    if errores_lexicos:
        resultado.append("\n--- ERRORES LÉXICOS ---")
        resultado.extend(errores_lexicos)
    else:
        resultado.append("\nNo se encontraron errores léxicos.")

    return "\n".join(resultado)


# ---------- Análisis Sintáctico ----------
def analizar_sintactico(codigo: str) -> str:
    parser_sintactico.errorlog = None
    errores_sintacticos.clear()

    try:
        parser_sintactico.parse(codigo)
    except Exception as e:
        errores_sintacticos.append(f"[Error Sintáctico] {str(e)}")

    resultado = ["=== ANÁLISIS SINTÁCTICO ==="]
    if errores_sintacticos:
        resultado.append("\n--- ERRORES SINTÁCTICOS ---")
        resultado.extend(errores_sintacticos)
    else:
        resultado.append("No se encontraron errores sintácticos.")

    return "\n".join(resultado)


# ---------- Análisis Semántico ----------
def analizar_semantico(codigo: str) -> str:
    parser_semantico.errorlog = None
    errores_semanticos.clear()

    try:
        parser_semantico.parse(codigo)
    except Exception as e:
        errores_semanticos.append(f"[Error Semántico] {str(e)}")

    resultado = ["=== ANÁLISIS SEMÁNTICO ==="]
    if errores_semanticos:
        resultado.append("\n--- ERRORES SEMÁNTICOS ---")
        resultado.extend(errores_semanticos)
    else:
        resultado.append("No se encontraron errores semánticos.")

    return "\n".join(resultado)
