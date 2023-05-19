import bpy
import random


def setup_gpu_device():
    bpy.context.preferences.addons['cycles'].preferences.get_devices()
    bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    gpu_devices = bpy.context.preferences.addons['cycles'].preferences.devices

    found_device = False
    if gpu_devices:
        for device in gpu_devices:
            print("Found device:", device.name, device.use)
            device.use = False
            if 'RTX' in device.name:
                device.use = True
                found_device = True

    if not found_device:
        raise Exception("Blender does not have access to any RTX GPU. exiting now")


def clear_scene():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()


# Asked ChatGPT to create a "visually interesting complex structure",
# this is what it came up with:
def create_fractal_structure(iterations, radius, position):
    collection_name = "FractalObjects"
    if iterations > 0:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=position)
        obj = bpy.context.active_object
        obj.name = f"Sphere_{iterations}"
        bpy.ops.object.shade_smooth()

        # Create a new collection if it doesn't exist
        if collection_name not in bpy.data.collections:
            bpy.ops.collection.create(name=collection_name)

        # Link the object to the collection
        collection = bpy.data.collections[collection_name]
        # collection.objects.link(obj)

        print(f"Created sphere: {obj.name}")

        for i in range(random.randint(2, 6)):
            next_radius = radius * random.uniform(0.2, 0.8)
            next_position = (
                position[0] + random.uniform(-1, 1),
                position[1] + random.uniform(-1, 1),
                position[2] + random.uniform(-1, 1)
            )
            print(f"Iteration {iterations - 1}: Creating child {i + 1}...")
            create_fractal_structure(iterations - 1, next_radius, next_position)


def setup_camera_and_lights():
    # Remove the default light
    bpy.data.worlds['World'].use_nodes = True
    bpy.data.worlds['World'].node_tree.nodes.remove(bpy.data.worlds['World'].node_tree.nodes["Background"])

    # Create three-point lighting
    light_locations = [(5, -5, 5), (-5, -5, 5), (-5, 5, 5)]
    light_colors = [(1, 0.8, 0.6), (0.4, 0.6, 1.0), (0.4, 0.6, 1.0)]
    light_types = ['KEY', 'FILL', 'RIM']

    for loc, color, light_type in zip(light_locations, light_colors, light_types):
        bpy.ops.object.light_add(type='AREA', location=loc)
        light = bpy.context.active_object
        light.data.energy = 1000  # Adjust the light energy to increase brightness
        light.data.color = color
        light.name = f"{light_type}_Light"

    # Set up camera
    bpy.ops.object.camera_add(location=(5, -5, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.0, 0.0, 0.8)
    bpy.context.scene.camera = camera


def render():
    win = bpy.context.window
    scr = win.screen
    areas3d = [area for area in scr.areas if area.type == 'VIEW_3D']
    region = [region for region in areas3d[0].regions if region.type == 'WINDOW']
    override = {'window': win,
                'screen': scr,
                'area': areas3d[0],
                'region': region[0],
                'scene': bpy.context.scene,
                }

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.feature_set = 'SUPPORTED'
    # bpy.context.scene.cycles.denoiser = 'OPTIX'
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.cycles.adaptive_threshold = 0.01
    bpy.context.scene.cycles.samples = 128
    bpy.context.scene.render.resolution_x = 2048
    bpy.context.scene.render.resolution_y = 2048
    bpy.context.scene.view_settings.view_transform = 'Filmic'
    bpy.context.scene.display_settings.display_device = 'sRGB'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.frame_set(0)
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.render.image_settings.quality = 90
    bpy.context.scene.render.filepath = "/tests/output.jpg"

    with bpy.context.temp_override(**override):
        bpy.ops.view3d.view_camera()

    bpy.ops.render.render(animation=False, write_still=True, use_viewport=True)


setup_gpu_device()
clear_scene()
create_fractal_structure(iterations=5, radius=1.0, position=(0, 0, 0))
setup_camera_and_lights()
render()
bpy.ops.wm.quit_blender()
