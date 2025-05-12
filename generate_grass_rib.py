import random
import os

# Parameters
x_range = (-10, 10)
z_range = (-3, 8)
y_base = -1.0
min_height = 0.08
max_height = 0.15

patch_size = 2.0        # each patch covers a 2x2 area
blades_per_patch = 4000 # density control per patch

output_dir = 'grass_patches'
os.makedirs(output_dir, exist_ok=True)

# patch grid layout
x_start, x_end = x_range
z_start, z_end = z_range

num_patches_x = int((x_end - x_start) / patch_size)
num_patches_z = int((z_end - z_start) / patch_size)

rib_header = \
"""
AttributeBegin
\tBxdf "PxrSurface" "PxrGrass"
\t\t"color diffuseColor" [0.2 0.5 0.1]
\t\t"float diffuseGain" [1.0]
\t\t"float specularRoughness" [0.3]
"""

# generate each patch
for i in range(num_patches_x):
    for j in range(num_patches_z):
        x0 = x_start + i * patch_size
        x1 = x0 + patch_size
        z0 = z_start + j * patch_size
        z1 = z0 + patch_size

        filename = os.path.join(output_dir, f"grass_patch_{i}_{j}.rib")

        with open(filename, "w") as f:
            f.write(rib_header)

            for _ in range(blades_per_patch):
                x = random.uniform(x0, x1) # generates a random float within x_range
                z = random.uniform(z0, z1) # generates a random float within z_range
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

# create a master list of readarchive calls
with open("include_all_patches.rib", "w") as f:
    for i in range(num_patches_x):
        for j in range(num_patches_z):
            f.write(f'ReadArchive "{output_dir}/grass_patch_{i}_{j}.rib"\n')