# mc-scramblor

This is a simple python script for making different versions of a multiple-choice exam in LaTeX.

```
usage: scram.py [-h] [-i] [--save] [--vers VERS] filename [filename ...]

positional arguments:
  filename           files to scramble

optional arguments:
  -h, --help         show this help message and exit
  -i, --interactive  interactive mode
  --save             actually produce output
  --vers VERS        what to call this version (default is 'un'scrambled)
```

Be sure to include the resulting `mcVERS/mcmaster.tex` file _inside_ an `enumerate` environment.

Example:
```
\newcommand{\vers}{VERS}
...
\section*{Multiple Choice}

\begin{enumerate} \setlength{\itemsep}{.5 cm}

  \input{mc\vers/mcmaster.tex}

\end{enumerate}
```
