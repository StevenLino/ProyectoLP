usuarios = []

def registrar_usuario
  print "Ingresa el nombre: "
  nombre = gets.chomp

  print "Ingresa la edad: "
  edad = gets.chomp.to_i

  usuario = { nombre: nombre, edad: edad }
  return usuario
end

3.times do
  usuario = registrar_usuario
  usuarios << usuario
end

usuarios.each do |u|
  if u[:edad] >= 18
    puts "#{u[:nombre]} es mayor de edad."
  else
    puts "#{u[:nombre]} es menor de edad."
  end
end