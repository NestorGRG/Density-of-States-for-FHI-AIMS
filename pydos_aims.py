import pandas as pd
import os
from collections import defaultdict
import matplotlib.pyplot as plt
from cycler import cycler

pd.set_option('display.max_rows', None,
              'display.max_columns', None,
              'display.max_colwidth', None,
              'display.precision', 5)

#Asking if the calculation is spin polarized or not
spin= int(input("Spin polarized? (1=no, 2=yes) "))

#Reading Fermi Energy Level
with open("KS_DOS_total.dat","r") as ksdos:
    lines = ksdos.readlines()
    efermi = float(lines[1].strip().split()[-2])

#Printing Fermi Energy Level
print("Fermi Energy: ", efermi, " eV")

#Reading Total DOS with the energies with respect to the fermi level
total_dos = pd.read_table("KS_DOS_total.dat",delimiter="\s+",index_col=0, skiprows=4, header=None)
if spin == 1:
    total_dos = total_dos.rename(columns={1:"Total DOS"})
if spin == 2:
    total_dos = total_dos.rename(columns={1:"UP",2:"DOWN"})
    #Making the down DOS negative for plotting purpouses
    zero = total_dos*0
    zero["UP"] = total_dos["UP"]
    total_dos["DOWN"] = zero["DOWN"].sub(total_dos["DOWN"])

total_dos.index.name = "Energy"

#Reading how many atoms are in the system from geometry.in input
with open ("geometry.in","r") as geometry:
    lines_geometry = geometry.readlines()
#List of atoms
list_atoms = []
for line in lines_geometry:
    if "atom" in line:
        list_atoms.append(line.strip().split()[-1])
#Dictionary of atom species and number of atoms for each specie
dic_atoms = defaultdict(int)
for item in list_atoms:
    dic_atoms[item] += 1

#Alphabetically sorting the dictionary
dic_atoms = dict(dic_atoms)
dic_atoms = dict(sorted(dic_atoms.items(), key=lambda x: x[0].lower()))
print(dic_atoms)

#Reading the atom_proj_dos with the energies with respect to the fermi level
#Reading the files in pwd
listoffiles = os.listdir()
if spin == 1:
    proj = "atom_projected_dos_"
if spin == 2:
    proj = "atom_proj_dos_"
#Removing the files from the list that are not usefull
list_files = []
for line in listoffiles:
    if proj in line: list_files.append(line)

#Removing the raw files and alphabetically sort the list of files
for item in list_files:
    if "raw" in item:
        list_files.remove(item)
list_ofprojDOS = [item for item in list_files if "raw" not in item]

#Whether the calculation is spin polarized or not, this list contains all the file names 
list_ofprojDOS = sorted(list_ofprojDOS)

#If the calculation is spin polarized, separate the list files into up and down list of files and sort it alphabetically
if spin == 2:
    upfiles = []
    dnfiles = []
    for line in list_ofprojDOS:
        if "dn" in line:
            dnfiles.append(line)
        if "up" in line:
            upfiles.append(line)
    dnfiles = sorted(dnfiles)
    upfiles = sorted(upfiles)

#Reading the atom projected DOS
if spin == 1:
    #Empty list for DataFrames
    df_list = []
    #Looping over each file and reading it into a dataframe, df
    for file in list_ofprojDOS:
            df = pd.read_table(file, delimiter="\s+",index_col=0, skiprows=4, header=None)
            #Renaming the columns and index
            #df = df.rename(columns={1:"Total Dos",2:"s",3:"p",4:"d",5:"f",6:"g",7:"h"})
            df = df.rename(columns={1:"Total Dos",2:"l=0",3:"l=1",4:"l=2",5:"l=3",6:"l=4",7:"l=5"})
            df.index.name = "Energy / eV"
            #Appending the df into the list
            df_list.append(df)

if spin == 2:
    #Empty list for DataFrames
    df_listup = []
    df_listdn = []
    #Looping over each file and reading it into a dataframe, df
    for file in dnfiles:
        if "dn" in file:
            dfdn = pd.read_table(file, delimiter="\s+",index_col=0, skiprows=4, header=None)
            #Renaming the columns and index
            #dfdn = dfdn.rename(columns={1:"Total Dos",2:"s",3:"p",4:"d",5:"f",6:"g",7:"h"})
            dfdn = dfdn.rename(columns={1:"Total Dos",2:"l=0",3:"l=1",4:"l=2",5:"l=3",6:"l=4",7:"l=5"})
            dfdn.index.name = "Energy / eV"
            #Appending the df into the list
            df_listdn.append(dfdn)

    for file in upfiles:
        if "up" in file:
            dfup = pd.read_table(file, delimiter="\s+",index_col=0, skiprows=4, header=None)
            #Renaming the columns and index
            dfup = dfup.rename(columns={1:"Total Dos",2:"l=0",3:"l=1",4:"l=2",5:"l=3",6:"l=4",7:"l=5"})
            #dfup = dfup.rename(columns={1:"Total Dos",2:"s",3:"p",4:"d",5:"f",6:"g",7:"h"})
            dfup.index.name = "Energy / eV"
            #Appending the df into the list
            df_listup.append(dfup)

#Grouping DOS by species
#Converting the dictionay into a list in order to call it by position
dic_list_atoms = list(dic_atoms.items())

#Creating a list with DataFrame = 0
if spin == 1:
    dosaux = []
    for i in range(len(dic_list_atoms)):
        dosaux.append(df_list[0]*0)

    #Looping over the number of species
    k = 0
    for i in range(len(dic_list_atoms)):
        #Looping over the number of atoms of each specie
        for j in range(dic_list_atoms[i][1]):
            #Adding the DOS to the auxiliar DOS tuple of DataFrame
            dosaux[i] = dosaux[i].add(df_list[k])
            k = k + 1

if spin == 2:
    #Creating a list with DataFrame = 0
    dosauxup = []
    dosauxdn = []
    for i in range(len(dic_list_atoms)):
        dosauxup.append(df_listup[0]*0)
        dosauxdn.append(df_listup[0]*0)

    #Looping over the number of species
    k = 0
    for i in range(len(dic_list_atoms)):
        #Looping over the number of atoms of each specie
        for j in range(dic_list_atoms[i][1]):
            #Adding the DOS to the auxiliar DOS tuple of DataFrame
            dosauxup[i] = dosauxup[i].add(df_listup[k])
            dosauxdn[i] = dosauxdn[i].add(df_listdn[k])
            k = k + 1

    #Making the down DOS negative for plotting porpouses
    zeroaux = []
    for i in range(len(dic_list_atoms)):
        zeroaux.append(df_listup[0]*0)
    for i in range(len(dosauxdn)):
        dosauxdn[i] = zeroaux[i].sub(dosauxdn[i])

#Saving DOS per species in files of up and down
#for i in range(len(dic_list_atoms)):
#    name_up = 'dos_'+str(dic_list_atoms[i][0])+'.txt'
#    with open(name_up, "w") as f:
#        for item in dosauxup:
#            string = item.to_string(header =True, index=True)
#            f.write(f"{string}\n")
#if spin == 2:
#    for i in range(len(dic_list_atoms)): 
#        name_dn = 'dos_'+str(dic_list_atoms[i][0])+'_down.txt'
#        with open(name_dn, "w") as f:
#            for item in dosauxdn:
#                string = item.to_string(header =True, index=True)
#                f.write(f"{string}\n")

#Plot
#Plotting Style
if spin == 1:
    custom_cycler= (cycler(color=["black","crimson","#0099cc","limegreen"]) +
                    #cycler(marker=["o","o","o","","","","","",""]) +
                    #cycler(markersize=[8,8,8,0,0,0,0,0,0]) +
                    cycler(linestyle=["-","-","-","-"]) +
                    cycler(linewidth=[1,1,1,1]))
if spin == 2:
    custom_cycler= (cycler(color=["black","black","crimson","crimson","#0099cc","#0099cc","limegreen","limegreen"]) +
                    #cycler(marker=["o","o","o","","","","","",""]) +
                    #cycler(markersize=[8,8,8,0,0,0,0,0,0]) +
                    cycler(linestyle=["-","-","-","-","-","-","-","-"]) +
                    cycler(linewidth=[1,1,1,1,1,1,1,1]))
font= {"family": "normal",
       "size"  : 14}
plt.rc("font",**font)
plt.rcParams["font.family"]="sans-serif"
plt.rcParams["font.sans-serif"]="Times New Roman"
plt.rcParams["axes.prop_cycle"] = custom_cycler

#Plotting
#Total DOS
plot = total_dos.plot(legend=None)
plot.axvline(x=0, color="black", linestyle="--")

#PDOS
if spin == 1:
    plot1 = dosaux[0]["l=1"].plot(ax=plot,label="C (p)")
    plot1 = dosaux[1]["l=2"].plot(ax=plot,label="Ti (d)")
    plot1 = dosaux[1]["l=1"].plot(ax=plot,label="Ti (p)")
if spin == 2:
    plot1 = dosauxup[0]["l=1"].plot(ax=plot,label="C (p)")
    plot1 = dosauxdn[0]["l=1"].plot(ax=plot,legend=None)
    plot1 = dosauxup[1]["l=2"].plot(ax=plot,label="Ti (d)")
    plot1 = dosauxdn[1]["l=2"].plot(ax=plot,legend=None)
    plot1 = dosauxup[1]["l=1"].plot(ax=plot,label="Ti (p)")
    plot1 = dosauxdn[1]["l=1"].plot(ax=plot,legend=None)

#Legend
handles, labels = plot.get_legend_handles_labels()
if spin == 1:
    new_labels = ["Total DOS","Ti (d)", "Ti (p)", "C (p)"]
    legend = plot.legend(loc="center left",bbox_to_anchor=[1.01, 0.5],frameon=False)
if spin == 2:
    new_handles = [handles[0],handles[2],handles[4],handles[6]]
    new_labels = ["Total DOS","C (d)", "Ti (d)", "Ti (p)"]
    legend = plot.legend(handles=new_handles,labels=new_labels,loc="center left",bbox_to_anchor=[1.01, 0.5],frameon=False)
#                      handler_map={str: LegendTitle({'fontsize': 28})})

# plot.set_title("b) $\mathdefault{Ti_2C}$",x=-0.3,fontdict={'fontsize': 26})
# plot.set_xlim(xmin=1,xmax=8)
# plot.set_ylim(ymin=-75,ymax=125)
# plot.set_yticks(range(-75,170,50))

plt.xlabel("$\mathdefault{∆E(E-E_{f}}$) (eV)")
plt.ylabel("DOS (states/eV)")

# #Saving the plot
name = "DOS-Ti2C"
plt.savefig(fname=name,dpi=1000,bbox_inches="tight")

