import os

sockets = {
    'widths': [31, 29, 27, 25.5, 23],
    'heights': [64.75, 64.75, 57, 57, 54.5],
    'spacing': 0.5,
    'offsets': []
}
base = {
    'border': 5,
    'bottom': 3
}
magnet = {
    'diameter': 6.5,
    'height': 2.5
}
shunt = {
    'width': 5,
    'height': 5,
    'length': 34.5
}
paths = {
    'openscad': '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD',
    'stl': '/Users/raven/PycharmProjects/socket_trays/sockets.stl',
    'scad': '/Users/raven/PycharmProjects/socket_trays/sockets.scad'
}

# Calculate socket_offsets
for i in range(0, len(sockets['widths'])):
    if i == 0:
        sockets['offsets'].append((sockets['widths'][i] / 2) + base['border'])
    else:
        sockets['offsets'].append((sockets['widths'][i] / 2) + (sockets['widths'][i - 1] / 2) + sockets['offsets'][i - 1] + sockets['spacing'])

# Determine tray width by adding all socket widths, socket spacing between each socket, and two borders.
tray_width = 0
for width in sockets['widths']:
    tray_width += width
tray_width += (len(sockets['widths']) - 1) * sockets['spacing']
tray_width += base['border'] * 2

# Determine tray depth by adding the largest socket height and two borders.
tray_depth = max(sockets['heights']) + base['border'] * 2

# Determine tray height by adding the largest socket width's radius, the bottom padding, height of the shunt and magnet.
tray_height = (max(sockets['widths']) / 2) + base['bottom'] + shunt['height'] + magnet['height']

# Create .scad contents
output = f'''
socket_widths = {sockets['widths']};
socket_heights = {sockets['heights']};
socket_offsets = {sockets['offsets']};

difference()
{{
    cube([{tray_width}, {tray_depth}, {tray_height}]);

    union()
    {{
        for(i = [0:1:len(socket_widths)-1])
            rotate([90, 0, 0])
                translate([socket_offsets[i], {tray_height}, -1.0 * (socket_heights[i] + {base['border']})])
                    cylinder(socket_heights[i], d=socket_widths[i], true);
        for(i = [0:1:len(socket_widths)-1])
            translate([socket_offsets[i], (socket_heights[i]/4)* 1 + {base['border']}, {tray_height} - (socket_widths[i]/2) - {magnet['height'] - 0.5}])
                cylinder({magnet['height']}, d={magnet['diameter']}, true);
        for(i = [0:1:len(socket_widths)-1])
            translate([socket_offsets[i], (socket_heights[i]/4)* 3 + {base['border']}, {tray_height} - (socket_widths[i]/2) - {magnet['height'] - 0.5}])
                cylinder({magnet['height']}, d={magnet['diameter']}, true);
        for(i = [0:1:len(socket_widths)-1])
            rotate([90, 0, 0])
                translate([socket_offsets[i], {tray_height} - (socket_widths[i]/2) - {magnet['height']/2}, -1 * ((socket_heights[i]/2) + {base['border']})])
                    cube([{shunt['width']}, {shunt['height'] + magnet['height']}, {shunt['length']}], true);
    }}
}}'''

# Write .scad file
outfile = open(paths['scad'], "w")
outfile.write(output)
outfile.close()

# Convert to .stl
os.system(f"open -a {paths['openscad']} --args -o {paths['stl']} {paths['scad']}")
