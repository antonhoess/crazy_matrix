from __future__ import annotations
from typing import List
import sys


from base.basic import Circuit, Point
from base.black_box import BlackBox
from blocks.bool import *
from blocks.const_var import *
from blocks.math import *
from blocks.complex import *
from crazy_matrix import CrazyMatrix


# XXX wo anders einordnen
#
# class Discr(Block):
#     def __init__(self):
#         Block.__init__(self, 1, 1)
#     # end def
#
#     def _calc_values(self):
#         self._pin_value[0] = np.abs(self._conn_in[0].value)
#     # end def
# # end class
# XXX einen discretizer kann man auch als block bauen.
# eiglt. alles so umbauen, dass alle pixel als matrix auf einmal ausgewrtet werden, dann kann ich auch funktionen machen, die wissen müssen,w as min und max werte aller pixel (bzw. deren an diesem punkt berechneten werte) sind


def main(_argv: List[str]):
    c = Circuit()

    p = c.point
    d = c.drawer

    test = 12

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

        sq = Square()
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

        x_sq = Square()
        x_sq.conn_to_prev_block(diff_x)

        y_sq = Square()
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

        # Geht Rekursion überhaupt, wenn ich von Hinten nach vorne traversiere? -> Müsste es nicht anders herum sein?

        #### Fibonacci (evtl. auch mit float anstatt int?) ist das das gleiche, nur skaliert?
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
            add_xy_sq.conn_to_prev_block(Square(diff_x), 0, 0)
            add_xy_sq.conn_to_prev_block(Square(diff_y), 0, 1)

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
    # end if

    cm = CrazyMatrix(c)

    cm.plot()
    x = 0  # XXX just for setting a breakpoint
# end def


if __name__ == "__main__":
    main(sys.argv)
