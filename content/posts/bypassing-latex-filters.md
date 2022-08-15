+++
title = "Bypassing LaTeX Filters"
date = "2021-03-20"
author = "Matthew Toms-Zuberec"
description = "Hacking with LaTeX to pwn your computer. Bypass filters to achieve RCE, read of sensitive files, and more."
+++

---------------------------------------------------------------------------
## Introduction

In this blogpost I will demonstrate a new technique I have discovered that abuses some of LaTeX's functionality to bypass filters and attack web based LaTeX compilers. 

# 

### What is LaTeX?

As stated on the offical website: 
>LaTeX is a high-quality typesetting system; it includes features designed for the production of technical and scientific documentation

It is commonly used in by university/college students and scientist/researchers for writing papers and documents, as its typesetting capabilities allow you to effortlessly use mathematical and scientifc symbols and notation.

# 

### What exactly is exploitable?

LaTeX itself is pretty harmless, but has a few functions that can be especially dangerous in a corporate environment. When converting LaTeX codes to generate documents such as PDF's via ```pdflatex```, things can get risky, especially if it's externally facing, running alongside other applications, or has the potential to access sensitive data.

Out of the box, LaTeX provides the ability to read/write files, and execute commands. In the right hands, this functionality can be of great use to those who need it, but can easliy be taken advantage of for malicious purposes.

# 

### A word on pdflatex security

Obviously, someone realized these functions were a massive security risk, and created 3 operation modes for ```pdflatex```. It should be noted that ```\write18{}``` allows one to execute shell commands.

>```-no-shell-escape```
> Disable the \write18{command} construct, even if it is enabled in the texmf.cnf file.

>```-shell-escape```
>Enable the \write18{command} construct. The command can be any shell command. This construct is normally disallowed for security reasons.

>```-shell-restricted```
>Same as -shell-escape, but limited to a 'safe' set of predefined commands.

#

### Bypassing the filter/blacklist

Regardless of the mode pdflatex is running as, if the command you are trying to use is just blacklisted and not flat out disabled, it can be bypassed with ease. 

The typical bypass that most people use involves **\def**, however, that can easily be stopped/blocked.

The method I have developed today is similar, but much more powerful. We can abuse the ```\catcode`\``` function, and trick LaTex into using the hexadecimal value of a character instead. 

The following example is to read the contents of the file ```secrets.txt``` located in ```/tmp/```, where the ```input``` command is blacklisted.

``` shell
\documentclass{article}

\catcode`\@=7

\begin{document}
\in@@70ut{@@2ftmp@@2fsecrets.txt}
\end{document}
```
#

### How does it work?

To start, it sets the "**@**" character to represent superscript values. We use two of them to tell LaTeX to use the hex value that follows after.

When compiling and generating a PDF, this bypasses the filter, as it only checks for an exact match of the blacklisted word.

The superscript values haven't been translated to regular characters yet, so it slips right under the radar.

Our blacklisted commands then run :)
**— MTZ**

*Checkout [https://seethespread.com](https://seethespread.com)!*
