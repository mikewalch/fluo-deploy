# Copyright 2014 Muchos authors (see AUTHORS)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from muchos.hosts import MuchosHosts
from muchos.config import MuchosConfig

def test_defaults():
  c = MuchosConfig("muchos", "../../conf/muchos.props.example", "../../conf/hosts/example/", "example_cluster")
  h = MuchosHosts(c)
  assert h.get_hosts() == {'leader2': ('10.0.0.1', None), 'leader3': ('10.0.0.2', None), 'leader1': ('10.0.0.0', '23.0.0.0'),
                           'worker1': ('10.0.0.3', None), 'worker3': ('10.0.0.5', None), 'worker2': ('10.0.0.4', None)}
  assert h.get_public_ip('leader1') == '23.0.0.0'
  assert h.get_private_ip('leader1') == '10.0.0.0'
  assert h.proxy_public_ip() == "23.0.0.0"
  assert h.proxy_private_ip() == "10.0.0.0"
  assert h.get_non_proxy() == [('10.0.0.1', 'leader2'), ('10.0.0.2', 'leader3'), ('10.0.0.3', 'worker1'), ('10.0.0.4', 'worker2'), ('10.0.0.5', 'worker3')]
