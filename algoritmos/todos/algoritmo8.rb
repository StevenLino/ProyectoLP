clase Usuario   # Error léxico: 'class' mal escrito
   def iniciar(nombre
       @nombre = nombre
   end

   def saludar
       puts "Hola, soy #{@nombre}"
   end
end

persona = Usuario.new("Ana")
x = "5"
y = 3
resultado = x * y # Error semántico: multiplicación string * int no válida en Ruby
persona.saludar!!