
"""
simplemap.map.py
~~~~~~~~~~~~~~~~

This module contains all core functionality related to map generation

"""

from jinja2 import Environment, FileSystemLoader
from html_render import SilentUndefined
import json
import os
import sys
import traceback

TEMPLATES_DIR = FileSystemLoader('simplemap/templates')
ZOOM_DEFAULT = 11
LINES_DEFAULT = []

class Map(object):
	def __init__(self, title, center=None, zoom=11, markers=None, message=None, points=None, html_template='basic.html', config_file='config.json'):
		self._env = Environment(loader=TEMPLATES_DIR, trim_blocks=True, undefined=SilentUndefined)
		self.title = title
		self.template = self._env.get_template(html_template)
		self.center = center
		self.zoom = zoom
		self.config = config_file
		self.markers = markers
		# message added in.
		self.message = message
		# points for lines added in
		self.points = points

	def set_center(self, center_point):
		self._center = '{{ lat:{}, lng:{}}}'.format(*center_point) if center_point else 'null'

	def get_center(self):
		return self._center

	def set_zoom(self, zoom):
		if zoom:
			self._zoom = zoom
		else:
			#Don't allow zoom to be null if customer center is given 
			self._zoom = ZOOM_DEFAULT if self.center else 'null'
	# Message setter and getter methods I added. Similar concept to zoom, optional for the user.
	def set_message(self, message):
		self._message = message

	def get_message(self):
		return self._message

	# Points setter and getter
	def set_points(self, points):
		if points:
			self._points = points
		else:
			self._points = LINES_DEFAULT

	def get_points(self):
		return self._points

	def get_zoom(self):
		return self._zoom
	
	def set_config(self, config_file):
		try:
			with open(config_file, "r") as config:    
				self._config = json.load(config)
		except IOError:
			sys.exit("Error, unable to open {} config file.".format(config_file))
		except KeyError:
			sys.exit("Error, `api_entry` not found in {} config file.".format(config_file))
		except Exception:
			print "An unknown error occured while attempting to read {} config file.".format(config_file)
			traceback.print_exc()
			sys.exit()

	def get_config(self):
		return self._config

	def set_markers(self, markers):
		if markers:
			for i in markers:
				if len(i) == 2:
					i.insert(0, '')
			self._markers = markers

	def get_markers(self):
		return self._markers

	config = property(get_config, set_config)
	markers = property(get_markers, set_markers)
	center = property(get_center, set_center)
	zoom = property(get_zoom, set_zoom)
	# Declare the names of the setter and getters
	message = property(get_message, set_message)
	# Declare the names of the setter and getters
	points = property(get_points, set_points)

	def write(self, output_path):
		try:
			html = self.template.render(map_title = self.title, center=self.center,
				zoom=self.zoom, markers=self.markers, message=self.message, points=self.points, api_key=self.config['api_key'])
			with open(output_path, "w") as out_file:
				out_file.write(html)
			return 'file://' + os.path.join(os.path.abspath(os.curdir), output_path)
		except IOError:
			sys.exit("Error, unable to write {}".format(output_path))
		except Exception:
			print "Undefined error occured while writing generating {}".format(output_path)
			traceback.print_exc()
			sys.exit()
