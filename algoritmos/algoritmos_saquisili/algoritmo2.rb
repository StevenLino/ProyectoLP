# Comentario mal cerrado
=begin
  Comentario sin final
puts "Esto no se debería ejecutar"
# ERROR: Falta `=end` para comentario multilínea

# Operación inválida
x = 5 + "hola"
# ERROR: Suma entre Integer y String

# Comparador inválido
es_valido = "Juan" > 10
# ERROR: Comparación entre String e Integer

# Return fuera de función
return "esto no debe estar aquí"
# ERROR: 'return' fuera de función

# Hash mal formado
usuario = { nombre => "Ana", edad: 25 }
# ERROR: Uso incorrecto de `=>`, el lexer solo acepta `:` y `=`
