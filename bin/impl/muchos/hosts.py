# Copyright 2016 Muchos authors (see AUTHORS)
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

from util import exit_with_help
import os
from os.path import isfile, join

def get_cluster_name(hosts_dir):
  clusters = [ f for f in os.listdir(hosts_dir) if isfile(join(hosts_dir, f))]

  if len(clusters) == 0:
    exit_with_help("ERROR - No clusters found in conf/hosts or specified by --cluster option")
  elif len(clusters) == 1:
    return clusters[0]
  else:
    exit_with_help("ERROR - Multiple clusters {0} found in conf/hosts/.  Please pick one using --cluster option".format(clusters))

class MuchosHosts:

  def __init__(self, config):
    self.config = config
    if not os.path.isfile(config.hosts_path):
      exit('ERROR - A hosts file does not exist for cluster at %s' % config.hosts_path)
    self.hosts = {}
    with open(config.hosts_path) as f:
      for line in f:
        line = line.strip()
        if line.startswith("#") or not line:
          continue
        args = line.split(' ')
        if len(args) == 2:
          self.hosts[args[0]] = (args[1], None)
        elif len(args) == 3:
          self.hosts[args[0]] = (args[1], args[2])
        else:
          exit('ERROR - Bad line %s in hosts %s' % (line, config.hosts_path))

  def get_non_proxy(self):
    retval = []
    proxy_ip = self.get_private_ip(self.config.get('general', 'proxy_hostname'))
    for (hostname, (private_ip, public_ip)) in self.hosts.items():
      if private_ip != proxy_ip:
        retval.append((private_ip, hostname))
    retval.sort()
    return retval

  def get_private_ip_hostnames(self):
    retval = []
    for (hostname, (private_ip, public_ip)) in self.hosts.items():
      retval.append((private_ip, hostname))
    retval.sort()
    return retval

  def get_hosts(self):
    return self.hosts

  def get_private_ip(self, hostname):
    return self.get_hosts()[hostname][0]

  def get_public_ip(self, hostname):
    return self.get_hosts()[hostname][1]

  def proxy_public_ip(self):
    retval = self.get_public_ip(self.config.get('general', 'proxy_hostname'))
    if not retval:
      exit("ERROR - Leader {0} does not have a public IP".format(self.get('general', 'proxy_hostname')))
    return retval

  def proxy_private_ip(self):
    return self.get_private_ip(self.config.get('general', 'proxy_hostname'))
