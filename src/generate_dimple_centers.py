import os
import math

def fibonacci_sphere(samples):
    # Generates `samples` points evenly distributed on a unit sphere
    points = []
    phi = math.pi * (3.0 - math.sqrt(5.0))      # golden angle in radians
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)
        theta = phi * i
        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        points.append((x, y, z))
    return points

def write_oslinclude(points, filepath):
    # Writes the points into a get_dimple_center() function
    with open(filepath, "w") as f:
        f.write("point get_dimple_center(int i)\n")
        f.write("{\n")
        f.write(f"    point dimple_centers[{len(points)}] = {{\n")

        for i, (x, y, z) in enumerate(points):
            comma = "," if i < len(points) - 1 else ""
            f.write(f"        point({x:.6f}, {y:.6f}, {z:.6f}){comma}\n")

        f.write("    };\n")
        f.write("    return dimple_centers[i];\n")
        f.write("}\n")

def generate_dimple_centers(num_dimples=377, base_dir="generated", filename="dimple_centers.oslinclude"):
    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, filename)
    points = fibonacci_sphere(num_dimples)
    write_oslinclude(points, filepath=filepath)
    print(f"Wrote {num_dimples} dimple centers to {filepath}")

if __name__ == "__main__":
    generate_dimple_centers(num_dimples=377)
