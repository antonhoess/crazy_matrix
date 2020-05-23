import sys

from base.basic import Point
from base.black_box import BlackBox, RepeatBox
from blocks.bool import *
from blocks.math import *
from blocks.const_var import *
from blocks.deprecated import *
from crazy_matrix import CrazyMatrix
from templates.block import IdGenerator, BlockTemplateFactory
from templates.circuit import *
from templates.box import *
from templates.bond import *
from base.block import Conn


def main(_argv: List[str]):
    c = Circuit()

    p = c.point
    d = c.drawer

    test = 25

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

            dists.add_conn_to_prev_block(gravity)
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
        out_filename = "test01.cmc"
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

        cf.store(out_filename)

        # Check, if storing and loading really works
        if True:
            cf: CircuitFactory = CircuitFactory()
            cf.load(out_filename)
        # end if

        c = cf.inst()

        cm = CrazyMatrix(c)

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
        # Definces, stores and loads a black box
        out_filename = "test01.cmb"  # cmb = crazy matrix (black) box
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

        my_func.store(out_filename)

        if True:
            my_func: BlackBoxFactory = BlackBoxFactory()
            my_func.load(out_filename)
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
        bb_normal1 = normal_func.inst( "normal_func")

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

        store_and_load = True
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

            dist = normal_dist_func.add_block(btf.get_block_template(BlockType.BOX, "dist.cmb"))
            normal = normal_dist_func.add_block(btf.get_block_template(BlockType.BOX, "normal.cmb"))

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
        # Added distance of three points using a black box consisting of two other black boxes
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

        test = 1  # Select experiment

        scale = 5.
        bb_mat_rot = mat_rot.inst("rotation_matrix")

        if test == 0:
            fn_dist = "dist.cmb"  # From previous step
            dist_func: BlackBoxFactory = BlackBoxFactory()
            dist_func.load(fn_dist)
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
        # Test using a repeat box to square a number n times
        fn_square_n_times = "square_n_times.cmr"

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

        square_n_times.store(fn_square_n_times)

        if True:
            square_n_times: RepeatBoxFactory = RepeatBoxFactory()
            square_n_times.load(fn_square_n_times)
        # end if

        # --
        square_n_times_func = square_n_times.inst("square_n_times")
        square_n_times_func.conn_to_prev_block(p, 0, 0)
        square_n_times_func.conn_to_prev_block(Const(3), 0, 1)

        d.conn_to_prev_block(square_n_times_func, 0, 0)
    # end if

    cm = CrazyMatrix(c)

    cm.plot()
# end def


if __name__ == "__main__":
    main(sys.argv)
