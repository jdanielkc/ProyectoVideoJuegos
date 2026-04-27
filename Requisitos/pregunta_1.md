# Pregunta 1

## Enunciado

Complemente el programa entregado en el ejercicio anterior con la siguiente funcionalidad:

- Agregue un texto para dibujar un título en la pantalla principal del juego
- Agregue un evento extra para pausar y reanudar el juego con la tecla "P". Debe de mostrar un texto que indica que el juego está pausado
- Cargue efectos de sonido para las colisiones y para el movimiento del personaje.
- Haga sonar los efectos de sonido en los momentos adecuados
- Use los patrones ServiceLocator para cargar los recursos de sonido, imagen y texto que necesite

## Personalización del juego

Esta es la oportunidad para hacer el juego propio, con características propias que deseen. Deben implementar aunque sea una característica única. Las condiciones para la característica son:

- Que use un elemento de input del teclado o el ratón
- Que sea temporal y requiera "recargar"
- Que tenga algún elemento visible que sea diferente de los actuales.
- Que la opción de recargar se vea ya sea en una barra de carga o en un número en forma de texto desplegado en la pantalla
- Se espera que apliquen los elementos de gamefeel en este efecto especial (en resumen, hagan que se sienta bien)
- Se esperan instrucciones de input muy simples en forma de texto en la pantalla

No hay una regla para el efecto que deseen crear. pero si necesitan ayuda, aquí hay un par de sugerencias.

- Una defensa especial por 2 segundos activados por una tecla o el ratón. Durante esos 2 segundos, todos los enemigos a una distancia menor a dU serán eliminados. Una vez usada, la defensa no puede activarse por 5 segundos.
- Una ataque especial activado con una tecla o el ratón. El ataque divide una bala en cuatro que disparan en las diagonales de la bala. Una vez usado, el ataque especial no puede usarse por 2.5 segundos. (Demostrado en el proyecto de ejemplo)

## Distribución

Finalmente, suba el juego a itch.io, ya sea en despliegue web o en despliegue de ejecutable descargable y adjunte un archivo README.txt con el enlace dentro de la entrega.

Aquí pueden ver un ejemplo de un potencial producto terminado usando una de las sugerencias:
(SEMANA CUATRO - EJERCICIO - RESULTADO WEB)

https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2026-12/

No tienen que usar esto como plantilla de ejemplo. si desean hacer otro efecto o especial personalizado ¡Son bienvenidos y de hecho, se promueve hacerlo!

## Detalles de recursos

Este proyecto va a utilizar recursos de imagenes y sonidos Estos recursos los pueden encontrar aquí:
(SEMANA CUATRO - EJERCICIO - RECURSOS PARA VERIFICACIÓN)

https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2026-12/

## Detalles de configuración

Solamente existe un cambio nuevo en los archivos de configuración actuales:

### Sonidos

Los sonidos se encuentran asociados a cada entidad que los necesite, con el parámetro sound.

Los asteroides, las balas y las explosiones tienen un sonido cuando aparecen en la pantalla. Los enemigos de tipo Hunter únicamente tiene un sonido tiene un sonido llamado sound_chase , que se activa cuando comienza a perseguir al jugador.

### Interfaz

La configuración de la interfaz se establece en un archivo de su creación llamado interface.json. Este archivo contiene propiedades de texto fijo, la cuales son:

- La ruta de recurso de fuente tipo .ttf, que debe ser cargado usando el patrón Service Locator.
- Una cadena de caracteres que indica el contenido texto
- El color del texto
- Un tamaño del texto

No hay una especificación de cómo está construido este archivo. La estructura y ordenamiento del mismo es a su discreción. El único requerimiento es que exista y lo usen para procesar las propiedades básicas de sus textos.

### Personalización

Para los detalles de personalización no se provee ningún archivo de configuración dedicado. Se espera que ustedes creen esos archivos de configuración, si lo ven necesario.

## Detalles de implementación

Los elementos más importante que se recomiendan crear son los siguientes:

- Una clase de ServiceLocator, que guarde los servicios de carga de sonidos, imágenes, fuentes, etc.
- Los servicios individuales deben tener métodos específicos para cada clase.
- Los textos en pygame son superficies y se  recomienda modificar el componente de superficie para poder crear a partir de texto, colores y fuentes.
- Para crear texto estático solo se requiere un método de clase llamado from_text para obtener una superficie a partir de texto.
- Un texto dinámico requiere de recrear la superficie de fuente desde cero fon font.render(texto, color). Es decir que un texto que cambie debe hacer esto dentro de un sistema que ejecuta la función de font.render con el texto adecuado y reemplazar la superficie y el área del componente.

La personalización es individual y depende de lo que deseen lograr. Sin embargo, como objetivo de este curso se requiere ejercer al patrón ECS de principio a fin.

Para pausar y reanudar un juego en ECS, simplemente deben considerar ejecutar o no los sistemas pertinentes en pausa. Sin un sistema de movimiento, nada se mueve o sin un sistema de colisión, nada "choca".

## Detalles de recursos

En esta dirección se encuentran los recursos necesarios para este proyecto:
(SEMANA CUATRO - EJERCICIO - RECURSOS PARA VERIFICACIÓN)

https://misw-4407-desarrollo-de-videojuegos.github.io/web-cohorte-2026-12/

Puesto que hay un componente de personalización, es bienvenido el uso libre de recursos.

Aquí hay varios sitios recomendados para conseguir recursos libres o gratis (importante siempre revisar la licencia de lo que consigan si requiere de créditos o pagar por lo que descarguen):

- https://opengameart.org/
- https://kenney.nl/
- https://freesound.org/
- https://indiegamemusic.com/

## Entrega y rúbricas

Suba el archivo ZIP del proyecto entero con el programa funcionando con las especificaciones establecidas. El archivo ZIP también debe contener un archivo de texto README.txt con el enlace a itch.io del juego compilado.

La siguiente rúbrica presenta las dimensiones que se tendrán en cuenta en la revisión del ejercicio.

| Dimensión | Peso | Deficiente | Regular | Muy bien | Excelente |
| --- | --- | --- | --- | --- | --- |
| Funcionamiento básico | 10% | No entrega | El programa no ejecuta o tiene errores de ejecución. | El programa ejecuta, pero tiene problemas internos de ejecución. | El programa ejecuta correctamente. |
| Carga y despliegue de sprites y sonidos | 10% | No entrega | El programa no usa sonidos ni sprites ni fuentes | El programa carga recursos, pero de una manera deficiente | El programa carga correctamente los recursos |
| Carga y despliegue de texto y fuentes | 10% | No entrega | El programa no carga textos de ningún tipo | El programa no carga texto correctamente o no corresponden al estado del juego | El programa carga correctamente textos |
| Pausar y reanudar el juego | 10% | No entrega | El programa no pausa | El programa pausa pero no muestra ningún texto de pausa o no se puede reanudar | El programa pausa y reanuda correctamente y muestra un texto de pausa |
| Patrón Service Locator | 20% | No entrega | El programa no ua el patrón Service Locator | El programa no usa completamente el patrón Service Locator | el programa usa completamente el patrón Service Locator |
| Característica única del juego | 20% | No entrega | No se entrega una nueva característica única del juego | La característica única no usa todos los elementos exigidos correctamente o no usa el patrón ECS | La característica única se despliega correctamente junto con el uso del patrón ECS. |
| Publicación en itch.io | 20% | No entrega | El programa no está publicado en itch.io |  | El programa está publicado en itch.io listo para jugar o descargar #codebase |
