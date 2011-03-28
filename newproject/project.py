import newproject.config as config
import subprocess
import json
import os
from string import Template

class Project(object):
	"""docstring for Project"""
	def __init__(self, **kwargs):
		self.name         = kwargs["project_name"] if "project_name" in kwargs else None
		self.host         = kwargs["host"] if "host" in kwargs else None
		self.config_file  = kwargs["config_file"] if "config_file" in kwargs else None
		
		
	def create(self):
		"""docstring for create"""
		vhost = None
		cfg = config.Config(self.config_file)
		
		#create Project Directory
		self.create_directories(cfg)
		
		#create VirtualHost
		if self.host is not None:
			self.create_virtual_host(cfg)
	
	def create_directories(self, cfg):
		base_path = "{0}/{1}".format(cfg.project_path, self.name)
		
		with open(cfg.structure) as f:
			folders = json.loads(f.read())
		
		def build(part, path=base_path):
			
			if not os.path.isdir(path):
				subprocess.call(["su", "-", os.getlogin(), "-c", "mkdir " + path])
				
			for key in part.keys():
				next_path = "{0}/{1}".format(path, key)
				
				if not os.path.isdir(next_path):
					subprocess.call(["su", "-", os.getlogin(), "-c", "mkdir " + next_path])
					
				
				if part[key] is not None:
					build(part[key], next_path)
				
		build(folders)
		
	def create_virtual_host(self, cfg):
		vhost = VirtualHost(cfg.virtual_host)
		vhost.set_params({"server_admin": cfg.email,
		                  "document_root": "{0}/{1}/{2}".format(cfg.project_path, self.name, cfg.document_root_suffix),
		                  "log_path": cfg.log_path,
		                  "server_alias": self.host,
		                  "server_name":self.host})
		
		with open("/etc/hosts", "a") as f:
			f.write("\n127.0.0.1\t{0}".format(self.host))
			
		with open("{0}/{1}".format(cfg.sites_available_path, self.host), "w") as f:
			f.write(str(vhost))
			
		subprocess.call(["ln", "-s", "{0}/{1}".format(cfg.sites_available_path, self.host),
		                             "{0}/{1}".format(cfg.sites_enabled_path, self.host)])
		
		subprocess.call([cfg.apachectl, "restart"])

class VirtualHost(object):
	"""docstring for VirtualHost"""
	def __init__(self, template):
		self.template = template
	
	def set_params(self, subs):
		self.substitutions = subs
	
	def __str__(self):
		template = Template(self.template)
		return template.safe_substitute(self.substitutions).decode("string-escape")
		