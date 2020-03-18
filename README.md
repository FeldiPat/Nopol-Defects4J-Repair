# Nopol-Defects4J-Repair
This repository contains the source code and the experimental results of the repair of Nopol on a subset of the Defects4J dataset. The subset consists of four open-source projects: Apache Commons Math 1 (106 bugs), Apache Commons Lang 2 (65 bugs), Jfreechart 3 (26 bugs) and Joda-time 4 (27 bugs). 

The experiment is an adaption of the analysis done by Matias Martinez, Thomas Durieux, Romain Sommerard, Jifeng Xuan and Martin Monperrus ([Automatic Repair of Real Bugs in Java: A Large-Scale Experiment on the Defects4J Dataset](https://hal.archives-ouvertes.fr/hal-01387556/document")). 

# Getting Started

1. Download the [Defects4J dataset](https://github.com/rjust/defects4j).
2. Follow the Defects4J [Getting Started](https://github.com/rjust/defects4j#getting-started). 
3. Export Defects4J into your PATH: ```PATH=$PATH:~/<defects4j_path>/framework/bin```
4. Checkout all bugs
```bash
for bug in $(seq 1 26); do defects4j checkout -p Chart -v ${bug}b -w ~/projects/chart/chart_${bug}; done
for bug in $(seq 1 65); do defects4j checkout -p Lang -v ${bug}b -w ~/projects/lang/lang_${bug}; done
for bug in $(seq 1 106); do defects4j checkout -p Math -v ${bug}b -w ~/projects/math/math_${bug}; done
for bug in $(seq 1 27); do defects4j checkout -p Time -v ${bug}b -w ~/projects/time/time_${bug}; done
```
5. Edit the Defects4J-repair config: ```src/python/core/Config.py```
6. Run ```src/python/repair.py```
7. To process results run ```src/python/processResults.py```

# Repair Arguments

```bash
usage: src/python/repair.py [-h] -project PROJECT -tool MODE -id ID

arguments:
  -h, --help        shows help message
  -project PROJECT  Which project (math, lang, time, chart, all)
  -mode MODE        Which repair mode (ranking, conditional, precondition)
  -id ID            Bug id
```
