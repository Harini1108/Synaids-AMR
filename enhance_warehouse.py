from pathlib import Path

WORLD = Path.home() / "synaids_amr/worlds/warehouse_multi.sdf"
OUT = Path.home() / "synaids_amr/worlds/warehouse_enhanced.sdf"


def box(name, x, y, z, sx, sy, sz,
        color="0.65 0.65 0.65 1",
        collision=True):

    collision_xml = ""

    if collision:
        collision_xml = f"""
        <collision name="collision">
          <geometry>
            <box>
              <size>{sx} {sy} {sz}</size>
            </box>
          </geometry>
        </collision>
        """

    return f"""
    <model name="{name}">
      <static>true</static>
      <pose>{x} {y} {z} 0 0 0</pose>
      <link name="link">

        {collision_xml}

        <visual name="visual">
          <geometry>
            <box>
              <size>{sx} {sy} {sz}</size>
            </box>
          </geometry>
          <material>
            <ambient>{color}</ambient>
            <diffuse>{color}</diffuse>
          </material>
        </visual>

      </link>
    </model>
"""


def cylinder(name, x, y, z, radius, height,
             color="0.95 0.55 0.05 1"):

    return f"""
    <model name="{name}">
      <static>true</static>
      <pose>{x} {y} {z} 0 0 0</pose>
      <link name="link">

        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>{radius}</radius>
              <length>{height}</length>
            </cylinder>
          </geometry>
        </collision>

        <visual name="visual">
          <geometry>
            <cylinder>
              <radius>{radius}</radius>
              <length>{height}</length>
            </cylinder>
          </geometry>
          <material>
            <ambient>{color}</ambient>
            <diffuse>{color}</diffuse>
          </material>
        </visual>

      </link>
    </model>
"""


original = WORLD.read_text()

objects = []

# ============================================================
# 1. RACK INVENTORY
# ============================================================

rack_positions = [
    (-6, 3),
    (0, 3),
    (6, 3),
    (-6, -3),
    (0, -3),
    (6, -3),
]

colors = [
    "0.58 0.32 0.12 1",
    "0.12 0.38 0.65 1",
    "0.72 0.42 0.18 1",
    "0.35 0.42 0.48 1",
]

idx = 0

for rx, ry in rack_positions:

    # Upper cartons
    for dx, dy, c in [
        (-0.65, -0.55, colors[0]),
        (0.0, -0.55, colors[1]),
        (0.65, -0.55, colors[2]),
        (-0.35, 0.45, colors[3]),
        (0.35, 0.45, colors[0]),
    ]:

        objects.append(
            box(
                f"inventory_{idx}",
                rx + dx,
                ry + dy,
                2.45,
                0.45,
                0.45,
                0.45,
                c
            )
        )

        idx += 1

    # Small bins
    for dx, dy in [(-0.7, 0.45), (0.7, 0.45)]:

        objects.append(
            box(
                f"bin_{idx}",
                rx + dx,
                ry + dy,
                2.85,
                0.38,
                0.38,
                0.32,
                "0.08 0.30 0.55 1"
            )
        )

        idx += 1


# ============================================================
# 2. PALLETS / CARTONS
# ============================================================

pallet_locations = [
    (-8.0, 1.8),
    (-7.2, -1.5),
    (3.8, 5.4),
    (7.0, -1.8),
    (3.2, -6.0),
]

for i, (x, y) in enumerate(pallet_locations):

    # pallet base
    objects.append(
        box(
            f"pallet_{i}",
            x,
            y,
            0.10,
            1.2,
            0.9,
            0.20,
            "0.50 0.28 0.10 1"
        )
    )

    # boxes on pallet
    objects.append(
        box(
            f"pallet_box_{i}_a",
            x - 0.25,
            y,
            0.45,
            0.45,
            0.45,
            0.55,
            "0.63 0.37 0.14 1"
        )
    )

    objects.append(
        box(
            f"pallet_box_{i}_b",
            x + 0.25,
            y,
            0.45,
            0.45,
            0.45,
            0.55,
            "0.70 0.45 0.20 1"
        )
    )


# ============================================================
# 3. CENTRAL INTERSECTION
# ============================================================

# Yellow conflict-zone border
objects.extend([
    box(
        "intersection_north",
        0,
        1.55,
        0.015,
        4.2,
        0.08,
        0.03,
        "0.95 0.75 0.05 1",
        False
    ),

    box(
        "intersection_south",
        0,
        -1.55,
        0.015,
        4.2,
        0.08,
        0.03,
        "0.95 0.75 0.05 1",
        False
    ),

    box(
        "intersection_east",
        2.05,
        0,
        0.015,
        0.08,
        3.1,
        0.03,
        "0.95 0.75 0.05 1",
        False
    ),

    box(
        "intersection_west",
        -2.05,
        0,
        0.015,
        0.08,
        3.1,
        0.03,
        "0.95 0.75 0.05 1",
        False
    ),
])


# ============================================================
# 4. STOP LINES
# ============================================================

objects.extend([
    box(
        "stop_R1",
        -2.6,
        2.0,
        0.02,
        1.2,
        0.10,
        0.035,
        "0.95 0.95 0.95 1",
        False
    ),

    box(
        "stop_R3",
        -2.6,
        -2.0,
        0.02,
        1.2,
        0.10,
        0.035,
        "0.95 0.95 0.95 1",
        False
    ),

    box(
        "stop_R2",
        2.6,
        0,
        0.02,
        0.10,
        1.2,
        0.035,
        "0.95 0.95 0.95 1",
        False
    ),
])


# ============================================================
# 5. TRAFFIC / SAFETY BOLLARDS
# ============================================================

bollards = [
    (-2.0, 1.8),
    (2.0, 1.8),
    (-2.0, -1.8),
    (2.0, -1.8),
]

for i, (x, y) in enumerate(bollards):

    objects.append(
        cylinder(
            f"bollard_{i}",
            x,
            y,
            0.45,
            0.10,
            0.90,
            "0.95 0.65 0.05 1"
        )
    )


# ============================================================
# 6. SAFETY CONES
# ============================================================

cones = [
    (-4.0, 2.2),
    (-4.0, -2.2),
    (4.0, 2.2),
    (4.0, -2.2),
    (1.8, 3.8),
]

for i, (x, y) in enumerate(cones):

    objects.append(
        cylinder(
            f"safety_cone_{i}",
            x,
            y,
            0.25,
            0.13,
            0.50,
            "0.95 0.25 0.03 1"
        )
    )


# ============================================================
# 7. RESTRICTED AREA BARRIERS
# ============================================================

objects.extend([
    box(
        "restricted_barrier_1",
        -9,
        -5.1,
        0.55,
        2.0,
        0.12,
        1.1,
        "0.95 0.75 0.05 1"
    ),

    box(
        "restricted_barrier_2",
        -7.95,
        -6,
        0.55,
        0.12,
        1.8,
        1.1,
        "0.95 0.75 0.05 1"
    ),
])


# ============================================================
# 8. LOADING AREA
# ============================================================

objects.extend([
    box(
        "loading_marking",
        8.5,
        -5.0,
        0.012,
        3.0,
        0.08,
        0.025,
        "0.20 0.65 0.95 1",
        False
    ),

    box(
        "loading_pallet",
        7.5,
        -6.2,
        0.10,
        1.2,
        0.9,
        0.20,
        "0.50 0.28 0.10 1"
    ),
])


# ============================================================
# 9. SMALL MAINTENANCE OBSTACLE
# ============================================================

objects.extend([
    box(
        "maintenance_cart",
        8.0,
        2.8,
        0.45,
        1.0,
        0.65,
        0.9,
        "0.30 0.32 0.35 1"
    ),

    box(
        "maintenance_box",
        8.0,
        2.8,
        1.15,
        0.5,
        0.45,
        0.45,
        "0.75 0.35 0.10 1"
    ),
])


# ============================================================
# INSERT BEFORE </world>
# ============================================================

if "</world>" not in original:
    raise RuntimeError("Could not find </world>")

enhanced = original.replace(
    "</world>",
    "\n".join(objects) + "\n</world>"
)

OUT.write_text(enhanced)

print("======================================")
print("ENHANCED WAREHOUSE CREATED")
print("======================================")
print(OUT)
print(f"Added {len(objects)} static objects.")
