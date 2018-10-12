from bitfieldpy.bitfieldpy import BitField
from attrdict import AttrDict

attr = AttrDict({"src": '[{"bits": 1, "name": "ENABLE"}, {"bits": 7, "name": ""}]',
                 "svg": "svg.svg",
                 "vspace": 50,
                 "hspace": 800,
                 "lanes": 1,
                 "bits": 8,
                 "font_family": "source sans pro",
                 "font_weight": "normal",
                 "font_size": 14,
                 })
bf = BitField(attr)
bf.render()
