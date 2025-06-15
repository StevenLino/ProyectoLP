class Tarea
    attr_accessor :titulo, :completada
   def initialize(titulo)
      @titulo = titulo
      @completada = false
   end
   def marcar_como_completada
     @completada = true
   end
   def mostrar
      estado = @completada ? "✔️" : "❌"
      puts "#{estado} #{@titulo}"
   end
end
tareas = [ Tarea.new("Estudiar para el examen"), Tarea.new("Preparar presentación") ]
tareas[0].marcar_como_completada
tareas.each(&:mostrar)