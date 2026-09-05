from pathlib import Path

BASE = Path.home() / "synaids_amr/worlds/warehouse_multi.sdf"
OUT = Path.home() / "synaids_amr/worlds/warehouse_realistic.sdf"


def material(color):
    return f"""
      <material>
        <ambient>{color}</ambient>
        <diffuse>{color}</diffuse>
        <specular>0.15 0.15 0.15 1</specular>
      </material>
"""


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
        <visual name="visual">
          <geometry>
            <box>
              <size>{sx} {sy} {sz}</size>
            </box>
          </geometry>
          {material(color)}
        </visual>
        {collision_xml}
      </link>
    </model>
"""


def cylinder(name, x, y, z, radius, height,
             color="0.8 0.5 0.1 1"):

    return f"""
    <model name="{name}">
      <static>true</static>
      <pose>{x} {y} {z} 0 0 0</pose>

      <link name="link">
        <visual name="visual">
          <geometry>
            <cylinder>
              <radius>{radius}</radius>
              <length>{height}</length>
            </cylinder>
          </geometry>
          {material(color)}
        </visual>

        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>{radius}</radius>
              <length>{height}</length>
            </cylinder>
          </geometry>
        </collision>
      </link>
    </model>
"""


def rack(name, x, y, levels=4, boxes=True):

    s = ""

    # Rack dimensions
    width = 2.2
    depth = 1.0
    post_h = 3.4

    # Four vertical posts
    for i, (px, py) in enumerate([
        (-width/2, -depth/2),
        (-width/2,  depth/2),
        ( width/2, -depth/2),
        ( width/2,  depth/2),
    ]):
        s += box(
            f"{name}_post_{i}",
            x + px,
            y + py,
            post_h/2,
            0.12,
            0.12,
            post_h,
            "0.12 0.14 0.16 1"
        )

    # Horizontal shelf beams
    for level in range(levels):
        z = 0.65 + level * 0.78

        s += box(
            f"{name}_beam_front_{level}",
            x,
            y - depth/2,
            z,
            width,
            0.10,
            0.10,
            "0.95 0.60 0.08 1"
        )

        s += box(
            f"{name}_beam_back_{level}",
            x,
            y + depth/2,
            z,
            width,
            0.10,
            0.10,
            "0.95 0.60 0.08 1"
        )

        # Shelf deck
        s += box(
            f"{name}_shelf_{level}",
            x,
            y,
            z - 0.08,
            width,
            depth,
            0.08,
            "0.25 0.28 0.30 1"
        )

        if boxes:
            # Three inventory packages on each level
            package_colors = [
                "0.72 0.48 0.22 1",
                "0.85 0.65 0.30 1",
                "0.42 0.62 0.78 1"
            ]

            for b in range(3):

                bx = x - 0.65 + b * 0.65

                s += box(
                    f"{name}_package_{level}_{b}",
                    bx,
                    y,
                    z + 0.22,
                    0.42,
                    0.55,
                    0.42,
                    package_colors[b]
                )

    # Rack end protection
    s += cylinder(
        f"{name}_guard_left",
        x - width/2 - 0.18,
        y,
        0.35,
        0.07,
        0.7,
        "0.95 0.65 0.05 1"
    )

    s += cylinder(
        f"{name}_guard_right",
        x + width/2 + 0.18,
        y,
        0.35,
        0.07,
        0.7,
        "0.95 0.65 0.05 1"
    )

    return s


def pallet(name, x, y, z=0.10):

    s = ""

    # Wooden pallet
    s += box(
        f"{name}_base",
        x, y, z,
        1.2, 0.9, 0.18,
        "0.55 0.34 0.16 1"
    )

    # Pallet slats
    for i in range(3):
        px = x - 0.40 + i * 0.40

        s += box(
            f"{name}_slat_{i}",
            px,
            y,
            z + 0.11,
            0.10,
            0.82,
            0.06,
            "0.72 0.48 0.24 1"
        )

    return s


def package(name, x, y, z, sx=0.55, sy=0.55, sz=0.55,
            color="0.78 0.56 0.28 1"):

    return box(
        name,
        x, y, z,
        sx, sy, sz,
        color
    )


def floor_mark(name, x, y, sx, sy,
               color="0.95 0.85 0.05 1"):

    return box(
        name,
        x, y, 0.012,
        sx, sy, 0.025,
        color,
        collision=False
    )


def build():

    text = BASE.read_text()

    objects = []

    # ==========================================================
    # CENTRAL INTERSECTION
    # ==========================================================

    objects.append(
        box(
            "intersection_surface",
            0, 0, 0.018,
            4.0, 4.0, 0.025,
            "0.92 0.72 0.05 1",
            False
        )
    )

    # Cross markings
    objects += [
        floor_mark("intersection_line_1", 0, -1.75, 3.6, 0.08),
        floor_mark("intersection_line_2", 0,  1.75, 3.6, 0.08),
        floor_mark("intersection_line_3", -1.75, 0, 0.08, 3.6),
        floor_mark("intersection_line_4",  1.75, 0, 0.08, 3.6),
    ]

    # ==========================================================
    # RACK AISLES
    # ==========================================================

    rack_positions = [
        (-6.5,  3.0),
        (-3.3,  3.0),
        ( 3.3,  3.0),
        ( 6.5,  3.0),

        (-6.5, -3.0),
        (-3.3, -3.0),
        ( 3.3, -3.0),
        ( 6.5, -3.0),
    ]

    for i, (x, y) in enumerate(rack_positions):
        objects.append(
            rack(
                f"storage_rack_{i+1}",
                x, y,
                levels=4,
                boxes=True
            )
        )

    # ==========================================================
    # EXTRA SIDE STORAGE
    # ==========================================================

    for i, y in enumerate([5.8, 6.9, -5.8, -6.9]):

        objects.append(
            rack(
                f"wall_rack_{i+1}",
                -9.5,
                y,
                levels=3,
                boxes=True
            )
        )

        objects.append(
            rack(
                f"wall_rack_right_{i+1}",
                9.5,
                y,
                levels=3,
                boxes=True
            )
        )

    # ==========================================================
    # PICKUP ZONES P1 P2 P3
    # ==========================================================

    pickup = [
        (-7.8, 6.0),
        (-4.8, 6.0),
        (-1.8, 6.0)
    ]

    for i, (x, y) in enumerate(pickup, 1):

        objects.append(
            floor_mark(
                f"pickup_zone_{i}",
                x, y,
                2.2, 1.8,
                "0.15 0.75 0.35 1"
            )
        )

        objects.append(
            pallet(
                f"pickup_pallet_{i}",
                x, y,
                0.11
            )
        )

        objects.append(
            package(
                f"pickup_package_{i}",
                x, y,
                0.48,
                0.65, 0.65, 0.65
            )
        )

    # ==========================================================
    # DROP-OFF ZONES D1 D2 D3
    # ==========================================================

    dropoff = [
        (-6.5, -7.0),
        (0.0, -7.0),
        (6.5, -7.0)
    ]

    for i, (x, y) in enumerate(dropoff, 1):

        objects.append(
            floor_mark(
                f"dropoff_zone_{i}",
                x, y,
                2.5, 1.5,
                "0.15 0.40 0.90 1"
            )
        )

        objects.append(
            pallet(
                f"dropoff_pallet_{i}",
                x, y,
                0.11
            )
        )

        objects.append(
            package(
                f"dropoff_package_{i}",
                x, y,
                0.48,
                0.65, 0.65, 0.65,
                "0.55 0.68 0.82 1"
            )
        )

    # ==========================================================
    # CHARGING STATION
    # ==========================================================

    objects.append(
        floor_mark(
            "charging_floor",
            7.7, 6.2,
            3.5, 2.2,
            "0.20 0.80 0.25 1"
        )
    )

    for i in range(3):

        x = 6.6 + i * 1.1

        # charging pedestal
        objects.append(
            box(
                f"charger_{i+1}",
                x, 6.2, 0.7,
                0.35, 0.35, 1.2,
                "0.08 0.12 0.10 1"
            )
        )

        # green charging indicator
        objects.append(
            box(
                f"charger_light_{i+1}",
                x, 5.98, 0.95,
                0.12, 0.04, 0.15,
                "0.20 1.0 0.20 1",
                False
            )
        )

    # ==========================================================
    # WAITING / PARKING BAY
    # ==========================================================

    objects.append(
        floor_mark(
            "waiting_bay",
            7.0, -3.8,
            3.2, 2.0,
            "0.20 0.45 0.90 1"
        )
    )

    for i in range(2):

        objects.append(
            pallet(
                f"waiting_pallet_{i+1}",
                6.5 + i * 0.9,
                -3.8
            )
        )

    # ==========================================================
    # BLOCKED AISLE / DYNAMIC OBSTACLE
    # ==========================================================

    objects.append(
        box(
            "blocked_aisle_zone",
            -8.0, 0.2, 0.025,
            2.2, 2.4, 0.05,
            "0.90 0.18 0.18 1",
            False
        )
    )

    # Large pallet blocking aisle
    objects.append(
        pallet(
            "blocked_pallet",
            -8.0,
            0.2,
            0.12
        )
    )

    objects.append(
        package(
            "blocked_package_1",
            -8.0,
            0.2,
            0.55,
            0.85,
            0.75,
            0.75
        )
    )

    # ==========================================================
    # SAFETY BOLLARDS
    # ==========================================================

    bollards = [
        (-2.2,  2.2), (2.2,  2.2),
        (-2.2, -2.2), (2.2, -2.2),
        (-4.5,  1.8), (4.5,  1.8),
        (-4.5, -1.8), (4.5, -1.8),
        (-9.0,  1.8), (-9.0, -1.8),
        (9.0,  1.8), (9.0, -1.8)
    ]

    for i, (x, y) in enumerate(bollards):
        objects.append(
            cylinder(
                f"safety_bollard_{i}",
                x, y,
                0.40,
                0.09,
                0.80,
                "0.95 0.65 0.05 1"
            )
        )

    # ==========================================================
    # SAFETY BARRIERS AROUND BLOCKED AISLE
    # ==========================================================

    objects += [
        box(
            "blocked_barrier_left",
            -9.0, 0.2, 0.55,
            0.12, 2.8, 1.1,
            "0.90 0.12 0.12 1"
        ),
        box(
            "blocked_barrier_right",
            -7.0, 0.2, 0.55,
            0.12, 2.8, 1.1,
            "0.90 0.12 0.12 1"
        )
    ]

    # ==========================================================
    # EXTRA PALLETS THROUGHOUT WAREHOUSE
    # ==========================================================

    loose_pallets = [
        (-10.0, 3.5),
        (-10.0, -3.5),
        (-5.0, 0.9),
        (5.0, 0.9),
        (-5.0, -0.9),
        (5.0, -0.9),
        (8.8, -5.0)
    ]

    for i, (x, y) in enumerate(loose_pallets):

        objects.append(
            pallet(
                f"loose_pallet_{i}",
                x, y
            )
        )

        objects.append(
            package(
                f"loose_package_{i}",
                x, y,
                0.48
            )
        )

    # ==========================================================
    # ROAD / AISLE MARKINGS
    # ==========================================================

    # Horizontal main aisle
    objects += [
        floor_mark("road_horizontal_top", 0, 2.25, 20, 0.055,
                    "0.95 0.95 0.95 1"),
        floor_mark("road_horizontal_bottom", 0, -2.25, 20, 0.055,
                    "0.95 0.95 0.95 1"),

        # Vertical main aisle
        floor_mark("road_vertical_left", -2.25, 0, 0.055, 14,
                    "0.95 0.95 0.95 1"),
        floor_mark("road_vertical_right", 2.25, 0, 0.055, 14,
                    "0.95 0.95 0.95 1")
    ]

    # Yellow aisle boundaries
    for x in [-4.5, -2.9, 2.9, 4.5]:
        objects.append(
            floor_mark(
                f"aisle_boundary_{x}",
                x, 0,
                0.045, 14,
                "0.95 0.75 0.05 1"
            )
        )

    # ==========================================================
    # MAINTENANCE AREA
    # ==========================================================

    objects.append(
        floor_mark(
            "enhanced_maintenance_area",
            9.0, 0,
            2.0, 2.5,
            "0.55 0.55 0.58 1"
        )
    )

    objects.append(
        box(
            "maintenance_workbench",
            9.0, 0.0, 0.8,
            1.6, 0.6, 0.12,
            "0.20 0.22 0.25 1"
        )
    )

    objects.append(
        box(
            "maintenance_toolbox",
            9.0, -0.5, 0.35,
            0.7, 0.4, 0.55,
            "0.80 0.15 0.10 1"
        )
    )

    # ==========================================================
    # RESTRICTED ZONE
    # ==========================================================

    objects.append(
        floor_mark(
            "enhanced_restricted_zone",
            -9.0, -6.0,
            3.0, 2.2,
            "0.75 0.12 0.12 1"
        )
    )

    for i, x in enumerate([-10.2, -9.0, -7.8]):
        objects.append(
            cylinder(
                f"restricted_post_{i}",
                x, -6.0,
                0.45,
                0.08,
                0.9,
                "0.90 0.10 0.10 1"
            )
        )

    # ==========================================================
    # EXTRA SAFETY CONES
    # ==========================================================

    for i, (x, y) in enumerate([
        (-9.4, 1.5),
        (-8.6, 1.5),
        (-9.4, -1.1),
        (-8.6, -1.1),
        (-1.0, 2.0),
        (1.0, 2.0)
    ]):

        objects.append(
            cylinder(
                f"traffic_cone_{i}",
                x, y,
                0.20,
                0.13,
                0.40,
                "1.0 0.35 0.05 1"
            )
        )

    # ==========================================================
    # INSERT EVERYTHING BEFORE </world>
    # ==========================================================

    insertion = "\n".join(objects)

    if "</world>" not in text:
        raise RuntimeError("Could not find </world> in base SDF")

    text = text.replace(
        "</world>",
        insertion + "\n</world>"
    )

    OUT.write_text(text)

    print()
    print("==============================================")
    print(" REALISTIC WAREHOUSE CREATED")
    print("==============================================")
    print(f"Output: {OUT}")
    print(f"Objects added: {len(objects)}")
    print("==============================================")


if __name__ == "__main__":
    build()
