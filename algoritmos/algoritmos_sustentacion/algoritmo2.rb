# Ángel: Validación de unless, case, clases, rangos, funciones sin paréntesis y control de flujo

# Unless
edad = 16
unless edad >= 18
  puts "No puede votar"
end

# Case
clima = "lluvioso"
case clima
when "soleado"
  puts "Lleva gafas"
when "lluvioso"
  puts "Lleva paraguas"
else
  puts "Consulta el clima"
end

# Clase y objeto
class Animal
  def hablar
    puts "Hola soy un animal"
  end
end

gato = Animal.new
gato.hablar

# Bucle con break y next
def bucle
  i = 0
  while i < 5
    i += 1
    if i == 2
      next
    elsif i == 4
      break
    end
    puts i
  end
end

# Función sin paréntesis
def saludar nombre
  puts "Hola, #{nombre}"
end

