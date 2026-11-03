# quatro-quadrados

Todo número inteiro positivo é soma de no máximo **quatro** quadrados.

```
7  = 2² + 1² + 1² + 1²     precisa dos quatro
6  = 2² + 1² + 1²          três bastam
5  = 2² + 1²               dois bastam
9  = 3²                    um basta
```

Lagrange provou isso em 1770. A pergunta que sobra é **quantos** números realmente
precisam dos quatro — e a resposta é exatamente **um sexto** deles.

Este repositório não usa fórmula nenhuma para decidir: ele **procura** o mínimo de
quadrados de cada número, e só depois compara o resultado com a forma fechada, que é o
juiz e não o método.

```bash
python -m unittest discover -s testes -t . -v   # 18 testes
python -m ferramentas.medidor                   # todas as tabelas
python -m ferramentas.medidor --completo        # até 200 mil (job próprio)
```

Python 3.11+, sem dependência nenhuma fora da biblioteca padrão.

## A conta até 20.000

```
mínimo   quantos   fatia
1        141       0,7050%
2        5.117     25,5850%
3        11.411    57,0550%
4        3.331     16,6550%
```

**Nenhum número precisou de cinco.** Isso é o teorema de Lagrange, e aqui ele foi
conferido número a número em vez de assumido — há um teste que enumera as representações
de quatro quadrados de todo `n` até 600 e exige que a lista nunca venha vazia.

Os 141 que precisam de um só são exatamente os **quadrados perfeitos** até 20.000 — e
`141² = 19.881`, enquanto `142² = 20.164` já passa.

E a maioria absoluta — **57%** — precisa de exatamente três.

## Um sexto, e já nasce assim

```
faixa                quantos   fatia
1 a 2.000            332       0,16600
2.001 a 4.000        333       0,16650
4.001 a 6.000        333       0,16650
6.001 a 8.000        334       0,16700
...
18.001 a 20.000      334       0,16700

no total        : 0,166550
previsto por 1/6: 0,166667
diferença       : 0,000117
```

A fatia **não converge para 1/6**: ela já está lá desde a primeira faixa, e fica. Cada
bloco de dois mil inteiros tem 332, 333 ou 334 números que precisam dos quatro quadrados.

## De onde vem o sexto

Um número precisa de quatro quadrados exatamente quando se escreve como `4^a · (8b + 7)`
— é o teorema dos três quadrados, de Legendre. Separando os achados pelo expoente `a`:

```
a    quantos   fatia
0    2.500     75,05%
1    625       18,76%
2    156       4,68%
3    39        1,17%
4    9         0,27%
5    2         0,06%
```

`2500 → 625 → 156 → 39`: **cada potência de quatro contribui com um quarto da anterior**.
Os ímpares congruentes a 7 módulo 8 são um em cada oito; multiplicando por 4, por 16, por
64, a série fica

```
1/8 + 1/32 + 1/128 + ... = (1/8) / (1 − 1/4) = 1/6
```

A tabela não foi construída a partir dessa conta — ela é a contagem bruta, e a conta
explica o que ela mostrou.

## As três conferências

```
a busca x a forma fechada de Legendre  : 5.000 números conferidos
toda representação soma mesmo o número : 5.000 conferidas
todo número cabe em quatro quadrados   : 400 conferidos por enumeração
```

A primeira é a que importa: a busca, que não conhece teorema nenhum e simplesmente tenta
um, dois e três quadrados antes de desistir, concorda com `4^a(8b+7)` em cinco mil casos
seguidos.

## O que as medidas me corrigiram

**Esperei a fatia convergir.** Escrevi a tabela por faixa imaginando ver um número subindo
devagar até 1/6. Ele já está em 0,166 na primeira faixa de dois mil e fica lá. Densidade
assintótica aqui não é um limite que se aproxima — é uma proporção que vale localmente,
porque a condição `4^a(8b+7)` é periódica.

**Achei que os que precisam de quatro fossem raros.** Um em cada seis é muito: são 3.331
números em vinte mil, contra 141 quadrados perfeitos. O caso "difícil" do teorema aparece
**vinte e três vezes mais** que o caso mais fácil de todos, e não é exceção nenhuma — é
17% de tudo.

**`math.sqrt` teria mentido no teste de quadrado perfeito.** Com `int(math.sqrt(n))`,
números acima de 2⁵³ começam a errar o último dígito e quadrados perfeitos deixam de ser
reconhecidos. Tudo usa `math.isqrt`, e um teste confere isso em `10²⁰`.

**A busca do mínimo tinha um `return 4` sem prova.** Depois de tentar um, dois e três
quadrados, o código devolve 4 porque Lagrange garante. Isso é confiar num teorema dentro
do programa que deveria medi-lo. A conferência `conferir_lagrange` existe por causa disso:
ela **enumera** as representações de quatro quadrados e exige que existam, em vez de
assumir que existem.

## Quatro achados

1. **Nenhum número entre 1 e 20.000 precisou de cinco quadrados** — e isso foi conferido
   por enumeração, não assumido do teorema.
2. **Exatamente um sexto dos inteiros precisa dos quatro**, e a fatia **não converge**:
   ela já vale 0,166 na primeira faixa de dois mil e fica lá.
3. Entre os que precisam de quatro, **cada potência de 4 contribui com um quarto da
   anterior** — 2.500, 625, 156, 39, 9, 2 — e é essa série geométrica que soma 1/6.
4. A maioria absoluta dos números, **57,06%**, precisa de exatamente **três** quadrados —
   são 11.411, mais que os de um, dois e quatro **somados** (8.589).
