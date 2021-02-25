from __future__ import annotations
from typing import List, Optional
import sys
import argparse

"""Draw some graphics based on mathematical rules."""

from base.basic import Point
from base.black_box import BlackBox, RepeatBox
from blocks.bool import *
from blocks.math import *
from blocks.const_var import *
from blocks.deprecated import *
from core.crazy_matrix import CrazyMatrix
from core.block_manager import BlockManager
from templates.block import IdGenerator, BlockTemplateFactory, BlockTemplate, BlockType
from templates.circuit import Circuit, CircuitFactory
from templates.box import BlackBoxFactory, RepeatBoxFactory
from templates.bond import BoxSide, BondTemplate
from templates.conn import ConnTemplate
from base.block import Conn
from gui import Gui


__author__ = "Anton Höß"
__copyright__ = "Copyright 2021"
__credits__ = list()
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Anton Höß"
__email__ = "anton.hoess42@gmail.com"
__status__ = "Development"


def main(_argv: List[str]):

    # Read command line arguments
    parser = argparse.ArgumentParser(description="Draw some graphics based on mathematical rules.")
    parser.add_argument("-t", "--test", type=int, required=True,
                        help="Defines the test example to run.")
    args = parser.parse_args()

    # Run selected example
    c = Circuit()

    p = c.point
    d = c.drawer

    bm = BlockManager(base_dir="user_blocks", schema_filename="core/box_data_schema_v1.0.yaml")
    bm.scan_dir()

    # test 26 creates all predefined user-blocks anew
    test = args.test  # 29  # 17 (circuit), 19 (black box), 25 (repeat box)

    draw = True

    width = 400
    height = 200

    if test == 0:
        pi = Const(4.27)
        d.conn_to_prev_block(pi)

    elif test == 1:
        d.conn_to_prev_block(p, 1)

    elif test == 2:
        sin = Sin(deg=True)
        sin.conn_to_prev_block(p, 1)
        d.conn_to_prev_block(sin)

    elif test == 3:
        mul: Block = Mul2()
        mul.conn_to_prev_block(p, 0, 0)
        mul.conn_to_prev_block(p, 1, 1)
        d.conn_to_prev_block(mul)

    elif test == 4:
        sin = Sin(deg=True)
        sin.conn_to_prev_block(p, 0)

        mul = Mul2()
        mul.conn_to_prev_block(sin, 0, 0)
        mul.conn_to_prev_block(p, 1, 1)
        d.conn_to_prev_block(mul)

    elif test == 5:
        cos = Cos(deg=True)
        cos.conn_to_prev_block(p, 0)

        mul_p = Mul2()
        mul_p.conn_to_prev_block(p, 0, 0)
        mul_p.conn_to_prev_block(p, 1, 1)

        mul_ps = Mul2()
        mul_ps.conn_to_prev_block(cos)
        mul_ps.conn_to_prev_block(mul_p, 0, 1)
        d.conn_to_prev_block(mul_ps)

    elif test == 6:
        cos = Cos(deg=True)
        cos.conn_to_prev_block(p, 0)

        absx = Abs()
        absx.conn_to_prev_block(p, 0)

        absy = Abs()
        absy.conn_to_prev_block(p, 1)

        mul_p = Mul2()
        mul_p.conn_to_prev_block(absx, 0, 0)
        mul_p.conn_to_prev_block(p, 1, 1)

        mul_ps = Mul2()
        mul_ps.conn_to_prev_block(cos)
        mul_ps.conn_to_prev_block(mul_p, 0, 1)

        sq = Sq()
        sq.conn_to_prev_block(mul_ps)
        d.conn_to_prev_block(sq)

    elif test == 7:
        modn = Const(40)

        modx = Mod()
        modx.conn_to_prev_block(p, 0, 0)
        modx.conn_to_prev_block(modn, 0, 1)

        mody = Mod()
        mody.conn_to_prev_block(p, 1, 0)
        mody.conn_to_prev_block(modn, 0, 1)

        mul = Mul2()
        mul.conn_to_prev_block(modx, 0, 0)
        mul.conn_to_prev_block(mody, 0, 1)

        d.conn_to_prev_block(mul)

    elif test == 8:
        max_dist = Const(100)
        point1 = Point(50, 40)

        diff_x = Sub2()
        diff_x.conn_to_prev_block(p, 0, 0)
        diff_x.conn_to_prev_block(point1, 0, 1)

        diff_y = Sub2()
        diff_y.conn_to_prev_block(p, 1, 0)
        diff_y.conn_to_prev_block(point1, 1, 1)

        x_sq = Sq()
        x_sq.conn_to_prev_block(diff_x)

        y_sq = Sq()
        y_sq.conn_to_prev_block(diff_y)

        add_xy_sq = Add2()
        add_xy_sq.conn_to_prev_block(x_sq, 0, 0)
        add_xy_sq.conn_to_prev_block(y_sq, 0, 1)

        dist = Sqrt()
        dist.conn_to_prev_block(add_xy_sq)

        gt = Gt()
        gt.conn_to_prev_block(max_dist, 0, 0)
        gt.conn_to_prev_block(dist, 0, 1)

        mul = Mul2()
        mul.conn_to_prev_block(dist, 0, 0)
        mul.conn_to_prev_block(gt, 0, 1)

        d.conn_to_prev_block(mul)

    elif test == 9:
        # Repeating block with reassigning values through variables und the implicit usage of synchronization barriers in the black box
        var: Block = Variable()
        add: Block = Add2()
        add.conn_to_prev_block(var, 0, 1)

        rb = RepeatBox(2, "FibonacciN")

        rb.assign_conn_in(add, 0, 0)
        rb.assign_conn_in(var, 0, 1)

        rb.assign_pin_value(var, 0, 0)
        rb.assign_pin_value(add, 0, 1)

        # rb.conn_to_prev_block(Const(1), 0, 0)  # Initial values
        # rb.conn_to_prev_block(Const(1), 0, 1)
        rb.conn_to_prev_block(p, 0, 0)
        rb.conn_to_prev_block(p, 1, 1)
        rb.conn_to_prev_block(Const(5), 0, 2)  # no. rep.

        d.conn_to_prev_block(rb, 1)

        # function defining a mandelbrot
        # def mandelbrot(x, y):
        #     c0 = complex(x, y)
        #     c = 0
        #     for i in range(1, 1000):
        #         if abs(c) > 2:
        #             return i  # rgb_conv(i)
        #         c = c * c + c0
        #     return (0, 0, 0)

    elif test == 10:
        # Sum if distances to three points
        points = list()
        points.append(Point(50, 40))
        points.append(Point(-50, -40))
        points.append(Point(150, -75))

        dists = AddN()

        for i, point in enumerate(points):
            diff_x = Sub2()
            diff_x.conn_to_prev_block(p, 0, 0)
            diff_x.conn_to_prev_block(point, 0, 1)

            diff_y = Sub2()
            diff_y.conn_to_prev_block(p, 1, 0)
            diff_y.conn_to_prev_block(point, 1, 1)

            add_xy_sq = Add2()
            add_xy_sq.conn_to_prev_block(Sq(diff_x), 0, 0)
            add_xy_sq.conn_to_prev_block(Sq(diff_y), 0, 1)

            _dist = Sqrt(add_xy_sq)

            __dist = Add2()
            __dist.conn_to_prev_block(_dist, 0, 0)
            __dist.conn_to_prev_block(Const(100.), 0, 1)

            dist = Mul2()
            dist.conn_to_prev_block(__dist, 0, 0)
            dist.conn_to_prev_block(Const(1.) if i > 0 else Const(1.5), 0, 1)

            gravity = Div2()
            gravity.conn_to_prev_block(Const(1.), 0, 0)
            gravity.conn_to_prev_block(dist, 0, 1)

            dists.conn_to_prev_block(gravity)
        # end for

        d.conn_to_prev_block(dists)

    elif test == 11:
        # Black square in the middle of the plot
        dist = Const(50.)

        gt_x = Gt()
        gt_x.conn_to_prev_block(p, 0, 0)
        gt_x.conn_to_prev_block(Minus(dist), 0, 1)

        lt_x = Lt()
        lt_x.conn_to_prev_block(p, 0, 0)
        lt_x.conn_to_prev_block(dist, 0, 1)

        gt_y = Gt()
        gt_y.conn_to_prev_block(p, 1, 0)
        gt_y.conn_to_prev_block(Minus(dist), 0, 1)

        lt_y = Lt()
        lt_y.conn_to_prev_block(p, 1, 0)
        lt_y.conn_to_prev_block(dist, 0, 1)

        # Block
        and_a = And2()

        and_b = And2()

        and_res = And2()
        and_res.conn_to_prev_block(and_a, 0, 0)
        and_res.conn_to_prev_block(and_b, 0, 1)
        # End block

        and_a.conn_to_prev_block(gt_x, 0, 0)
        and_a.conn_to_prev_block(lt_x, 0, 1)

        and_b.conn_to_prev_block(gt_y, 0, 0)
        and_b.conn_to_prev_block(lt_y, 0, 1)

        d.conn_to_prev_block(and_res)

    elif test == 12:
        # Black square in the middle of the plot using a And4 black box
        dist = Const(50.)

        gt_x = Gt()
        gt_x.conn_to_prev_block(p, 0, 0)
        gt_x.conn_to_prev_block(Minus(dist), 0, 1)

        lt_x = Lt()
        lt_x.conn_to_prev_block(p, 0, 0)
        lt_x.conn_to_prev_block(dist, 0, 1)

        gt_y = Gt()
        gt_y.conn_to_prev_block(p, 1, 0)
        gt_y.conn_to_prev_block(Minus(dist), 0, 1)

        lt_y = Lt()
        lt_y.conn_to_prev_block(p, 1, 0)
        lt_y.conn_to_prev_block(dist, 0, 1)

        # Block
        bb = BlackBox(4, 1, "And4")

        and_a = And2()

        and_b = And2()

        and_res = And2()
        and_res.conn_to_prev_block(and_a, 0, 0)
        and_res.conn_to_prev_block(and_b, 0, 1)

        # --

        bb.assign_conn_in(and_a, 0, 0)
        bb.assign_conn_in(and_a, 1, 1)
        bb.assign_conn_in(and_b, 0, 2)
        bb.assign_conn_in(and_b, 1, 3)
        bb.assign_pin_value(and_res, 0, 0)
        # End block

        bb.conn_to_prev_block(gt_x, 0, 0)
        bb.conn_to_prev_block(lt_x, 0, 1)

        bb.conn_to_prev_block(gt_y, 0, 2)
        bb.conn_to_prev_block(lt_y, 0, 3)

        d.conn_to_prev_block(bb)

    elif test == 13:
        class SquareXn(BlockFixed):
            def __init__(self, prev_block: Optional[BlockFixed], prev_pin: Optional[int] = None, name: Optional[str] = None):
                BlockFixed.__init__(self, 2, 1, name)
                self.__cnt = 0
                self.__n_rep = 0
                self.__inited = False

                if prev_block is not None:  # Apply this shortcut to other items as well
                    self.conn_to_prev_block(prev_block, prev_pin)
                # end if

            # end def

            def _calc_values(self):
                if not self.__inited:
                    self.__n_rep = int(self._conn_in[1].value) - 1
                    self.__inited = True
                # end if

                if self.__cnt < self.__n_rep:
                    self.__cnt += 1
                    x = Conn(self, 0).value  # This recursively triggers _calc_values()
                else:
                    self.__cnt = 0
                    self.__inited = False
                    x = self._conn_in[0].value
                # end if

                self._pin_value[0] = x * x
            # end def
        # end class

        sxn = SquareXn(None, name="10 squared 4 times")
        sxn.conn_to_prev_block(p, 0, 0)
        sxn.conn_to_prev_block(Const(10), 0, 1)

        d.conn_to_prev_block(sxn)

    elif test == 14:
        # Exponentiation (repeated squaring) using a RepeatBox
        sq = Sq()

        rb = RepeatBox(1, "SquareTimesN")

        rb.assign_conn_in(sq, 0, 0)
        rb.assign_pin_value(sq, 0, 0)

        rb.conn_to_prev_block(Const(10), 0, 0)
        rb.conn_to_prev_block(Const(2), 0, 1)  # no. rep.

        d.conn_to_prev_block(rb)

    elif test == 15:
        # Shifting (e.g. Rot13) using a RepeatBox and a special Rot4 block
        rot4 = Rot1_4()

        rb = RepeatBox(4, "Rot")

        rb.assign_conn_in(rot4, 0, 0)
        rb.assign_conn_in(rot4, 1, 1)
        rb.assign_conn_in(rot4, 2, 2)
        rb.assign_conn_in(rot4, 3, 3)

        rb.assign_pin_value(rot4, 0, 0)
        rb.assign_pin_value(rot4, 1, 1)
        rb.assign_pin_value(rot4, 2, 2)
        rb.assign_pin_value(rot4, 3, 3)

        rb.conn_to_prev_block(Const(10), 0, 0)
        rb.conn_to_prev_block(Const(20), 0, 1)
        rb.conn_to_prev_block(Const(30), 0, 2)
        rb.conn_to_prev_block(Const(40), 0, 3)
        rb.conn_to_prev_block(Const(2), 0, 4)  # no. rep.

        d.conn_to_prev_block(rb, 1, 0)

    elif test == 16:
        # Three numbers (1, 2, 3), each squared 3 times and their 3 resulting values are summed up = 6818
        sq1 = Sq()
        sq2 = Sq()
        sq3 = Sq()

        rb = RepeatBox(3, "rb")

        rb.assign_conn_in(sq1, 0, 0)
        rb.assign_conn_in(sq2, 0, 1)
        rb.assign_conn_in(sq3, 0, 2)

        rb.assign_pin_value(sq1, 0, 0)
        rb.assign_pin_value(sq2, 0, 1)
        rb.assign_pin_value(sq3, 0, 2)

        rb.conn_to_prev_block(Const(1), 0, 0)
        rb.conn_to_prev_block(Const(2), 0, 1)
        rb.conn_to_prev_block(Const(3), 0, 2)
        rb.conn_to_prev_block(Const(3), 0, 3)  # no. rep.

        addn: Block = AddN()
        addn.conn_to_prev_block(rb, 0)
        addn.conn_to_prev_block(rb, 1)
        addn.conn_to_prev_block(rb, 2)

        d.conn_to_prev_block(addn, 0)

    elif test == 17:
        # Store and load a complete circuit - this example cannot use the global circuit, since it instantiates its own
        out_filename = "test17"
        idg: IdGenerator = IdGenerator()

        cf: CircuitFactory = CircuitFactory()
        btf: BlockTemplateFactory = BlockTemplateFactory(idg)

        fac: BlockTemplate = cf.add_block(btf.get_block_template(BlockType.VAL_CONST, .3))
        mul: BlockTemplate = cf.add_block(btf.get_block_template(BlockType.MATH_MUL))
        add: BlockTemplate = cf.add_block(btf.get_block_template(BlockType.MATH_ADD))

        cf.add_conn(ConnTemplate("0", 0, mul.id, None))
        cf.add_conn(ConnTemplate(fac.id, 0, mul.id, None))
        cf.add_conn(ConnTemplate(mul.id, 0, add.id, None))
        cf.add_conn(ConnTemplate("0", 1, add.id, None))
        cf.add_conn(ConnTemplate(add.id, 0, "1", 0))

        # Check, if storing and loading really works
        if True:
            bm.store(cf, out_filename)
            bm.scan_dir()
            cf = bm.load(out_filename)
        # end if

        c = cf.inst()

        cm = CrazyMatrix(c, width=100, height=100)

        cm.plot()

    elif test == 18:
        # Construct and use an black box instance
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        my_add = BlackBoxFactory()

        addn: BlockTemplate = btf.get_block_template(BlockType.MATH_ADD)
        my_add.add_block(addn)

        my_add.add_bond(BondTemplate(BoxSide.IN, addn.id, None, 0))
        my_add.add_bond(BondTemplate(BoxSide.IN, addn.id, None, 1))
        my_add.add_bond(BondTemplate(BoxSide.OUT, addn.id, None, 0))

        bb = my_add.inst("my_add")

        bb.conn_to_prev_block(p, 0, 0)
        bb.conn_to_prev_block(p, 1, 1)
        d.conn_to_prev_block(bb, 0, 0)

    elif test == 19:
        # Defines, stores and loads a black box
        out_filename = "test19"
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        my_func = BlackBoxFactory()

        fac: BlockTemplate = my_func.add_block(btf.get_block_template(BlockType.VAL_CONST, .3))
        muln: BlockTemplate = my_func.add_block(btf.get_block_template(BlockType.MATH_MUL))
        addn: BlockTemplate = my_func.add_block(btf.get_block_template(BlockType.MATH_ADD))

        # Interconnect the blocks of the box
        my_func.add_conn(ConnTemplate(fac.id, 0, muln.id, None))
        my_func.add_conn(ConnTemplate(muln.id, 0, addn.id, None))

        # Bond the block of the box to the box pins
        my_func.add_bond(BondTemplate(BoxSide.IN, muln.id, None, 0))
        my_func.add_bond(BondTemplate(BoxSide.IN, addn.id, None, 1))
        my_func.add_bond(BondTemplate(BoxSide.OUT, addn.id, 0, 0))

        if True:
            bm.store(my_func, out_filename)
            bm.scan_dir()
            my_func: BlackBoxFactory = bm.load(out_filename)
        # end if

        bb = my_func.inst("my_func")

        bb.conn_to_prev_block(p, 0, 0)
        bb.conn_to_prev_block(p, 1, 1)
        d.conn_to_prev_block(bb, 0, 0)

    elif test == 20:
        # Defines the distance function as black box
        out_filename = "dist.cmb"
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        dist_func = BlackBoxFactory()

        # --

        diff_x = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_y = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_x_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
        diff_y_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
        add_xy_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_ADD))
        dist = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQRT))
        dist_rescaled = dist_func.add_block(btf.get_block_template(BlockType.MATH_MUL))

        # Interconnect the blocks of the box
        dist_func.add_conn(ConnTemplate(diff_x.id, 0, diff_x_sq.id, 0))
        dist_func.add_conn(ConnTemplate(diff_y.id, 0, diff_y_sq.id, 0))
        dist_func.add_conn(ConnTemplate(diff_x_sq.id, 0, add_xy_sq.id, None))
        dist_func.add_conn(ConnTemplate(diff_y_sq.id, 0, add_xy_sq.id, None))
        dist_func.add_conn(ConnTemplate(add_xy_sq.id, 0, dist.id, 0))
        dist_func.add_conn(ConnTemplate(dist.id, 0, dist_rescaled.id, None))

        # Bond the block of the box to the box pins
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 0, 0))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 0, 1))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 1, 2))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 1, 3))
        dist_func.add_bond(BondTemplate(BoxSide.IN, dist_rescaled.id, None, 4))
        dist_func.add_bond(BondTemplate(BoxSide.OUT, dist_rescaled.id, 0, 0))

        dist_func.store(out_filename)

        if True:
            dist_func: BlackBoxFactory = BlackBoxFactory()
            dist_func.load(out_filename)
        # end if

        bb = dist_func.inst("dist_func")

        my_p_x = Const(-130)
        my_p_y = Const(80)
        rescale_factor = Const(10.)
        bb.conn_to_prev_block(p, 0, 0)
        bb.conn_to_prev_block(p, 1, 1)
        bb.conn_to_prev_block(my_p_x, 0, 2)
        bb.conn_to_prev_block(my_p_y, 0, 3)
        bb.conn_to_prev_block(rescale_factor, 0, 4)

        d.conn_to_prev_block(bb, 0, 0)

    elif test == 21:
        # Test with multiple instances of the same black box
        out_filename = "dist.cmb"
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        dist_func = BlackBoxFactory()

        # --

        diff_x = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_y = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_x_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
        diff_y_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
        add_xy_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_ADD))
        dist = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQRT))
        dist_rescaled = dist_func.add_block(btf.get_block_template(BlockType.MATH_MUL))

        # Interconnect the blocks of the box
        dist_func.add_conn(ConnTemplate(diff_x.id, 0, diff_x_sq.id, 0))
        dist_func.add_conn(ConnTemplate(diff_y.id, 0, diff_y_sq.id, 0))
        dist_func.add_conn(ConnTemplate(diff_x_sq.id, 0, add_xy_sq.id, None))
        dist_func.add_conn(ConnTemplate(diff_y_sq.id, 0, add_xy_sq.id, None))
        dist_func.add_conn(ConnTemplate(add_xy_sq.id, 0, dist.id, 0))
        dist_func.add_conn(ConnTemplate(dist.id, 0, dist_rescaled.id, None))

        # Bond the block of the box to the box pins
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 0, 0))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 0, 1))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 1, 2))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 1, 3))
        dist_func.add_bond(BondTemplate(BoxSide.IN, dist_rescaled.id, None, 4))
        dist_func.add_bond(BondTemplate(BoxSide.OUT, dist_rescaled.id, 0, 0))

        dist_func.store(out_filename)

        if True:
            dist_func: BlackBoxFactory = BlackBoxFactory()
            dist_func.load(out_filename)
        # end if

        scale = 0.001
        dist_total = AddN()

        bb0 = dist_func.inst("dist_func")

        p0_x = Const(-130)
        p0_y = Const(80)
        p0_scale = Const(scale)

        bb0.conn_to_prev_block(p, 0, 0)
        bb0.conn_to_prev_block(p, 1, 1)
        bb0.conn_to_prev_block(p0_x, 0, 2)
        bb0.conn_to_prev_block(p0_y, 0, 3)
        bb0.conn_to_prev_block(p0_scale, 0, 4)

        dist_total.conn_to_prev_block(Inv(bb0), 0, None)

        bb1 = dist_func.inst("dist_func")

        p1_x = Const(100)
        p1_y = Const(70)
        p1_scale = Const(scale*.5)

        bb1.conn_to_prev_block(p, 0, 0)
        bb1.conn_to_prev_block(p, 1, 1)
        bb1.conn_to_prev_block(p1_x, 0, 2)
        bb1.conn_to_prev_block(p1_y, 0, 3)
        bb1.conn_to_prev_block(p1_scale, 0, 4)

        dist_total.conn_to_prev_block(Inv(bb1), 0, None)

        bb2 = dist_func.inst("dist_func")

        p2_x = Const(0)
        p2_y = Const(-90)
        p2_scale = Const(scale)

        bb2.conn_to_prev_block(p, 0, 0)
        bb2.conn_to_prev_block(p, 1, 1)
        bb2.conn_to_prev_block(p2_x, 0, 2)
        bb2.conn_to_prev_block(p2_y, 0, 3)
        bb2.conn_to_prev_block(p2_scale, 0, 4)

        dist_total.conn_to_prev_block(Inv(bb2), 0, None)

        d.conn_to_prev_block(dist_total, 0, 0)

    elif test == 22:
        # Added distance of three points using multiple instances each of the dist- and the normal-function black box
        fn_dist = "dist.cmb"
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        dist_func = BlackBoxFactory()

        diff_x = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_y = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_x_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
        diff_y_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
        add_xy_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_ADD))
        dist = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQRT))
        dist_rescaled = dist_func.add_block(btf.get_block_template(BlockType.MATH_MUL))

        # Interconnect the blocks of the box
        dist_func.add_conn(ConnTemplate(diff_x.id, 0, diff_x_sq.id, 0))
        dist_func.add_conn(ConnTemplate(diff_y.id, 0, diff_y_sq.id, 0))
        dist_func.add_conn(ConnTemplate(diff_x_sq.id, 0, add_xy_sq.id, None))
        dist_func.add_conn(ConnTemplate(diff_y_sq.id, 0, add_xy_sq.id, None))
        dist_func.add_conn(ConnTemplate(add_xy_sq.id, 0, dist.id, 0))
        dist_func.add_conn(ConnTemplate(dist.id, 0, dist_rescaled.id, None))

        # Bond the block of the box to the box pins
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 0, 0))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 0, 1))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 1, 2))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 1, 3))
        dist_func.add_bond(BondTemplate(BoxSide.IN, dist_rescaled.id, None, 4))
        dist_func.add_bond(BondTemplate(BoxSide.OUT, dist_rescaled.id, 0, 0))

        dist_func.store(fn_dist)

        # normal distribution
        # Test in multiple instances of a black box
        fn_normal = "normal.cmb"
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        normal_func = BlackBoxFactory()

        exp_term_fac = normal_func.add_block(btf.get_block_template(BlockType.VAL_CONST, -.5))
        exp_term_x_sq = normal_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
        exp_term = normal_func.add_block(btf.get_block_template(BlockType.MATH_MUL))
        normal = normal_func.add_block(btf.get_block_template(BlockType.MATH_EXP))

        # Interconnect the blocks of the box
        normal_func.add_conn(ConnTemplate(exp_term_fac.id, 0, exp_term.id, None))
        normal_func.add_conn(ConnTemplate(exp_term_x_sq.id, 0, exp_term.id, None))
        normal_func.add_conn(ConnTemplate(exp_term.id, 0, normal.id, 0))

        # Bond the block of the box to the box pins
        normal_func.add_bond(BondTemplate(BoxSide.IN, exp_term_x_sq.id, 0, 0))
        normal_func.add_bond(BondTemplate(BoxSide.OUT, normal.id, 0, 0))

        normal_func.store(fn_normal)

        if True:
            dist_func: BlackBoxFactory = BlackBoxFactory()
            dist_func.load(fn_dist)

            normal_func: BlackBoxFactory = BlackBoxFactory()
            normal_func.load(fn_normal)
        # end if

        scale = .05
        dist_total = AddN()

        # Point 0
        bb_dist0 = dist_func.inst("dist_func")
        bb_normal0 = normal_func.inst("normal_func")

        p0_x = Const(70)
        p0_y = Const(60)
        p0_scale = Const(scale)

        bb_dist0.conn_to_prev_block(p, 0, 0)
        bb_dist0.conn_to_prev_block(p, 1, 1)
        bb_dist0.conn_to_prev_block(p0_x, 0, 2)
        bb_dist0.conn_to_prev_block(p0_y, 0, 3)
        bb_dist0.conn_to_prev_block(p0_scale, 0, 4)

        bb_normal0.conn_to_prev_block(bb_dist0, 0, 0)

        dist_total.conn_to_prev_block(bb_normal0, 0, None)

        # Point 1
        bb_dist1 = dist_func.inst("dist_func")
        bb_normal1 = normal_func.inst("normal_func")

        p1_x = Const(-100)
        p1_y = Const(80)
        p1_scale = Const(scale*2)

        bb_dist1.conn_to_prev_block(p, 0, 0)
        bb_dist1.conn_to_prev_block(p, 1, 1)
        bb_dist1.conn_to_prev_block(p1_x, 0, 2)
        bb_dist1.conn_to_prev_block(p1_y, 0, 3)
        bb_dist1.conn_to_prev_block(p1_scale, 0, 4)

        bb_normal1.conn_to_prev_block(bb_dist1, 0, 0)

        dist_total.conn_to_prev_block(bb_normal1, 0, None)

        # Point 2
        bb_dist2 = dist_func.inst("dist_func")
        bb_normal2 = normal_func.inst("normal_func")

        p2_x = Const(-80)
        p2_y = Const(-20)
        p2_scale = Const(scale/3)

        bb_dist2.conn_to_prev_block(p, 0, 0)
        bb_dist2.conn_to_prev_block(p, 1, 1)
        bb_dist2.conn_to_prev_block(p2_x, 0, 2)
        bb_dist2.conn_to_prev_block(p2_y, 0, 3)
        bb_dist2.conn_to_prev_block(p2_scale, 0, 4)

        bb_normal2.conn_to_prev_block(bb_dist2, 0, 0)

        dist_total.conn_to_prev_block(bb_normal2, 0, None)

        d.conn_to_prev_block(dist_total, 0, 0)

    elif test == 23:
        # Added distance of three points using a black box consisting of two other black boxes
        fn_dist = "dist.cmb"
        fn_normal = "normal.cmb"
        fn_normal_dist = "normal_dist.cmb"

        store_and_load = False#True
        if not store_and_load:
            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            dist_func = BlackBoxFactory()

            diff_x = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
            diff_y = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
            diff_x_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
            diff_y_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
            add_xy_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_ADD))
            dist = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQRT))
            dist_rescaled = dist_func.add_block(btf.get_block_template(BlockType.MATH_MUL))

            # Interconnect the blocks of the box
            dist_func.add_conn(ConnTemplate(diff_x.id, 0, diff_x_sq.id, 0))
            dist_func.add_conn(ConnTemplate(diff_y.id, 0, diff_y_sq.id, 0))
            dist_func.add_conn(ConnTemplate(diff_x_sq.id, 0, add_xy_sq.id, None))
            dist_func.add_conn(ConnTemplate(diff_y_sq.id, 0, add_xy_sq.id, None))
            dist_func.add_conn(ConnTemplate(add_xy_sq.id, 0, dist.id, 0))
            dist_func.add_conn(ConnTemplate(dist.id, 0, dist_rescaled.id, None))

            # Bond the block of the box to the box pins
            dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 0, 0))
            dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 0, 1))
            dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 1, 2))
            dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 1, 3))
            dist_func.add_bond(BondTemplate(BoxSide.IN, dist_rescaled.id, None, 4))
            dist_func.add_bond(BondTemplate(BoxSide.OUT, dist_rescaled.id, 0, 0))

            dist_func.store(fn_dist)

            # normal distribution
            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            normal_func = BlackBoxFactory()

            exp_term_fac = normal_func.add_block(btf.get_block_template(BlockType.VAL_CONST, -.5))
            exp_term_x_sq = normal_func.add_block(btf.get_block_template(BlockType.MATH_SQ))
            exp_term = normal_func.add_block(btf.get_block_template(BlockType.MATH_MUL))
            normal = normal_func.add_block(btf.get_block_template(BlockType.MATH_EXP))

            # Interconnect the blocks of the box
            normal_func.add_conn(ConnTemplate(exp_term_fac.id, 0, exp_term.id, None))
            normal_func.add_conn(ConnTemplate(exp_term_x_sq.id, 0, exp_term.id, None))
            normal_func.add_conn(ConnTemplate(exp_term.id, 0, normal.id, 0))

            # Bond the block of the box to the box pins
            normal_func.add_bond(BondTemplate(BoxSide.IN, exp_term_x_sq.id, 0, 0))
            normal_func.add_bond(BondTemplate(BoxSide.OUT, normal.id, 0, 0))

            normal_func.store(fn_normal)

            # normal-dist function
            ######################
            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            normal_dist_func = BlackBoxFactory()

            dist = normal_dist_func.add_block(btf.get_block_template(BlockType.BOX, box_name="dist"))
            normal = normal_dist_func.add_block(btf.get_block_template(BlockType.BOX, box_name="normal"))

            # Interconnect the blocks of the box
            normal_dist_func.add_conn(ConnTemplate(dist.id, 0, normal.id, 0))

            # Bond the block of the box to the box pins
            normal_dist_func.add_bond(BondTemplate(BoxSide.IN, dist.id, 0, 0))
            normal_dist_func.add_bond(BondTemplate(BoxSide.IN, dist.id, 1, 1))
            normal_dist_func.add_bond(BondTemplate(BoxSide.IN, dist.id, 2, 2))
            normal_dist_func.add_bond(BondTemplate(BoxSide.IN, dist.id, 3, 3))
            normal_dist_func.add_bond(BondTemplate(BoxSide.IN, dist.id, 4, 4))
            normal_dist_func.add_bond(BondTemplate(BoxSide.OUT, normal.id, 0, 0))

            normal_dist_func.store(fn_normal_dist)

        else:
            dist_func: BlackBoxFactory = BlackBoxFactory()
            dist_func.load(fn_dist)

            normal_func: BlackBoxFactory = BlackBoxFactory()
            normal_func.load(fn_normal)

            normal_dist_func: BlackBoxFactory = BlackBoxFactory()
            normal_dist_func.load(fn_normal_dist)
        # end if

        scale = .05
        points = ((70, 60, 1), (-100, 80, 2), (-80, -20, 1/3))

        dist_total = AddN()

        for pp in range(len(points)):
            p_x = Const(points[pp][0])
            p_y = Const(points[pp][1])
            p_scale = scale * points[pp][2]

            bb_normal_dist = normal_dist_func.inst("normal_dist_func")

            bb_normal_dist.conn_to_prev_block(p, 0, 0)
            bb_normal_dist.conn_to_prev_block(p, 1, 1)
            bb_normal_dist.conn_to_prev_block(p_x, 0, 2)
            bb_normal_dist.conn_to_prev_block(p_y, 0, 3)
            bb_normal_dist.conn_to_prev_block(Const(p_scale), 0, 4)

            dist_total.conn_to_prev_block(bb_normal_dist, 0, None)
        # end for

        d.conn_to_prev_block(dist_total, 0, 0)

    elif test == 24:
        # Build a rotation matrix black box and multiply the current position with it.
        fn_mat_rot = "mat_rot.cmb"

        store_and_load = False

        if not store_and_load:
            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            mat_rot = BlackBoxFactory()

            mul_11 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_MUL))
            mul_12 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_MUL))
            mul_21 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_MUL))
            mul_22 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_MUL))

            cos_11 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_COS))
            sin_12 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_SIN))
            sin_21 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_SIN))
            cos_22 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_COS))

            sub_11_12 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_SUB))
            add_21_22 = mat_rot.add_block(btf.get_block_template(BlockType.MATH_ADD))

            # Interconnect the blocks of the box
            mat_rot.add_conn(ConnTemplate(cos_11.id, 0, mul_11.id, None))
            mat_rot.add_conn(ConnTemplate(sin_12.id, 0, mul_12.id, None))
            mat_rot.add_conn(ConnTemplate(sin_21.id, 0, mul_21.id, None))
            mat_rot.add_conn(ConnTemplate(cos_22.id, 0, mul_22.id, None))

            mat_rot.add_conn(ConnTemplate(mul_11.id, 0, sub_11_12.id, 0))
            mat_rot.add_conn(ConnTemplate(mul_12.id, 0, sub_11_12.id, 1))

            mat_rot.add_conn(ConnTemplate(mul_21.id, 0, add_21_22.id, None))
            mat_rot.add_conn(ConnTemplate(mul_22.id, 0, add_21_22.id, None))

            # Bond the block of the box to the box pins
            mat_rot.add_bond(BondTemplate(BoxSide.IN, mul_11.id, None, 0))
            mat_rot.add_bond(BondTemplate(BoxSide.IN, mul_21.id, None, 0))
            mat_rot.add_bond(BondTemplate(BoxSide.IN, mul_12.id, None, 1))
            mat_rot.add_bond(BondTemplate(BoxSide.IN, mul_22.id, None, 1))
            mat_rot.add_bond(BondTemplate(BoxSide.IN, cos_11.id, 0, 2))
            mat_rot.add_bond(BondTemplate(BoxSide.IN, sin_12.id, 0, 2))
            mat_rot.add_bond(BondTemplate(BoxSide.IN, sin_21.id, 0, 2))
            mat_rot.add_bond(BondTemplate(BoxSide.IN, cos_22.id, 0, 2))

            mat_rot.add_bond(BondTemplate(BoxSide.OUT, sub_11_12.id, 0, 0))
            mat_rot.add_bond(BondTemplate(BoxSide.OUT, add_21_22.id, 0, 1))

            mat_rot.store(fn_mat_rot)

        else:
            mat_rot: BlackBoxFactory = BlackBoxFactory()
            mat_rot.load(fn_mat_rot)
        # end if

        # --

        subtest = 0  # Select experiment

        scale = 5.
        bb_mat_rot = mat_rot.inst("rotation_matrix")

        if subtest == 0:
            fn_dist = "dist"  # From previous step
            bm.scan_dir()
            dist_func = bm.load(fn_dist)
            bb_dist = dist_func.inst("dist_func")

            bb_dist.conn_to_prev_block(p, 0, 0)
            bb_dist.conn_to_prev_block(p, 1, 1)
            bb_dist.conn_to_prev_block(Const(0), 0, 2)
            bb_dist.conn_to_prev_block(Const(0), 0, 3)
            bb_dist.conn_to_prev_block(Const(scale), 0, 4)

            bb_mat_rot.conn_to_prev_block(p, 0, 0)
            bb_mat_rot.conn_to_prev_block(p, 1, 1)
            bb_mat_rot.conn_to_prev_block(bb_dist, 0, 2)

        else:
            psx = MulN()
            psx.conn_to_prev_block(Const(scale))
            psx.conn_to_prev_block(p, 0)
            psy = MulN()
            psy.conn_to_prev_block(Const(scale))
            psy.conn_to_prev_block(p, 1)

            bb_mat_rot.conn_to_prev_block(psx, 0, 0)
            bb_mat_rot.conn_to_prev_block(psy, 0, 1)
            # Fixed rotation angle:
            # bb_mat_rot.conn_to_prev_block(Const(5), 0, 2)
            # Crazy result with dynamic rotation angle
            bb_mat_rot.conn_to_prev_block(psx, 0, 2)
        # end if

        d.conn_to_prev_block(bb_mat_rot, 1, 0)

    elif test == 25:
        store_and_load = True

        # Test using a repeat box to square a number n times
        fn_square_n_times = "square_n_times"

        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        square_n_times = RepeatBoxFactory()

        sq_nx = square_n_times.add_block(btf.get_block_template(BlockType.MATH_SQ))

        # Interconnect the blocks of the box
        # -> Nothing to connect

        # Bond the block of the box to the box pins
        square_n_times.add_bond(BondTemplate(BoxSide.IN, sq_nx.id, 0, 0))
        square_n_times.add_bond(BondTemplate.empty())
        square_n_times.add_bond(BondTemplate(BoxSide.OUT, sq_nx.id, 0, 0))

        if store_and_load:
            bm.store(square_n_times, fn_square_n_times, overwrite=True)
            bm.scan_dir()
            square_n_times = bm.load(fn_square_n_times)
        # end if

        # --
        if square_n_times is not None:
            square_n_times_func = square_n_times.inst("square_n_times")
            square_n_times_func.conn_to_prev_block(p, 0, 0)
            square_n_times_func.conn_to_prev_block(Const(3), 0, 1)

            d.conn_to_prev_block(square_n_times_func, 0, 0)
        else:
            draw = False
        # end if

    elif test == 26:
        draw = False

        # Create and store multiple blocks
        def create_cart2pol():
            name = "cart2pol"

            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            func = BlackBoxFactory()
            func.add_desc("Transforms cartesian coordinates [degree] to polar coordinates.\n"
                          "\n"
                          "IN pins:\n"
                          "* [0] X-coordinate.\n"
                          "* [1] XY-coordinate.\n"
                          "\n"
                          "OUT pins:\n"
                          "* [0] Radius.\n"
                          "* [1] Theta (angle) [degree].")

            x_sq = func.add_block(btf.get_block_template(BlockType.MATH_SQ, name="x_sq"))
            y_sq = func.add_block(btf.get_block_template(BlockType.MATH_SQ, name="y_sq"))
            sum_xy_sq = func.add_block(btf.get_block_template(BlockType.MATH_ADD, name="sum_xy_sq"))
            r = func.add_block(btf.get_block_template(BlockType.MATH_SQRT, name="r"))

            theta = func.add_block(btf.get_block_template(BlockType.MATH_ATAN2, name="theta"))

            # Interconnect the blocks of the box
            func.add_conn(ConnTemplate(x_sq.id, 0, sum_xy_sq.id, None))
            func.add_conn(ConnTemplate(y_sq.id, 0, sum_xy_sq.id, None))
            func.add_conn(ConnTemplate(sum_xy_sq.id, 0, r.id, 0))

            # Bond the block of the box to the box pins
            func.add_bond(BondTemplate(BoxSide.IN, x_sq.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.IN, y_sq.id, 0, 1))
            func.add_bond(BondTemplate(BoxSide.OUT, r.id, 0, 0))

            func.add_bond(BondTemplate(BoxSide.IN, theta.id, 1, 0))
            func.add_bond(BondTemplate(BoxSide.IN, theta.id, 0, 1))
            func.add_bond(BondTemplate(BoxSide.OUT, theta.id, 0, 1))

            bm.store(func, name, overwrite=True)
        # end def

        def create_dist_euclidean_scaled():
            name = "dist_euclidean_scaled"

            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            func = BlackBoxFactory()
            func.add_desc("Calculates the euclidean distance between two points, scaled by a factor.\n"
                          "\n"
                          "IN pins:\n"
                          "* [0] X-coordinate of point A.\n"
                          "* [1] Y-coordinate of point A.\n"
                          "* [2] X-coordinate of point B.\n"
                          "* [3] Y-coordinate of point B.\n"
                          "* [4] Scaling factor.\n"
                          "\n"
                          "OUT pins:\n"
                          "* [0] Distance.\n")

            diff_x = func.add_block(btf.get_block_template(BlockType.MATH_SUB, name="diff_x"))
            diff_y = func.add_block(btf.get_block_template(BlockType.MATH_SUB, name="diff_y"))
            diff_x_sq = func.add_block(btf.get_block_template(BlockType.MATH_SQ, name="diff_x_sq"))
            diff_y_sq = func.add_block(btf.get_block_template(BlockType.MATH_SQ, name="diff_y_sq"))
            add_xy_sq = func.add_block(btf.get_block_template(BlockType.MATH_ADD, name="add_xy_sq"))
            dist = func.add_block(btf.get_block_template(BlockType.MATH_SQRT, name="dist"))
            dist_rescaled = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="dist_rescaled"))

            # Interconnect the blocks of the box
            func.add_conn(ConnTemplate(diff_x.id, 0, diff_x_sq.id, 0))
            func.add_conn(ConnTemplate(diff_y.id, 0, diff_y_sq.id, 0))
            func.add_conn(ConnTemplate(diff_x_sq.id, 0, add_xy_sq.id, None))
            func.add_conn(ConnTemplate(diff_y_sq.id, 0, add_xy_sq.id, None))
            func.add_conn(ConnTemplate(add_xy_sq.id, 0, dist.id, 0))
            func.add_conn(ConnTemplate(dist.id, 0, dist_rescaled.id, None))

            # Bond the block of the box to the box pins
            func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 0, 1))
            func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 1, 2))
            func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 1, 3))
            func.add_bond(BondTemplate(BoxSide.IN, dist_rescaled.id, None, 4))
            func.add_bond(BondTemplate(BoxSide.OUT, dist_rescaled.id, 0, 0))

            bm.store(func, name, overwrite=True)
        # end def

        # normal distribution
        def create_normal_standard_pdf():
            name = "normal_standard_pdf"

            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            func = BlackBoxFactory()
            func.add_desc("Calculates (normalized) the standard normal distribution pdf of the given value x.\n"
                          "\n"
                          "IN pin:\n"
                          "* [0] Value x.\n"
                          "\n"
                          "OUT pin:\n"
                          "* [0] PDF value at position x.")

            norm_const_2 = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 2., name="norm_const_2"))
            norm_const_pi = func.add_block(btf.get_block_template(BlockType.VAL_CONST_PI, name="norm_const_pi"))
            norm = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="norm"))
            norm_inv = func.add_block(btf.get_block_template(BlockType.MATH_INV, name="norm_inv"))

            exp_term_fac = func.add_block(btf.get_block_template(BlockType.VAL_CONST, -.5, name="exp_term_fac"))
            exp_term_x_sq = func.add_block(btf.get_block_template(BlockType.MATH_SQ, name="exp_term_x_sq"))
            exp_term = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="exp_term"))
            exp = func.add_block(btf.get_block_template(BlockType.MATH_EXP, name="exp"))

            normal = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="normal"))

            # Interconnect the blocks of the box
            func.add_conn(ConnTemplate(norm_const_2.id, 0, norm.id, None))
            func.add_conn(ConnTemplate(norm_const_pi.id, 0, norm.id, None))
            func.add_conn(ConnTemplate(norm.id, 0, norm_inv.id, 0))

            func.add_conn(ConnTemplate(exp_term_fac.id, 0, exp_term.id, None))
            func.add_conn(ConnTemplate(exp_term_x_sq.id, 0, exp_term.id, None))
            func.add_conn(ConnTemplate(exp_term.id, 0, exp.id, 0))

            func.add_conn(ConnTemplate(norm_inv.id, 0, normal.id, None))
            func.add_conn(ConnTemplate(exp.id, 0, normal.id, None))

            # Bond the block of the box to the box pins
            func.add_bond(BondTemplate(BoxSide.IN, exp_term_x_sq.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.OUT, exp.id, 0, 0))

            bm.store(func, name, overwrite=True)
        # end def

        # Rotation matrix
        def create_mat_rot():
            name = "mat_rot"

            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            func = BlackBoxFactory()
            func.add_desc("Performs a matrix multiplication of this rotation matrix (R[theta]) with a given vector (x) and the rotation angle theta [degree]: R×x.\n"
                          "\n"
                          "IN pins:\n"
                          "* [0] X-coordinate of point.\n"
                          "* [1] Y-coordinate of point.\n"
                          "* [2] Angle theta for the rotation matrix R.\n"
                          "\n"
                          "OUT pins:\n"
                          "* [0] X-coordinate of the rotated point.\n"
                          "* [1] Y-coordinate of the rotated point.")

            mul_11 = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_11"))
            mul_12 = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_12"))
            mul_21 = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_21"))
            mul_22 = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_22"))

            cos_11 = func.add_block(btf.get_block_template(BlockType.MATH_COS, name="cos_11"))
            sin_12 = func.add_block(btf.get_block_template(BlockType.MATH_SIN, name="sin_12"))
            sin_21 = func.add_block(btf.get_block_template(BlockType.MATH_SIN, name="sin_21"))
            cos_22 = func.add_block(btf.get_block_template(BlockType.MATH_COS, name="cos_22"))

            sub_11_12 = func.add_block(btf.get_block_template(BlockType.MATH_SUB, name="sub_11_12"))
            add_21_22 = func.add_block(btf.get_block_template(BlockType.MATH_ADD, name="add_21_22"))

            # Interconnect the blocks of the box
            func.add_conn(ConnTemplate(cos_11.id, 0, mul_11.id, None))
            func.add_conn(ConnTemplate(sin_12.id, 0, mul_12.id, None))
            func.add_conn(ConnTemplate(sin_21.id, 0, mul_21.id, None))
            func.add_conn(ConnTemplate(cos_22.id, 0, mul_22.id, None))

            func.add_conn(ConnTemplate(mul_11.id, 0, sub_11_12.id, 0))
            func.add_conn(ConnTemplate(mul_12.id, 0, sub_11_12.id, 1))

            func.add_conn(ConnTemplate(mul_21.id, 0, add_21_22.id, None))
            func.add_conn(ConnTemplate(mul_22.id, 0, add_21_22.id, None))

            # Bond the block of the box to the box pins
            func.add_bond(BondTemplate(BoxSide.IN, mul_11.id, None, 0))
            func.add_bond(BondTemplate(BoxSide.IN, mul_21.id, None, 0))
            func.add_bond(BondTemplate(BoxSide.IN, mul_12.id, None, 1))
            func.add_bond(BondTemplate(BoxSide.IN, mul_22.id, None, 1))
            func.add_bond(BondTemplate(BoxSide.IN, cos_11.id, 0, 2))
            func.add_bond(BondTemplate(BoxSide.IN, sin_12.id, 0, 2))
            func.add_bond(BondTemplate(BoxSide.IN, sin_21.id, 0, 2))
            func.add_bond(BondTemplate(BoxSide.IN, cos_22.id, 0, 2))

            func.add_bond(BondTemplate(BoxSide.OUT, sub_11_12.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.OUT, add_21_22.id, 0, 1))

            bm.store(func, name, overwrite=True)
        # end def

        def create_if_else():
            name = "if_else"

            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            func = BlackBoxFactory()
            func.add_desc("Returns either one or the other values, depending on a indicator value.\n"
                          "\n"
                          "IN pins:\n"
                          "* [0] Indicator value. If value is exactly 1, it's interpreted as the condition is fulfilled.\n"
                          "* [1] IF-Value for output if condition is fulfilled.\n"
                          "* [2] ELSE-Value for output if condition is not fulfilled.\n"
                          "\n"
                          "OUT pins:\n"
                          "* [0] Value from either IF or ELSE pin, depending on the indicator value.\n")

            not_1 = func.add_block(btf.get_block_template(BlockType.BOOL_NOT, name="not_1"))
            not_2 = func.add_block(btf.get_block_template(BlockType.BOOL_NOT, name="not_2"))
            mul_if = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_if"))
            mul_else = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_else"))
            res = func.add_block(btf.get_block_template(BlockType.MATH_ADD, name="mul_else"))

            # Interconnect the blocks of the box
            func.add_conn(ConnTemplate(not_1.id, 0, not_2.id, 0))
            func.add_conn(ConnTemplate(not_1.id, 0, mul_else.id, None))
            func.add_conn(ConnTemplate(not_2.id, 0, mul_if.id, None))
            func.add_conn(ConnTemplate(mul_if.id, 0, res.id, None))
            func.add_conn(ConnTemplate(mul_else.id, 0, res.id, None))

            # Bond the block of the box to the box pins
            func.add_bond(BondTemplate(BoxSide.IN, not_1.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.IN, mul_if.id, None, 1))
            func.add_bond(BondTemplate(BoxSide.IN, mul_else.id, None, 2))
            func.add_bond(BondTemplate(BoxSide.OUT, res.id, 0, 0))

            bm.store(func, name, overwrite=True)
        # end def
        #
        # def create_complex_abs():
        #     name = "complex_abs"
        #
        #     idg: IdGenerator = IdGenerator()
        #
        #     btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        #     func = BlackBoxFactory()
        #     func.add_desc("Returns either one or the other values, depending on a indicator value.\n"
        #                   "\n"
        #                   "IN pins:\n"
        #                   "* [0] Indicator value. If value is exactly 1, it's interpreted as the condition is fulfilled.\n"
        #                   "* [1] IF-Value for output if condition is fulfilled.\n"
        #                   "* [2] ELSE-Value for output if condition is not fulfilled.\n"
        #                   "\n"
        #                   "OUT pins:\n"
        #                   "* [0] Value from either IF or ELSE pin, depending on the indicator value.\n")
        #
        #     not_1 = func.add_block(btf.get_block_template(BlockType.BOOL_NOT, name="not_1"))
        #     not_2 = func.add_block(btf.get_block_template(BlockType.BOOL_NOT, name="not_1"))
        #     mul_if = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_if"))
        #     mul_else = func.add_block(btf.get_block_template(BlockType.MATH_MUL, name="mul_else"))
        #     res = func.add_block(btf.get_block_template(BlockType.MATH_ADD, name="mul_else"))
        #
        #     # Interconnect the blocks of the box
        #     func.add_conn(ConnTemplate(not_1.id, 0, mul_else.id, None))
        #     func.add_conn(ConnTemplate(not_2.id, 0, mul_if.id, None))
        #     func.add_conn(ConnTemplate(mul_if.id, 0, res.id, None))
        #     func.add_conn(ConnTemplate(mul_else.id, 0, res.id, None))
        #
        #     # Bond the block of the box to the box pins
        #     func.add_bond(BondTemplate(BoxSide.IN, not_1.id, 0, 0))
        #     func.add_bond(BondTemplate(BoxSide.IN, mul_if.id, None, 1))
        #     func.add_bond(BondTemplate(BoxSide.IN, mul_else.id, None, 2))
        #     func.add_bond(BondTemplate(BoxSide.OUT, res.id, 0, 0))
        #
        #     bm.store(func, name, overwrite=True)
        # # end def

        create_cart2pol()
        create_dist_euclidean_scaled()
        create_normal_standard_pdf()
        create_mat_rot()
        create_if_else()

    elif test == 27:
        # Test cart2pol box
        bm.scan_dir()
        cart2pol = bm.load("cart2pol")

        if cart2pol is not None:
            cart2pol_func = cart2pol.inst("cart2pol1")
            cart2pol_func.conn_to_prev_block(p, 0, 0)
            cart2pol_func.conn_to_prev_block(p, 1, 1)
            mul = MulN()
            mul.conn_to_prev_block(cart2pol_func, 0, None)
            mul.conn_to_prev_block(cart2pol_func, 1, None)

            d.conn_to_prev_block(mul, 0, 0)
        else:
            draw = False
        # end if

    elif test == 28:
        # Test normal_standard_pdf box
        bm.scan_dir()
        normal_standard_pdf = bm.load("normal_standard_pdf")

        if normal_standard_pdf is not None:
            normal_standard_pdf_x = normal_standard_pdf.inst(name="normal_standard_pdf_x")
            normal_standard_pdf_y = normal_standard_pdf.inst(name="normal_standard_pdf_y")

            scale = Const(.01)
            p_x_scaled = MulN()
            p_x_scaled.conn_to_prev_block(scale, 0, None)
            p_x_scaled.conn_to_prev_block(p, 0, None)

            p_y_scaled = MulN()
            p_y_scaled.conn_to_prev_block(scale, 0, None)
            p_y_scaled.conn_to_prev_block(p, 1, None)

            normal_standard_pdf_x.conn_to_prev_block(p_x_scaled, 0, 0)
            normal_standard_pdf_y.conn_to_prev_block(p_y_scaled, 0, 0)

            pdf = MulN()
            pdf.conn_to_prev_block(normal_standard_pdf_x, 0, None)
            pdf.conn_to_prev_block(normal_standard_pdf_y, 0, None)

            d.conn_to_prev_block(pdf, 0, 0)
        else:
            draw = False
        # end if

    elif test == 29:
        def create_mandelbrot_inner():
            name = "mandelbrot_inner"

            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            func = RepeatBoxFactory()
            func.add_desc("Does the inner loop of the mandelbrot calculation for a given point on the complex plane defined by c0.\n"
                          "\n"
                          "IN pins:\n"
                          "* [0] c0: Real part of the input point on the complex plane.\n"
                          "* [1] c0: Imaginary part of the input point on the complex plane.\n"
                          "* [2] c: Real part of the continuously updated value within this box.\n"
                          "* [3] c: Imaginary part of the continuously updated value within this box.\n"
                          "* [4] i: Counter variable.\n"
                          "* [5] res: Resulting mandelbrot-value for the given point.\n"
                          "* [6] n_rep Number of repetitions.\n"
                          "\n"
                          "OUT pins:\n"
                          "* [0] c0: See input. (Needed for repetition only).\n"
                          "* [1] c0: See input. (Needed for repetition only).\n"
                          "* [2] c: See input. (Needed for repetition only).\n"
                          "* [3] c: See input. (Needed for repetition only).\n"
                          "* [4] i: See input. (Needed for repetition only).\n"
                          "* [5] res: See input. (Needed for repetition also).\n")

            # c0
            c0_real = func.add_block(btf.get_block_template(BlockType.VAL_VAR, name="c0_real"))
            c0_imag = func.add_block(btf.get_block_template(BlockType.VAL_VAR, name="c0_imag"))

            # CABS(c)
            abs_helper_const_real = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 0., name="abs_helper_const_real"))
            abs_helper_const_imag = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 0., name="abs_helper_const_imag"))
            abs_helper_const_scale = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 1., name="abs_helper_const_scale"))

            # -> Yes, abs(c) is just the same as the euclidean distance of a point to the origin
            abs_c = func.add_block(btf.get_block_template(BlockType.BOX, box_name=bm.get_filename_from_name("dist_euclidean_scaled"), name="abs_c"))

            # CABS(c) >= 2 - and its NOT-version
            border_const = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 2., name="border_const"))

            abs_c_gt_2 = func.add_block(btf.get_block_template(BlockType.BOOL_GT, name="abs_c_gt_2"))
            abs_c_not_gt_2 = func.add_block(btf.get_block_template(BlockType.BOOL_NOT, name="abs_c_not_gt_2"))

            # res == 0
            res_eq_0_helper_const = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 0., name="res_eq_0_helper_const"))
            res_eq_0 = func.add_block(btf.get_block_template(BlockType.BOOL_EQ, name="res_eq_0"))

            # c = c * c + c0
            c_sq = func.add_block(btf.get_block_template(BlockType.COMPLEX_MUL, name="c_sq"))
            c_sq_plus_c0 = func.add_block(btf.get_block_template(BlockType.COMPLEX_ADD, name="c_sq_plus_c0"))

            # res == 0 and CABS(c) >= 2
            res_eq_0_and_abs_c_gt_2 = func.add_block(btf.get_block_template(BlockType.BOOL_AND, name="res_eq_0_and_abs_c_gt_2"))

            # res == 0 and not CABS(c) >= 2
            res_eq_0_and_abs_c_not_gt_2 = func.add_block(btf.get_block_template(BlockType.BOOL_AND, name="res_eq_0_and_abs_c_not_gt_2"))

            # if res == 0 and not CABS(c) >= 2 then c = c * c + c0 [else c = c]
            if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_real = func.add_block(btf.get_block_template(BlockType.BOX, box_name=bm.get_filename_from_name("if_else"), name="if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_real"))
            if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_imag = func.add_block(btf.get_block_template(BlockType.BOX, box_name=bm.get_filename_from_name("if_else"), name="if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_imag"))

            # if res == 0 and CABS(c) >= 2 then res = i [else res = res]
            if_res_eq_0_and_abs_c_gt_2_then_i_else_res = func.add_block(btf.get_block_template(BlockType.BOX, box_name=bm.get_filename_from_name("if_else"), name="if_res_eq_0_and_abs_c_gt_2_then_i_else_res"))

            # i = i + 1
            i_plus_1_helper_const = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 1., name="i_plus_1_helper_const"))
            i_plus_1 = func.add_block(btf.get_block_template(BlockType.MATH_ADD, name="i_plus_1"))

            # Interconnect the blocks of the box
            # abs(c)
            func.add_conn(ConnTemplate(abs_helper_const_real.id, 0, abs_c.id, 2))
            func.add_conn(ConnTemplate(abs_helper_const_imag.id, 0, abs_c.id, 3))
            func.add_conn(ConnTemplate(abs_helper_const_scale.id, 0, abs_c.id, 4))

            # CABS(c) >= 2 - and its NOT-version
            func.add_conn(ConnTemplate(abs_c.id, 0, abs_c_gt_2.id, 0))
            func.add_conn(ConnTemplate(border_const.id, 0, abs_c_gt_2.id, 1))

            func.add_conn(ConnTemplate(abs_c_gt_2.id, 0, abs_c_not_gt_2.id, 0))

            # res == 0
            func.add_conn(ConnTemplate(res_eq_0_helper_const.id, 0, res_eq_0.id, None))

            # c = c * c + c0
            func.add_conn(ConnTemplate(c_sq.id, 0, c_sq_plus_c0.id, None))
            func.add_conn(ConnTemplate(c_sq.id, 1, c_sq_plus_c0.id, None))
            func.add_conn(ConnTemplate(c0_real.id, 0, c_sq_plus_c0.id, None))
            func.add_conn(ConnTemplate(c0_imag.id, 0, c_sq_plus_c0.id, None))

            # res == 0 and CABS(c) >= 2
            func.add_conn(ConnTemplate(res_eq_0.id, 0, res_eq_0_and_abs_c_gt_2.id, None))
            func.add_conn(ConnTemplate(abs_c_gt_2.id, 0, res_eq_0_and_abs_c_gt_2.id, None))

            # res == 0 and not CABS(c) >= 2
            func.add_conn(ConnTemplate(res_eq_0.id, 0, res_eq_0_and_abs_c_not_gt_2.id, None))
            func.add_conn(ConnTemplate(abs_c_not_gt_2.id, 0, res_eq_0_and_abs_c_not_gt_2.id, None))

            # if res == 0 and not CABS(c) >= 2 then c = c * c + c0 [else c = c]
            func.add_conn(ConnTemplate(res_eq_0_and_abs_c_not_gt_2.id, 0, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_real.id, 0))
            func.add_conn(ConnTemplate(c_sq_plus_c0.id, 0, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_real.id, 1))

            func.add_conn(ConnTemplate(res_eq_0_and_abs_c_not_gt_2.id, 0, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_imag.id, 0))
            func.add_conn(ConnTemplate(c_sq_plus_c0.id, 1, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_imag.id, 1))

            # if res == 0 and CABS(c) >= 2 then res = i [else res = res]
            func.add_conn(ConnTemplate(res_eq_0_and_abs_c_gt_2.id, 0, if_res_eq_0_and_abs_c_gt_2_then_i_else_res.id, 0))

            # i = i + 1
            func.add_conn(ConnTemplate(i_plus_1_helper_const.id, 0, i_plus_1.id, None))

            # Bond the block of the box to the box pins
            func.add_bond(BondTemplate(BoxSide.IN, c0_real.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.IN, c0_imag.id, 0, 1))
            func.add_bond(BondTemplate(BoxSide.IN, abs_c.id, 0, 2))
            func.add_bond(BondTemplate(BoxSide.IN, abs_c.id, 1, 3))
            func.add_bond(BondTemplate(BoxSide.IN, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_real.id, 2, 2))
            func.add_bond(BondTemplate(BoxSide.IN, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_imag.id, 2, 3))
            func.add_bond(BondTemplate(BoxSide.IN, c_sq.id, None, 2))
            func.add_bond(BondTemplate(BoxSide.IN, c_sq.id, None, 3))
            func.add_bond(BondTemplate(BoxSide.IN, c_sq.id, None, 2))
            func.add_bond(BondTemplate(BoxSide.IN, c_sq.id, None, 3))
            func.add_bond(BondTemplate(BoxSide.IN, i_plus_1.id, None, 4))
            func.add_bond(BondTemplate(BoxSide.IN, res_eq_0.id, None, 5))
            func.add_bond(BondTemplate(BoxSide.IN, if_res_eq_0_and_abs_c_gt_2_then_i_else_res.id, 1, 4))
            func.add_bond(BondTemplate(BoxSide.IN, if_res_eq_0_and_abs_c_gt_2_then_i_else_res.id, 2, 5))
            func.add_bond(BondTemplate.empty())

            func.add_bond(BondTemplate(BoxSide.OUT, c0_real.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.OUT, c0_imag.id, 0, 1))
            func.add_bond(BondTemplate(BoxSide.OUT, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_real.id, 0, 2))
            func.add_bond(BondTemplate(BoxSide.OUT, if_res_eq_0_and_abs_c_not_gt_2_then_c_sq_plus_c0_else_c_imag.id, 0, 3))
            func.add_bond(BondTemplate(BoxSide.OUT, i_plus_1.id, 0, 4))
            func.add_bond(BondTemplate(BoxSide.OUT, if_res_eq_0_and_abs_c_gt_2_then_i_else_res.id, 0, 5))

            bm.store(func, name, overwrite=False)
        # end def

        def create_mandelbrot():
            name = "mandelbrot"

            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            func = BlackBoxFactory()
            func.add_desc("Calculates the mandelbrot value for a given point on the complex plane defined by c0.\n"
                          "\n"
                          "IN pins:\n"
                          "* [0] c0: Real part of the input point on the complex plane.\n"
                          "* [1] c0: Imaginary part of the input point on the complex plane.\n"
                          "* [2] n_rep Number of repetitions.\n"
                          "\n"
                          "OUT pins:\n"
                          "* [0] res: The resulting mandelbrot value for the given point.\n")

            c_real = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 0., name="c_real"))
            c_imag = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 0., name="c_imag"))
            ii = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 1., name="i"))
            res = func.add_block(btf.get_block_template(BlockType.VAL_CONST, 0., name="res"))
            mandelbrot_inner = func.add_block(btf.get_block_template(BlockType.BOX, box_name=bm.get_filename_from_name("mandelbrot_inner"), name="mandelbrot_inner"))

            #xxx = func.add_block(btf.get_block_template(BlockType.VAL_VAR, name="xxx"))

            # Interconnect the blocks of the box
            func.add_conn(ConnTemplate(c_real.id, 0, mandelbrot_inner.id, 2))
            func.add_conn(ConnTemplate(c_imag.id, 0, mandelbrot_inner.id, 3))
            func.add_conn(ConnTemplate(ii.id, 0, mandelbrot_inner.id, 4))
            func.add_conn(ConnTemplate(res.id, 0, mandelbrot_inner.id, 5))
            #func.add_conn(ConnTemplate(xxx.id, 0, mandelbrot_inner.id, 6))

            # Bond the block of the box to the box pins
            func.add_bond(BondTemplate(BoxSide.IN, mandelbrot_inner.id, 0, 0))
            func.add_bond(BondTemplate(BoxSide.IN, mandelbrot_inner.id, 1, 1))
            func.add_bond(BondTemplate(BoxSide.IN, mandelbrot_inner.id, 6, 2))
            #func.add_bond(BondTemplate(BoxSide.IN, xxx.id, 0, 2))
            func.add_bond(BondTemplate(BoxSide.OUT, mandelbrot_inner.id, 4, 0))  # 5, 0))  # XXX For test on how many iterations are made before inspecting the mandelbrot values

            bm.store(func, name, overwrite=True)
        # end def

        create_mandelbrot_inner()
        create_mandelbrot()

        bm.scan_dir()
        mandelbrot_inner = bm.load("mandelbrot_inner")
        mandelbrot = bm.load("mandelbrot")

        # --

        scale = Const(1. / 5)
        p_x_scaled = MulN()
        p_x_scaled.conn_to_prev_block(scale, 0, None)
        p_x_scaled.conn_to_prev_block(p, 0, None)
        p_y_scaled = MulN()
        p_y_scaled.conn_to_prev_block(scale, 0, None)
        p_y_scaled.conn_to_prev_block(p, 1, None)

        test_inner = True#False#True

        if test_inner:
            if mandelbrot_inner is not None:
                mandelbrot_inner_func = mandelbrot_inner.inst("mandelbrot_inner")

                mandelbrot_inner_func.conn_to_prev_block(p_x_scaled, 0, 0)
                mandelbrot_inner_func.conn_to_prev_block(p_y_scaled, 0, 1)
                mandelbrot_inner_func.conn_to_prev_block(Const(0), 0, 2)
                mandelbrot_inner_func.conn_to_prev_block(Const(0), 0, 3)
                mandelbrot_inner_func.conn_to_prev_block(Const(1), 0, 4)
                mandelbrot_inner_func.conn_to_prev_block(Const(0), 0, 5)
                mandelbrot_inner_func.conn_to_prev_block(Const(10), 0, 6)

                d.conn_to_prev_block(mandelbrot_inner_func, 5, 0)
            else:
                draw = False
            # end if
        else:
            if mandelbrot is not None:
                mandelbrot_func = mandelbrot.inst("mandelbrot")

                mandelbrot_func.conn_to_prev_block(p_x_scaled, 0, 0)
                mandelbrot_func.conn_to_prev_block(p_y_scaled, 0, 1)
                mandelbrot_func.conn_to_prev_block(Const(10), 0, 2)

                d.conn_to_prev_block(mandelbrot_func, 0, 0)

                # XXX
                # Doesn't work. Findings so far: in the RepeatBox doesn't happen any repetition... how is this possible?
                # Do I have to build in something after the RepeatBox, that "pulls" on the output pins because they might even not get calculated if no one asks for their values - in this case the example above won't work with mandelbrot_inner, too
                # Might it be linked to the fact that I have multiple output values and the settings of values_calculated doesn't work properly?
            else:
                draw = False
            # end if
        # end if

        width = 40
        height = 20
    # end if

    if draw:
        cm = CrazyMatrix(circuit=c, width=width, height=height)

        image = cm.calc_image()
        gui = Gui()
        gui.load_test()  # Only for testing (example)
        gui.show_image(image)  # Will later get called from within the gui
        gui.run()
    # end if
# end def


if __name__ == "__main__":
    main(sys.argv)
# end if
