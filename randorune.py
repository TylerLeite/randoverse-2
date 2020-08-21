from enum import Enum
from math import floor, sin, cos, pi
import random as r
from uuid import uuid4

import cairo

class Rune:
  top = ['angstrom', 'antennae', 'docstring', 'swinton']
  shape = ['shape_'+a for a in ['circle', 'boob', 'penis', 'yinyang', 'triangup', 'deniro', 'triangdown', 'beatrice', 'grimace', 'box', 'domino', 'teeth', 'panini', 'fermata']]
  line = ['line_'+a+'-'+b for a in ['single', 'double', 'wiggle', 'invisible'] for b in ['dr', 'ur', 'x', 'deniro', 'beatrice', 'jesus', 'frankenstein', 'ribs', 'machamp', 'babymachamp', 'f', 'backwardsf', 'waterfall', 'naruto', 'none']]
  bottom = ['crabgot', 'legs', 'flatline', 'dingleberry']
  flair = [a+'/'+b for a in ['chops', 'dot'] for b in ['left', 'right', 'both']] + [None] # i dont like to talk about it
  flair_chance = [1/4, 1/4, 1/4]

  def __init__(self):
    # p1 = len(Rune.top)*len(Rune.line)*len(Rune.shape)*len(Rune.line)*len(Rune.bottom)*len(Rune.flair)*len(Rune.flair)*len(Rune.flair)
    # p2 = len(Rune.top)*len(Rune.shape)*len(Rune.line)*len(Rune.shape)*len(Rune.bottom)*len(Rune.flair)*len(Rune.flair)*len(Rune.flair)
    # print(p1 + p2, 'total possibilities!') # 341,134,080
    parity = r.randrange(0, 2)

    self.parts = [r.choice(Rune.top), None, None, None, r.choice(Rune.bottom)]
    self.flair = [None, None, None]
    for i in range(1, 4):
      if (parity+i)%2 == 0:
        self.parts[i] = r.choice(Rune.line)
      else:
        self.parts[i] = r.choice(Rune.shape)

      if r.random() < Rune.flair_chance[i-1]:
        self.flair[i-1] = r.choice(Rune.flair)

  def render(self):
    print(self.parts, self.flair)
    with cairo.SVGSurface('runes/' + uuid4().__str__() + '.svg', 320, 320) as surface:
      ctx = cairo.Context(surface)
      ctx.scale(320, 320)
      ctx.set_line_width(0.01)
      ctx.set_source_rgba(0.7, 0.4, 0.8, 1)

      coords = [
        (0.5, 1/16),
        (0.5, 0.25),
        (0.5, 0.5),
        (0.5, 0.75),
        (0.5, 15/16),
      ]

      xlf = 11/32
      xrf = 21/32

      for i, part in enumerate(self.parts):
        if '-' in part:
          line, ornament = part.split('-')
          getattr(Rune, 'draw_'+line)(ctx, coords[i][0], coords[i][1])
          getattr(Rune, 'draw_'+ornament)(ctx, coords[i][0], coords[i][1])
        else:
          getattr(Rune, 'draw_'+part)(ctx, coords[i][0], coords[i][1])

      for i, flair in enumerate(self.flair):
        if flair is None:
          continue
        else:
          glyph, position = flair.split('/')
          if position in ['left', 'both']:
            getattr(Rune, 'draw_'+glyph)(ctx, xlf, coords[i+1][1])
          if position in ['right', 'both']:
            getattr(Rune, 'draw_'+glyph)(ctx, xrf, coords[i+1][1])

      ctx.stroke()

  # Tops
  def draw_angstrom(ctx, sx, sy):
    Rune.draw_circle(ctx, sx, sy, 1/32)

  def draw_antennae(ctx, sx, sy):
    ctx.move_to(sx+1/32, sy)
    ctx.line_to(sx+2/32, sy-1/32)
    ctx.move_to(sx-1/32, sy)
    ctx.line_to(sx-2/32, sy-1/32)
    ctx.stroke()

  def draw_docstring(ctx, sx, sy):
    ctx.move_to(sx, sy-1/32)
    ctx.line_to(sx, sy)
    ctx.move_to(sx+1/16, sy-1/32)
    ctx.line_to(sx+1/16, sy)
    ctx.move_to(sx-1/16, sy-1/32)
    ctx.line_to(sx-1/16, sy)
    ctx.stroke()

  def draw_swinton(ctx, sx, sy):
    # dont ask me how this works, i just guessed
    ctx.move_to(sx-2/64, sy-2/64)
    ctx.arc(sx-2/64, sy+5/64, 7/64, 11*pi/8, 13*pi/8)
    ctx.move_to(sx+5/64, sy-2/64)
    ctx.arc(sx+2/64, sy-33/256, 7/64, 3*pi/8, 5*pi/8)
    ctx.stroke()

  # Lines

  def draw_line_single(ctx, sx, sy):
    ctx.move_to(sx, sy-5/32)
    ctx.line_to(sx, sy+5/32)
    ctx.stroke()

  def draw_line_double(ctx, sx, sy):
    ctx.move_to(sx+1/32, sy-5/32)
    ctx.line_to(sx+1/32, sy+5/32)
    ctx.move_to(sx-1/32, sy-5/32)
    ctx.line_to(sx-1/32, sy+5/32)
    ctx.stroke()

  def draw_line_wiggle(ctx, sx, sy):
    ctx.move_to(sx, sy-5/32)
    ctx.arc(sx-5/64, sy-5/64, 7/64, 7*pi/4, pi/4)

    ctx.move_to(sx, sy+5/32)
    ctx.arc(sx+5/64, sy+5/64, 7/64, 3*pi/4, 5*pi/4)
    ctx.stroke()

  def draw_line_invisible(ctx, sx, sy):
    pass # lol

  def draw_dr(ctx, sx, sy):
    ctx.move_to(sx-3/32, sy-3/32)
    ctx.line_to(sx+3/32, sy+3/32)
    ctx.stroke()

  def draw_ur(ctx, sx, sy):
    ctx.move_to(sx+3/32, sy-3/32)
    ctx.line_to(sx-3/32, sy+3/32)
    ctx.stroke()

  def draw_x(ctx, sx, sy):
    Rune.draw_dr(ctx, sx, sy)
    Rune.draw_ur(ctx, sx, sy)

  def draw_deniro(ctx, sx, sy):
    ctx.move_to(sx, sy)
    ctx.line_to(sx+3/32, sy+3/32)
    ctx.move_to(sx, sy)
    ctx.line_to(sx-3/32, sy+3/32)
    ctx.stroke()

  def draw_beatrice(ctx, sx, sy):
    ctx.move_to(sx, sy)
    ctx.line_to(sx+3/32, sy-3/32)
    ctx.move_to(sx, sy)
    ctx.line_to(sx-3/32, sy-3/32)
    ctx.stroke()

  def draw_jesus(ctx, sx, sy):
    ctx.move_to(sx-1/8, sy)
    ctx.line_to(sx+1/8, sy)
    ctx.stroke()

  def draw_frankenstein(ctx, sx, sy):
    ctx.move_to(sx-1/8, sy+1/16)
    ctx.line_to(sx+1/8, sy+1/16)
    ctx.move_to(sx-1/16, sy-1/16)
    ctx.line_to(sx+1/16, sy-1/16)
    ctx.stroke()

  def draw_ribs(ctx, sx, sy):
    ctx.move_to(sx-1/16, sy+1/16)
    ctx.line_to(sx+1/16, sy+1/16)
    ctx.move_to(sx-1/8, sy-1/16)
    ctx.line_to(sx+1/8, sy-1/16)
    ctx.stroke()

  def draw_machamp(ctx, sx, sy):
    ctx.move_to(sx-1/8, sy+1/16)
    ctx.line_to(sx+1/8, sy+1/16)
    ctx.move_to(sx-1/8, sy-1/16)
    ctx.line_to(sx+1/8, sy-1/16)
    ctx.stroke()

  def draw_babymachamp(ctx, sx, sy):
    ctx.move_to(sx-1/16, sy+1/16)
    ctx.line_to(sx+1/16, sy+1/16)
    ctx.move_to(sx-1/16, sy-1/16)
    ctx.line_to(sx+1/16, sy-1/16)
    ctx.stroke()

  def draw_f(ctx, sx, sy):
    ctx.move_to(sx, sy+1/16)
    ctx.line_to(sx+1/16, sy+1/16)
    ctx.move_to(sx, sy-1/16)
    ctx.line_to(sx+1/8, sy-1/16)
    ctx.stroke()

  def draw_backwardsf(ctx, sx, sy):
    ctx.move_to(sx, sy+1/16)
    ctx.line_to(sx-1/16, sy+1/16)
    ctx.move_to(sx, sy-1/16)
    ctx.line_to(sx-1/8, sy-1/16)
    ctx.stroke()

  def draw_waterfall(ctx, sx, sy):
    ctx.move_to(sx, sy)
    ctx.arc(sx-5/64, sy-5/64, 7/64, pi/4, 3*pi/4)
    ctx.move_to(sx, sy)
    ctx.arc(sx+5/64, sy+5/64, 7/64, 5*pi/4, 7*pi/4)
    ctx.stroke()

  def draw_naruto(ctx, sx, sy):
    ctx.move_to(sx, sy)
    for d in range(633):
      theta = (d%360)*pi/180
      r = d/5040 # (5/8)(1/8)*d/630

      x = r * cos(theta)
      y = r * sin(theta)

      ctx.line_to(sx+x, sy+y)
    ctx.stroke()

  def draw_none(ctx, sx, sy):
    pass # teehee

  # Shapes

  def draw_shape_circle(ctx, sx, sy):
    Rune.draw_circle(ctx, sx, sy, 3/32)

  def draw_shape_boob(ctx, sx, sy):
    Rune.draw_circle(ctx, sx, sy, 3/32)
    Rune.draw_dot(ctx, sx, sy)

  def draw_shape_penis(ctx, sx, sy):
    Rune.draw_circle(ctx, sx, sy, 3/32)
    ctx.move_to(sx-3/32, sy)
    ctx.line_to(sx+3/32, sy)
    ctx.stroke()

  def draw_shape_yinyang(ctx, sx, sy):
    Rune.draw_circle(ctx, sx, sy, 3/32)
    ctx.move_to(sx, sy-3/32)
    ctx.line_to(sx-3/64, sy-1/64)
    ctx.line_to(sx, sy)
    ctx.line_to(sx+3/64, sy+1/64)
    ctx.line_to(sx, sy+3/32)
    ctx.stroke()

  def draw_shape_triangup(ctx, sx, sy):
    Rune.draw_shape_deniro(ctx, sx, sy)
    ctx.move_to(sx+3/32, sy+3/32)
    ctx.line_to(sx-3/32, sy+3/32)
    ctx.stroke()

  def draw_shape_deniro(ctx, sx, sy):
    ctx.move_to(sx, sy-3/32)
    ctx.line_to(sx-3/32, sy+3/32)
    ctx.move_to(sx, sy-3/32)
    ctx.line_to(sx+3/32, sy+3/32)
    ctx.stroke()

  def draw_shape_triangdown(ctx, sx, sy):
    Rune.draw_shape_beatrice(ctx, sx, sy)
    ctx.move_to(sx+3/32, sy-3/32)
    ctx.line_to(sx-3/32, sy-3/32)
    ctx.stroke()

  def draw_shape_beatrice(ctx, sx, sy):
    ctx.move_to(sx, sy+3/32)
    ctx.line_to(sx-3/32, sy-3/32)
    ctx.move_to(sx, sy+3/32)
    ctx.line_to(sx+3/32, sy-3/32)
    ctx.stroke()

  def draw_shape_grimace(ctx, sx, sy):
    ctx.move_to(sx-3/32, sy)
    ctx.line_to(sx+3/32, sy)
    ctx.stroke()

  def draw_shape_box(ctx, sx, sy):
    ctx.move_to(sx-3/32, sy-3/32)
    ctx.line_to(sx-3/32, sy+3/32)
    ctx.line_to(sx+3/32, sy+3/32)
    ctx.line_to(sx+3/32, sy-3/32)
    ctx.line_to(sx-3/32, sy-3/32)
    ctx.stroke()

  def draw_shape_domino(ctx, sx, sy):
    Rune.draw_shape_box(ctx, sx, sy)
    ctx.move_to(sx, sy-3/32)
    ctx.line_to(sx, sy+3/32)
    ctx.stroke()

  def draw_shape_teeth(ctx, sx, sy):
    Rune.draw_shape_box(ctx, sx, sy)
    ctx.move_to(sx-1/32, sy-3/32)
    ctx.line_to(sx-1/32, sy+3/32)
    ctx.move_to(sx+1/32, sy-3/32)
    ctx.line_to(sx+1/32, sy+3/32)
    ctx.stroke()
    Rune.draw_shape_grimace(ctx, sx, sy)

  def draw_shape_panini(ctx, sx, sy):
    Rune.draw_shape_box(ctx, sx, sy)
    Rune.draw_shape_grimace(ctx, sx, sy)

  def draw_shape_fermata(ctx, sx, sy):
    r = 3/32
    ctx.move_to(sx-r, sy)
    ctx.arc(sx, sy, r, pi, 0)
    ctx.stroke()
    Rune.draw_dot(ctx, sx, sy)

  # Flair

  def draw_dot(ctx, sx, sy):
    Rune.draw_circle(ctx, sx, sy, 1/64)

  def draw_chops(ctx, sx, sy):
    ctx.move_to(sx, sy+1/32)
    ctx.line_to(sx, sy-1/32)
    ctx.stroke()

  # Bottom

  def draw_crabgot(ctx, sx, sy):
    ctx.move_to(sx-3/32, sy)
    ctx.line_to(sx-4/32, sy+1/32)
    ctx.move_to(sx-3/64, sy)
    ctx.line_to(sx-3/64, sy+1/32)
    ctx.move_to(sx+3/64, sy)
    ctx.line_to(sx+3/64, sy+1/32)
    ctx.move_to(sx+3/32, sy)
    ctx.line_to(sx+4/32, sy+1/32)

  def draw_legs(ctx, sx, sy):
    ctx.move_to(sx-2/32, sy)
    ctx.line_to(sx-3/32, sy+1/32)
    ctx.move_to(sx+2/32, sy)
    ctx.line_to(sx+3/32, sy+1/32)

  def draw_flatline(ctx, sx, sy):
    ctx.move_to(sx-3/32, sy)
    ctx.line_to(sx+3/32, sy)
    ctx.stroke()

  def draw_dingleberry(ctx, sx, sy):
    Rune.draw_dot(ctx, sx, sy)

  # Debug / General

  def draw_circle(ctx, sx, sy, r):
    ctx.move_to(sx+r, sy)
    ctx.arc(sx, sy, r, 0, 2*pi)
    ctx.stroke()

  def draw_partitions(ctx, y_vals, x_vals):
    for y in y_vals:
      ctx.move_to(0, y)
      ctx.line_to(1, y)
      ctx.stroke()

    for x in x_vals:
      ctx.move_to(x, 0)
      ctx.line_to(x, 1)
      ctx.stroke()

Rune().render()
