# generate_balls.py
import random
import os

BALL_TEMPLATE = """
AttributeBegin
    TransformBegin
        Translate {x} 0.0 {z}
        Rotate {rot_x:.2f} 1 0 0
        Rotate {rot_y:.2f} 0 1 0
        Rotate {rot_z:.2f} 0 0 1

        Attribute "displacementbound" "sphere" [0.1]
        Attribute "dice" "float micropolygonlength" [0.5]

        # 1. Call the OSL pattern shader to compute dispAmount
        Pattern "dimples" "dimplePattern{name}"
            "float dimple_radius" [0.1]
            "float dimple_depth" [0.25]
            "int numDimples" [{num_dimples}]
            "color baseColor" [{r} {g} {b}]
            "int useShadowDarken" [{shadow_darken}]

        # 2. Pass dispAmount to PxrDisplace
        Displace "PxrDisplace" "golfballDisp{name}"
            "float dispAmount" [0.1]
            "reference float dispScalar" ["dimplePattern{name}:dispAmount"]

        Bxdf "PxrSurface" "PxrGolfBall{name}"
            # Plastic base
            "reference color diffuseColor" ["dimplePattern{name}:shadowTint"]
            "float diffuseGain" [1.0]
            "float diffuseExponent" [0.0]

            # Specular reflection (gloss)
            "int specularFresnelMode" [1] #setting it 1 will ignore faceColor and fresnelExponent
            "color specularIor" [1.5 1.5 1.5]

            # Make dirt matte
            "reference float specularRoughness" ["dimplePattern{name}:roughnessMod"]

            # Reduce specular where dirty
            "color specularEdgeColor" [0.6 0.6 0.6]
            "reference color clearcoatFaceColor" ["dimplePattern{name}:clearcoatColor"]

            # clear coat
            "color clearcoatFaceColor" [0.015 0.015 0.015]  # Subtle gloss contribution
            "color clearcoatEdgeColor" [0.25 0.25 0.25]     # Stronger at glancing angles
            "float clearcoatRoughness" [0.03]               # Sharp highlight
            "float clearcoatAnisotropy" [0.0]

            # Enable bump-like shading from dimples
            "int specularModelType" [1] # GGX is better for rough surfaces

        Sphere 1 -1 1 360
    TransformEnd
AttributeEnd
"""

# Abstracted common colors
PINK_COLOR = (0.95, 0.27, 0.6)
PINK_XZ_TRANS = (0.0, 0.0)
# You could also define other common colors here if needed.

def generate_balls(num_dimples, mode="both"):
    os.makedirs("balls", exist_ok=True)

    if mode in ("single", "both"):
        # Single pink ball (image 1)
        fpath = "balls/single_ball.rib"
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

        fpath = "balls/all_balls.rib"
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
