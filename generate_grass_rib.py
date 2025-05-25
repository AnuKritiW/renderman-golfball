import random
import os
import shutil
import math
import argparse

def generate_grass(use_image2):
    # Parameters based on image selection
    if use_image2:
        x_range = (-15, 15)
        z_range = (-3, 17)
        min_height = 0.3
        max_height = 0.6
        max_blades_per_patch = 2500
        base_width_range = (0.02, 0.035)
        tip_width_range = (0.005, 0.01)
        output_dir = 'grass_patches_image2'
    else:
        x_range = (-10, 10)
        z_range = (-3, 8)
        min_height = 0.08
        max_height = 0.15
        max_blades_per_patch = 4000
        base_width_range = (0.008, 0.012)
        tip_width_range = (0.001, 0.003)
        output_dir = 'grass_patches_image1'

    y_base = -1.0
    patch_size = 2.0            # each patch covers a 2x2 area
    min_blades_per_patch = 100

    # Clear out old patches to avoid stale files
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # patch grid layout
    x_start, x_end = x_range
    z_start, z_end = z_range

    max_patch_distance = math.sqrt(x_end**2 + z_end**2)
    fade_start = 0.2 * max_patch_distance  # full density until this distance
    fade_end = max_patch_distance          # taper to min beyond this

    num_patches_x = int((x_end - x_start) / patch_size)
    num_patches_z = int((z_end - z_start) / patch_size)

    rib_header = """
AttributeBegin
\tBxdf "PxrSurface" "PxrGrass"
\t\t"color diffuseColor" [0.2 0.5 0.1]
\t\t"float diffuseGain" [1.0]
\t\t"float specularRoughness" [0.3]
"""

    patch_paths = []

    # generate each patch
    for i in range(num_patches_x):
        for j in range(num_patches_z):
            # r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 0.9)es_z):
            x0 = x_start + i * patch_size
            x1 = x0 + patch_size
            z0 = z_start + j * patch_size
            z1 = z0 + patch_size

            # compute patch center and distance to camera
            patch_center_x = (x0 + x1) / 2
            patch_center_z = (z0 + z1) / 2
            distance = math.sqrt(patch_center_x**2 + patch_center_z**2)

            # determine blade count based on distance
            if distance < fade_start:
                blades_per_patch = max_blades_per_patch
            elif distance >= fade_end:
                blades_per_patch = min_blades_per_patch
            else:
                t = (distance - fade_start) / (fade_end - fade_start)
                blades_per_patch = int(
                    max_blades_per_patch * (1 - t) + min_blades_per_patch * t
                )

            filename = os.path.join(output_dir, f"grass_patch_{i}_{j}.rib")
            patch_paths.append(filename)

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

                    base_width = random.uniform(*base_width_range)
                    tip_width = random.uniform(*tip_width_range)

                    # non periodic means it's an open curve (not looping)
                    f.write('\tCurves "cubic" [4] "nonperiodic"\n')
                    f.write(f'\t\t"P" [ {p_str} ]\n')
                    f.write(f'\t\t"width" [ {base_width:.4f} {tip_width:.4f} ]\n\n')

                f.write('AttributeEnd\n')

    # Create master include RIB file in the output directory
    include_rib_path = os.path.join(output_dir, "include_all_patches.rib")
    with open(include_rib_path, "w") as f:
        for path in patch_paths:
            f.write(f'ReadArchive "{path}"\n')

    print(f"Generated grass patches in {output_dir}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=int, choices=[1, 2], default=2)
    args = parser.parse_args()
    use_image2 = (args.image == 2)
    generate_grass(use_image2)

if __name__ == "__main__":
    main()
