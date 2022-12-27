# RESUMEN DE LA HISTORIA DE LOS SISTEMAS OPERATIVOS
## Sistemas Operativos Modernos - Tanenbaum

## La primera generación (1945 a 1955): tubos al vacío
Las primeras computadoras digitales fueron creadas utilizando tubos al vacío, cerca de
1945. Estas computadoras eran manipuladas por un grupo de personas sin importar su especialización.
Se realizaba un trabajo agotador solo para la programación de cálculos simples.
Luego aparecieron las tarjetas perforadas que mejoro un poco la rutina, mediante la lectura de estas.
 
## La segunda generación (1955 a 1965): transistores y sistemas de procesamiento por lotes
A mediados de 1950, con la tecnología de transistores, las computadoras se empezaron a
comerciar solo con grandes empresas, universidades y agencias gubernamentales, ya que eran muy
caras. Su uso requería que un programador escriba en papel en FORTRAN o lenguaje ensamblador, el
programa, o los programas, y luego se pasaba a tarjetas perforadas.
Mediante el sistema de procesamiento por lotes y una estructura típica de trabajo que seguía
el programador, como por ejemplo indicar en una tarjeta al sistema operativo que compilador
cargar, se logró reducir costos.
 
## La tercera generación (1965 a 1980): circuitos integrados y multiprogramación
Para que una misma computadora pueda hacer diferentes trabajos, IBM introdujo la familia
de computadoras 360 utilizando circuitos integrados a pequeña escala. Estas tenian software compatible 
entre sí y variaban en precio y rendimiento. La compatibilidad entre todas las computadoras no fue 
fácil ya que el software debía soportar todos los diferentes usos y entornos.
Una de las técnicas claves de esta generación fue la multiprogramación (a partir de particionar
la memoria en varias piezas), evitando esperar que termine un trabajo para empezar otro y,
así, evitando la inactividad por mucho tiempo.
Otra técnica importante fue el spooling, leyendo trabajos y guardandolos en el disco de manera
que podía ejecutar trabajos nuevos rápidamente.
Mediante timesharing los programadores podían compartir la CPU y esta asignarles turnos para
su uso y así obtener un tiempo rápido de respuesta para, por ejemplo, depurar.
En esta generación se desarrollaron minicomputadoras que eran mucho menos costosas y suficientemente
eficientes. En una PDP-7, una minicomputadora, Ken Thompson, escribió una versión simple de
MULTICS (un sistema multiplexado para muchas computadoras), pero para un solo usuario, convirtiéndose
luego en UNIX. Como UNIX era de código fuente abierto, se desarrollaron en él varias versiones propias.
El autor también creó MINIX, siendo una versión menor y de fines educativos. Un estudiante finlandés,
llamado Linus Torvalds, uso MINIX para escribir el conocido Linux.
 
## La cuarta generación (1980 a la fecha): las computadoras personales
El chip microprocesador, construido a partir de circuitos integrados a gran escala, logró que
un individuo tuviera su propia computadora personal. Kildall construyó CP/M un SO para microcomputadoras.
Bill Gates compró DOS a Tim Paterson, un sistema operativo en disco y ofreció a IBM un paquete de DOS/BASIC para
su IBM PC. Esto fue un éxito debido a que Gates vendió MS-DOS (el SO rediseñado por Paterson para IBM) a empresas
y no a usuarios finales como Kildall.
En la década de 1960, Doug Engelbart inventó la Interfaz Gráfica de Usuario GUI. Steve Jobs construyó
la Apple Macintosh con una GUI, siendo esta user-friendly. Influenciado por esto, Microsoft produjo
Windows también basado en GUI. Windows estaba basado en MS-DOS pero en 1995 se creó el SO Windows 95,
que fue actualizando hasta llegar a Windows Vista.
El otro competidor es UNIX, siendo fuerte en servidores, aunque haciendo cada vez más presencia en PCs
de escritorio. En UNIX, muchos usuarios programadores, prefieren una línea de comando en vez de una GUI.
