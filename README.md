# ReprapThermalCamera

Hey! Do you need to take a thermal image of a surface - a shorted PCB, for instance? Do you have a reprap 3D printer, an Arduino, and $50? 

Just mount a mlx90621 (the low-FOV one, model -XXB) to the extruder, put your board or item on the table, wire the mlx to an arduino, set the scan pattern in the python script, and bam;

![Got you now, shorted board!](/demo.png?raw=true)

It actually gives pretty decent results; in one pass, we found the short on this board. The resolution is limited by the Z height and stuff but was 100x100 for this run, so about 30ppi. There's a bit of raster artifacting, but if you make sure your part is secure on the bed, it's fine.

This was a quick weekend project based on https://github.com/longjos/MLX90621_Arduino_Camera (thanks). Public Domain. Hopefully someone'll find it useful.
