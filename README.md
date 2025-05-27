# Renderman Golfball

<p align="center"> <img src="assets/4K_images/scene_1-4k-1024.png" alt="Scene 1" width="45%"/> <img src="assets/4K_images/scene_2-4k-1024.png" alt="Scene 2" width="45%"/> </p>

## Overview

A procedural RenderMan project showcasing a golf ball render with custom texturing, displacement, and shading techniques.

> ## Table of Contents:
> - [Overview](#overview)
> - [Features](#features)
> - [Project Structure](#project-structure)
> - [Dependencies](#dependencies)
> - [Usage](#usage)
> - [Output](#output)

## Features

This project demonstrates a procedural approach to modeling, shading, and scene composition using Pixar’s RenderMan, Python, and OSL shaders.

* Procedural Dimple Modeling

    The golf ball’s dimples are generated using a Fibonacci sphere algorithm to distribute points quasi-uniformly over the ball’s surface, approximating the dimple pattern. Unlike the complex Goldberg polyhedral pattern, the Fibonacci method provides an even, non-overlapping distribution that avoids clustering at the poles, ensuring a realistic look with tunable parameters for dimple count and depth.

* Advanced Shading and Lighting

    The PxrSurface shader was used to create a glossy, plastic-like surface with subtle clearcoat highlights. To enhance the perception of dimple depth, OSL shaders introduce a shadow tinting technique, darkening dimples based on proximity and falloff calculations, achieving depth through shading without increasing geometry complexity. The lighting setup combines an environment map with additional sphere and disk lights for balanced ambient light and softened shadows.

* Procedural Dirt and Wear Effectsrenderman-golfball

    The shader includes procedural dirt distribution, targeting dimple rims with noise-based masks, complemented by scattered speckles and layered Perlin noise. This creates a natural wear effect, with color variation and adjustments to roughness and specularity to replicate used golf balls. Dirt-affected regions appear matte, contrasting with the glossy clean areas.

* Procedural Grass Generation

    A Python-based patch-based grass system generates RenderMan Curves primitives with random heights, widths, and bends for natural variation. Density falls off dynamically with distance from the camera, optimizing performance by reducing memory overhead and rendering load for distant patches.

* Multi-Ball Scene Composition

    A Python script generates multiple golf ball instances with random rotations and varied colors, enhancing realism and visual interest in the second render. The pink ball remains unrotated to serve as a focal point, maintaining consistency with the single-ball render.

Read the full report [here](./assets/RendermanReport_AnuKritiWadhwa.pdf).

## Project Structure

```
renderman-golfball/
├── assets/
│   ├── scene_1-HD-1024.exr                     # Sample scene 1 HD exr render
│   ├── scene_2-HD-1024.exr                     # Sample scene 2 HD exr render
│   ├── 4K_images/                              # png versions of the renders at a higher 4K resolution
│   │   ├── scene_1-4k-1024.png                 # Sample scene 1 4K png render
│   │   ├── scene_2-4k-1024.png                 # Sample scene 2 4K png render
│   ├── reference_images/                       # Selected reference images
│   │   ├── scene_1_reference.jpg               # Reference for scene 1
│   │   ├── scene_2_reference.jpg               # Reference for scene 2
│   │   ├── dirt_region_reference.jpg           # Reference showing dirt regions
│   │   ├── dirt_speckles_reference.jpg         # Reference showing dirt speckles
|   ├── RendermanReport_AnuKritiWadhwa.pdf      # Report outlining the work done in this project
├── src/                                        # Source code
│   ├── assets/                                 # External assets used
│   │   ├── limpopo_golf_course_4k.tx           # Texture file*
│   ├── lighting/                               # Lighting RIB files
│   │   ├── lighting_common.rib                 # Common lighting setup script
│   │   ├── lighting_image1.rib                 # Image 1 lighting setup script
│   │   ├── lighting_image1.rib                 # Image 2 lighting setup script
│   ├── dimples.osl                             # Golf ball shader script
│   ├── dimples.osl                             # Golf ball shader script
│   ├── generate_balls.py                       # Script to generate single or multiple golf balls
│   ├── generate_dimple_centers.py              # Script to set predetermined dimple center coordinates
│   ├── generate_grass.py                       # Grass generation script
│   ├── generate_scenes.py                      # Scene generating script
│   └── render_pipeline.py                      # Main rendering script
├── .gitignore
└── README.md
```
\* texture file from [https://polyhaven.com/a/limpopo_golf_course](https://polyhaven.com/a/limpopo_golf_course)

## Dependencies

- Pixar RenderMan
- Open Shading Language (OSL)
- Python (for initial procedural modeling tests)

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/AnuKritiW/renderman-golfball.git
    cd renderman-golfball
    ```
2. Navigate to the `src/` directory:

    ```bash
    cd src/
    ```

3. If you would like to change the render settings, adjust the constants in `src/render_pipeline.py`

    ```python
    num_dimples = 377
    resolution = "HD"  # Options: "HD", "4K", "8K"
    samples = 1024
    ```

4. Run the RenderMan pipeline:

    ```bash
    python3 render_pipeline.py
    ```

## Output
HD (1920x1080p) renders (`.exr`):
- [Scene 1](./assets/scene_1-HD-1024.exr)
- [Scene 2](./assets/scene_2-HD-1024.exr)

4K (3840x2160p) renders (`.png`):
- [Scene 1](./assets/4K_images/scene_1-4k-1024.png)
- [Scene 2](./assets/4K_images/scene_2-4k-1024.png)

Read the full report [here](./assets/RendermanReport_AnuKritiWadhwa.pdf).