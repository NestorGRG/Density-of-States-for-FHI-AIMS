# Density-of-States-for-FHI-AIMS
Python program to plot the Density of States (DOS) from FHI-AIMS outputs.

# Needed Files
The necessary input files are:
  1.  geometry.in
  2.  KS_DOS_total.dat
  3.  atom_proj_dos_....dat or atom_proj_dos_spin_....dat
##  The input files must contain the atom projected DOS, *NOT* the species projected DOS given that the last one is an average DOS per atom of the same species. 

# Requirements  
The following Python modules must be installed:
  1.  Pandas
  2.  Cycler
  3.  Matplotlib
  4.  Os

# Instructions
This program must be runned in the same directory as the input files.
The use of this program is very simple:
1.  The user must specify whether the system is spin polarized or not following the screen-displayed instructions.
1.  Make sure that the input files have the aforementioned names.
2.  The above mentioned python modules are installed.
3.  In the Plotting section, the user is able to select the style of the plot. Including: color, linewidth, marker, font, etc.
4.  In the same section, the user must indicate which atom species and which orbital angular momentum (*l* number) is selected for the plot. The program creates a list of atom species and the number of atoms per species. The index of "dosaux", "dosauxup" and "dosauxdn", that contains the sum of the PDOS per atom species, is the same index than the list of list of atom species and the number of atoms per species, which is printed when the user runs the program. e.g. index = 0: C, index = 1: Ti.
5.  The user must change the labels of the leyend and add or remove them according to the properties of the studied system.
6.  The user can change the name of the generated png file by changing the variable "name".
