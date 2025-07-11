# Entrada válida
edad = gets.chomp

# Operación semánticamente inválida
resultado = edad + 10
# ERROR: `edad` es String, no se puede sumar con Integer

# Función mal declarada
def saludar(nombre
  puts "Hola, #{nombre}"
end
# ERROR: Falta paréntesis de cierre → error sintáctico

# Condicional válida
if edad != ""
  puts "Edad ingresada"
end

# Variable sin definir
puts total
# ERROR: Variable 'total' no definida

# Hash válido
config = { modo: "oscuro", version: 1.2 }
puts config