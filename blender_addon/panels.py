import bpy


class RIUKIN_PT_main_panel(bpy.types.Panel):
    """Main panel for RiuKin CS2 Generator"""
    bl_label = "RiuKin CS2 Generator"
    bl_idname = "RIUKIN_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RiuKin'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Asset type selection
        layout.prop(scene, "riukin_asset_type")
        layout.separator()
        
        # Generate buttons based on type
        if scene.riukin_asset_type == 'WEAPON':
            layout.prop(scene, "riukin_weapon_type")
            layout.prop(scene, "riukin_poly_count")
            layout.separator()
            layout.operator("riukin.generate_weapon", 
                          text="Generate Weapon", 
                          icon='FORCE_WIND')
            
        elif scene.riukin_asset_type == 'PROP':
            layout.operator("riukin.generate_prop",
                          text="Generate Prop",
                          icon='CUBE')
        
        layout.separator()
        
        # Scene setup
        box = layout.box()
        box.label(text="Scene Setup", icon='SCENE_DATA')
        box.operator("riukin.setup_cs2_scene",
                    text="Setup CS2 Scene",
                    icon='PREFERENCES')
        
        layout.separator()
        
        # Export
        box = layout.box()
        box.label(text="Export", icon='EXPORT')
        box.operator("riukin.export_game",
                    text="Export Game-Ready",
                    icon='FILE_NEW')


class RIUKIN_PT_weapon_settings(bpy.types.Panel):
    """Detailed weapon settings"""
    bl_label = "Weapon Settings"
    bl_idname = "RIUKIN_PT_weapon_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'RiuKin'
    bl_parent_id = "RIUKIN_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if scene.riukin_asset_type == 'WEAPON':
            layout.label(text="Details:")
            
            col = layout.column(align=True)
            col.prop(scene, "riukin_weapon_type")
            col.prop(scene, "riukin_poly_count")
            
            layout.separator()
            
            # Info box
            box = layout.box()
            poly_map = {
                'LOW': "~5,000 tris",
                'MEDIUM': "~15,000 tris",
                'HIGH': "~50,000 tris",
                'ULTRA': "~100,000 tris"
            }
            box.label(text=f"Target: {poly_map.get(scene.riukin_poly_count, 'Unknown')}")
            box.label(text="CS2 Reference: 30-50K tris")
        else:
            layout.label(text="Select 'Weapon' asset type")
