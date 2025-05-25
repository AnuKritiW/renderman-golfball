import subprocess
from generate_balls import generate_balls
from generate_dimple_centers import generate_dimple_centers
from generate_scenes import generate_scene
from generate_grass import generate_grass

def compile_shader(shader_name="dimples.osl", num_dimples=377):
    print(f"⛳ Generating {num_dimples} Dimple Centers")
    generate_dimple_centers(num_dimples=num_dimples)
    print(f"📦 Compiling shader: {shader_name}")
    subprocess.run(["oslc", shader_name], check=True)

def generate_grass_in_pipeline(image):
    print(f"🌱 Generating grass for image {image}")
    generate_grass(image=image)

def generate_balls_in_pipeline(num_dimples=377):
    print(f"⛳ Generating Balls with {num_dimples} dimples")
    generate_balls(num_dimples=num_dimples, mode="both")  # or "single", "all" as needed

def render_scene(rib_file):
    print(f"🎬 Rendering scene: {rib_file}")
    subprocess.run(["prman", rib_file], check=True)

def open_in_it(*exr_files):
    print(f"🖼️  Opening image(s) in it: {', '.join(exr_files)}")
    subprocess.run(["it", *exr_files], check=True)

def main():
    num_dimples = 400
    resolution = "HD"  # Options: "HD", "4K", "8K"
    samples = 16

    compile_shader("dimples.osl", num_dimples=num_dimples)

    # Generate grass for both images (image 1 and image 2)
    generate_grass_in_pipeline(image=1)
    generate_grass_in_pipeline(image=2)

    generate_balls_in_pipeline(num_dimples=num_dimples)

    # Generate scene RIBs dynamically
    generate_scene("scene_1.rib", resolution=resolution, samples=samples, image_num=1)
    generate_scene("scene_2.rib", resolution=resolution, samples=samples, image_num=2)

    # Render scenes that use different grass sets
    render_scene("scenes/scene_1.rib")
    render_scene("scenes/scene_2.rib")

    # Open corresponding renders in 'it'
    open_in_it("scene_1.exr", "scene_2.exr")

if __name__ == "__main__":
    main()
