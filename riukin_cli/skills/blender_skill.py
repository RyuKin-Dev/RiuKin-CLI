"""Blender skill - 3D model generation and Blender automation"""
import click
import subprocess
import os
from pathlib import Path


@click.group(name="blender")
def blender_group():
    """Blender 3D operations and model generation"""
    pass


@blender_group.command()
@click.argument("project_name")
@click.option("--type", "model_type", default="weapon", 
              type=click.Choice(["weapon", "character", "prop", "environment"]))
@click.option("--output", "-o", default="./output")
def create_project(project_name, model_type, output):
    """Create new Blender project with CS2-quality base setup"""
    output_path = Path(output) / project_name
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create directory structure
    (output_path / "models").mkdir(exist_ok=True)
    (output_path / "textures" / "pbr").mkdir(parents=True, exist_ok=True)
    (output_path / "textures" / "uv").mkdir(exist_ok=True)
    (output_path / "exports" / "fbx").mkdir(parents=True, exist_ok=True)
    (output_path / "exports" / "obj").mkdir(exist_ok=True)
    (output_path / "renders").mkdir(exist_ok=True)
    (output_path / "scripts").mkdir(exist_ok=True)
    
    # Generate base Blender file with CS2-quality setup
    script_path = output_path / "scripts" / "setup_base.py"
    script_path.write_text(generate_cs2_base_script(model_type))
    
    click.echo(f"Project created: {output_path}")
    click.echo(f"Type: {model_type}")
    click.echo("Run: riukin blender setup-base " + str(output_path))


@blender_group.command()
@click.argument("project_path")
def setup_base(project_path):
    """Initialize Blender file with CS2-quality settings"""
    script = Path(project_path) / "scripts" / "setup_base.py"
    if not script.exists():
        click.echo("Error: Run create-project first")
        return
    
    blend_file = Path(project_path) / "models" / "base_scene.blend"
    
    cmd = [
        "blender",
        "--background",
        "--python", str(script),
        "--",
        str(blend_file)
    ]
    
    subprocess.run(cmd)
    click.echo(f"Base scene created: {blend_file}")


@blender_group.command()
@click.argument("project_path")
@click.option("--type", "asset_type", default="rifle")
def generate_weapon(project_path, asset_type):
    """Generate CS2-quality weapon model"""
    script = generate_weapon_script(asset_type)
    script_path = Path(project_path) / "scripts" / "gen_weapon.py"
    script_path.write_text(script)
    
    cmd = [
        "blender",
        "--background",
        "--python", str(script_path)
    ]
    
    subprocess.run(cmd)
    click.echo(f"Weapon generated: {asset_type}")


@blender_group.command()
@click.argument("project_path")
def export_game(project_path):
    """Export models in game-ready formats (FBX, OBJ)"""
    script = generate_export_script()
    script_path = Path(project_path) / "scripts" / "export_game.py"
    script_path.write_text(script)
    
    cmd = [
        "blender",
        "--background",
        "--python", str(script_path)
    ]
    
    subprocess.run(cmd)
    click.echo("Export complete: fbx/ and obj/ folders")


def generate_cs2_base_script(model_type: str) -> str:
    """Generate Blender Python script for CS2-quality base scene"""
    return '''
import bpy
import sys

# CS2 Quality Settings - Game Asset Pipeline
class CS2AssetSetup:
    """Setup for Counter-Strike 2 quality game assets"""
    
    def __init__(self):
        self.units = "METERS"
        self.scale_factor = 0.01  # CS2 uses cm-scale internally
        self.texel_density = 10.24  # pixels per unit for 1k textures
        
    def clear_scene(self):
        """Remove default objects"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
    def setup_units(self):
        """Configure metric units for game assets"""
        scene = bpy.context.scene
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.scale_length = self.scale_factor
        scene.unit_settings.length_unit = 'CENTIMETERS'
        
    def setup_render_settings(self):
        """Optimize render settings for game asset preview"""
        scene = bpy.context.scene
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 128
        scene.render.resolution_x = 2048
        scene.render.resolution_y = 2048
        
    def create_camera_rig(self):
        """Create turntable camera setup"""
        # Main camera
        bpy.ops.object.camera_add(location=(7, -7, 4))
        camera = bpy.context.active_object
        camera.rotation_euler = (1.1, 0, 0.785)
        camera.data.lens = 50  # 50mm for realistic perspective
        
        # Empty for camera to track
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        target = bpy.context.active_object
        target.name = "CameraTarget"
        
        # Add track to constraint
        constraint = camera.constraints.new(type='TRACK_TO')
        constraint.target = target
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
        
        # Set as active camera
        bpy.context.scene.camera = camera
        
    def create_lighting_studio(self):
        """Create 3-point lighting for game asset presentation"""
        # Key light
        bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
        key = bpy.context.active_object
        key.data.energy = 1000
        key.data.size = 4
        key.rotation_euler = (0.9, 0, 0.785)
        
        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-5, -2, 4))
        fill = bpy.context.active_object
        fill.data.energy = 400
        fill.data.size = 3
        fill.rotation_euler = (1.1, 0, -1.3)
        
        # Rim light
        bpy.ops.object.light_add(type='AREA', location=(0, 6, 6))
        rim = bpy.context.active_object
        rim.data.energy = 600
        rim.data.size = 2
        rim.rotation_euler = (0.8, 0, 3.14)
        
    def create_material_library(self):
        """Create PBR materials for CS2-style assets"""
        # Weapon steel
        steel = bpy.data.materials.new(name="CS2_Weapon_Steel")
        steel.use_nodes = True
        nodes = steel.node_tree.nodes
        nodes.clear()
        
        # Add Principled BSDF
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        # CS2 steel properties
        bsdf.inputs['Base Color'].default_value = (0.2, 0.2, 0.22, 1)
        bsdf.inputs['Metallic'].default_value = 0.95
        bsdf.inputs['Roughness'].default_value = 0.3
        bsdf.inputs['Specular'].default_value = 0.5
        
        steel.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Grip polymer
        polymer = bpy.data.materials.new(name="CS2_Polymer_Grip")
        polymer.use_nodes = True
        nodes = polymer.node_tree.nodes
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Roughness'].default_value = 0.7
        
        polymer.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
    def create_collections(self):
        """Organize scene collections for game pipeline"""
        # Create main collections
        col_high = bpy.data.collections.new("HighPoly")
        col_low = bpy.data.collections.new("LowPoly")
        col_cage = bpy.data.collections.new("Cage")
        col_references = bpy.data.collections.new("References")
        
        scene_col = bpy.context.scene.collection
        scene_col.children.link(col_high)
        scene_col.children.link(col_low)
        scene_col.children.link(col_cage)
        scene_col.children.link(col_references)
        
    def execute(self):
        """Run full setup"""
        self.clear_scene()
        self.setup_units()
        self.setup_render_settings()
        self.create_camera_rig()
        self.create_lighting_studio()
        self.create_material_library()
        self.create_collections()
        
        # Save file
        if len(sys.argv) > 1:
            output_path = sys.argv[-1]
            bpy.ops.wm.save_as_mainfile(filepath=output_path)
            print(f"Saved: {output_path}")

# Run setup
if __name__ == "__main__":
    setup = CS2AssetSetup()
    setup.execute()
'''


def generate_weapon_script(weapon_type: str) -> str:
    """Generate weapon model script"""
    return f'''
import bpy
import bmesh
import math

class CS2WeaponGenerator:
    """Generate CS2-quality weapon models"""
    
    def __init__(self):
        self.scale = 0.01  # CS2 scale
        
    def create_rifle_body(self):
        """Create main rifle body block"""
        # Main receiver
        bpy.ops.mesh.primitive_cube_add(
            size=1, 
            location=(0, 0, 0),
            scale=(8, 1.2, 2.5)
        )
        receiver = bpy.context.active_object
        receiver.name = "Receiver"
        
        # Apply smooth shading
        bpy.ops.object.shade_smooth()
        
        # Add bevel for hard edges
        mod = receiver.modifiers.new(name="Bevel", type='BEVEL')
        mod.width = 0.02
        mod.segments = 2
        
        return receiver
        
    def create_barrel(self):
        """Create rifle barrel"""
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16,
            radius=0.4,
            depth=10,
            location=(8, 0, 0)
        )
        barrel = bpy.context.active_object
        barrel.name = "Barrel"
        barrel.rotation_euler = (0, math.radians(90), 0)
        
        # Add muzzle brake
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8,
            radius=0.6,
            depth=1.5,
            location=(13.5, 0, 0)
        )
        brake = bpy.context.active_object
        brake.name = "MuzzleBrake"
        brake.rotation_euler = (0, math.radians(90), 0)
        
        return barrel
        
    def create_stock(self):
        """Create adjustable stock"""
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(-6, 0, -0.5),
            scale=(5, 1, 2)
        )
        stock = bpy.context.active_object
        stock.name = "Stock"
        
        # Stock buffer tube
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12,
            radius=0.5,
            depth=4,
            location=(-4, 0, 0)
        )
        buffer = bpy.context.active_object
        buffer.name = "BufferTube"
        buffer.rotation_euler = (0, math.radians(90), 0)
        
        return stock
        
    def create_magazine(self):
        """Create curved magazine"""
        # Main mag body
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(1, 0, -4),
            scale=(2.5, 1.2, 6)
        )
        mag = bpy.context.active_object
        mag.name = "Magazine"
        mag.rotation_euler = (0.2, 0, 0)  # Slight curve
        
        # Apply subdivision for smooth curves
        subsurf = mag.modifiers.new(name="Subdivision", type='SUBSURF')
        subsurf.levels = 1
        
        return mag
        
    def create_grip(self):
        """Create pistol grip"""
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(-1, 0, -3),
            scale=(1.5, 1, 4)
        )
        grip = bpy.context.active_object
        grip.name = "Grip"
        grip.rotation_euler = (-0.3, 0, 0)  # Ergonomic angle
        
        return grip
        
    def setup_uv_project(self):
        """Setup UV project from view for texturing"""
        bpy.ops.object.select_all(action='SELECT')
        
        # Smart UV project for game assets
        bpy.ops.uv.smart_project(
            angle_limit=math.radians(66),
            island_margin=0.02,
            area_weight=0,
            correct_aspect=True
        )
        
    def setup_materials(self):
        """Apply CS2 materials"""
        # Get materials from library or create
        steel = bpy.data.materials.get("CS2_Weapon_Steel")
        polymer = bpy.data.materials.get("CS2_Polymer_Grip")
        
        if not steel:
            steel = bpy.data.materials.new(name="CS2_Weapon_Steel")
            steel.use_nodes = True
            
        if not polymer:
            polymer = bpy.data.materials.new(name="CS2_Polymer_Grip")
            polymer.use_nodes = True
        
        # Apply materials
        for obj in bpy.data.objects:
            if "Receiver" in obj.name or "Barrel" in obj.name:
                obj.data.materials.append(steel)
            elif "Grip" in obj.name or "Stock" in obj.name or "Mag" in obj.name:
                obj.data.materials.append(polymer)
                
    def execute(self):
        """Generate complete weapon"""
        # Clear mesh objects only
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Create components
        self.create_rifle_body()
        self.create_barrel()
        self.create_stock()
        self.create_magazine()
        self.create_grip()
        
        # UV and materials
        self.setup_uv_project()
        self.setup_materials()
        
        print("Generated {weapon_type} model")

# Run
if __name__ == "__main__":
    gen = CS2WeaponGenerator()
    gen.execute()
'''


def generate_export_script() -> str:
    """Generate game-ready export script"""
    return '''
import bpy
import os

class CS2Exporter:
    """Export models for CS2/Unity/Unreal"""
    
    def __init__(self):
        self.base_path = bpy.path.abspath("//")
        self.fbx_path = os.path.join(self.base_path, "exports", "fbx")
        self.obj_path = os.path.join(self.base_path, "exports", "obj")
        
    def ensure_folders(self):
        os.makedirs(self.fbx_path, exist_ok=True)
        os.makedirs(self.obj_path, exist_ok=True)
        
    def export_fbx(self, name="weapon"):
        """Export FBX for Unity/Unreal"""
        filepath = os.path.join(self.fbx_path, f"{name}.fbx")
        
        # Select mesh objects only
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        
        # FBX export settings for game engines
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            global_scale=1.0,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_NONE',
            axis_forward='-Z',
            axis_up='Y',
            bake_space_transform=True,
            use_mesh_modifiers=True,
            mesh_smooth_type='FACE',
            use_mesh_edges=False,
            use_tspace=True,
            use_custom_props=True,
            add_leaf_bones=False,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            use_armature_deform_only=True,
            bake_anim=True,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=False,
            bake_anim_use_all_actions=True,
            bake_anim_force_startend_keying=True
        )
        
        print(f"Exported FBX: {filepath}")
        
    def export_obj(self, name="weapon"):
        """Export OBJ as backup format"""
        filepath = os.path.join(self.obj_path, f"{name}.obj")
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        
        # OBJ export
        bpy.ops.export_scene.obj(
            filepath=filepath,
            use_selection=True,
            global_scale=1.0,
            axis_forward='-Z',
            axis_up='Y',
            use_mesh_modifiers=True,
            use_edges=True,
            use_smooth_groups=True,
            use_smooth_groups_bitflags=False,
            use_normals=True,
            use_uvs=True,
            use_materials=True,
            path_mode='AUTO'
        )
        
        print(f"Exported OBJ: {filepath}")
        
    def export_all(self):
        """Export in all formats"""
        self.ensure_folders()
        self.export_fbx()
        self.export_obj()
        print("Export complete!")

# Run
if __name__ == "__main__":
    exporter = CS2Exporter()
    exporter.export_all()
'''
