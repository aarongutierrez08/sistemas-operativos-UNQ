# grupo 8

### Integrantes:

| Nombre y Apellido              |      Mail                      |     usuario Gitlab   |
| -----------------------------  | ------------------------------ | -------------------  |
| Aaron Gutierrez                | aarongastongutierrez@gmail.com | aarongasgu           |  
|                                |                                |                      |


## Entregas:

### Práctica 0: **Ok**
 - [Historia de los Sistemas Operativos](https://gitlab.com/so-unq-2022-s2/grupo_8/-/blob/main/practicas/practica_0/Historia_SOs.md)

### Práctica 1: **Aprobado**
 - [Batch](https://gitlab.com/so-unq-2022-s2/grupo_8/-/tree/main/practicas/practica_1)

### Práctica 2: **Aprobado**
 - [Kill Interruption](https://gitlab.com/so-unq-2022-s2/grupo_8/-/tree/main/practicas/practica_2)

### Práctica 3: **Aprobado**
 - [Multiprogramación](https://gitlab.com/so-unq-2022-s2/grupo_8/-/tree/main/practicas/practica_3)



- Loader: (esta bien) https://gitlab.com/so-unq-2022-s2/grupo_8/-/blob/main/practicas/practica_3/so.py#L106

(para no andar haciendo tantas sumas y restas sobre _lastMemoryDir)
 si te lo guardas al comenzar, y vas incrementando de a 1 en el for, te queda mas simple  
 -- No lo tenes que cambiar, es solo "feedback" --
 
```
 baseDir = self._lastMemoryDir
for index in range(0, progSize):        
    HARDWARE.memory.write(self._lastMemoryDir, inst)
    self._lastMemoryDir = self._lastMemoryDir + 1
return baseDir
```




- PCBTable:
getNewPID(): https://gitlab.com/so-unq-2022-s2/grupo_8/-/blob/main/practicas/practica_3/so.py#L182
siempre debe retornar un ID distinto... (hagas un addPCB o no )
lo correcto seria  poner la linea que incrementa _newPID en el getNewPID : https://gitlab.com/so-unq-2022-s2/grupo_8/-/blob/main/practicas/practica_3/so.py#L170

- Kill:  https://gitlab.com/so-unq-2022-s2/grupo_8/-/blob/main/practicas/practica_3/so.py#L224
 no es necesario porque lo hace el dispatcher: https://gitlab.com/so-unq-2022-s2/grupo_8/-/blob/main/practicas/practica_3/so.py#L124
- IoIn: https://gitlab.com/so-unq-2022-s2/grupo_8/-/blob/main/practicas/practica_3/so.py#L257
idem al Kill

los cambios marcados aca (PCBTable, Kill, IoIn), los podes aplicar directamente en la P4 o P5.


### Práctica 4:  **Aprobado** 
- [Schedulers](https://gitlab.com/so-unq-2022-s2/grupo_8/-/tree/main/practicas/practica_4)

 hay que aplicar las correciones de la P3 antes de entregar la P5
(las correciones las haces en la P5 directamente... no es necesario que actualizes la P3)

- [Paginación](https://gitlab.com/so-unq-2022-s2/grupo_8/-/tree/main/practicas/practica_5)

*Las correciones fueron hechas en la P5 y ya esta subida para entregar (con Gantt incluido).*


### Práctica 5: **Aprobado**

**Diagrama de Gantt aplicado en la Práctica 5**


### Extra:

- [Shell](https://gitlab.com/so-unq-2022-s2/grupo_8/-/tree/main/practicas/practica_5/shell.py)

**Shell aplicada en la práctica 5**
