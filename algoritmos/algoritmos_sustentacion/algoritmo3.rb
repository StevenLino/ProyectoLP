# Silvia: Validación de condiciones, comparaciones, if, elsif, else, funciones y hash

# --- Comparaciones y condiciones ---
a = 10
b = 20
c = "Ruby"

# Comparaciones válidas
puts a == b          # false
puts a != b          # true
puts a < b           # true
puts a <= 10         # true
puts c == "Ruby"     # true
puts c != "Python"   # true

# --- Condicional if con elsif y else ---
nota = 85

if nota >= 90
  puts "Excelente"
elsif nota >= 70
  puts "Aprobado"
else
  puts "Reprobado"
end

# --- Condicional con operadores lógicos ---
es_estudiante = true
tiene_carnet = false

if es_estudiante && tiene_carnet
  puts "Descuento aplicado"
elsif es_estudiante || tiene_carnet
  puts "Descuento parcial"
else
  puts "Precio completo"
end

# --- Estructura Hash ---
persona = {
  nombre: "Laura",
  edad: 22,
  ciudad: "Quito"
}

# Acceso a valores del hash
puts persona[:nombre]
puts persona[:edad]

# --- Definición de función con parámetros ---
def mostrar_info(nombre, edad)
  puts "Nombre: #{nombre}, Edad: #{edad}"
end

puts mostrar_info("Luis", 30)

# --- Función con parámetros por defecto ---
def saludar(nombre = "Visitante")
  puts "Hola, #{nombre}"
end
saludar
saludar("Camila")
