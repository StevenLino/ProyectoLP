puts "¿Cuántas veces debo saludar?"
veces = gets.chomp.to_i

i = 0
until i == veces
  puts "¡Hola número #{i + 1}!"
  i += 1
end

def calcular_area(base, altura)
  if base <= 0 || altura <= 0
    return "Valores inválidos"
  end
  area = base * altura
  return area
end

base = "diez"   # Error semántico: string no puede multiplicarse con int
altura = 5

area = calcular_area(base, altura)
puts "Área: #{area}"

caso = 3   # Error: variable mal usada en `case`, debe ser `case caso`

case valor
when 1
  puts "Opción 1"
when 2
  puts "Opción 2"
else
  puts "Otra opción"
end
