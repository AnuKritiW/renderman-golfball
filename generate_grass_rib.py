import random

# Parameters
num_blades = 200000
x_range = (-10, 10)
z_range = (-3, 8)
y_base = -1.0
min_height = 0.08
max_height = 0.15

rib_header = \
"""
AttributeBegin
\tBxdf "PxrSurface" "PxrGrass"
\t\t"color diffuseColor" [0.2 0.5 0.1]
\t\t"float diffuseGain" [1.0]
\t\t"float specularRoughness" [0.3]
"""

with open("grass_generated.rib", "w") as f:
    f.write(rib_header)

    for _ in range(num_blades):
        # *x_range/*z_range unpacks tuple
        x = random.uniform(*x_range) # generates a random float within x_range
        z = random.uniform(*z_range) # generates a random float within z_range
        height = random.uniform(min_height, max_height)

        # random bend offsets
        bend1 = random.uniform(-0.02, 0.02) # slight bend at base
        bend2 = random.uniform(-0.04, 0.04) # stronger bend near the tip

        # compute intermediate heights for ctrl pts from base to tip
        y1 = y_base + height * 0.33
        y2 = y_base + height * 0.66
        y3 = y_base + height

        # define the 4 ctrl pts of the blade's cubic curve
        p = [
            x, y_base, z,               # base point (root of blade)
            x + bend1, y1, z + bend1,   # lower ctrl pt
            x + bend2, y2, z + bend2,   # upper ctrl pt
            x, y3, z                    # tip (returns to center)
        ]
        p_str = " ".join([f"{v:.4f}" for v in p])

        base_width = random.uniform(0.008, 0.012) # base is slightly thicker
        tip_width = random.uniform(0.001, 0.003)  # tip is thinner

        # non periodic means it's an open curve (not looping)
        f.write('\tCurves "cubic" [4] "nonperiodic"\n')
        f.write(f'\t\t"P" [ {p_str} ]\n')
        f.write(f'\t\t"width" [ {base_width:.4f} {tip_width:.4f} ]\n\n')

    f.write('AttributeEnd\n')
