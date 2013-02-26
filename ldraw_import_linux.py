# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Blender 2.6 LDraw Importer 0.8 Beta 2",
    "description": "Import LDraw models in .dat, and .ldr format",
    "author": "David Pluntze, JrMasterModelBuilder, le717",
    "version": (0, 8, 0),
    "blender": (2, 6, 3),
    "api": 31236,
    "location": "File > Import",
    "warning": "A few bugs, otherwise fully functional script.",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Import-Export/LDRAW_Importer",
    "tracker_url": "not"
                   "never",
    "category": "Import-Export"}

import os
import math
import mathutils

import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import *


# global variables
file_list = {}
mat_list = {}
scale = 1.0
LDrawDir = "~/ldraw/"
mode_save = bpy.context.mode
objects = []
colors = {}
    
# class to scan the files   
class ldraw_file (object):

    def __init__ (self, filename, mat, colour = None ):
        self.subfiles = []
        self.points = []
        self.faces = []
        self.subparts = []
        self.submodels = []
        self.part_count = 0
        
        self.mat = mat
        self.colour = colour
        self.me = bpy.data.meshes.new('LDrawMesh')
        self.ob = bpy.data.objects.new('LDrawObj', self.me)
        self.ob.name = os.path.basename(filename)
        
        self.ob.location = (0,0,0)
        
        if ( colour is None ):
            self.material = None
        else:
            if colour in mat_list:
                self.ob.data.materials.append( mat_list[colour] )
            else:
                mat_list[colour] = bpy.data.materials.new('Mat_'+colour+"_")
                mat_list[colour].diffuse_color = colors[ colour ]
                #mat_list[colour].use_nodes = True
                self.ob.data.materials.append( mat_list[colour] )
                
        # Link object to scene
        bpy.context.scene.objects.link(self.ob)
        
        self.parse(filename)
        
        self.me.from_pydata(self.points, [], self.faces)
        
        self.ob.select = True
        
        objects.append(self.ob) 
        for i in self.subparts:
            self.submodels.append( ldraw_file( i[0], i[1], i[2] ) )
                
    def parse_line(self, line):
        verts = []
#       color = int(line[1])
        num_points = int ( ( len(line) - 2 ) / 3 )
        #matrix = mathutils.Matrix(mat)
        for i in range(num_points):
                self.points.append( ( self.mat * mathutils.Vector( ( float(line[i * 3 + 2]), float(line[i * 3 + 3]), float(line[i * 3 + 4]) ) ) ).
                to_tuple() )
                verts.append(len(self.points)-1)
        self.faces.append(verts)
                
    def parse (self, filename):

        while True:
#           file_found = True
            try:
                f_in = open(filename)
            except:
                try:
                    finds = locate( filename )
                    isPart = finds[1]
                    f_in = open(finds[0])
                except:
                    print("File not found: ",filename)
#                   file_found = False
            self.part_count = self.part_count + 1
            if self.part_count > 1 and isPart:
                self.subparts.append([filename, self.mat, self.colour])
            else:
                lines = f_in.readlines()
                f_in.close()
                for retval in lines:
                    tmpdate = retval.strip()
                    if tmpdate != '':
                        tmpdate = tmpdate.split()
                        #comment
                        if tmpdate[0] == "0":
                            if len(tmpdate) >= 3:
                                if tmpdate[1] == "!LDRAW_ORG" and 'Part' in tmpdate[2] :
                                    if self.part_count > 1:
                                        self.subparts.append([filename, self.mat, self.colour])
                                        break
                        #file
                        if tmpdate[0] == "1":
                            new_file = tmpdate[14]
                            x, y, z, a, b, c, d, e, f, g, h, i = map(float, tmpdate[2:14])
#                           mat_new = self.mat * mathutils.Matrix( [[a, d, g, 0], [b, e, h, 0], [c, f, i, 0], [x, y, z, 1]] )
                            mat_new = self.mat * mathutils.Matrix( ((a, b, c, x), (d, e, f, y), (g, h, i, z), (0, 0, 0, 1)) )
                            self.subfiles.append([new_file, mat_new, tmpdate[1]])
                            
                        #triangle
                        if tmpdate[0] == "3":
                            self.parse_line(tmpdate)
                            
                        #quadrilateral
                        if tmpdate[0] == "4":
                            self.parse_line(tmpdate)
            if len(self.subfiles) > 0:
                subfile = self.subfiles.pop()
                filename = subfile[0]
                self.mat = subfile[1]
                self.colour = subfile[2]
            else:        
                break
            
            
# find the needed parts and add it to the list, so second scan is not necessary -David Pluntze
# Every last LDraw Brick Library folder added for the ability to import every single brick. -le717, @Unknown in V0.7
def locate( pattern ):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    finds = []
    fname = pattern.replace('\\', os.path.sep)
    isPart = False
    if str.lower( os.path.split(fname)[0] ) == 's' :
        isSubpart = True
    else:
        isSubpart = False
        
    parts = {os.path.join(root, part).lower(): os.path.join(root, part)
        for root, _, files in os.walk(LDrawDir) for part in files}
          
    ldrawPath = os.path.join(LDrawDir, fname).lower()
    hiResPath = os.path.join(LDrawDir, "P", "48", fname).lower()
    primitivesPath = os.path.join(LDrawDir, "P", fname).lower()
    partsPath = os.path.join(LDrawDir, "PARTS", fname).lower()
    partsSPath = os.path.join(LDrawDir, "PARTS", "S", fname).lower()
    UnofficialPath = os.path.join(LDrawDir, "UNOFFICIAL", fname).lower()
    UnofficialhiResPath = os.path.join(LDrawDir, "UNOFFICIAL",  "P", "48", fname).lower()
    UnofficialPrimPath = os.path.join(LDrawDir, "UNOFFICIAL",  "P", fname).lower()
    UnofficialPartsPath = os.path.join(LDrawDir, "UNOFFICIAL",  "PARTS", fname).lower()
    UnofficialPartsSPath = os.path.join(LDrawDir, "UNOFFICIAL",  "PARTS", "S", fname).lower()   
    if os.path.exists(fname):
        pass
    elif ldrawPath in parts:
        fname = parts[ldrawPath]
    elif hiResPath in parts:
        fname = parts[hiResPath]
    elif primitivesPath in parts:
        fname = parts[primitivesPath]
    elif partsPath in parts:
        fname = parts[partsPath]
    elif partsSPath in parts:
        fname = parts[partsSPath]
    elif UnofficialPath in parts:
        fname = parts[UnofficialPath]
    elif UnofficialhiResPath in parts:
        fname = parts[UnofficialhiResPath]
    elif UnofficialPrimPath in parts:
        fname = parts[UnofficialPrimPath]
    elif UnofficialPartsPath in parts:
        fname = parts[UnofficialPartsPath]
    elif UnofficialPartsSPath in parts:
        fname = parts[UnofficialPartsSPath]
        if isSubpart == False:
            isPart = True
    else:
        print("Could not find file %s" % fname)
        return

    finds.append(fname)
    finds.append(isPart)
    return finds    

# create the actual model -David Pluntze          
def create_model(self, context):
    file_name = self.filepath
    print(file_name)
    try:
        
        # set the initial transformation matrix, set the scale factor to 0.05 
        # and rotate -90 degrees around the x-axis, so the object is upright -David Pluntze
        mat = mathutils.Matrix( ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)) ) * 0.05
        mat = mat * mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
 
# Reverted back to LDConfig.ldr from LDCfgalt.ldr due to issues finding the file. -le717, @12-11-12 in V0.7.2
        # scan LDConfig to get the material infos
        ldconfig = open ( locate( "LDConfig.ldr" )[0] )
        ldconfig_lines = ldconfig.readlines()
        ldconfig.close()
        
        for line in ldconfig_lines:
            if len(line) > 3 :
                if line[2:4].lower() == '!c':
                    line_split = line.split()
                    print( line, 'color ', line_split[4], 'code ', line_split[6][1:] )
                    colors[line_split[4]] = [ float (int ( line_split[6][1:3], 16) ) / 255.0, float (int ( line_split[6][3:5], 16) ) / 255.0, float 
                    (int ( line_split[6][5:7], 16) ) / 255.0 ]
                    
        model = ldraw_file (file_name, mat)
# Restored and corrected 'Remove Doubles' and 'Recalculate Normals' code from V0.6. -le717 @ 12-6-12 in V0.8
        for cur_obj in objects:
            bpy.context.scene.objects.active = cur_obj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.mesh.normals_make_consistent()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set()
       
    except:
        print("Oops. Something messed up.")
        pass
   
    print ("Import complete!")

def get_path(self, context):
    print(self)
    print(context)
    
#----------------- Operator -------------------------------------------
class IMPORT_OT_ldraw ( bpy.types.Operator, ImportHelper ):
    bl_idname = "import_scene.ldraw"
    bl_description = 'Import an LDraw model (.dat/.ldr)'
    bl_label = "Import LDraw Model"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {'UNDO'}
    
    ## OPTIONS ##
    
    ldraw_path = StringProperty( 
        name="LDraw Home directory", 
        description=( "The directory where LDraw is installed to." ), 
        default="C:\LDraw", subtype="DIR_PATH",
        update=get_path
        )

    ## DRAW ##
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label('Import Options:', icon='FILTER')
# need to find a way to set the LDraw homedir interactivly -David Pluntze
#       box.prop(self, 'ldraw_path')

    def execute(self, context):
        print("executes\n")
        create_model(self, context)
        return {'FINISHED'}

# Registering / Unregister
def menu_import(self, context):
    self.layout.operator(IMPORT_OT_ldraw.bl_idname, text="LDraw (.dat/.ldr)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_import)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()