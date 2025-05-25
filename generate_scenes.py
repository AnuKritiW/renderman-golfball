# generate_scenes.py
RESOLUTIONS = {
    "HD": (1920, 1080),
    "4K": (3840, 2160),
    "8K": (7680, 4320)
}

def generate_scene_rib(filename, resolution="HD", samples=16, image_num=1):
    width, height = RESOLUTIONS.get(resolution, RESOLUTIONS["HD"])
    exr_output = "golfball-1.exr" if image_num == 1 else "golfball-2.exr"
    grass_archive = "grass_patches_image1/include_all_patches.rib" if image_num == 1 else "grass_patches_image2/include_all_patches.rib"
    ball_archive = "balls/single_ball.rib" if image_num == 1 else "balls/all_balls.rib"
    fov = 45 if image_num == 1 else 40

    # Different camera and lighting setups for image 1 and 3
    if image_num == 1:
        world_transform = """
\tTranslate 0 0 5
"""
        lights = '\tReadArchive "lighting/lighting_common.rib"\n\tReadArchive "lighting/lighting_image1.rib"\n'
        ground_plane = """
\tAttributeBegin
\t\tBxdf "PxrSurface" "PxrGroundSurface"
\t\t\t"color diffuseColor" [0.071 0.039 0.0]
\t\t\t"float diffuseGain" [1]
\t\tPolygon "P" [-10 -1.05 8
\t\t\t\t\t 10 -1.05 8
\t\t\t\t\t 10 -1.05 -3
\t\t\t\t\t-10 -1.05 -3]
\tAttributeEnd
"""
    else:
        world_transform = """
\tTranslate 0 -0.5 8.7
\tRotate -35 1 0 0
"""
        lights = '\tReadArchive "lighting/lighting_common.rib"\n\tReadArchive "lighting/lighting_image2.rib"\n'
        ground_plane = """
\tAttributeBegin
\t\tBxdf "PxrSurface" "PxrGroundSurface"
\t\t\t"color diffuseColor" [0.071 0.039 0.0]
\t\t\t"float diffuseGain" [1]
\t\tPolygon "P" [-15 -1.05 17.5
\t\t\t\t\t 15 -1.05 17.5
\t\t\t\t\t 15 -1.05 -3
\t\t\t\t\t-15 -1.05 -3]
\tAttributeEnd
"""

    rib_content = f"""# Generated scene RIB for golfball-{image_num}
Option "searchpath" "shader" ["./"]

Display "{exr_output}" "openexr" "rgba"
Format {width} {height} 1.0

Projection "perspective" "float fov" [{fov}]

Integrator "PxrPathTracer" "integrator"
Hider "raytrace" "int incremental" [1] "int maxsamples" [{samples}]
PixelFilter "gaussian" 2 2
PixelVariance 0.001

WorldBegin
{world_transform}
{lights}
{ground_plane}

\t# grass and balls
\tReadArchive "{grass_archive}"
\tReadArchive "{ball_archive}"

WorldEnd
"""
    with open(filename, "w") as f:
        f.write(rib_content)
    print(f"Generated {filename} with resolution {resolution} and samples {samples}")

if __name__ == "__main__":
    generate_scene_rib("golfball.rib", resolution="HD", samples=16, image_num=1)
    generate_scene_rib("golfball-3.rib", resolution="HD", samples=16, image_num=2)
