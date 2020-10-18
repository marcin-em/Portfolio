bl_info = {
    "name": "Measure Tool",
    "author": "MarcinEm",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Adds a measure",
    "location": "3D View > Side Bar"
}

import bpy


class MeasurePanel(bpy.types.Panel):
    bl_label = 'Measure'
    bl_idname = 'MEASURE_PT_Measure'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Measure Tool'
    
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row.label(text='Generate measure')
        row = layout.row()
        row.operator('wm.measure_op')

        
class WM_OT_measureOp(bpy.types.Operator):
    bl_label = 'Generate'
    bl_idname = 'wm.measure_op'
    
    scale = bpy.props.FloatProperty(name='Scale (m):', default=1, min=0.1, max=5.0)
    
    def execute(self, context):
        
        cur_3d = context.scene.cursor.location
        
        scale = self.scale
        count = int(scale * 100)
        incr = 0.01
 
        # zaznacza 'Scene Collection', aby w niej stworzyc nowa collection
        scene_collection = bpy.context.view_layer.layer_collection
        bpy.context.view_layer.active_layer_collection = scene_collection 
        
        # tworzenie collection
        coll = bpy.data.collections.new('Measure')
        bpy.context.scene.collection.children.link(coll)
        
        # tworzenie empty (parent)
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=cur_3d)
        
        emp_scale = scale * .4
        bpy.ops.transform.resize(value=(emp_scale,emp_scale,emp_scale))
        emp = bpy.context.selected_objects[0]
        bpy.context.scene.collection.objects.unlink(emp)
        coll.objects.link(emp)
        
        # tworzenie slupa
        bpy.ops.mesh.primitive_plane_add(size=.05, location=cur_3d)
        bpy.ops.transform.resize(value=(1, 0.5, 1))
        bar = bpy.context.selected_objects[0]
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers['Solidify'].thickness = -scale - incr
        coll.objects.link(bar)
        bpy.context.scene.collection.objects.unlink(bar)
        bar.parent = emp
        bar.matrix_parent_inverse = emp.matrix_world.inverted()

        # tworzenie miarki
        for obj in range(0,(count + 1)):
            
            if obj > 0:

                bpy.ops.mesh.primitive_plane_add(size=.6, location=(cur_3d.x, cur_3d.y, (cur_3d.z + (obj * incr))))
                plane = bpy.context.selected_objects[0]
                bpy.ops.transform.resize(value=(.2, .02, .2))
                coll.objects.link(plane)
                bpy.context.scene.collection.objects.unlink(plane)
                plane.parent = emp
                plane.matrix_parent_inverse = emp.matrix_world.inverted()
                
                if obj % 100 == 0:
                    
                    bpy.ops.transform.resize(value=(3, 1, 1))
                    
                    # txt
                    bpy.ops.object.text_add(location=(cur_3d.x, cur_3d.y, (cur_3d.z + (obj * incr))))
                    txt = bpy.context.selected_objects[0]
                    bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL')

                    ob = bpy.context.object
                    ob.data.body = '{} m'.format(int(obj/100))
                    ob.data.extrude = .005
                    ob.data.size = .05
                    ob.data.align_x = 'RIGHT'
                    ob.data.offset_x = -.2
                    coll.objects.link(txt)
                    bpy.context.scene.collection.objects.unlink(txt)
                    txt.parent = emp
                    txt.matrix_parent_inverse = emp.matrix_world.inverted()
                
                elif obj % 10 == 0:
                    
                    bpy.ops.transform.resize(value=(1.5, 1, 1))
                    
                    # txt
                    bpy.ops.object.text_add(location=(cur_3d.x, cur_3d.y, (cur_3d.z + (obj * incr))))
                    txt = bpy.context.selected_objects[0]
                    bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL')

                    ob = bpy.context.object
                    ob.data.body = '{} cm'.format(obj)
                    ob.data.size = .03
                    ob.data.align_x = 'RIGHT'
                    ob.data.offset_x = -.1
                    coll.objects.link(txt)
                    bpy.context.scene.collection.objects.unlink(txt)
                    txt.parent = emp
                    txt.matrix_parent_inverse = emp.matrix_world.inverted()
                    
        return {'FINISHED'}
    
    
    def invoke(self, context,event):
        return context.window_manager.invoke_props_dialog(self)
        
        
def register():
    bpy.utils.register_class(MeasurePanel)
    bpy.utils.register_class(WM_OT_measureOp)


def unregister():
    bpy.utils.unregister_class(MeasurePanel)
    bpy.utils.unregister_class(WM_OT_measureOp)


if __name__ == "__main__":
    register()
