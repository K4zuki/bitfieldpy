#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" bitfieldpy
With great respect to original designer:
A Python3 porting of bitfield nodeJS module(https://github.com/drom/bitfield)
MIT License 2018 (c) Kazuki Yamamoto
"""

import svgwrite
import argparse
import json
from attrdict import AttrDict


class BitField(object):

    def __init__(self, args):
        with open(args.input, "r") as f:
            self.src = json.load(f, object_hook=AttrDict)
        self.args = args
        # print(self.args)
        # print(self.src)

    def hline(self, len, x=None, y=None):
        x1 = x if x is not None else 0
        x2 = (x + len) if x is not None else len
        y1 = y if y is not None else 0
        y2 = y if y is not None else 0

        ret = svgwrite.shapes.Line(start=(x1, y1), end=(x2, y2))
        return ret

    def vline(self, len, x=None, y=None):
        x1, x2 = (x, x) if x is not None else (0, 0)
        y1 = y if y is not None else 0
        y2 = (y + len) if y is not None else len

        ret = svgwrite.shapes.Line(start=(x1, y1), end=(x2, y2))
        return ret

    def labelArr(self):
        ret = svgwrite.container.Group()

        step = self.args.hspace / self.args.mod

        bits = svgwrite.container.Group()
        bits.translate(step / 2, self.args.vspace / 5)
        names = svgwrite.container.Group()
        names.translate(step / 2, self.args.vspace / 2 + 4)
        attrs = svgwrite.container.Group()
        attrs.translate(step / 2, self.args.vspace)
        blanks = svgwrite.container.Group()
        blanks.translate(0, self.args.vspace / 4)

        fontsize = self.args.font_size
        fontfamily = self.args.font_family
        fontweight = self.args.font_weight

        fontconfig = (fontsize, fontfamily, fontweight)

        def sub(bits, fontconfig, elem):
            fontsize, fontfamily, fontweight = fontconfig
            lText = []  # leftText
            aText = []  # attrText?
            lsbm = 0
            msbm = int(self.args.mod - 1)
            lsb = int(self.args.index * self.args.mod)
            msb = int((self.args.index + 1) * self.args.mod - 1)
            if int(elem.lsb / self.args.mod) == self.args.index:
                lsbm = int(elem.lsbm)
                lsb = int(elem.lsb)
                if int(elem.msb / self.args.mod) == self.args.index:
                    msb = int(elem.msb)
                    msbm = int(elem.msbm)

            else:
                if (int(elem.msb / self.args.mod) == self.args.index):
                    msb = int(elem.msb)
                    msbm = int(elem.msbm)
                else:
                    return

            bits.add(svgwrite.text.Text(str(lsb),
                                        x=[step * (self.args.mod - lsbm - 1)],
                                        font_size=str(int(fontsize)),
                                        font_family=fontfamily,
                                        font_weight=fontweight
                                        )
                     )
            if lsbm != msbm:
                bits.add(svgwrite.text.Text(str(msb),
                                            x=[step * (self.args.mod - msbm - 1)],
                                            font_size=str(fontsize),
                                            font_family=fontfamily,
                                            font_weight=fontweight
                                            ))
            if elem.get("name"):
                names.add(svgwrite.text.Text(elem.name,
                                             x=[step * (self.args.mod - ((msbm + lsbm) / 2) - 1)],
                                             font_size=fontsize,
                                             font_family=fontfamily,
                                             font_weight=fontweight
                                             )
                          )
            else:
                blanks.add(svgwrite.shapes.Rect(
                    insert=(step * (self.args.mod - msbm - 1), 0),
                    size=(step * (msbm - lsbm + 1), self.args.vspace / 2),
                    fill_opacity=0.1,
                    # style="fill-opacity:0.5",
                    fill="black")
                )
            if elem.get("attr"):

                attrs.add(svgwrite.text.Text(elem.attr,
                                             x=[step * (self.args.mod - ((msbm + lsbm) / 2) - 1)],
                                             font_size=fontsize,
                                             font_family=fontfamily,
                                             font_weight=fontweight
                                             )
                          )
            return
        [sub(bits, fontconfig, d) for d in self.src]
        ret = svgwrite.container.Group()
        ret.add(blanks)
        ret.add(bits)
        ret.add(names)
        ret.add(attrs)
        return ret

    def labels(self):
        ret = svgwrite.container.Group(text_anchor="middle")
        ret.add(self.labelArr())
        return ret

    def cage(self):
        hspace = self.args.hspace
        vspace = self.args.vspace
        mod = self.args.mod
        dx = 0
        dy = vspace / 4
        res = svgwrite.container.Group(stroke="black",
                                       stroke_width=1,
                                       stroke_linecap="round",
                                       )

        res.translate(dx, dy)
        res.add(self.hline(hspace))
        res.add(self.vline(vspace / 2))
        res.add(self.hline(hspace, 0, vspace / 2))

        i = self.args.index * self.args.mod
        j = self.args.mod

        def tf(e, i):
            return True if e.lsb == i else False
        while j:
            if (j == self.args.mod) or any([tf(elem, i) for elem in self.src]):
                res.add(self.vline((vspace / 2), j * (hspace / mod)))
            else:
                res.add(self.vline((vspace / 16), j * (hspace / mod)))
                res.add(self.vline((vspace / 16), j * (hspace / mod), vspace * 7 / 16))

            i += 1
            j -= 1

        return res

    def lane(self):
        dx = 4.5
        dy = (self.args.lanes - self.args.index - 1) * self.args.vspace + 0.5
        res = svgwrite.container.Group()
        res.translate(dx, dy)
        res.add(self.cage())
        res.add(self.labels())
        return res

    def render(self):
        width = self.args.hspace + 9
        height = self.args.vspace * self.args.lanes + 5
        view = "0 0 {w} {h}".format(w=width, h=height)
        dwg = svgwrite.Drawing(filename=self.args.svg,
                               size=(width, height),
                               viewBox=view
                               )

        lsb = 0
        mod = self.args.bits / self.args.lanes
        self.args.mod = mod

        for elem in self.src:
            elem.lsb = lsb
            elem.lsbm = lsb % mod
            lsb += elem.bits
            elem.msb = lsb - 1
            elem.msbm = elem.msb % mod

        for i in range(self.args.lanes):
            self.args.index = i
            dwg.add(self.lane())

        dwg.save()


def main():
    parser = argparse.ArgumentParser(description="bitfield clone in python(experimental)")
    parser.add_argument("--input", "-i", help="<input bitfield source filename>")
    parser.add_argument("--svg", "-s", help="<output SVG image file name>")

    parser.add_argument("--vspace", "-V", type=int, default=80, help="height per lane in px")
    parser.add_argument("--hspace", "-H", type=int, default=640, help="width per lane in px")
    parser.add_argument("--lanes", "-L", type=int, default=2, help="number of lane")
    parser.add_argument("--bits", "-B", type=int, default=32, help="total bitwidth")
    parser.add_argument("--font-family", "-F", default="sans-serif", help="font family for all texts")
    parser.add_argument("--font-weight", "-W", default="normal", help="font weight")
    parser.add_argument("--font-size", "-S", type=int, default=14, help="font size")
    # parser.add_argument("--bigendian", "-E", default=False, help="endian")

    attr = AttrDict()
    args = parser.parse_args(namespace=attr)
    args.vspace = args.vspace
    args.hspace = args.hspace
    args.lanes = args.lanes
    args.bits = args.bits
    if args.svg is None or args.input is None:
        parser.print_help()
    else:
        bf = BitField(args)
        bf.render()


if __name__ == "__main__":
    main()
