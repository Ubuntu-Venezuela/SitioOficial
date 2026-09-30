---
title: "Radio Online Ubuntu-ve"
date: "Thu, 17 Sep 2026 10:47:31 +0000"
type: "noticias"
source: "ubuntu-ve"
thumbnail: "images/seleccic3b3n_001.png"
tags: ["radio"]
---

Hoy tenemos el honor de dirigirnos a ustedes estimados miembros de Ubuntu-ve, la razón por la cual hoy escribimos estas lineas es primero que todo para recordarles nuestro compromiso como miembros activos de nuestra COMUNIDAD en la cual cada uno hacemos vida dentro de esta fraternidad antes mencionada. Es por esto que uno de los principales motivos de este post es incentivarlos a la participación activa de la radio on-line la cual esta a la disposición de todos.


Los miembros que quieran participar en la parrilla de programación deben registrarse en la wiki la cual es la siguiente:


[https://wiki.ubuntu.com/Radio%20Online%20Fraternidad%20Ubuntu%20Venezuela](https://wiki.ubuntu.com/Radio%20Online%20Fraternidad%20Ubuntu%20Venezuela)


...allí deben llenar los datos de postulación, los cuales serán evaluados por el grupo Administrativo de la radio, a fin de cuadrar horarios en la parrilla de programación.  Los programas se dividen en los géneros MUSICAL, INFORMATIVO, INTERACTIVO,  los cuales deben tener un objetivo concreto, y de igual forma deben estar registrados previamente en en grupo “Radio Online Fraternidad Ubuntu Venezuela” su enlace es : [https://launchpad.net/%7Eradio-online-ubuntu-venezuela](https://launchpad.net/~radio-online-ubuntu-venezuela), luego de esto deben esperar que se les notifique acerca de su programa postulado.


Requerimientos Técnicos:


- Configuración de la Distribución:


Primer Paso: Instalación del Jack


apt-get install build-essential jackd qjackctl vorbis-tools alsa libjack-dev libvorbis-dev libogg-dev libmad0-dev \ libsamplerate0-dev libflac-dev libsndfile1-dev libavcodec-dev libavformat-dev libspeex-dev python-gtk2-dev \ python-mutagen checkinstall
Dicho proceso de instalación preguntará si desea dar prioridad de Tiempo Real (RT) a jackd. Se aconseja responder SI, con lo cual se tendrá un sistema de baja latencia de audio.


OJO: si tu computadora tiene un puerto firewire y su tarjeta de sonido es externa y conectada a ese puerto, deberás incluir en el aptitude el paquete “jackd-firewire”


Hecho esto podremos proseguir con el próximo paso:


Segundo Paso: Instalación de IDJC

Esta aplicación es el máster de transmisión el cual puede ser encontrado e instalado directamente por el centro de Software de Ubuntu en caso tal de no encontrarse en en el centro de Software o usar otra distribución debe hacerlo de la forma siguiente:
Compilación del IDJC. Nos descargamos el paquete (para el momento de escribir esto la versión actual es la 0.8.4) desde la página oficial del proyecto:


[http://sourceforge.net/projects/idjc/](http://sourceforge.net/projects/idjc/)


Descomprimimos y compilamos las fuentes. En este caso se usa la versión 0.8.4 del IDJC.


tar xzf idjc-0.8.4.tar.gz
cd idjc-0.8.4
./configure
make
sudo checkinstall

Usando “checkinstall” en vez de “make install” estaremos instalando el paquete y generando un .deb

Tercer Paso: Configurando el Kernel
Para que el JACK pueda trabajar en tiempo real adecuadamente requiere hacer más de un paso.


Primero será necesario unir el usuario un grupo que podrá luego invocar el tiempo real en el kernel.


adduser tu-usuario audio
Luego se debe editar el archivo /etc/security/limits.conf y allí agregar al final estas dos líneas que dan permiso al grupo @audio:


@audio - rtprio 100
@audio - nice -10
@audio - memlock unlimited
“memlock” será la cantidad de memoria que la aplicación puede usar para si misma. Para trabajar con audio se recomiendan 2GB de memoria o más. Este valor se puede expresar numéricamente (en KB) para definir un máximo permitido. Ejemplo:


@audio - memlock 769515
Reiniciar la sesión del usuario es suficiente para tomar los cambios, pero no viene mal en este punto reiniciar.


init 6
Es importante en adelante hacer uso comedido del procesador. Es decir, ver un video y sobretodo si el mismo tiene algún nivel de compresión alto es algo que demanda uso de CPU. Use esta computadora sólo para el IDJC y el JACKD. Si se necesita navegar en internet, se sugiere el uso de una sola ventana y una sola pestaña de navegación.


La manera más sencilla de invocar un servidor con JACK es usando una aplicación llamada **qjackctl**. Para quienes no usen una interfaz gráfica, el servidor puede ser levantado con las opciones que se deseen desde el intérprete de lineas de comando.


El nombre de QJACKCTL es definido por CTL (que significa Control) del servidor JACK y que está hecho con librerías gráficas QT, por eso la Q al principio.


Al invocar QJACKCTL tendremos una pantalla como esta:





[http://elubuntazo.files.wordpress.com/2011/09/seleccic3b3n_001.png](
![](http://elubuntazo.files.wordpress.com/2011/09/seleccic3b3n_001.png)
)


Antes de darle a INICIAR, tenemos que verificar que su configuración sea correcta. en SETUP.


Para ello tendremos que asegurarnos de varias configuraciones antes. Lo primero es que para que funcione todo en TIEMPO REAL, es necesario que nuestro kernel soporte tal cosa, de lo contrario dará errores. Se sugiere la primera vez no activar esta opción.


[http://elubuntazo.files.wordpress.com/2011/09/seleccic3b3n_002.png](
![](http://elubuntazo.files.wordpress.com/2011/09/seleccic3b3n_002.png)
)


Otras dos configuraciones son importantes y darán finalmente la latencia con la cual trabajaremos. Brevemente, “latencia” significa retardo, y es en este caso el retardo que tendrá el sonido desde que entra al sistema hasta que sale del mimso. Evidentemente, mientras menos retardo será mejor. La combinación de la FRECUENCIA DE MUESTREO (se recomienda no mover de 44.100 Hz), los CUADROS/PERÍODO y los PERIODOS/BUFFER darán como resultado la latencia resultante. A mayor latencia menor uso del procesador: a menor latencia mayor consumo de procesador y viceversa


Ahora, que ya está el JACK levantado (le hemos dado PLAY al qjackctl y no ha dado error) es cuando abrimos el IDJC. Es importante mantener este orden. IDJC no funcionará bien sin JACK levantado.


Emanuel Torres (Lord system)