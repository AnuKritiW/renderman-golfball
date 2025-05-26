import os
import subprocess
from generate_balls import generate_balls
from generate_dimple_centers import generate_dimple_centers
from generate_scenes import generate_scene
from generate_grass import generate_grass

def compile_shader(shader_name="dimples.osl", num_dimples=377, base_dir="generated"):
    print(f"⛳ Generating {num_dimples} Dimple Centers")
    generate_dimple_centers(num_dimples=num_dimples, base_dir=base_dir)
    print(f"📦 Compiling shader: {shader_name}")
    subprocess.run(["oslc", shader_name], check=True)

def generate_grass_in_pipeline(image, base_dir):
    print(f"🌱 Generating grass for image {image}")
    generate_grass(image=image, base_dir=base_dir)

def generate_balls_in_pipeline(num_dimples=377, base_dir="generated"):
    print(f"⛳ Generating Balls with {num_dimples} dimples")
    generate_balls(num_dimples=num_dimples, mode="both", base_dir=base_dir)  # or "single", "all" as needed

def render_scene(rib_file):
    print(f"🎬 Rendering scene: {rib_file}")
    subprocess.run(["prman", rib_file], check=True)

def open_in_it(*exr_files):
    print(f"🖼️  Opening image(s) in it: {', '.join(exr_files)}")
    subprocess.run(["it", *exr_files], check=True)

def main():
    num_dimples = 400
    resolution = "4K"  # Options: "HD", "4K", "8K"
    samples = 1024

    base_dir = "generated"
    os.makedirs(base_dir, exist_ok=True)

    compile_shader("dimples.osl", num_dimples=num_dimples, base_dir=base_dir)

    # Generate grass for both images (image 1 and image 2)
    generate_grass_in_pipeline(image=1, base_dir=base_dir)
    generate_grass_in_pipeline(image=2, base_dir=base_dir)

    generate_balls_in_pipeline(num_dimples=num_dimples, base_dir=base_dir)

    # Generate scene RIBs dynamically
    generate_scene("scene_1.rib", resolution=resolution, samples=samples, image_num=1, base_dir=base_dir)
    generate_scene("scene_2.rib", resolution=resolution, samples=samples, image_num=2, base_dir=base_dir)

    # Render scenes that use different grass sets
    render_scene(os.path.join(base_dir, "scenes/scene_1.rib"))
    render_scene(os.path.join(base_dir, "scenes/scene_2.rib"))

    # Open corresponding renders in 'it'
    open_in_it(os.path.join(base_dir, "scene_1.exr"), os.path.join(base_dir, "scene_2.exr"))

if __name__ == "__main__":
    main()
