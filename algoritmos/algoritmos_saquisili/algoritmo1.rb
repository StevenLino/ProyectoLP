# Entrada y saludo
nombre = gets.chomp
puts "Hola, #{nombre}"

# Aritmética válida
a = 10
b = 5
suma = a + b
puts suma

# Función con retorno
def saludar(nombre = "invitado")
  return "Hola, #{nombre}"
end

mensaje = saludar("Luis")
puts mensaje

# Hash válido
persona = { nombre: "Ana", edad: 30 }
puts persona

# Condicional válida
if a > b
  puts "a es mayor que b"
end
