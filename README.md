# PROYECTO-FINAL
Realizado por: Andres Ortiz y Thomas Peña

En este repositorio se encuentran todos requerimientos solicitados en el aula de clase respecto a la entrega del proyecto final, estos son: 
  -  Video introductorio del proyecto
  -  Poster informativo
  -  Codigos de python usados

El enfoque que se le dio a la carroceria del carrito seguidor de linea fue implementar una plancha colgante imantada para que así adquiriese el rol de una grúa portica electromagnetica, la cual esta en capacidad de movilizar el mastil principal en dos aritulaciones independientes y es capaz tambien de recontraer y desplegar el iman colgante.

Para este desarrollo se adquirio:

  -  Pantalla Oled
  -  Camará OV7670
  -  Servomotores
  -  Puente H
  -  Motorreductores
  -  2 Raspberries Pico W
  -  Carroceria
  -  Power Bank

Dado que se hizo uso de 2 Raspberries, una de ellas es controlado por MicroPython y la otra con CircuitPython, esto se debe a un manejo de librerias diferentes entre estos dos formatos y la necesidad de requerir mas pines de las raspberries.

Ademas de ello, se lanzo un servidor web en el cual se realizo una interfaz web capaz de controlar vía remota la grúa mediante botones con acciones previamente preestablecidas, de modo tal que tambien pueden ser evidenciados los movimientos de la grúa en un modelo virtual del carrito creado en Three.JS.

Los protocolos de comunicación utilizados en este proyecto fueron I2C, UART y edición de URL. De forma que el primero fue usado para inicializar y mandar datos a la OLED y a la OV7670, el segundo para comunicar ambas rasberries con el fin de mostrarse al usuario en que estado se encontraba la plancha magnetica y el tercero para comunicar las acciones opturadas por el usuario y la raspberry que controlaba los servomotores

