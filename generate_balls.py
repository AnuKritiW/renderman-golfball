# generate_balls.py
import math
import random

BALL_TEMPLATE = """
AttributeBegin
    TransformBegin
        Translate {x} 0.0 {z}
        Rotate {rot_x:.2f} 1 0 0
        Rotate {rot_y:.2f} 0 1 0
        Rotate {rot_z:.2f} 0 0 1
    
        Attribute "displacementbound" "sphere" [0.1]
        Attribute "dice" "float micropolygonlength" [0.5]

        Pattern "dimples" "dimplePattern{name}"
            "float dimple_radius" [0.1]
            "float dimple_depth" [0.25]
            "int numDimples" [377]
            "color baseColor" [{r} {g} {b}]
            "int useShadowDarken" [1]

        Displace "PxrDisplace" "golfballDisp{name}"
            "float dispAmount" [0.1]
            "reference float dispScalar" ["dimplePattern{name}:dispAmount"]

        Bxdf "PxrSurface" "PxrGolfBall{name}"
            "reference color diffuseColor" ["dimplePattern{name}:shadowTint"]
            "float diffuseGain" [1.0]
            "float diffuseExponent" [0.0]
            "int specularFresnelMode" [1]
            "color specularIor" [1.5 1.5 1.5]
            "reference float specularRoughness" ["dimplePattern{name}:roughnessMod"]
            "color specularEdgeColor" [0.6 0.6 0.6]
            "reference color clearcoatFaceColor" ["dimplePattern{name}:clearcoatColor"]
            "color clearcoatFaceColor" [0.015 0.015 0.015]
            "color clearcoatEdgeColor" [0.25 0.25 0.25]
            "float clearcoatRoughness" [0.03]
            "float clearcoatAnisotropy" [0.0]
            "int specularModelType" [1]

        Sphere 1 -1 1 360
    TransformEnd
AttributeEnd
"""

balls = [
    ("Red",   -4.0, 2.75, (1.0, 0.0, 0.0)),
    ("Blue",   -0.75, 5.25, (0.0, 0.0, 1.0)),
    ("Pink",   0.0, 0.0, (0.95, 0.27, 0.6)),
    ("Green",  4.0, 1.5, (0.082, 0.859, 0.082)),
]

with open("balls/all_balls.rib", "w") as f:
    for name, x, z, (r, g, b) in balls:
        rot_x = rot_y = rot_z = 0.0
        if name != "Pink":
            rot_x = random.uniform(0, 360)
            rot_y = random.uniform(0, 360)
            rot_z = random.uniform(0, 360)
        f.write(BALL_TEMPLATE.format(name=name,
                                     x=x, z=z,
                                     rot_x=rot_x, rot_y=rot_y, rot_z=z,
                                     r=r, g=g, b=b))
        f.write("\n\n")
