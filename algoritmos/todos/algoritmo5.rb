def calcular(a, b, operador)
  case operador
  when "+"
    return a + b
  when "-"
    return a - b
  when "*"
    return a * b
  when "/"
    return b != 0 ? a / b : "Error: división por cero"
  else
    return "Operador no válido"
  end
end

#Comentario de prueba
#Ingreso de datos
print "Número 1: "
num1 = gets.chomp.to_f
print "Número 2: "
num2 = gets.chomp.to_f

print "Operador (+, -, *, /): "
op = gets.chomp

resultado = calcular(num1, num2, op)
puts "Resultado: #{resultado}"