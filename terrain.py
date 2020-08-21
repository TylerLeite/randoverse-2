from math import pi, sin, cos

import json

from direct.showbase.ShowBase import ShowBase
from panda3d.core import\
  GeomVertexData,\
  GeomVertexFormat,\
  GeomVertexWriter,\
  Geom,\
  GeomNode,\
  GeomTriangles,\
  DirectionalLight,\
  LVecBase2f,\
  LVecBase3f,\
  PerlinNoise2,\
  PerlinNoise3

TABLE = json.load(open('./table.json'))

def gpugemsTerrain():
  W, H, D = (1,1,2)
  noise = PerlinNoise3(1,1,1,256,0)
  warpNoise = PerlinNoise3(1,1,1,256,1)
  # noise = PerlinNoise3()
  # warpNoise = PerlinNoise3()

  def densityFunction(x, y, z):
    point = LVecBase3f(x, y, z)
    warpfactor = 0.0004

    warp = warpNoise(LVecBase3f(x*warpfactor, y*warpfactor, z*warpfactor)) * 8
    point.componentwiseMult(LVecBase3f(warp, warp, warp))
    density = -point.z
    floor = 4

    ω = [16.03, 8.05, 4.03, 1.96, 1.01, 0.49, 0.23, 0.097] # frequencies
    A = [0.25, 0.25, 0.5, 0.5, 1, 2, 8, 32] # amplitudes
    for i in range(len(ω)):
      ωVec = LVecBase3f(ω[i], ω[i], ω[i])
      ωVec.componentwiseMult(point)
      density += noise(ωVec) * A[i]

    density += max(min((floor - point.z)*3, 1), 0)*40;

    return density

  def casePoint(density):
    if density < 0:
      return 0
    else:
      return 1

  g = 1 # granularity
  chunk = [[[
    [[[densityFunction((x+32*w)/g, (y+32*h)/g, (z+32*d)/g) for x in range(33)] for y in range(33)] for z in range(33)]
  for w in range(W)] for h in range(H)] for d in range(D)]

  vdata = GeomVertexData('Land', GeomVertexFormat.get_v3n3c4(), Geom.UHStatic)
  vdata.setNumRows(33*33*4)

  vertices = GeomVertexWriter(vdata, 'vertex')
  normals = GeomVertexWriter(vdata, 'normal')
  colors = GeomVertexWriter(vdata, 'color')

  waterNoise = PerlinNoise2()

  ct = 0

  for h in range(H):
    for w in range(W):
      for d in range(D):
        # bigger!
        for z in range(32):
          for y in range(32):
            for x in range(32):
              v0 = chunk[d][h][w][z+1][y][x]
              v1 = chunk[d][h][w][z][y][x]
              v2 = chunk[d][h][w][z][y][x+1]
              v3 = chunk[d][h][w][z+1][y][x+1]
              v4 = chunk[d][h][w][z+1][y+1][x]
              v5 = chunk[d][h][w][z][y+1][x]
              v6 = chunk[d][h][w][z][y+1][x+1]
              v7 = chunk[d][h][w][z+1][y+1][x+1]


              case = casePoint(chunk[d][h][w][z+1][y][x])\
                    + 2*casePoint(chunk[d][h][w][z][y][x])\
                    + 4*casePoint(chunk[d][h][w][z][y][x+1])\
                    + 8*casePoint(chunk[d][h][w][z+1][y][x+1])\
                    + 16*casePoint(chunk[d][h][w][z+1][y+1][x])\
                    + 32*casePoint(chunk[d][h][w][z][y+1][x])\
                    + 64*casePoint(chunk[d][h][w][z][y+1][x+1])\
                    + 128*casePoint(chunk[d][h][w][z+1][y+1][x+1])\

              if case == 0 or case == 255:
                continue

              numpolys = TABLE['case_to_numpolys'][case][0]

              for polyIndex in range(numpolys):
                edgeConnects = TABLE['g_triTable'][case][polyIndex]

                currentTriangleVertices = []
                currentTriangleColors = []
                for edgeIndex in range(3):
                  edge = edgeConnects[edgeIndex]

                  X = x+32*w
                  Y = y+32*h
                  Z = z+32*d

                  scale = 1
                  X = scale*X
                  Y = scale*Y
                  Z = scale*Z

                  ph = min(1, (d*32+z)/32) # point height
                  ph = ph*ph*ph

                  color = None
                  # if d == 0 and z <= 7:
                  #   v = waterNoise.noise(LVecBase2f(X, Y))
                  #   b= 1 - v**2
                  #   if b > 0.99:
                  #     color = [0.12, 0.29, b, 1]

                  if edge == 0:
                    diff = abs(v0)/(abs(v0)+abs(v1))
                    diff = scale * diff
                    currentTriangleVertices.append([X, Y, Z-diff])
                    if color is None:
                      color = [0.49+0.51*ph, 0.84+0.16*ph, 0.06+0.94*ph, 1]
                    currentTriangleColors.append(color)
                  elif edge == 1:
                    diff = abs(v1)/(abs(v1)+abs(v2))
                    diff = scale * diff
                    currentTriangleVertices.append([X+diff, Y, Z-scale])
                    currentTriangleColors.append([0.89, 0.17, 0.1, 1])
                  elif edge == 2:
                    diff = abs(v3)/(abs(v3)+abs(v2))
                    diff = scale * diff
                    currentTriangleVertices.append([X+scale, Y, Z-diff])
                    if color is None:
                      color = [0.49+0.51*ph, 0.84+0.16*ph, 0.06+0.94*ph, 1]
                    currentTriangleColors.append(color)
                  elif edge == 3:
                    diff = abs(v0)/(abs(v0)+abs(v3))
                    diff = scale * diff
                    currentTriangleVertices.append([X+diff, Y, Z])
                    currentTriangleColors.append([0.89, 0.17, 0.1, 1])
                  elif edge == 4:
                    diff = abs(v4)/(abs(v4)+abs(v5))
                    diff = scale * diff
                    currentTriangleVertices.append([X, Y+scale, Z-diff])
                    if color is None:
                      color = [0.49+0.51*ph, 0.84+0.16*ph, 0.06+0.94*ph, 1]
                    currentTriangleColors.append(color)
                  elif edge == 5:
                    diff = abs(v5)/(abs(v5)+abs(v6))
                    diff = scale * diff
                    currentTriangleVertices.append([X+diff, Y+scale, Z-scale])
                    currentTriangleColors.append([0.89, 0.17, 0.1, 1])
                  elif edge == 6:
                    diff = abs(v7)/(abs(v7)+abs(v6))
                    diff = scale * diff
                    currentTriangleVertices.append([X+scale, Y+scale, Z-diff])
                    if color is None:
                      color = [0.49+0.51*ph, 0.84+0.16*ph, 0.06+0.94*ph, 1]
                    currentTriangleColors.append(color)
                  elif edge == 7:
                    diff = abs(v4)/(abs(v4)+abs(v7))
                    diff = scale * diff
                    currentTriangleVertices.append([X+diff, Y+scale, Z])
                    currentTriangleColors.append([0.89, 0.17, 0.1, 1])
                  elif edge == 8:
                    diff = abs(v0)/(abs(v0)+abs(v4))
                    diff = scale * diff
                    currentTriangleVertices.append([X, Y+diff, Z])
                    currentTriangleColors.append([0.89, 0.34, 0.1, 1])
                  elif edge == 9:
                    diff = abs(v1)/(abs(v1)+abs(v5))
                    diff = scale * diff
                    currentTriangleVertices.append([X, Y+diff, Z-scale])
                    currentTriangleColors.append([0.89, 0.34, 0.1, 1])
                  elif edge == 10:
                    diff = abs(v2)/(abs(v2)+abs(v6))
                    diff = scale * diff
                    currentTriangleVertices.append([X+scale, Y+diff, Z-scale])
                    currentTriangleColors.append([0.89, 0.34, 0.1, 1])
                  elif edge == 11:
                    diff = abs(v3)/(abs(v3)+abs(v7))
                    diff = scale * diff
                    currentTriangleVertices.append([X+scale, Y+diff, Z])
                    currentTriangleColors.append([0.89, 0.34, 0.1, 1])

                a = currentTriangleVertices[0]
                b = currentTriangleVertices[1]
                c = currentTriangleVertices[2]
                ba = LVecBase3f(b[0]-a[0], b[1]-a[1], b[2]-a[2])
                ca = LVecBase3f(c[0]-a[0], c[1]-a[1], c[2]-a[2])
                normal = ba.cross(ca).normalized()

                for i in range(3):
                  ct += 1
                  cv = currentTriangleVertices[i]
                  cn = normal
                  cc = currentTriangleColors[i]

                  vertices.addData3f(cv[0], cv[1], cv[2])
                  normals.addData3f(cn[0], cn[1], cn[2])
                  colors.addData4f(cc[0], cc[1], cc[2], cc[3])

  prim = GeomTriangles(Geom.UHStatic)
  i = 0
  while i <= ct-1:
    prim.addVertices(i, i+1, i+2)
    prim.close_primitive()
    i += 3

  geom = Geom(vdata)
  geom.addPrimitive(prim)

  return geom

class MyApp(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    terrainNode = GeomNode('terrain_node')
    terrainNode.addGeom(gpugemsTerrain())
    terrainNodePath = render.attachNewNode(terrainNode)
    # terrainNodePath.setTwoSided (True);
    terrainNodePath.setPos(-16, -16, -32)

    sun = DirectionalLight('sun')
    sun.setColor((1, 1, 1, 1))
    sun.setDirection(LVecBase3f(0.5, 0.5, -1))
    sunNodePath = render.attachNewNode(sun)

    render.setLight(sunNodePath)
    render.setShaderAuto()

app = MyApp()
app.run()
