# File Searcher

## Enunt
Implementați un script care implementează funcționalitatea comenzii “find” din linux.

## Overview

`File Searcher` Este un proiect realizat in cadrul cursului de programare in Python, in care am implementat o versiune simplificata a comenzii `find` din Linux. Programul permite cautarea fisierelor si directoarelor in functie de diferite criterii, precum numele, tipul, dimensiunea si timpul de creare, modificare si accesare . Rezultatele cautarii pot fi afisate atat in consola cat si redirectionate catre un fisier de output. De asemenea, cautarea poate fi realizata recursiv, incepand de la un director specificat. Mai mult, mai multe expresii de cautare pot fi combinate pentru a crea interogari complexe.

## Features

- **Criterii de cautarer:** Cauta fisiere si directoare in functie de diferite criterii, precum numele, tipul, dimensiunea si timpul de creare, modificare si accesare.

- **Output:** Afiseaza rezultatele cautarii in consola sau le redirectioneaza catre un fisier de output fie prin suprascriere fie prin concatenare.

- **Cautare recursiva:** Cauta fisiere si directoare recursiv, incepand de la un director specificat.

- **Expresii complexe:** Mai multe expresii de cautare pot fi combinate pentru a crea interogari complexe.

## Utilizare

### Basic Usage

```bash
python find.py [start_directory] [expression] { [ > / >> output_file] }
```

- `start_directory` - directorul de unde incepe cautarea `.` pentru directorul curent sau `start_directory` pentru un director specificat
- `expression` - expresia de cautare de forma `-option argument`
- `output_file` - fisierul de output
- `>` - suprascrie fisierul de output
- `>>` - concateneaza la fisierul de output

### Options

- `-name` - cauta fisiere si directoare dupa nume
  - poate fii numelui exact sau o expresie regulata

- `-type` - cauta fisiere si directoare dupa tip
  - `f` - fisier
  - `d` - director
- `-size` - cauta fisiere si directoare dupa dimensiune
  - `mn` - dimensiunea mai mare decat n
  - `ln` - dimensiunea mai mica decat n
  - `en` - dimensiunea egala cu n
- `-ctime` - cauta fisiere si directoare dupa timpul de creare
  - `n` - daca timpul de creare este mai vechi de n secunde
- `-mtime` - cauta fisiere si directoare dupa timpul de modificare
  - `n` - daca timpul de modificare este mai vechi de n secunde
- `-atime` - cauta fisiere si directoare dupa timpul de accesare
  - `n` - daca timpul de accesare este mai vechi de n secunde

### Exemple de utilizare

```bash
python find.py . -name file.txt
```
Cauta fisiere si directoare cu numele `file.txt` incepand de la directorul curent.

```bash
python find.py . -name file.txt > output.txt
```
Cauta fisiere si directoare cu numele `file.txt` si redirecteaza rezultatele in fisierul `output.txt` incepand de la directorul curent.

```bash
python find.py myDirectory -name file.txt -ctime 100
```
Cauta fisiere si directoare cu numele `file.txt` care au fost create mai tarziu de 100 de secunde incepand de la directorul myDirectory.

```bash
python find.py . -name *.txt -mtime 100 -size m100 -type f
```
Cauta doar fisiere cu numele `*.txt` cu dimensiunea mai mare de 100 bytes care au fost modificate mai tarziu de 100 de secunde incepand de la directorul curent.
