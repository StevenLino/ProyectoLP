=begin
Este programa define una clase base Persona,
y una subclase Estudiante que hereda sus
propiedades.
=end

class Persona
  attr_accessor :nombre, :edad

  def initialize(nombre, edad)
    @nombre = nombre
    @edad = edad
  end

  def presentarse
    puts "Hola, soy #{@nombre} y tengo #{@edad}
años."
  end
end

class Estudiante < Persona
  attr_accessor :curso

  def initialize(nombre, edad, curso)
    super(nombre, edad)
    @curso = curso
  end

  def presentarse
    super
    puts "Estudio en el curso #{@curso}."
  end
end

alumno = Estudiante.new("Carlos", 20, "Ruby101")
alumno.presentarse