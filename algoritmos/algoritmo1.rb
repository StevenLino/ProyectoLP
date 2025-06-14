BEGIN { puts "Inicio del script" }
END { puts "Fin del script" }

class Animal
  def initialize(nombre)
    @nombre = nombre
  end

  def hablar
    if @nombre == "Perro"
      puts "Guau"
    elsif @nombre == "Gato"
      puts "Miau"
    else
      puts "Desconocido"
    end
  end
end

animales = [Animal.new("Perro"), Animal.new("Gato")]

for animal in animales
  animal.hablar
end

def saludar
  yield if block_given?
end

saludar { puts "¡Hola desde el bloque!" }

unless animales.empty?
  puts "Hay animales en la lista"
end
