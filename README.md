# TALOS_PDB_Mapping
Will take both predSS and predS2 files via TALOS and color/map secondary structure or thickness (There is no need to modify the files)
This script contains 2 functions, an ss function and an S2 function. There are parameters for both that can (and should) be modified to obtain the desired colors/look. 

The script is designed in a manner so it is easy to switch between the 2 functions (and thus looks) and thus ray trace them both in the same position without needing to do anything. I.E. You can switch between SS colors/look and S2 colors/look. 

***TO USE***

For SS:
ss molecule,starting amino acid
```
ss 1mmi,startaa=3
```
For S2
```
s2 1mmi,startaa=3
```
The starting amino acid determines what parts of the protein are getting colored. If you assigned a single domain for example (242-333), and the pdb is of the entire protein (1-333), then your startaa would be 242. Or vice versa your peaklist contains values from 1-333, and the protein is truncated (5-333) then your startaa would be 5. 




***SS function***

This script will color the protein using the TALOS predicted secondary structure and their color scheming. Helices predicted in TALOS are red, and sheets blue. 

You may change the color by modifying line 36:
```
cmd.spectrum("b","grey blue red", "%s and n. CA " %mol)
```
You may add custom colors by simply typing in the color name(s) followed by a space 
```
cmd.spectrum("b","red white blue", "%s and n. CA " %mol)
```
You may use pre-set colors 
```
cmd.spectrum("b","rainbow", "%s and n. CA " %mol)
```
There are multiple pre-set colors: https://pymolwiki.org/index.php/Spectrum
And a looot of single colors: https://pymolwiki.org/index.php/Color_Values

***S2 function***

This script will color and vary the thickness of the protein using the TALOS RCI Predicted S2 values. The more dynamic regions are thicker and red, the more rigid regions thinner and white.

Thickness may be modified by altering line 64
```
bfact=((1/(float(line)))-float(line))/1.5
```
Pymol maps thickness from 0 being thinnest, and thickness increasing as the numbers increase. So you take the inverse of the S2 values to make the more dynamic regions (lower S2 values) thicker. Then I subtract by the same value so there is a bigger discrepancy between the rigid and dynamic values (i.e. Subtracting 0.5 from 1/0.5 is not as a big of a reduction as subtracting 0.8 from 0.8). However, this inversion means the very dynamic regions are going to be very thick, thus I divide by 1.5 to get the desired thickness. ***Its important to simply modify values relative to one another, as such you will still have a gradient of values rather than removing the values***. You may modify the above equation to give you a thickness you desire. 

The color that is mapped onto the protein is modified as above in the secondary structure portion. 

The color bar is defined by line 76:
```
cmd.ramp_new("color_bar", obj, [min(bfacts), max(bfacts)],["white","red"])
```
The range of this color bar will be the minimum and max value of your S2 modified versions. You may modify this to any value you desire however.
I.E. If you just want it for 0 to 1
```
cmd.ramp_new("color_bar", obj, [0, 1],["white","red"])
```
The colors of the color bar may also be modified. Again, you may use preset colors (rainbow) or choose custom colors. If custom, the colors must be separated by a comma. 
***Make sure if you change the color in the color bar, you also change the color that is being applied to your protein in line 75***
I.E. If you want to change the colors to red, white, and blue
```
cmd.spectrum("b","red white blue", "%s and n. CA " %mol)
cmd.ramp_new("color_bar", obj, [min(bfacts), max(bfacts)],["red","white","blue"])
```
