import simpy
import random 

def procesos(nombre,env,cpu,memoria):


        llegada_de_proceso = random.expovariate(1.0/1)
        print(nombre,'tiempo a esperar',llegada_de_proceso )
        yield env.timeout(llegada_de_proceso)

        memoria_pedida = random.randint(1,10)
        instrucciones = random.randint(1,10)
        print('%s memoria pedida fue %d' %(nombre,memoria_pedida))
        yield env.timeout(memoria_pedida)
        tiempo = env.now

        flag = True
        while(flag):
                if memoria.level >= memoria_pedida:
                        yield memoria.get(memoria_pedida)
                        print('%s Entro a READY ' % nombre)
                        flag = False
                else:
                        print('%s Esperando READY' % nombre)
                        yield env.timeout(memoria_pedida)


        while(instrucciones!=0):
                print ('%s Esta en ready' % nombre)
                with cpu.request() as turno:
                        yield turno
                        print ('%s esta procesando' %nombre)
                        yield env.timeout(instrucciones)
                        if(instrucciones == 0):
                                break
                        else:
                                instrucciones = instrucciones - 3
                                if (instrucciones<0):
                                        instrucciones=0
                        print('%s salio del procesador' %nombre)

                if(instrucciones >0):
                        estado = random.randint(1,2)
                        if(estado == 1):
                                print ('%s entro a waiting'%nombre)
                                yield env.timeout(estado)
        print('%s ha terminado'%nombre)
        print ('Restaura: %d' %memoria_pedida)
        yield memoria.put(memoria_pedida)
        print (env.now)
        tiempo_promedio = (env.now/(i+1.0))
        print ('Tiempo: %d'%tiempo_promedio)
        print (tiempo_promedio)
        

env = simpy.Environment()
cpu = simpy.Resource(env,capacity = 2)
memoria = simpy.Container(env, 100, init = 100)
random.seed(10)
for i in range(200):
        env.process(procesos('Proceso %d'%i,env,cpu,memoria))

env.run(until = 10000)


