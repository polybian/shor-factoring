# Simplified explanation

*El algoritmo de Shor sin matemáticas que asusten: cómo una computadora
cuántica factoriza el 15, y por qué eso le quita el sueño a los bancos.*

---

## 🔓 Capítulo 1: El candado más famoso del mundo

Casi todo internet está protegido por un candado llamado **RSA**. Su
seguridad depende de algo muy simple: multiplicar es fácil, pero
**des-multiplicar es dificilísimo**.

Multiplicar 3 × 5 = 15 lo hace un niño. Pero si te doy un número gigante
de 600 dígitos y te pregunto "¿qué dos números lo multiplicaron?", ni
todas las computadoras del mundo juntas lo resuelven en tu vida.

Ese es el candado. Y **el algoritmo de Shor es la llave maestra
cuántica**: una computadora cuántica suficientemente grande podría
factorizar esos números gigantes. Por eso los bancos y gobiernos están
migrando a criptografía post-cuántica *ahora mismo*.

> 🧒 *"¿Y este proyecto rompe los bancos?"*
> No 😄 — factoriza el 15, no un número de 600 dígitos. Pero demuestra
> que el algoritmo funciona de verdad, paso a paso.

---

## 🔄 Capítulo 2: El truco — encontrar el ciclo

Shor no busca los factores directamente. Busca algo más astuto: **el
ciclo** de un número.

Multiplica 7 por sí mismo, una y otra vez, quedándote solo con el resto
al dividir entre 15:

- 7¹ mod 15 = **7**
- 7² mod 15 = **4**
- 7³ mod 15 = **13**
- 7⁴ mod 15 = **1** ← ¡volvimos al 1!

El ciclo mide **4**. Ese número, r = 4, es *el orden* de 7 módulo 15.
Y aquí viene la magia matemática: del ciclo salen los factores.

---

## 🧮 Capítulo 3: Del ciclo a los factores

Con r = 4 en la mano, el resto es aritmética de primaria:

1. Calcula 7^(4/2) mod 15 = 7² mod 15 = **4**
2. p = mcd(4 − 1, 15) = mcd(3, 15) = **3**
3. q = mcd(4 + 1, 15) = mcd(5, 15) = **5**

**15 = 3 × 5** 🎉

Lo único difícil de todo el algoritmo es el paso 1: encontrar el ciclo.
Clásicamente hay que probar multiplicando (para números grandes,
imposible). Cuánticamente se hace con **estimación de fase**.

---

## 🌊 Capítulo 4: La parte cuántica

Imagina que el número 7 módulo 15 es una canción con ritmo de 4 tiempos:
**7, 4, 13, 1, 7, 4, 13, 1…**

La computadora cuántica "escucha" esa canción usando superposición: pone
los 4 tiempos a sonar **a la vez** y usa interferencia para que sobreviva
solo la información del ritmo. Al medir, obtiene fracciones como 1/4,
1/2 o 3/4 — y de ahí se deduce que el ciclo mide 4.

En el proyecto verás el histograma: cuatro picos iguales en las fases
0, 1/4, 1/2 y 3/4. Cada pico es la canción revelando su ritmo. 🎵

---

## ⚙️ Capítulo 5: El circuito "compilado" (honestidad ante todo)

El circuito de este proyecto tiene un atajo: en vez de construir una
máquina general que multiplique cualquier número módulo cualquier N
(eso es dificilísimo), usa una secuencia de compuertas hecha a medida
para **N=15, a=7** — swaps y compuertas X arregladas para que hagan
exactamente "multiplica por 7 módulo 15".

A eso se le dice circuito **compilado**: demuestra la parte cuántica
real (estimación de fase, el corazón del algoritmo) pero se salta la
parte dura de ingeniería (el multiplicador general). Por eso factorizar
el 15 no significa poder factorizar el número de tu banco.

---

## 🏔️ Capítulo 6: Del 15 al RSA-2048 (el abismo)

Para factorizar un RSA-2048 real se necesitarían, según estimaciones
publicadas, unos **20 millones de qubits físicos** con corrección de
errores trabajando horas. Las computadoras cuánticas actuales tienen
~1.000 qubits sin corrección de errores.

El algoritmo está probado. El hardware está a décadas de distancia. Y
ese abismo — decoherencia, fidelidad, corrección de errores — es
exactamente lo que estudia la **ingeniería cuántica**. ⚛️

---

## ▶️ Cómo correrlo

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash run_all.sh
```

Verás el histograma de fases, el orden r = 4 recuperado por fracciones
continuas, y el veredicto final: **15 = 3 × 5**. 🎉
