#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

#torre kill monkey
pilas = pilasengine.iniciar()
pilas.fondos.Cesped()
TIEMPO = 6
fin_de_juego = False

# Usar un fondo estándar
# Añadir un marcador
puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
puntos.magnitud = 40
# Añadir el conmutador de Sonido
pilas.actores.Sonido()

# Variables y Constantes
balas_simples = pilas.actores.Bala
monos = []

# Funciones
# Actualizar el marcador con un efecto bonito

def crear_mono():
    # Crear un enemigo nuevo
    enemigo=pilas.actores.Mono()
    efecto_bonito=random.uniform(0.25, 0.75)
    enemigo.escala=[0.75,efecto_bonito, 1, ]
    enemigo.rotacion=[360]
    # Hacer que se aparición sea con un efecto bonito
    enemigo.escala = .5
    ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
    # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
    enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Situarlo en una posición al azar, no demasiado cerca del jugador
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    # Dotarlo de un movimiento irregular más impredecible
    tipo_interpolacion = ['lineal',
                            'aceleracion_gradual',
                            'desaceleracion_gradual',
                            'rebote_inicial',
                            'rebote_final']
    
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    #enemigo.x = pilas.interpolar(0,tiempo,tipo=random.choice(tipo_interpolacion))
    #enemigo.y = pilas.interpolar(0, tiempo,tipo=random.choice(tipo_interpolacion))
    # Añadirlo a la lista de enemigos
    monos.append(enemigo)


    if  random.randrange(0,20)>15:
        if torreta.municion!=pilasengine.actores.Misil:
            estrella=pilas.actores.Estrella(x, y)
            estrella.escala=[1,0,1],.1
            pilas.colisiones.agregar(estrella,torreta.habilidades.DispararConClick.proyectiles,asignar_arma_mejorada)
            pilas.tareas.agregar(3, eliminar_estrella, estrella)
    # Permitir la creación de enemigos mientras el juego esté en activo
    if fin_de_juego:
        return False
    else:
        return True

def mono_destruido(disparo,enemigo):
    enemigo.eliminar()
    disparo.eliminar()
    puntos.aumentar()
    puntos.escala=[1,0,5,1]
    
def fin_juego(torreta, enemigo):
    global fin_de_juego
    enemigo.sonreir()
    torreta.eliminar()
    
    fin_de_juego = True
    pilas.avisar("Tu puntaje fue %d puntos"%(puntos.obtener()))
    pilas.actores.Texto("JUEGO TERMINADO")


def asignar_arma_simple():
    torreta.municion=pilasengine.actores.Bala

def asignar_arma_mejorada(estrella, proyectil):
    global torreta
    torreta.municion=pilasengine.actores.Estrella
    estrella.eliminar()
    pilas.tareas.agregar(10, asignar_arma_simple)
    pilas.avisar("MEJORA DE MUNICION")

def eliminar_estrella(estrella):
    estrella.eliminar()
    
	

# Añadir la torreta del jugador

torreta = pilas.actores.Torreta(enemigos=monos, cuando_elimina_enemigo=mono_destruido)
torreta.municion=pilasengine.actores.Bala




pilas.tareas.agregar(1, crear_mono)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja


pilas.colisiones.agregar(torreta, monos, fin_juego)
pilas.ejecutar()
