import os

socket_widths = [18.0, 17.5, 16.25, 15.25, 13.5]
socket_heights = [50.25, 50.25, 50.25, 50.25, 50.25]
socket_offsets = []
border_width = 5
base_height = 3
socket_spacing = 0.25
path_to_openscad = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'
path_to_stl = "/Users/raven/PycharmProjects/socket_trays/sockets.stl"
path_to_scad = "/Users/raven/PycharmProjects/socket_trays/sockets.scad"

i = -1
for width in socket_widths:
    i += 1
    if i == 0:
        socket_offsets.append(width/2 + border_width)
    else:
        socket_offsets.append(width/2 + socket_widths[i-1]/2 + socket_offsets[i-1] + socket_spacing)

print(socket_offsets)

tray_width = 0
for width in socket_widths:
    tray_width += width
tray_width += (len(socket_widths)-1) * socket_spacing
tray_width += border_width * 2

tray_depth = socket_heights[0] + border_width * 2

tray_height = socket_widths[0]/2 + base_height

# Example output
output = f'''
socket_widths = {socket_widths};
socket_heights = {socket_heights};
socket_offsets = {socket_offsets};

border_width = {border_width};
base_height = {base_height};
socket_spacing = {socket_spacing};

difference()
{{
    cube([{tray_width}, {tray_depth}, {tray_height}]);

    union()
    {{
        for(i = [0:1:len(socket_widths)-1])
            rotate([90, 0, 0])
                translate([socket_offsets[i], socket_widths[i]/2.0 + base_height, -1.0 * (socket_heights[i] + border_width)])
                    cylinder(socket_heights[i], d=socket_widths[i], true);
        for(i = [0:1:len(socket_widths)-1])
            translate([socket_offsets[i], (socket_heights[i]/4)* 1 + border_width, 0.75])
                cylinder(3, d=6.5, true);
        for(i = [0:1:len(socket_widths)-1])
            translate([socket_offsets[i], (socket_heights[i]/4)* 3 + border_width, 0.75])
                cylinder(3, d=6.5, true);
    }}
}}'''

outfile = open(path_to_scad, "w")
outfile.write(output)
outfile.close()
os.system(f"open -a {path_to_openscad} --args -o {path_to_stl} {path_to_scad}")
