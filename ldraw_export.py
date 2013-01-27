
bl_info = {
	"name": "Blender 2.6 LDraw Exporter",
	"description": "",
	"author": "",
	"version": (0, 0, 1),
	"blender": (2, 6, 3),
	"api": 666,
	"location": "File > Export",
	"warning": "First test",
	"wiki_url": "",
	"tracker_url": "not"
				   "never",
	"category": "Import-Export"}


# +---------------------------------------------------------+
# | Copyright (c) 2004 Oyster                               |
# | bl8nder@yahoo.com                                       |
# | Released under the Blender Artistic Licence (BAL)       |
# +---------------------------------------------------------+

import ldrawcolor
import bpy
from bpy_extras.io_utils import ImportHelper

def rgb2ldrawcolor(r,g,b):
	max_rms=255+255+255
	max_rms=255.0**2+255.0**2+255.0**2
	color=0
	for i in ldrawcolor.ldrawcolor.keys():
		rms=abs(ldrawcolor.ldrawcolor[i][0]-r)+abs(ldrawcolor.ldrawcolor[i][1]-g)+abs(ldrawcolor.ldrawcolor[i][2]-b)
		rms=abs(ldrawcolor.ldrawcolor[i][0]-r)**2+abs(ldrawcolor.ldrawcolor[i][1]-g)**2+abs(ldrawcolor.ldrawcolor[i][2]-b)**2
		if rms<max_rms:
			max_rms=rms
			color=i
	return color

# ===================================
# ==== Write ====
# ===================================
def write(filename):
	file = open(filename, "w")

	objects = Blender.Object.GetSelected()

	objects = Blender.Object.Get()
	for i in objects:
		objname = i.name
		meshname = i.data.name
		print('0 <objname = ',objname,' >')
		print('0 <meshname = ',meshname,' >')

	objects = filter(lambda e:type(e.getData())==Blender.Types.NMeshType,objects)

	'''
	print('objects= ',objects)
	print('len(objects)= ',len(objects))
	'''

	for i in objects:
		print('i= %s' % i)
		objname = i.name
		meshname = i.data.name
		file.write('0 <objname= %s>\n' %objname)
		file.write('0 <meshname= %s>\n'%meshname)

		mesh = Blender.NMesh.GetRawFromObject(i.name)

		for face in mesh.faces:
			facer,faceg,faceb=Blender.Material.Get()[face.materialIndex].R*255, Blender.Material.Get()[face.materialIndex].G*255, Blender.Material.Get()[face.materialIndex].B*255
			if len(face.v) == 2:		# line
				v1, v2 = face.v
				faceverts = tuple(v1.co) + tuple(v2.co)
				file.write("2 %i %f %f %f %f %f %f\n" % ((rgb2ldrawcolor(facer,faceg,faceb),)+faceverts))
			elif len(face.v) == 3:		# triangle
				v1, v2, v3 = face.v
				faceverts = tuple(v1.co) + tuple(v2.co) + tuple(v3.co)
				file.write("3 %i %f %f %f %f %f %f %f %f %f\n" % ((rgb2ldrawcolor(facer,faceg,faceb),)+faceverts))
			else:						# quadrilateral
				v1, v2, v3, v4 = face.v
				faceverts = tuple(v1.co) + tuple(v2.co) + tuple(v3.co)+tuple(v4.co)
				file.write("4 %i %f %f %f %f %f %f %f %f %f %f %f %f\n" % ((rgb2ldrawcolor(facer,faceg,faceb),)+faceverts))

	Blender.Window.DrawProgressBar(1.0, '')  # clear progressbar
	file.close()

	print('\n'*2)
	file.close()
	message = "Successfully exported " + Blender.sys.basename(filename)
	print(message)

def fs_callback(filename):
	if filename.find('.dat', -4) <= 0: filename += '.dat'
	write(filename)

#----------------- Operator -------------------------------------------

class EXPORT_OT_ldraw ( bpy.types.Operator, ImportHelper ):
	bl_idname = "export_scene.ldraw"
	bl_description = 'Export an LDraw model (.dat)'
	bl_label = "Export LDraw Model"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_options = {'UNDO'}
	
	## OPTIONS ##

	## DRAW ##
	def draw(self, context):
		layout = self.layout
		
		box = layout.box()
		box.label('Import Options:', icon='FILTER')
# need to find a way to set the LDraw homedir interactivly -David Pluntze
#		box.prop(self, 'ldraw_path')

#	def execute(self, context):
#		print("executes\n")
#		create_model(self, context)
#		return {'FINISHED'}

# Registering / Unregister
def menu_import(self, context):
	self.layout.operator(EXPORT_OT_ldraw.bl_idname, text="LDraw (.dat)")

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_export.append(menu_import)


def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_export.remove(menu_import)


if __name__ == "__main__":
	register()