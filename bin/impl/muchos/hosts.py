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

def clean(val):
  if val.lower() == 'none':
    return None
  return val

class MuchosHosts:

  def __init__(self, config):
    self.config = config
    self.hosts = {}
    self.instances = {}
    if isfile(config.hosts_path):
      with open(config.hosts_path) as f:
        for line in f:
          line = line.strip()
          if line.startswith("#") or not line:
            continue
          args = line.split(' ')
          if len(args) == 4:
            hostname = args[0]
            instance_id = clean(args[3])
            self.hosts[hostname] = (args[1], clean(args[2]), instance_id)
            if instance_id:
              self.instances[instance_id] = hostname
          else:
            exit('ERROR - Bad line %s in hosts %s' % (line, config.hosts_path))

  def add_host(self, hostname, private_ip, public_ip, instance_id):
    with open(self.config.hosts_path, 'a') as hosts_file:
      print >>hosts_file, hostname, private_ip, public_ip, instance_id
    self.hosts[hostname] = (private_ip, public_ip, instance_id)
    self.instances[instance_id] = hostname

  def has_host(self, hostname):
    return hostname in self.hosts

  def has_instance_id(self, instance_id):
    return instance_id in self.instances

  def get_num_hosts(self):
    return len(self.hosts)

  def get_private_ip_hostnames(self):
    retval = []
    for (hostname, (private_ip, public_ip)) in self.hosts.items():
      retval.append((private_ip, hostname))
    retval.sort()
    return retval

  def get_missing_hosts(self):
    retval = []
    for (hostname, services) in self.config.nodes().items():
      if hostname not in self.hosts:
        retval.append(hostname)
    return retval

  def get_hostnames(self):
    return self.hosts.keys()

  def get_private_ip(self, hostname):
    return self.hosts[hostname][0]

  def get_public_ip(self, hostname):
    return self.hosts[hostname][1]

  def get_instance_id(self, hostname):
    return self.hosts[hostname][2]

  def proxy_public_ip(self):
    retval = self.get_public_ip(self.config.get('general', 'proxy_hostname'))
    if not retval:
      exit("ERROR - Leader {0} does not have a public IP".format(self.config.get('general', 'proxy_hostname')))
    return retval

  def proxy_private_ip(self):
    return self.get_private_ip(self.config.get('general', 'proxy_hostname'))
