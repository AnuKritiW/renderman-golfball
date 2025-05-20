import subprocess

def compile_shader(shader_name="dimples.osl"):
    print(f"📦 Compiling shader: {shader_name}")
    subprocess.run(["oslc", shader_name], check=True)

def generate_grass(python_file="generate_grass_rib.py"):
    print(f"🌱 Generating Grass: {python_file}")
    subprocess.run(["python3", python_file], check=True)

def render_scene(rib_file="golfball.rib"):
    print(f"🎬 Rendering scene: {rib_file}")
    subprocess.run(["prman", rib_file], check=True)

def open_in_it(exr_file="golfball.exr"):
    print(f"🖼️  Opening image in it: {exr_file}")
    subprocess.run(["it", exr_file], check=True)

def main():
    compile_shader("dimples.osl")
    generate_grass("generate_grass_rib.py")
    render_scene("golfball.rib")
    open_in_it("golfball.exr")

if __name__ == "__main__":
    main()
