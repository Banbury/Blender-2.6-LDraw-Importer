bl_info = {
    "name": "Blender 2.6 LDraw Exporter",
    "description": "",
    "author": "",
    "version": (0, 0, 1),
    "blender": (2, 6, 3),
    "api": 717,
    "location": "File > Export",
    "warning": "First test",
    "wiki_url": "",
    "tracker_url": "who"
                   "knows",
    "category": "Import-Export"}


# +---------------------------------------------------------+
# | Copyright (c) 2004 Oyster                               |
# | bl8nder@yahoo.com                                       |
# | Released under the Blender Artistic Licence (BAL)       |
# +---------------------------------------------------------+

#import ldrawcolor
import bpy
from bpy_extras.io_utils import ImportHelper

def rgb2ldrawcolor(r,g,b):
    max_rms=255+255+255
    max_rms=255.0**2+255.0**2+255.0**2
    color=0
    for i in ldrawcolor.keys():
        rms=abs(ldrawcolor[i][0]-r)+abs(ldrawcolor[i][1]-g)+abs(ldrawcolor[i][2]-b)
        rms=abs(ldrawcolor[i][0]-r)**2+abs(ldrawcolor[i][1]-g)**2+abs(ldrawcolor[i][2]-b)**2
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
            if len(face.v) == 2:        # line
                v1, v2 = face.v
                faceverts = tuple(v1.co) + tuple(v2.co)
                file.write("2 %i %f %f %f %f %f %f\n" % ((rgb2ldrawcolor(facer,faceg,faceb),)+faceverts))
            elif len(face.v) == 3:      # triangle
                v1, v2, v3 = face.v
                faceverts = tuple(v1.co) + tuple(v2.co) + tuple(v3.co)
                file.write("3 %i %f %f %f %f %f %f %f %f %f\n" % ((rgb2ldrawcolor(facer,faceg,faceb),)+faceverts))
            else:                       # quadrilateral
                v1, v2, v3, v4 = face.v
                faceverts = tuple(v1.co) + tuple(v2.co) + tuple(v3.co)+tuple(v4.co)
                file.write("4 %i %f %f %f %f %f %f %f %f %f %f %f %f\n" % ((rgb2ldrawcolor(facer,faceg,faceb),)+faceverts))

    file.close()

    print('\n'*2)
    file.close()
    message = "Successfully exported " + Blender.sys.basename(filename)
    print(message)

def fs_callback(filename):
    if filename.find('.dat', -4) <= 0: filename += '.dat'
    write(filename)

#----------------- Operator -------------------------------------------

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

class EXPORT_OT_ldraw(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_scene.ldraw"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_description = "Export an LDraw model (.dat)"
    bl_label = "Export LDraw Model"


    filename_ext = ".dat"

    filter_glob = StringProperty(
            default="*.dat",
            options={'HIDDEN'},
            )

    def execute(self, filename):
        return write(filename)          
    
# Registering / Unregister

def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_ldraw.bl_idname, text="LDraw (.dat)")

def register():
    bpy.utils.register_class(EXPORT_OT_ldraw)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_ldraw)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()

############
#LDraw Color
###########

ldrawcolor={
1: [242, 243, 242],
2: [161, 165, 162],
3: [249, 233, 153],
5: [215, 197, 153],
6: [194, 218, 184],
9: [232, 186, 199],
12: [203, 132, 66],
18: [204, 142, 104],
21: [196, 40, 27],
22: [196, 112, 160],
23: [13, 105, 171],
24: [245, 205, 47],
25: [98, 71, 50],
26: [27, 42, 52],
27: [109, 110, 108],
28: [40, 127, 70],
29: [161, 196, 139],
36: [243, 207, 155],
37: [75, 151, 74],
38: [160, 95, 52],
39: [193, 202, 222],
40: [236, 236, 236],
41: [205, 84, 75],
42: [193, 223, 240],
43: [123, 182, 232],
44: [247, 241, 141],
45: [180, 210, 227],
47: [217, 133, 108],
48: [132, 182, 141],
49: [248, 241, 132],
50: [236, 232, 222],
100: [238, 196, 182],
101: [218, 134, 121],
102: [110, 153, 201],
103: [199, 193, 183],
104: [107, 50, 123],
105: [226, 155, 63],
106: [218, 133, 64],
107: [0, 143, 155],
108: [104, 92, 67],
110: [67, 84, 147],
111: [191, 183, 177],
112: [104, 116, 172],
113: [228, 173, 200],
115: [199, 210, 60],
116: [85, 165, 175],
118: [183, 215, 213],
119: [164, 189, 70],
120: [217, 228, 167],
121: [231, 172, 88],
123: [211, 111, 76],
124: [146, 57, 120],
125: [234, 184, 145],
126: [165, 165, 203],
127: [220, 188, 129],
128: [174, 122, 89],
131: [156, 163, 168],
133: [213, 115, 61],
134: [216, 221, 86],
135: [116, 134, 156],
136: [135, 124, 144],
137: [224, 152, 100],
138: [149, 138, 115],
140: [32, 58, 86],
141: [39, 70, 44],
143: [207, 226, 247],
145: [121, 136, 161],
146: [149, 142, 163],
147: [147, 135, 103],
148: [87, 88, 87],
149: [22, 29, 50],
150: [171, 173, 172],
151: [120, 144, 129],
153: [149, 121, 118],
154: [123, 46, 47],
157: [255, 246, 123],
158: [225, 164, 194],
168: [117, 108, 98],
176: [151, 105, 91],
178: [180, 132, 85],
179: [137, 135, 136],
180: [215, 169, 75],
190: [249, 214, 46],
191: [232, 171, 45],
192: [105, 64, 39],
193: [207, 96, 36],
194: [163, 162, 164],
195: [70, 103, 164],
196: [35, 71, 139],
198: [142, 66, 133],
199: [99, 95, 97],
200: [130, 138, 93],
208: [229, 228, 222],
209: [176, 142, 68],
210: [112, 149, 120],
211: [121, 181, 181],
212: [159, 195, 233],
213: [108, 129, 183],
216: [143, 76, 42],
217: [124, 92, 69],
218: [150, 112, 159],
219: [107, 98, 155],
220: [167, 169, 206],
221: [205, 98, 152],
222: [228, 173, 200],
223: [220, 144, 149],
224: [240, 213, 160],
225: [235, 184, 127],
226: [253, 234, 140],
232: [125, 187, 221],
268: [52, 43, 117],
40: [236, 236, 236],
41: [205, 84, 75],
42: [193, 223, 240],
43: [123, 182, 232],
44: [247, 241, 141],
47: [217, 133, 108],
48: [132, 182, 141],
49: [248, 241, 132],
50: [236, 232, 222],
111: [191, 183, 177],
113: [228, 173, 200],
126: [165, 165, 203],
133: [213, 115, 61],
134: [216, 221, 86],
143: [207, 226, 247],
157: [255, 246, 123],
158: [225, 164, 194],
176: [151, 105, 91],
178: [180, 132, 85],
179: [137, 135, 136],
}