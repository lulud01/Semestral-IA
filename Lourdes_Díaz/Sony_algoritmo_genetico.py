import retro
import pygame
import json
import os.path as path 
import random
from pygame.locals import *

largo = 10000 #La longitud del material genetico de cada individuo
num = 100 #La cantidad de individuos que habra en la poblacion
pressure = 50 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutation_chance = 0.3 #La probabilidad de que un individuo mute
valor_estatico = 0

def crea_genes():#["B",                "A",               "MODE",        "START",         "UP",          "DOWN",           "LEFT",             "RIGHT",             "C",           "Y",             "X",            "Z"]
    return (random.randint(0,1), valor_estatico, valor_estatico, valor_estatico, valor_estatico, valor_estatico, random.randint(0,1), random.randint(0,1), valor_estatico, valor_estatico, valor_estatico, valor_estatico)

def crearPoblacion():
    
    if path.exists('population.txt'):
       poblacion = []
       archivo = open("population.txt", "r")
       datos = archivo.read()
       archivo.close()
       poblacion = json.loads(datos)
       return poblacion
    
    else:
        poblacion = []
        for i in range(num):
            individuo = dict()
            individuo['movimientos'] = []
            individuo['fitness'] = 0
            for j in range(largo):
                individuo['movimientos'].append(crea_genes())
            poblacion.append(individuo)
        return poblacion
        
        


def seleccion_crossover_por_punto(population):
    puntuados = [ [i['fitness'], i] for i in population] 
    puntuados = [i[1] for i in sorted(puntuados)]       
    population = puntuados   
    
    selected =  puntuados[(len(puntuados)-pressure):] 
   
    for i in range(len(population)-pressure):
        punto = random.randint(1,largo-1) 
        padre = random.sample(selected, 2) 
        population[i]['movimientos'][:punto] = padre[0]['movimientos'][:punto] 
        population[i]['movimientos'][punto:] = padre[1]['movimientos'][punto:]
        
    
    datos = json.dumps(poblacion)
    f = open('population.txt', 'w')
    f.write(datos)
    f.close()
    print (len(population))
  
    for i in range(len(population)-pressure):
        if random.random() <= mutation_chance: 
            punto = random.randint(1,largo-1)    
            population[i]['movimientos'][punto] = crea_genes() 
        
  
    return population

      
def evaluar_poblacion(env, poblacion):
       
    for individuo in poblacion:
        _obs = env.reset() 
        for action in individuo['movimientos']:
            env.render()
            video_size = env.observation_space.shape[1], env.observation_space.shape[0]
            screen = pygame.display.set_mode(video_size)
            _obs, _rew, done, _info = env.step(action)
            if _info['lives'] < vidas:
                continue
            if done:
                break
            individuo['fitness'] = _info['x']    
        print (individuo['fitness'])
    return poblacion
        
       
env = retro.make(game='SonicTheHedgehog-Genesis', state='StarLightZone.Act2') 
fitness = 0
poblacion = crearPoblacion()
vidas = 3

    
for i in range (1000):
    poblacion = evaluar_poblacion(env, poblacion)
    poblacion = seleccion_crossover_por_punto(poblacion)
    
      


