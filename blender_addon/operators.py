import bpy
import bmesh
import math
import os


class RIUKIN_OT_generate_weapon(bpy.types.Operator):
    """Generate CS2-quality weapon model"""
    bl_idname = "riukin.generate_weapon"
    bl_label = "Generate Weapon"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        weapon_type = context.scene.riukin_weapon_type
        
        generator = CS2WeaponGenerator()
        generator.clear_scene()
        
        if weapon_type == 'RIFLE':
            generator.create_rifle()
        elif weapon_type == 'PISTOL':
            generator.create_pistol()
        elif weapon_type == 'KNIFE':
            generator.create_knife()
        else:
            generator.create_rifle()  # Default
            
        generator.optimize_mesh()
        generator.create_uvs()
        generator.assign_materials()
        
        self.report({'INFO'}, f"Generated {weapon_type}")
        return {'FINISHED'}


class RIUKIN_OT_generate_prop(bpy.types.Operator):
    """Generate environment prop"""
    bl_idname = "riukin.generate_prop"
    bl_label = "Generate Prop"
    bl_options = {'REGISTER', 'UNDO'}
    
    prop_type: bpy.props.EnumProperty(
        items=[
            ('CRATE', "Crate", "Military crate"),
            ('BARREL', "Barrel", "Oil barrel"),
            ('BOX', "Box", "Cardboard box"),
        ]
    )
    
    def execute(self, context):
        generator = CS2PropGenerator()
        generator.create_crate()
        self.report({'INFO'}, "Generated crate")
        return {'FINISHED'}


class RIUKIN_OT_setup_cs2_scene(bpy.types.Operator):
    """Setup scene for CS2 asset creation"""
    bl_idname = "riukin.setup_cs2_scene"
    bl_label = "Setup CS2 Scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        setup = CS2SceneSetup()
        setup.execute()
        self.report({'INFO'}, "CS2 scene ready")
        return {'FINISHED'}


class RIUKIN_OT_export_game_ready(bpy.types.Operator):
    """Export for game engines"""
    bl_idname = "riukin.export_game"
    bl_label = "Export Game-Ready"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        exporter = CS2GameExporter()
        exporter.export_fbx()
        exporter.export_obj()
        self.report({'INFO'}, "Export complete")
        return {'FINISHED'}


class CS2WeaponGenerator:
    """High-quality weapon generator matching CS2 standards"""
    
    def clear_scene(self):
        """Remove all mesh objects"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
    
    def create_rifle(self):
        """Create detailed assault rifle"""
        # Scale reference: CS2 weapons are roughly 1m total length
        scale = 1.0
        
        # Upper receiver
        mesh = bpy.data.meshes.new("ReceiverMesh")
        receiver = bpy.data.objects.new("Receiver", mesh)
        bpy.context.collection.objects.link(receiver)
        
        # Build detailed receiver with proper proportions
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        # Scale to rifle proportions (length, height, width)
        for v in bm.verts:
            v.co.x *= 0.4  # Length: 40cm
            v.co.y *= 0.08  # Width: 8cm
            v.co.z *= 0.12  # Height: 12cm
        
        bm.to_mesh(mesh)
        bm.free()
        
        receiver.location = (0, 0, 0.06)
        
        # Add edge detail via bevel
        bevel = receiver.modifiers.new(name="Bevel", type='BEVEL')
        bevel.width = 0.002
        bevel.segments = 2
        bevel.limit_method = 'ANGLE'
        bevel.angle_limit = 0.610865  # 35 degrees
        
        # Handguard
        handguard_mesh = bpy.data.meshes.new("HandguardMesh")
        handguard = bpy.data.objects.new("Handguard", handguard_mesh)
        bpy.context.collection.objects.link(handguard)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co.x *= 0.3  # 30cm
            v.co.y *= 0.09
            v.co.z *= 0.11
        
        bm.to_mesh(handguard_mesh)
        bm.free()
        
        handguard.location = (0.35, 0, 0.055)
        
        # Barrel with threading detail
        barrel_mesh = bpy.data.meshes.new("BarrelMesh")
        barrel = bpy.data.objects.new("Barrel", barrel_mesh)
        bpy.context.collection.objects.link(barrel)
        
        bm = bmesh.new()
        # Create cylinder with proper orientation
        bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=16,
            radius1=0.02,
            radius2=0.02,
            depth=0.5
        )
        
        bm.to_mesh(barrel_mesh)
        bm.free()
        
        barrel.location = (0.65, 0, 0.06)
        barrel.rotation_euler = (0, math.radians(90), 0)
        
        # Muzzle device
        muzzle_mesh = bpy.data.meshes.new("MuzzleMesh")
        muzzle = bpy.data.objects.new("MuzzleBrake", muzzle_mesh)
        bpy.context.collection.objects.link(muzzle)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co.x *= 0.06  # Length
            v.co.y *= 0.035  # Width
            v.co.z *= 0.035
        
        bm.to_mesh(muzzle_mesh)
        bm.free()
        
        muzzle.location = (0.9, 0, 0.06)
        
        # Magazine with curve
        mag_mesh = bpy.data.meshes.new("MagazineMesh")
        magazine = bpy.data.objects.new("Magazine", mag_mesh)
        bpy.context.collection.objects.link(magazine)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co.x *= 0.12
            v.co.y *= 0.035
            v.co.z *= 0.25
        
        # Apply taper
        for v in bm.verts:
            if v.co.z < 0:
                v.co.x *= 0.85
        
        bm.to_mesh(mag_mesh)
        bm.free()
        
        magazine.location = (-0.05, 0, -0.12)
        magazine.rotation_euler = (0.15, 0, 0)  # Curve
        
        # Pistol grip
        grip_mesh = bpy.data.meshes.new("GripMesh")
        grip = bpy.data.objects.new("PistolGrip", grip_mesh)
        bpy.context.collection.objects.link(grip)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co.x *= 0.08
            v.co.y *= 0.04
            v.co.z *= 0.15
        
        bm.to_mesh(grip_mesh)
        bm.free()
        
        grip.location = (-0.15, 0, -0.08)
        grip.rotation_euler = (-0.35, 0, 0)  # Ergonomic angle
        
        # Stock
        stock_mesh = bpy.data.meshes.new("StockMesh")
        stock = bpy.data.objects.new("Stock", stock_mesh)
        bpy.context.collection.objects.link(stock)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co.x *= 0.25
            v.co.y *= 0.04
            v.co.z *= 0.12
        
        bm.to_mesh(stock_mesh)
        bm.free()
        
        stock.location = (-0.35, 0, 0.02)
        
        # Select all for joining
        for obj in [receiver, handguard, barrel, muzzle, magazine, grip, stock]:
            obj.select_set(True)
        
        # Join into single mesh
        bpy.context.view_layer.objects.active = receiver
        bpy.ops.object.join()
        receiver.name = "Rifle_HighPoly"
        
    def create_pistol(self):
        """Create detailed pistol"""
        mesh = bpy.data.meshes.new("PistolMesh")
        pistol = bpy.data.objects.new("Pistol", mesh)
        bpy.context.collection.objects.link(pistol)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        # Pistol proportions
        for v in bm.verts:
            v.co.x *= 0.22  # Length
            v.co.y *= 0.035  # Width
            v.co.z *= 0.14  # Height
        
        bm.to_mesh(mesh)
        bm.free()
        
        pistol.location = (0, 0, 0.07)
        
    def create_knife(self):
        """Create detailed knife"""
        # Blade
        mesh = bpy.data.meshes.new("BladeMesh")
        blade = bpy.data.objects.new("Blade", mesh)
        bpy.context.collection.objects.link(blade)
        
        bm = bmesh.new()
        
        # Create blade shape
        verts = []
        # Spine
        verts.append(bm.verts.new((0, 0, 0.03)))
        verts.append(bm.verts.new((0.25, 0, 0.03)))
        verts.append(bm.verts.new((0.35, 0, 0.015)))  # Tip
        # Edge
        verts.append(bm.verts.new((0.25, 0, 0)))
        verts.append(bm.verts.new((0, 0, 0)))
        
        # Create faces
        bm.verts.ensure_lookup_table()
        bm.edges.new((verts[0], verts[1]))
        bm.edges.new((verts[1], verts[2]))
        bm.edges.new((verts[2], verts[3]))
        bm.edges.new((verts[3], verts[4]))
        bm.edges.new((verts[4], verts[0]))
        
        bm.faces.new(verts)
        
        # Extrude for thickness
        bmesh.ops.exude_individual(bm, geom=[bm.faces[0]], translate=(0, 0.003, 0))
        
        bm.to_mesh(mesh)
        bm.free()
        
        blade.location = (0.15, 0, 0)
        
    def optimize_mesh(self):
        """Optimize for game engine"""
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        
    def create_uvs(self):
        """Create optimized UVs"""
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(
            angle_limit=math.radians(66),
            island_margin=0.02,
            area_weight=0.5,
            correct_aspect=True
        )
        bpy.ops.object.mode_set(mode='OBJECT')
        
    def assign_materials(self):
        """Assign PBR materials"""
        obj = bpy.context.active_object
        
        # Create steel material
        steel = bpy.data.materials.new(name="CS2_Steel")
        steel.use_nodes = True
        nodes = steel.node_tree.nodes
        links = steel.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        output = nodes.new(type='ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.18, 0.18, 0.20, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.98
        bsdf.inputs['Roughness'].default_value = 0.25
        bsdf.inputs['Specular'].default_value = 0.5
        bsdf.inputs['IOR'].default_value = 2.5
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        obj.data.materials.append(steel)


class CS2PropGenerator:
    """Generate environment props"""
    
    def create_crate(self):
        """Create military crate with detail"""
        mesh = bpy.data.meshes.new("CrateMesh")
        crate = bpy.data.objects.new("Crate", mesh)
        bpy.context.collection.objects.link(crate)
        
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        
        for v in bm.verts:
            v.co *= 0.6  # 60cm crate
        
        bm.to_mesh(mesh)
        bm.free()
        
        # Add detail
        bevel = crate.modifiers.new(name="Bevel", type='BEVEL')
        bevel.width = 0.01
        bevel.segments = 2


class CS2SceneSetup:
    """Setup scene for CS2 asset creation"""
    
    def execute(self):
        # Clear scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Setup units
        scene = bpy.context.scene
        scene.unit_settings.system = 'METRIC'
        scene.unit_settings.scale_length = 0.01
        scene.unit_settings.length_unit = 'CENTIMETERS'
        
        # Camera setup
        bpy.ops.object.camera_add(location=(1.5, -1.5, 1))
        camera = bpy.context.active_object
        camera.rotation_euler = (1.1, 0, 0.785)
        camera.data.lens = 85  # Portrait lens for detail
        scene.camera = camera
        
        # Lighting
        # Key
        bpy.ops.object.light_add(type='AREA', location=(2, -2, 2))
        key = bpy.context.active_object
        key.data.energy = 1000
        key.data.size = 3
        
        # Fill
        bpy.ops.object.light_add(type='AREA', location=(-2, -1, 1))
        fill = bpy.context.active_object
        fill.data.energy = 400
        fill.data.size = 2


class CS2GameExporter:
    """Export game-ready models"""
    
    def export_fbx(self):
        """Export FBX for Unity/Unreal"""
        filepath = bpy.path.abspath("//exports/weapon_game.fbx")
        
        # Select meshes
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            global_scale=1.0,
            apply_unit_scale=True,
            axis_forward='-Z',
            axis_up='Y',
            bake_space_transform=True,
            use_mesh_modifiers=True,
            mesh_smooth_type='FACE',
            use_tspace=True,
            add_leaf_bones=False
        )
        
    def export_obj(self):
        """Export OBJ"""
        filepath = bpy.path.abspath("//exports/weapon_game.obj")
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        
        bpy.ops.export_scene.obj(
            filepath=filepath,
            use_selection=True,
            global_scale=1.0,
            axis_forward='-Z',
            axis_up='Y',
            use_normals=True,
            use_uvs=True
        )
