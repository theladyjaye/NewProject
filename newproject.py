#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Adam Venturella on 2011-03-27.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
from optparse import OptionParser
import newproject.project


def main(argv=None):
	
	domain = None
	parser = OptionParser(usage="%prog -d -n [-c]", version="%prog 1.0")
	
	parser.add_option("-d", "--domain", dest="domain", default=None,
	                  help="virtual host DOMAIN", metavar="DOMAIN")
	
	parser.add_option("-c", "--config", dest="config", default="newproject.cfg",
	                  help="config FILE to process. Defaults to %default", metavar="FILE")
	
	parser.add_option("-n", "--name", dest="name",
	                  help="Project NAME. This folder will be created in the project path you defined in the config", metavar="NAME")
	
	(options, args) = parser.parse_args()
	
	if not options.name:
		parser.error("Project Name (-n NAME | --name=NAME ) is required")
	
	project = newproject.project.Project(project_name=options.name, 
	                                     host=options.domain, 
	                                     config_file=options.config)
	
	project.create()

if __name__ == "__main__":
	sys.exit(main())
