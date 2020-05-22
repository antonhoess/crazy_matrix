import sys

from base.basic import Point
from base.black_box import BlackBox, RepeatBox
from blocks.bool import *
from crazy_matrix import CrazyMatrix
from templates.circuit import *
from templates.box import *
from templates.bond import *


def main(_argv: List[str]):
    c = Circuit()

    p = c.point
    d = c.drawer

    test = 23

    if test == 0:
        pi = ConstUser(4.27)
        d.conn_to_prev_block(pi)

    elif test == 1:
        d.conn_to_prev_block(p, 1)

    elif test == 2:
        sin = Sin(deg=True)
        sin.conn_to_prev_block(p, 1)
        d.conn_to_prev_block(sin)

    elif test == 3:
        mul = Mul2()
        # pi = ConstPi()
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
        #mul_p.conn_to_prev_block(absx, 0, 1)
        mul_p.conn_to_prev_block(p, 1, 1)

        mul_ps = Mul2()
        mul_ps.conn_to_prev_block(cos)
        mul_ps.conn_to_prev_block(mul_p, 0, 1)

        sq = Sq()
        sq.conn_to_prev_block(mul_ps)
        d.conn_to_prev_block(sq)

    elif test == 7:
        modn = ConstUser(40)

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
        max_dist = ConstUser(100)
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
        repeat = ConstUser(5)

        # XXX Fibonacci (evtl. auch mit float anstatt int?) ist das das gleiche, nur skaliert?
        # SUM
        var1 = Variable(0)
        var2 = Variable(1)

        add = Add2()
        add.conn_to_prev_block(var1, 0, 0)
        add.conn_to_prev_block(var2, 0, 1)

        var3 = Variable()
        var3.conn_to_prev_block(add)

        var1.conn_to_prev_block(var2)
        var2.conn_to_prev_block(var3)

        d.conn_to_prev_block(var3)



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
        sxn = SquareXn(None, name="10 squared 4 times")
        #sxn.conn_to_prev_block(Const(7), 0, 0)
        sxn.conn_to_prev_block(p, 0, 0)
        sxn.conn_to_prev_block(Const(10), 0, 1)

        d.conn_to_prev_block(sxn)

    elif test == 14:
        sq = Sq()

        rb = RepeatBox(1, "SquareTimesN")

        rb.assign_conn_in(sq, 0, 0)
        rb.assign_pin_value(sq, 0, 0)

        rb.conn_to_prev_block(Const(10), 0, 0)
        rb.conn_to_prev_block(Const(2), 0, 1)  # no. rep.

        d.conn_to_prev_block(rb)

    elif test == 15:
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
        sq1 = Sq()
        sq2 = Sq()
        sq3 = Sq()

        rb = RepeatBox(3, "XXX")

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

        addn = AddN()
        #addn.add_conn_to_prev_block(xxrb, 0)
        addn.add_conn_to_prev_block(rb, 1)
        addn.add_conn_to_prev_block(rb, 2)

        #d.conn_to_prev_block(addn, 0)
        d.conn_to_prev_block(rb, 2)

    elif test == 17:
        out_filename = "test01.cmc"  # cmc = crazy matrix circuit
        idg: IdGenerator = IdGenerator()

        cf: CircuitFactory = CircuitFactory()
        btf: BlockTemplateFactory = BlockTemplateFactory(idg)

        fac: BlockTemplate = btf.get_block_template(BlockType.VAL_CONST, .3)
        cf.add_block(fac)

        mul: BlockTemplate = btf.get_block_template(BlockType.MATH_MUL)
        cf.add_block(mul)

        add: BlockTemplate = btf.get_block_template(BlockType.MATH_ADD)
        cf.add_block(add)

        # --

        cf.add_conn(ConnTemplate("0", 0, mul.id, None))

        cf.add_conn(ConnTemplate(fac.id, 0, mul.id, None))

        cf.add_conn(ConnTemplate(mul.id, 0, add.id, None))

        cf.add_conn(ConnTemplate("0", 1, add.id, None))

        cf.add_conn(ConnTemplate(add.id, 0, "1", 0))

        cf.store(out_filename)

        if True:
            cf: CircuitFactory = CircuitFactory()
            cf.load(out_filename)
        # end if

        c = cf.inst()

        cm = CrazyMatrix(c)

        cm.plot()

    elif test == 18:
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        my_add = BoxFactory()

        addn: BlockTemplate = btf.get_block_template(BlockType.MATH_ADD)
        my_add.add_block(addn)

        my_add.add_bond(BondTemplate(BoxSide.IN, addn.id, None, 0))
        my_add.add_bond(BondTemplate(BoxSide.IN, addn.id, None, 1))
        my_add.add_bond(BondTemplate(BoxSide.OUT, addn.id, None, 0))

        bb = my_add.inst(2, 1, "my_add")

        bb.conn_to_prev_block(p, 0, 0)
        bb.conn_to_prev_block(p, 1, 1)
        d.conn_to_prev_block(bb, 0, 0)

    elif test == 19:
        out_filename = "test01.cmb"  # cmb = crazy matrix (black) box
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        my_func = BoxFactory()

        fac: BlockTemplate = btf.get_block_template(BlockType.VAL_CONST, .3)
        my_func.add_block(fac)

        muln: BlockTemplate = btf.get_block_template(BlockType.MATH_MUL)
        my_func.add_block(muln)

        addn: BlockTemplate = btf.get_block_template(BlockType.MATH_ADD)
        my_func.add_block(addn)

        # Interconnect the blocks of the box
        my_func.add_conn(ConnTemplate(fac.id, 0, muln.id, None))

        my_func.add_conn(ConnTemplate(muln.id, 0, addn.id, None))

        # Bond the block of the box to the box pins
        my_func.add_bond(BondTemplate(BoxSide.IN, muln.id, None, 0))
        my_func.add_bond(BondTemplate(BoxSide.IN, addn.id, None, 1))
        my_func.add_bond(BondTemplate(BoxSide.OUT, addn.id, 0, 0))

        my_func.store(out_filename)

        if True:
            my_func: BoxFactory = BoxFactory()
            my_func.load(out_filename)
        # end if

        bb = my_func.inst(2, 1, "my_func")  # XXX sollten diese parameter nicht auch mit abgespeichert werden? diese sollte nicht mehr explizit angegeben werden müssen...

        bb.conn_to_prev_block(p, 0, 0)
        bb.conn_to_prev_block(p, 1, 1)
        d.conn_to_prev_block(bb, 0, 0)

    elif test == 20:
        # Distance function as black box
        out_filename = "dist.cmb"  # cmb = crazy matrix (black) box
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        dist_func = BoxFactory()

        # --

        diff_x = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_y = dist_func.add_block(btf.get_block_template(BlockType.MATH_SUB))
        diff_x_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQUARE))
        diff_y_sq = dist_func.add_block(btf.get_block_template(BlockType.MATH_SQUARE))
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
            dist_func: BoxFactory = BoxFactory()
            dist_func.load(out_filename)
        # end if

        bb = dist_func.inst(5, 1, "dist_func")

        my_p_x = ConstUser(-130)
        my_p_y = ConstUser(80)
        rescale_factor = ConstUser(10.)
        bb.conn_to_prev_block(p, 0, 0)
        bb.conn_to_prev_block(p, 1, 1)
        bb.conn_to_prev_block(my_p_x, 0, 2)
        bb.conn_to_prev_block(my_p_y, 0, 3)
        bb.conn_to_prev_block(rescale_factor, 0, 4)

        d.conn_to_prev_block(bb, 0, 0)

    elif test == 21:
        # Test in multiple instances of a black box
        out_filename = "dist.cmb"  # cmb = crazy matrix (black) box
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        dist_func = BoxFactory()

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
        #XXX anstatt hier über x.id zu verwenden, kann ich nciht die .id in ConnTemplate direkt aufrufen und es mitr hier immer ersparen?  -> geht vllt. auch nciht, da es ja gespeichert und geladen werden können muss

        # Bond the block of the box to the box pins
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 0, 0))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 0, 1))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_x.id, 1, 2))
        dist_func.add_bond(BondTemplate(BoxSide.IN, diff_y.id, 1, 3))
        dist_func.add_bond(BondTemplate(BoxSide.IN, dist_rescaled.id, None, 4))
        dist_func.add_bond(BondTemplate(BoxSide.OUT, dist_rescaled.id, 0, 0))

        dist_func.store(out_filename)

        if True:
            dist_func: BoxFactory = BoxFactory()
            dist_func.load(out_filename)
        # end if

        scale = 0.001
        dist_total = AddN()

        bb0 = dist_func.inst(5, 1, "dist_func")  # XXX sollten diese parameter nicht auch mit abgespeichert werden? diese sollte nicht mehr explizit angegeben werden müssen...

        p0_x = ConstUser(-130)
        p0_y = ConstUser(80)
        p0_scale = ConstUser(scale)

        bb0.conn_to_prev_block(p, 0, 0)
        bb0.conn_to_prev_block(p, 1, 1)
        bb0.conn_to_prev_block(p0_x, 0, 2)
        bb0.conn_to_prev_block(p0_y, 0, 3)
        bb0.conn_to_prev_block(p0_scale, 0, 4)

        dist_total.conn_to_prev_block(Inv(bb0), 0, None)

        bb1 = dist_func.inst(5, 1, "dist_func")

        p1_x = ConstUser(100)
        p1_y = ConstUser(70)
        p1_scale = ConstUser(scale*.5)

        bb1.conn_to_prev_block(p, 0, 0)
        bb1.conn_to_prev_block(p, 1, 1)
        bb1.conn_to_prev_block(p1_x, 0, 2)
        bb1.conn_to_prev_block(p1_y, 0, 3)
        bb1.conn_to_prev_block(p1_scale, 0, 4)

        dist_total.conn_to_prev_block(Inv(bb1), 0, None)

        bb2 = dist_func.inst(5, 1, "dist_func")

        p2_x = ConstUser(0)
        p2_y = ConstUser(-90)
        p2_scale = ConstUser(scale)

        bb2.conn_to_prev_block(p, 0, 0)
        bb2.conn_to_prev_block(p, 1, 1)
        bb2.conn_to_prev_block(p2_x, 0, 2)
        bb2.conn_to_prev_block(p2_y, 0, 3)
        bb2.conn_to_prev_block(p2_scale, 0, 4)

        dist_total.conn_to_prev_block(Inv(bb2), 0, None)

        d.conn_to_prev_block(dist_total, 0, 0)

    elif test == 22:
        # > dist
        # Test in multiple instances of a black box
        fn_dist = "dist.cmb"  # cmb = crazy matrix (black) box
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        dist_func = BoxFactory()

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
        fn_normal = "normal.cmb"  # cmb = crazy matrix (black) box
        idg: IdGenerator = IdGenerator()

        btf: BlockTemplateFactory = BlockTemplateFactory(idg)
        normal_func = BoxFactory()

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
            dist_func: BoxFactory = BoxFactory()
            dist_func.load(fn_dist)

            normal_func: BoxFactory = BoxFactory()
            normal_func.load(fn_normal)
        # end if

        scale = .05
        dist_total = AddN()

        # Point 0
        bb_dist0 = dist_func.inst(5, 1, "dist_func")
        bb_normal0 = normal_func.inst(1, 1, "normal_func")

        p0_x = ConstUser(70)
        p0_y = ConstUser(60)
        p0_scale = ConstUser(scale)

        bb_dist0.conn_to_prev_block(p, 0, 0)
        bb_dist0.conn_to_prev_block(p, 1, 1)
        bb_dist0.conn_to_prev_block(p0_x, 0, 2)
        bb_dist0.conn_to_prev_block(p0_y, 0, 3)
        bb_dist0.conn_to_prev_block(p0_scale, 0, 4)

        bb_normal0.conn_to_prev_block(bb_dist0, 0, 0)

        dist_total.conn_to_prev_block(bb_normal0, 0, None)

        # Point 1
        bb_dist1 = dist_func.inst(5, 1, "dist_func")
        bb_normal1 = normal_func.inst(1, 1, "normal_func")

        p1_x = ConstUser(-100)
        p1_y = ConstUser(80)
        p1_scale = ConstUser(scale*2)

        bb_dist1.conn_to_prev_block(p, 0, 0)
        bb_dist1.conn_to_prev_block(p, 1, 1)
        bb_dist1.conn_to_prev_block(p1_x, 0, 2)
        bb_dist1.conn_to_prev_block(p1_y, 0, 3)
        bb_dist1.conn_to_prev_block(p1_scale, 0, 4)

        bb_normal1.conn_to_prev_block(bb_dist1, 0, 0)

        dist_total.conn_to_prev_block(bb_normal1, 0, None)

        # Point 2
        bb_dist2 = dist_func.inst(5, 1, "dist_func")
        bb_normal2 = normal_func.inst(1, 1, "normal_func")

        p2_x = ConstUser(-80)
        p2_y = ConstUser(-20)
        p2_scale = ConstUser(scale/3)

        bb_dist2.conn_to_prev_block(p, 0, 0)
        bb_dist2.conn_to_prev_block(p, 1, 1)
        bb_dist2.conn_to_prev_block(p2_x, 0, 2)
        bb_dist2.conn_to_prev_block(p2_y, 0, 3)
        bb_dist2.conn_to_prev_block(p2_scale, 0, 4)

        bb_normal2.conn_to_prev_block(bb_dist2, 0, 0)

        dist_total.conn_to_prev_block(bb_normal2, 0, None)

        d.conn_to_prev_block(dist_total, 0, 0)

    elif test == 23:
        fn_dist = "dist.cmb"
        fn_normal = "normal.cmb"
        fn_normal_dist = "normal_dist.cmb"

        if True:
            # > dist
            # Test in multiple instances of a black box
            # fn_dist = "dist.cmb"  # cmb = crazy matrix (black) box
            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            dist_func = BoxFactory()

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
            # fn_normal = "normal.cmb"  # cmb = crazy matrix (black) box
            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            normal_func = BoxFactory()

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
            # Test in multiple instances of a black box
            # fn_normal_dist = "normal_dist.cmb"  # cmb = crazy matrix (black) box
            idg: IdGenerator = IdGenerator()

            btf: BlockTemplateFactory = BlockTemplateFactory(idg)
            normal_dist_func = BoxFactory()

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
            dist_func: BoxFactory = BoxFactory()
            dist_func.load(fn_dist)

            normal_func: BoxFactory = BoxFactory()
            normal_func.load(fn_normal)

            normal_dist_func: BoxFactory = BoxFactory()
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
    # end if

    cm = CrazyMatrix(c)

    cm.plot()
# end def


if __name__ == "__main__":
    main(sys.argv)
