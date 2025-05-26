import random
import os

BALL_TEMPLATE = """
AttributeBegin
\tTransformBegin
\t\tTranslate {x} 0.0 {z}
\t\tRotate {rot_x:.2f} 1 0 0
\t\tRotate {rot_y:.2f} 0 1 0
\t\tRotate {rot_z:.2f} 0 0 1

\t\tAttribute "displacementbound" "sphere" [0.1]
\t\tAttribute "dice" "float micropolygonlength" [0.5]

\t\t# 1. Call the OSL pattern shader to compute dispAmount
\t\tPattern "dimples" "dimplePattern{name}"
\t\t\t"float dimple_radius" [0.1]
\t\t\t"float dimple_depth" [0.25]
\t\t\t"int numDimples" [{num_dimples}]
\t\t\t"color baseColor" [{r} {g} {b}]
\t\t\t"int useShadowDarken" [{shadow_darken}]

\t\t# 2. Pass dispAmount to PxrDisplace
\t\tDisplace "PxrDisplace" "golfballDisp{name}"
\t\t\t"float dispAmount" [0.1]
\t\t\t"reference float dispScalar" ["dimplePattern{name}:dispAmount"]

\t\tBxdf "PxrSurface" "PxrGolfBall{name}"
\t\t\t# Plastic base
\t\t\t"reference color diffuseColor" ["dimplePattern{name}:shadowTint"]
\t\t\t"float diffuseGain" [1.0]
\t\t\t"float diffuseExponent" [0.0]

\t\t\t# Specular reflection (gloss)
\t\t\t"int specularFresnelMode" [1] #setting it 1 will ignore faceColor and fresnelExponent
\t\t\t"color specularIor" [1.5 1.5 1.5]

\t\t\t# Make dirt matte
\t\t\t"reference float specularRoughness" ["dimplePattern{name}:roughnessMod"]

\t\t\t# Reduce specular where dirty
\t\t\t"color specularEdgeColor" [0.6 0.6 0.6]
\t\t\t"reference color clearcoatFaceColor" ["dimplePattern{name}:clearcoatColor"]

\t\t\t# clear coat
\t\t\t"color clearcoatFaceColor" [0.015 0.015 0.015]  # Subtle gloss contribution
\t\t\t"color clearcoatEdgeColor" [0.25 0.25 0.25]     # Stronger at glancing angles
\t\t\t"float clearcoatRoughness" [0.03]               # Sharp highlight
\t\t\t"float clearcoatAnisotropy" [0.0]

\t\t\t# Enable bump-like shading from dimples
\t\t\t"int specularModelType" [1] # GGX is better for rough surfaces

\t\tSphere 1 -1 1 360
\tTransformEnd
AttributeEnd
"""

# Abstracted common colors
PINK_COLOR = (0.95, 0.27, 0.6)
PINK_XZ_TRANS = (0.0, 0.0)

def generate_balls(num_dimples, mode="both", base_dir="generated"):
    output_dir = os.path.join(base_dir, "balls")
    os.makedirs(output_dir, exist_ok=True)

    if mode in ("single", "both"):
        # Single pink ball (image 1)
        fpath = os.path.join(output_dir, "single_ball.rib")
        with open(fpath, "w") as f:
            f.write(BALL_TEMPLATE.format(
                name="",
                x=PINK_XZ_TRANS[0], z=PINK_XZ_TRANS[1],
                rot_x=0.0, rot_y=0.0, rot_z=0.0,
                r=PINK_COLOR[0], g=PINK_COLOR[1], b=PINK_COLOR[2],
                num_dimples=num_dimples,
                shadow_darken=0
            ))

    if mode in ("all", "both"):
        # Multiple balls (image 2)
        balls = [
            ("Red", -4.0, 2.75, (1.0, 0.0, 0.0)),
            ("Blue", -0.75, 5.25, (0.0, 0.0, 1.0)),
            ("Pink", PINK_XZ_TRANS[0], PINK_XZ_TRANS[1], PINK_COLOR),
            ("Green", 4.0, 1.5, (0.082, 0.859, 0.082)),
        ]

        fpath = os.path.join(output_dir, "all_balls.rib")
        with open(fpath, "w") as f:
            for name, x, z, (r, g, b) in balls:
                rot_x = rot_y = rot_z = 0.0
                if name != "Pink":
                    rot_x = random.uniform(0, 360)
                    rot_y = random.uniform(0, 360)
                    rot_z = random.uniform(0, 360)
                f.write(BALL_TEMPLATE.format(
                    name=name,
                    x=x, z=z,
                    rot_x=rot_x, rot_y=rot_y, rot_z=rot_z,
                    r=r, g=g, b=b,
                    num_dimples=num_dimples,
                    shadow_darken=1
                ))
                f.write("\n\n")

if __name__ == "__main__":
    generate_balls(num_dimples=377, mode="both")
