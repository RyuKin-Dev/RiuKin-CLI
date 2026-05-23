"""PBR Material System for CS2-quality assets"""
import bpy
import os


class CS2MaterialLibrary:
    """Complete PBR material library matching CS2 standards"""
    
    def __init__(self):
        self.materials = {}
        
    def create_all(self):
        """Create all CS2 materials"""
        self.create_weapon_steel()
        self.create_polymer_black()
        self.create_polymer_tan()
        self.create_wood_laminate()
        self.create_rust_blued()
        self.create_nickel_plated()
        self.create_gold_plated()
        self.create_cerakote_olive()
        self.create_cerakote_black()
        self.create_case_hardened()
        self.create_carbon_fiber()
        self.create_rubber_grip()
        self.create_glass_optic()
        self.create_lens_glow()
        return self.materials
        
    def create_weapon_steel(self):
        """Standard weapon steel - balanced PBR"""
        mat = bpy.data.materials.new(name="CS2_Steel_Weapon")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Principled BSDF
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (400, 0)
        
        # Steel properties
        bsdf.inputs['Base Color'].default_value = (0.15, 0.15, 0.17, 1.0)
        bsdf.inputs['Subsurface'].default_value = 0.0
        bsdf.inputs['Metallic'].default_value = 0.98
        bsdf.inputs['Specular'].default_value = 0.5
        bsdf.inputs['Specular Tint'].default_value = 0.0
        bsdf.inputs['Roughness'].default_value = 0.28
        bsdf.inputs['Anisotropic'].default_value = 0.0
        bsdf.inputs['Anisotropic Rotation'].default_value = 0.0
        bsdf.inputs['Sheen'].default_value = 0.0
        bsdf.inputs['Sheen Tint'].default_value = 0.5
        bsdf.inputs['Clearcoat'].default_value = 0.0
        bsdf.inputs['Clearcoat Roughness'].default_value = 0.03
        bsdf.inputs['IOR'].default_value = 2.45
        bsdf.inputs['Transmission'].default_value = 0.0
        bsdf.inputs['Transmission Roughness'].default_value = 0.0
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['steel_weapon'] = mat
        return mat
        
    def create_polymer_black(self):
        """Black polymer - matte, subtle roughness variation"""
        mat = bpy.data.materials.new(name="CS2_Polymer_Black")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Specular'].default_value = 0.2
        bsdf.inputs['Roughness'].default_value = 0.75
        bsdf.inputs['IOR'].default_value = 1.45
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['polymer_black'] = mat
        return mat
        
    def create_polymer_tan(self):
        """Desert tan polymer"""
        mat = bpy.data.materials.new(name="CS2_Polymer_Tan")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.45, 0.35, 0.25, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Roughness'].default_value = 0.8
        bsdf.inputs['IOR'].default_value = 1.45
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['polymer_tan'] = mat
        return mat
        
    def create_wood_laminate(self):
        """Laminated wood stock - warm, slightly glossy"""
        mat = bpy.data.materials.new(name="CS2_Wood_Laminate")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.35, 0.20, 0.10, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Specular'].default_value = 0.3
        bsdf.inputs['Roughness'].default_value = 0.45
        bsdf.inputs['IOR'].default_value = 1.5
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['wood_laminate'] = mat
        return mat
        
    def create_rust_blued(self):
        """Blued steel with subtle sheen"""
        mat = bpy.data.materials.new(name="CS2_Steel_Blued")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        # Dark blue-black
        bsdf.inputs['Base Color'].default_value = (0.08, 0.10, 0.14, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.95
        bsdf.inputs['Specular'].default_value = 0.4
        bsdf.inputs['Roughness'].default_value = 0.32
        bsdf.inputs['IOR'].default_value = 2.4
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['steel_blued'] = mat
        return mat
        
    def create_nickel_plated(self):
        """Bright nickel/silver finish"""
        mat = bpy.data.materials.new(name="CS2_Nickel_Plated")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.65, 0.63, 0.60, 1.0)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Specular'].default_value = 0.7
        bsdf.inputs['Roughness'].default_value = 0.18
        bsdf.inputs['IOR'].default_value = 2.6
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['nickel_plated'] = mat
        return mat
        
    def create_gold_plated(self):
        """Gold finish - CS2 luxury skins"""
        mat = bpy.data.materials.new(name="CS2_Gold_Plated")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.85, 0.70, 0.25, 1.0)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Specular'].default_value = 0.8
        bsdf.inputs['Roughness'].default_value = 0.15
        bsdf.inputs['IOR'].default_value = 3.0
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['gold_plated'] = mat
        return mat
        
    def create_cerakote_olive(self):
        """Cerakote OD Green - realistic ceramic coating"""
        mat = bpy.data.materials.new(name="CS2_Cerakote_Olive")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.22, 0.28, 0.15, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Specular'].default_value = 0.15
        bsdf.inputs['Roughness'].default_value = 0.95
        bsdf.inputs['IOR'].default_value = 1.4
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['cerakote_olive'] = mat
        return mat
        
    def create_cerakote_black(self):
        """Cerakote Black"""
        mat = bpy.data.materials.new(name="CS2_Cerakote_Black")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Roughness'].default_value = 0.98
        bsdf.inputs['IOR'].default_value = 1.4
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['cerakote_black'] = mat
        return mat
        
    def create_case_hardened(self):
        """Case hardened pattern - CS2 classic skin"""
        mat = bpy.data.materials.new(name="CS2_Case_Hardened")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Create colorful case hardened pattern
        tex_coord = nodes.new('ShaderNodeTexCoord')
        tex_coord.location = (-800, 0)
        
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (-600, 0)
        noise.inputs['Scale'].default_value = 15.0
        noise.inputs['Detail'].default_value = 8.0
        noise.inputs['Roughness'].default_value = 0.6
        
        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (-400, 0)
        color_ramp.color_ramp.interpolation = 'LINEAR'
        
        # Case hardened colors: blue -> purple -> yellow -> silver
        color_ramp.color_ramp.elements.new(0.3)
        color_ramp.color_ramp.elements.new(0.6)
        color_ramp.color_ramp.elements.new(0.8)
        
        color_ramp.color_ramp.elements[0].color = (0.3, 0.5, 0.9, 1.0)  # Blue
        color_ramp.color_ramp.elements[1].color = (0.6, 0.3, 0.9, 1.0)  # Purple
        color_ramp.color_ramp.elements[2].color = (0.9, 0.7, 0.2, 1.0)  # Gold
        color_ramp.color_ramp.elements[3].color = (0.7, 0.75, 0.8, 1.0)  # Silver
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs['Metallic'].default_value = 0.98
        bsdf.inputs['Roughness'].default_value = 0.25
        
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (400, 0)
        
        links.new(tex_coord.outputs['Generated'], noise.inputs['Vector'])
        links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['case_hardened'] = mat
        return mat
        
    def create_carbon_fiber(self):
        """Carbon fiber - high-tech finish"""
        mat = bpy.data.materials.new(name="CS2_Carbon_Fiber")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.08, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Roughness'].default_value = 0.4
        bsdf.inputs['IOR'].default_value = 1.6
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['carbon_fiber'] = mat
        return mat
        
    def create_rubber_grip(self):
        """Rubber grip texture - matte, high friction"""
        mat = bpy.data.materials.new(name="CS2_Rubber_Grip")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.08, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Roughness'].default_value = 0.95
        bsdf.inputs['IOR'].default_value = 1.4
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['rubber_grip'] = mat
        return mat
        
    def create_glass_optic(self):
        """Optical glass - scopes/sights"""
        mat = bpy.data.materials.new(name="CS2_Glass_Optic")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        
        bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Specular'].default_value = 0.95
        bsdf.inputs['Roughness'].default_value = 0.02
        bsdf.inputs['IOR'].default_value = 1.52  # Glass IOR
        bsdf.inputs['Transmission'].default_value = 0.98
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials['glass_optic'] = mat
        return mat
        
    def create_lens_glow(self):
        """Optic lens with red dot glow"""
        mat = bpy.data.materials.new(name="CS2_Lens_Glow")
        mat.use_nodes = True
        mat.use_fake_user = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Emission for glow
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1.0, 0.1, 0.1, 1.0)  # Red dot
        emission.inputs['Strength'].default_value = 2.0
        
        # Glass base
        glass = nodes.new('ShaderNodeBsdfPrincipled')
        glass.inputs['Base Color'].default_value = (0.2, 0.0, 0.0, 1.0)
        glass.inputs['Transmission'].default_value = 0.9
        glass.inputs['Roughness'].default_value = 0.0
        glass.inputs['IOR'].default_value = 1.52
        
        # Mix shader
        mix = nodes.new('ShaderNodeMixShader')
        mix.inputs['Fac'].default_value = 0.7
        
        output = nodes.new('ShaderNodeOutputMaterial')
        
        links.new(glass.outputs['BSDF'], mix.inputs[1])
        links.new(emission.outputs['Emission'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])
        
        self.materials['lens_glow'] = mat
        return mat


def assign_cs2_material(obj, material_name):
    """Assign CS2 material to object"""
    mat = bpy.data.materials.get(material_name)
    if mat:
        obj.data.materials.append(mat)
    else:
        # Create library if not exists
        lib = CS2MaterialLibrary()
        lib.create_all()
        mat = bpy.data.materials.get(material_name)
        if mat:
            obj.data.materials.append(mat)
