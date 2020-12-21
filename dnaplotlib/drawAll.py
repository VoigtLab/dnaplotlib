'''script for drawing all sypported part glyphs
need to be moved outside the example directory 
at the same directory as render.py
'''

import render
import matplotlib.pyplot as plt


fig, ax = plt.subplots(1, figsize=(15,15))
# need to set axis first 
ax.set_xlim(-51.0, 51.0)
ax.set_ylim(-51.0, 51.0)

renderer = render.GlyphRenderer()


promoter = renderer.draw_glyph(ax, 'Promoter', (-40., 25.), 9, 0.)
assScar = renderer.draw_glyph(ax, 'AssemblyScar', (-30., 25.), 9, 0.)
bs = renderer.draw_glyph(ax, 'BluntRestrictionSite', (-20., 25.), 9, 0.)
cds = renderer.draw_glyph(ax, 'CDS', (-10., 25.), 9, 0.)
cpsite = renderer.draw_glyph(ax, 'Composite', (0., 25.), 9, 0.)
dnaCleavSite = renderer.draw_glyph(ax, 'DNACleavageSite', (10., 25.), 9, 0)
dnaLoc = renderer.draw_glyph(ax, 'DNALocation', (20., 25.), 9, 0.)
dnaStabElem = renderer.draw_glyph(ax, 'DNAStabilityElement', (30., 25.), 9, 0.)
engRegion = renderer.draw_glyph(ax, 'EngineeredRegion', (40., 25.), 9, 0.)

insulator = renderer.draw_glyph(ax, 'Insulator', (-40., 0.), 9, 0.)
noGlyph = renderer.draw_glyph(ax, 'NoGlyph', (-30., 0.), 9, 0.)
nonCodingRNA = renderer.draw_glyph(ax, 'NonCodingRNA', (-20, 0.), 9, 0.)
nucleicOneStand = renderer.draw_glyph(ax, 'NucleicAcidOneStrand', (-10., 0.), 9, 0.)
operator = renderer.draw_glyph(ax, 'Operator', (0., 0.), 9, 0)
ori = renderer.draw_glyph(ax, 'OriginOfReplication', (10., 0.), 9, 0.)
oritransfer = renderer.draw_glyph(ax, 'OriginOfTransfer', (20., 0.), 9, 0.)
overhang3 = renderer.draw_glyph(ax, 'OverhangSite3', (30., 0.), 9, 0.)
overhang5 = renderer.draw_glyph(ax, 'OverhangSite5', (40., 0.), 9, 0.)

primer = renderer.draw_glyph(ax, 'PrimerBindingSite', (-40., -20.), 9, 0.)
aptamer = renderer.draw_glyph(ax, 'Aptamer', (-30., -20.), 9, 0.)
recSite = renderer.draw_glyph(ax, 'RecombinationSite', (-20., -20.), 9, 0.)
ribEntrySite = renderer.draw_glyph(ax, 'RibosomeEntrySite', (-10., -20.), 9, 0.)
signature = renderer.draw_glyph(ax, 'Signature', (0., -20.), 9, 0.)
spacer = renderer.draw_glyph(ax, 'Spacer', (10., -20.), 9, 0.)
stickyResSite3 = renderer.draw_glyph(ax, 'StickyRestrictionSite3', (20., -20.), 9, 0.)
stickyResSite5 = renderer.draw_glyph(ax, 'StickyRestrictionSite5', (30., -20.), 9, 0.)
terminator = renderer.draw_glyph(ax, 'Terminator', (40., -20.), 9, 0.)

# polyASite = renderer.draw_glyph(ax, 'PolyASite', (25., 10.), 4.5, 0.)
# od = renderer.draw_glyph(ax, 'OmittedDetail', (-5., -10.), 20., 0.)
# unspecified = renderer.draw_glyph(ax, 'Unspecified', (-25., 0.), 4.5, 0.)

ax.set_axis_off()
plt.show()
