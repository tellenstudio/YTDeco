#
# DecoTengu - dive decompression library.
#
# Copyright (C) 2013 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Tests for DecoTengu dive decompression engine.
"""

from decotengu.engine import Engine, Step

import unittest
import mock

class EngineTestCase(unittest.TestCase):
    """
    DecoTengu dive decompression engine tests.
    """
    def setUp(self):
        """
        Create decompression engine.
        """
        self.engine = Engine()


    def test_depth_conversion(self):
        """
        Test deco engine depth to pressure conversion
        """
        self.engine.surface_pressure = 1.2
        v = self.engine._to_pressure(20)
        self.assertAlmostEquals(v, 3.197)


    def test_time_depth(self):
        """
        Test deco engine depth calculation using time
        """
        self.engine.ascent_rate = 10
        v = self.engine._to_depth(18)
        self.assertAlmostEquals(v, 3)


    def test_max_tissue_pressure(self):
        """
        Test calculation of maximum allowed tissue pressure (default gf)
        """
        tissues = (1.5, 2.5, 2.0, 2.9, 2.6)
        limit = (1.0, 2.0, 1.5, 2.4, 2.1)

        self.engine.gf_low = 0.1
        self.engine.calc.gf_limit = mock.MagicMock(return_value=limit)

        v = self.engine._max_tissue_pressure(tissues)
        self.engine.calc.gf_limit.assert_called_once_with(0.1, tissues)
        self.assertEquals(2.4, v)


    def test_max_tissue_pressure_gf(self):
        """
        Test calculation of maximum allowed tissue pressure (with gf)
        """
        tissues = (1.5, 2.5, 2.0, 2.9, 2.6)
        limit = (1.0, 2.0, 1.5, 2.4, 2.1)

        self.engine.calc.gf_limit = mock.MagicMock(return_value=limit)

        v = self.engine._max_tissue_pressure(tissues, 0.2)
        self.engine.calc.gf_limit.assert_called_once_with(0.2, tissues)
        self.assertEquals(2.4, v)


    def test_ascent_invariant(self):
        """
        Test ascent invariant
        """
        step = Step(40, 120, 3.0, [], 0.3)
        self.engine._max_tissue_pressure = mock.MagicMock(return_value=3.1)
        v = self.engine._inv_ascent(step)
        self.assertFalse(v)


    def test_ascent_invariant_edge(self):
        """
        Test ascent invariant (at limit)
        """
        step = Step(40, 120, 3.1, [], 0.3)
        self.engine._max_tissue_pressure = mock.MagicMock(return_value=3.1)
        v = self.engine._inv_ascent(step)
        self.assertFalse(v)


    def test_deco_stop_invariant(self):
        """
        Test decompression stop invariant
        """
        step = Step(18, 120, 2.8, [1.8, 1.8], 0.3)
        self.engine._tissue_pressure_ascent = mock.MagicMock(
            return_value=[2.6, 2.6])
        self.engine._max_tissue_pressure = mock.MagicMock(return_value=2.6)
        self.engine._to_pressure = mock.MagicMock(return_value=2.5)

        v = self.engine._inv_deco_stop(step, 0.4)

        self.engine._max_tissue_pressure.assert_called_once_with(
            [2.6, 2.6], gf=0.4)
        self.engine._to_pressure.assert_called_once_with(15)

        self.assertTrue(v)


    def test_dive_step(self):
        """
        Test creation of dive step record
        """
        self.engine.gf_low = 0.2
        step = self.engine._step(30, 1200, [0.1, 0.2])
        self.assertEquals(30, step.depth)
        self.assertEquals(1200, step.time)
        self.assertEquals(4.00875, step.pressure)
        self.assertEquals([0.1, 0.2], step.tissues)
        self.assertEquals(0.2, step.gf)


    def test_dive_step_gf(self):
        """
        Test creation of dive step record (with gf)
        """
        self.engine.gf_low = 0.2
        step = self.engine._step(30, 1200, [0.1, 0.2], 0.21)
        self.assertEquals(30, step.depth)
        self.assertEquals(1200, step.time)
        self.assertEquals(4.00875, step.pressure)
        self.assertEquals([0.1, 0.2], step.tissues)
        self.assertEquals(0.21, step.gf)


    def test_step_next(self):
        """
        Test creation of next dive step record
        """
        step = Step(20, 120, 3.0, [2.8, 2.8], 0.3)

        self.engine._tissue_pressure_const = mock.MagicMock(
                return_value=[3.0, 3.0])

        step = self.engine._step_next(step, 30)
        self.assertEquals(20, step.depth)
        self.assertEquals(150, step.time)
        self.assertEquals([3.0, 3.0], step.tissues)
        self.engine._tissue_pressure_const.assert_called_once_with(3.0, 30,
                [2.8, 2.8])


    def test_step_descent(self):
        """
        Test creation of next dive step record (descent)
        """
        step = Step(20, 120, 3.0, [2.8, 2.8], 0.3)

        self.engine._tissue_pressure_descent = mock.MagicMock(
                return_value=[3.1, 3.1])

        step = self.engine._step_next_descent(step, 30)
        self.assertEquals(25, step.depth)
        self.assertEquals(150, step.time)
        self.assertEquals([3.1, 3.1], step.tissues)

        self.engine._tissue_pressure_descent.assert_called_once_with(3.0, 30,
                [2.8, 2.8])


    def test_step_ascent(self):
        """
        Test creation of next dive step record (ascent)
        """
        step = Step(20, 120, 3.0, [2.8, 2.8], 0.3)

        self.engine._tissue_pressure_ascent = mock.MagicMock(
                return_value=[2.6, 2.6])

        step = self.engine._step_next_ascent(step, 30)
        self.assertEquals(15.0, step.depth)
        self.assertEquals(150, step.time)
        self.assertEquals([2.6, 2.6], step.tissues)

        self.engine._tissue_pressure_ascent.assert_called_once_with(3.0, 30,
                [2.8, 2.8])


    def test_tissue_load(self):
        """
        Test tissue loading at constant depth
        """
        self.engine.calc.load_tissues = mock.MagicMock(return_value=[1.2, 1.3])
        v = self.engine._tissue_pressure_const(2.0, 10, [1.1, 1.1])

        # check the rate is 0
        self.engine.calc.load_tissues.assert_called_once_with(2.0, 10, 0,
                [1.1, 1.1])


    def test_tissue_load_ascent(self):
        """
        Test tissue loading after ascent
        """
        self.engine.ascent_rate = 10
        self.engine.calc.load_tissues = mock.MagicMock(return_value=[1.2, 1.3])
        v = self.engine._tissue_pressure_ascent(2.0, 10, [1.1, 1.1])

        # rate for ascent has to be negative and converted to bars
        self.engine.calc.load_tissues.assert_called_once_with(2.0, 10,
                -0.9984999999999999, [1.1, 1.1])
        self.assertEquals([1.2, 1.3], v)


    def test_tissue_load_descent(self):
        """
        Test tissue loading after descent
        """
        self.engine.descent_rate = 10
        self.engine.calc.load_tissues = mock.MagicMock(return_value=[1.2, 1.3])
        v = self.engine._tissue_pressure_descent(2.0, 10, [1.1, 1.1])

        # rate for descent has to be positive number and converted to bars
        self.engine.calc.load_tissues.assert_called_once_with(2.0, 10,
                0.9984999999999999, [1.1, 1.1])
        self.assertEquals([1.2, 1.3], v)


    def test_dive_const_no_time_delta(self):
        """
        Test diving constant depth (no time delta)
        """
        step = Step(20, 120, 2, [1.9, 1.9], 0.3)

        self.engine.conveyor.time_delta = None

        assert self.engine.conveyor.time_delta is None, self.engine.conveyor.time_delta

        steps = list(self.engine._dive_const(step, 121))
        self.assertEquals(1, len(steps))

        step = steps[0]
        self.assertEquals(20, step.depth)
        self.assertEquals(241, step.time)


    def test_dive_const(self):
        """
        Test diving constant depth
        """
        step = Step(20, 120, 2, [1.9, 1.9], 0.3)

        self.engine.conveyor.time_delta = 60

        steps = list(self.engine._dive_const(step, 180))
        self.assertEquals(3, len(steps))

        s1, s2, s3 = steps
        self.assertEquals(20, s1.depth)
        self.assertEquals(180, s1.time)
        self.assertEquals(20, s2.depth)
        self.assertEquals(240, s2.time)
        self.assertEquals(20, s3.depth)
        self.assertEquals(300, s3.time)


    def test_dive_descent_no_time_delta(self):
        """
        Test dive descent (no time delta)
        """
        self.engine.conveyor.time_delta = None

        assert self.engine.conveyor.time_delta is None, self.engine.conveyor.time_delta

        steps = list(self.engine._dive_descent(21))
        self.assertEquals(2, len(steps)) # should contain start of a dive

        s1, s2 = steps
        self.assertEquals(0, s1.depth)
        self.assertEquals(0, s1.time)
        self.assertEquals(21, s2.depth)
        self.assertEquals(126, s2.time) # 1m is 6s at 10m/min


    def test_dive_descent(self):
        """
        Test dive descent
        """
        self.engine.conveyor.time_delta = 60

        steps = list(self.engine._dive_descent(21))
        self.assertEquals(4, len(steps)) # should contain start of a dive

        s1, s2, s3, s4 = steps
        self.assertEquals(0, s1.depth)
        self.assertEquals(0, s1.time)
        self.assertEquals(10, s2.depth)
        self.assertEquals(60, s2.time)
        self.assertEquals(20, s3.depth)
        self.assertEquals(120, s3.time)
        self.assertEquals(21, s4.depth)
        self.assertEquals(126, s4.time) # 1m is 6s at 10m/min


    @mock.patch('decotengu.engine.bisect_find')
    def test_first_stop_finder(self, f_bf):
        """
        Test first deco stop finder
        """
        self.engine._step_next_ascent = mock.MagicMock()
        start = Step(31, 1200, 4, [1.0, 1.0], 0.3)

        f_bf.return_value = 6 # 31m -> 30m - 18m -> 12m
        self.engine._find_first_stop(start)

        # 6 * 3m + 1m (6s) == 114s to ascent from 31m to 12m
        self.engine._step_next_ascent.assert_called_once_with(start, 114)


    @mock.patch('decotengu.engine.bisect_find')
    def test_first_stop_finder_steps(self, f_bf):
        """
        Test if first deco stop finder calculates proper amount of steps
        """
        self.engine._step_next_ascent = mock.MagicMock()
        start = Step(31, 1200, 4, [1.0, 1.0], 0.3)

        self.engine._find_first_stop(start)

        assert f_bf.called # test precondition
        self.assertEquals(10, f_bf.call_args_list[0][0][0])


    def test_first_stop_finder_surface(self):
        """
        Test finding first deco stop when no deco required
        """
        self.engine.surface_pressure = 1
        start = Step(30, 1200, 4, [1.0, 1.0], 0.3)

        stop = self.engine._find_first_stop(start)
        self.assertIsNone(stop)


    def test_free_ascent(self):
        """
        Test ascent from current to shallower depth without deco
        """
        pressure = self.engine._to_pressure
        self.engine.conveyor.time_delta = 60

        start = Step(31, 1200, pressure(31), [1.0, 1.0], 0.3)
        stop = Step(10, 1326, pressure(10), [1.33538844660, 1.22340240386], 0.3)
        steps = list(self.engine._free_ascent(start, stop))

        self.assertEquals(3, len(steps))

        s1, s2, s3 = steps
        self.assertEquals(s1.depth, 21.0)
        self.assertEquals(s1.time, 1260)
        self.assertEquals(s2.depth, 11.0)
        self.assertEquals(s2.time, 1320)
        self.assertEquals(s3.depth, 10.0)
        self.assertEquals(s3.time, 1326)


    def test_free_ascent_no_time_delta(self):
        """
        Test ascent from current to shallower depth without deco (no time delta)
        """
        pressure = self.engine._to_pressure
        self.engine.conveyor.time_delta = None

        assert self.engine.conveyor.time_delta is None, self.engine.conveyor.time_delta

        start = Step(31, 1200, pressure(31), [1.0, 1.0], 0.3)
        stop = Step(10, 1326, pressure(10), [1.33538844660, 1.22340240386], 0.3)
        steps = list(self.engine._free_ascent(start, stop))

        self.assertEquals(1, len(steps))

        step = steps[0]
        self.assertEquals(step.depth, 10)
        self.assertEquals(step.time, 1326)


# vim: sw=4:et:ai