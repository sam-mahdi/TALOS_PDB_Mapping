from pymol import cmd, stored, math
import re

def ss(mol,startaa=1, visual="Y"):
	"""
	Replaces B-factors with TALOS predicted secondary structure elements

	mol = any object selection (within one single object though)
	startaa = number of first amino acid in 'new B-factors' file (default=1)
	visual = redraws structure as cartoon_putty and displays bar with min/max values (default=Y)

	example: ss 1LVM, startaa=4
	"""
	source='predSS.tab'
	ss_dict={'L':0,'H':2,'E':1,'X':0}
	ss_only=[]
	with open(source) as ss_file:
		for lines in ss_file:
            		searcher=re.search('^\d+',lines.strip())
            		if searcher != None:
				if int(lines.strip().split()[0]) < int(startaa):
					continue
				ss_only.append(ss_dict[lines.strip().split()[8]])
	obj=cmd.get_object_list(mol)[0]
	cmd.alter(mol,"b=-1.0")
	counter=int(startaa)
	bfacts=[]
	for line in ss_only:
		bfact=float(line)
		bfacts.append(bfact)
		cmd.alter("%s and resi %s and n. CA"%(mol,counter), "b=%s"%bfact)
		counter=counter+1
	if visual=="Y":
		cmd.cartoon("automatic",mol)
		cmd.spectrum("b","grey blue red", "%s and n. CA " %mol)
		cmd.recolor()

def s2 (mol,startaa=1, visual="Y"):
	"""
	Replaces B-factors with TALOS predicted RCI S2 values
	Thickness and color are determined by S2 values with thicker values being more dynamic

	mol = any object selection (within one single object though)
	startaa = number of first amino acid in 'new B-factors' file (default=1)
	visual = redraws structure as cartoon_putty and displays bar with min/max values (default=Y)

	example: ss 1LVM, startaa=4
	"""
	source='predS2.tab'
	s2_only=[]
	with open(source) as s2_file:
		for lines in s2_file:
            		searcher=re.search('\d+\.\d{3}',lines)
            		if searcher != None:
				if int(lines.strip().split()[0]) < int(startaa):
					continue
				s2_only.append(searcher.group(0))
	obj=cmd.get_object_list(mol)[0]
	cmd.alter(mol,"b=-1.0")
	counter=int(startaa)
	bfacts=[]
	for line in s2_only:
		bfact=((1/(float(line)))-float(line))/1.5
		bfacts.append(bfact)
		cmd.alter("%s and resi %s and n. CA"%(mol,counter), "b=%s"%bfact)
		counter=counter+1
	if visual=="Y":
		cmd.show_as("cartoon",mol)
		cmd.cartoon("putty", mol)
		cmd.set("cartoon_putty_scale_min", min(bfacts),obj)
		cmd.set("cartoon_putty_scale_max", max(bfacts),obj)
		cmd.set("cartoon_putty_transform", 7,obj)
		cmd.set("cartoon_putty_radius", max(bfacts),obj)
		cmd.spectrum("b","white red", "%s and n. CA " %mol)
		cmd.ramp_new("color_bar", obj, [min(bfacts), max(bfacts)],["white","red"])
		cmd.recolor()

cmd.extend("s2", s2);
cmd.extend("ss", ss);
