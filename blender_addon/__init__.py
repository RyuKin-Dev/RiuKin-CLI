bl_info = {
    "name": "RiuKin CS2 Asset Generator",
    "author": "RiuKin",
    "version": (0, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > RiuKin",
    "description": "Generate CS2-quality 3D game assets",
    "category": "Object",
    "support": "COMMUNITY",
}

import bpy
from . import operators
from . import panels

classes = (
    operators.RIUKIN_OT_generate_weapon,
    operators.RIUKIN_OT_generate_prop,
    operators.RIUKIN_OT_setup_cs2_scene,
    operators.RIUKIN_OT_export_game_ready,
    panels.RIUKIN_PT_main_panel,
    panels.RIUKIN_PT_weapon_settings,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Scene properties
    bpy.types.Scene.riukin_asset_type = bpy.props.EnumProperty(
        name="Asset Type",
        items=[
            ('WEAPON', "Weapon", "CS2-style weapon"),
            ('PROP', "Prop", "Environment prop"),
            ('CHARACTER', "Character", "Character base"),
        ],
        default='WEAPON'
    )
    
    bpy.types.Scene.riukin_weapon_type = bpy.props.EnumProperty(
        name="Weapon Type",
        items=[
            ('RIFLE', "Rifle", "Assault rifle"),
            ('PISTOL', "Pistol", "Handgun"),
            ('SMG', "SMG", "Submachine gun"),
            ('SNIPER', "Sniper", "Sniper rifle"),
            ('SHOTGUN', "Shotgun", "Shotgun"),
            ('KNIFE', "Knife", "Melee weapon"),
        ],
        default='RIFLE'
    )
    
    bpy.types.Scene.riukin_poly_count = bpy.props.EnumProperty(
        name="Poly Count Target",
        items=[
            ('LOW', "Low (5K tris)", "Mobile/VR optimized"),
            ('MEDIUM', "Medium (15K tris)", "Standard quality"),
            ('HIGH', "High (50K tris)", "CS2 Reference quality"),
            ('ULTRA', "Ultra (100K tris)", "Cinematic"),
        ],
        default='HIGH'
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.riukin_asset_type
    del bpy.types.Scene.riukin_weapon_type
    del bpy.types.Scene.riukin_poly_count


if __name__ == "__main__":
    register()
