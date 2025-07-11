# Steven: Validación de reglas básicas, asignación y estructuras primitivas

# Entrada de usuario (input) y salida (puts)
nombre = gets.chomp
puts "Hola #{nombre}"

# Asignaciones y operaciones
a = 10
b = 5
suma = a + b
resta = a - b
multiplicacion = a * b

# Arreglo y acceso
numeros = [1, 2, 3]
puts numeros

# Bucle while con yield
i = 0
while i < 3
  yield if i == 1
  i += 1
end

# Método de clase con yield
class Ejemplo
  def self.saludar
    yield if block_given?
  end
end

Ejemplo.saludar { puts "Hola desde método de clase con yield" }
