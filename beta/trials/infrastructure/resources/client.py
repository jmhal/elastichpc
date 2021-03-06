import os
import subprocess
import xmlrpclib

class ResourcesProxy():
   def __init__(self, url, stack_name, stack_id):
      self.proxy = xmlrpclib.ServerProxy(url)      
      self.stack_name = stack_name
      self.stack_id = stack_id

   def add_node(self, n = 1):
      return self.proxy.add_node(self.stack_name, self.stack_id, n) 
       
   def remove_node(self, n = 1):
      return self.proxy.remove_node(self.stack_name, self.stack_id, n) 

   def get_resource_state(self):
      home = os.environ['HOME']
      p = subprocess.Popen([home + "/repositorios/elastichpc/beta/trials/tools/resource_state.sh"], stdout=subprocess.PIPE)
      return p.communicate()[0].rstrip()

   def configure_machine_file(self):
      machinefile = open(os.environ['HOME'] + "/machinefile_new", "w")
      
      ips = self.proxy.get_ips(self.stack_name, self.stack_id)
      
      self.number_of_nodes = 1
      machinefile.write(ips['head_node_ip'] + ":2" + "\n")
      for machine in ips['compute_node_ips']:
         machinefile.write(machine + ":2" + "\n")
	 self.number_of_nodes += 1
      machinefile.close()
      
      os.rename(os.environ['HOME'] + "/machinefile_new", os.environ['HOME'] + "/machinefile")

      return self.number_of_nodes


