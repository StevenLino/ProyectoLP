def multiplicar(a, b)
  if defined?(a) and defined?(b)
    return a * b
  els
    puts "Parámetros faltantes"
  end
end

for i in 0..2
  puts "Iteración #{i}"
end

begin
  resultado = multiplicar(2, nil)
rescue => e
  puts "Error: #{e}"
ensure
  puts "Proceso completado"
end
