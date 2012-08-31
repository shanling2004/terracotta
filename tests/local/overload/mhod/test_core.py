# Copyright 2012 Anton Beloglazov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mocktest import *
from pyqcy import *

import neat.local.overload.mhod.core as c


class Core(TestCase):

    def test_init_state(self):
        state = c.init_state([20, 40], 2)
        self.assertEquals(state['previous_state'], 0)
        self.assertTrue('request_windows' in state)
        self.assertTrue('estimate_windows' in state)
        self.assertTrue('variances' in state)
        self.assertTrue('acceptable_variances' in state)

    def test_utilization_to_state(self):
        state_config = [0.4, 0.7]
        self.assertEqual(c.utilization_to_state(state_config, 0.0), 0)
        self.assertEqual(c.utilization_to_state(state_config, 0.1), 0)
        self.assertEqual(c.utilization_to_state(state_config, 0.2), 0)
        self.assertEqual(c.utilization_to_state(state_config, 0.3), 0)
        self.assertEqual(c.utilization_to_state(state_config, 0.4), 1)
        self.assertEqual(c.utilization_to_state(state_config, 0.5), 1)
        self.assertEqual(c.utilization_to_state(state_config, 0.6), 1)
        self.assertEqual(c.utilization_to_state(state_config, 0.7), 2)
        self.assertEqual(c.utilization_to_state(state_config, 0.8), 2)
        self.assertEqual(c.utilization_to_state(state_config, 0.9), 2)
        self.assertEqual(c.utilization_to_state(state_config, 1.0), 2)
        self.assertEqual(c.utilization_to_state(state_config, 1.1), 2)

        self.assertEqual(c.utilization_to_state([1.0], 0.0), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.1), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.2), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.3), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.4), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.5), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.6), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.7), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.8), 0)
        self.assertEqual(c.utilization_to_state([1.0], 0.9), 0)
        self.assertEqual(c.utilization_to_state([1.0], 1.0), 1)
        self.assertEqual(c.utilization_to_state([1.0], 1.1), 1)

    def test_build_state_vector(self):
        state_config = [0.4, 0.7]
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.1]), [1, 0, 0])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.2]), [1, 0, 0])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.3]), [1, 0, 0])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.4]), [0, 1, 0])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.5]), [0, 1, 0])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.6]), [0, 1, 0])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.7]), [0, 0, 1])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.8]), [0, 0, 1])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 0.9]), [0, 0, 1])
        self.assertEqual(c.build_state_vector(state_config, [0.0, 1.0]), [0, 0, 1])

    def test_current_state(self):
        self.assertEqual(c.current_state([1, 0, 0]), 0)
        self.assertEqual(c.current_state([0, 1, 0]), 1)
        self.assertEqual(c.current_state([0, 0, 1]), 2)
