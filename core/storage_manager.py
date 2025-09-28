import os
import json
import shutil
import logging
from collections import defaultdict

class StorageManager:
	def __init__(self, config):
		self.logger = logging.getLogger(__name__)
		self.config = config
		self.locations = self._load_locations()

	def _load_locations(self):
		# Load from config or use defaults
		storage_conf = self.config.get('storage', {})
		default_locs = storage_conf.get('default_locations', {})
		locations = []
		for loc_type, path in default_locs.items():
			locations.append({
				'path': path,
				'type': loc_type.replace('_', ' ').title(),
			})
		return locations

	def get_storage_locations(self):
		# Return list of dicts with usage info
		result = []
		for loc in self.locations:
			usage = self._get_usage(loc['path'])
			result.append({
				'path': loc['path'],
				'type': loc['type'],
				'usage_gb': usage['used_gb'],
				'free_gb': usage['free_gb']
			})
		return result

	def add_storage_location(self, path, loc_type):
		# Add new location if not already present
		for loc in self.locations:
			if loc['path'] == path:
				return
		self.locations.append({'path': path, 'type': loc_type})

	def get_overall_usage(self):
		total = used = free = 0
		for loc in self.locations:
			usage = self._get_usage(loc['path'])
			total += usage['total_gb']
			used += usage['used_gb']
			free += usage['free_gb']
		percent_used = (used / total * 100) if total else 0
		return {
			'total_gb': total,
			'used_gb': used,
			'free_gb': free,
			'percent_used': percent_used
		}

	def _get_usage(self, path):
		try:
			if not os.path.exists(path):
				return {'total_gb': 0, 'used_gb': 0, 'free_gb': 0}
			stat = shutil.disk_usage(path)
			total_gb = stat.total / (1024 ** 3)
			used_gb = (stat.total - stat.free) / (1024 ** 3)
			free_gb = stat.free / (1024 ** 3)
			return {'total_gb': total_gb, 'used_gb': used_gb, 'free_gb': free_gb}
		except Exception as e:
			self.logger.error(f"Error getting usage for {path}: {e}")
			return {'total_gb': 0, 'used_gb': 0, 'free_gb': 0}

	def get_location_details(self, path):
		usage = self._get_usage(path)
		file_types = defaultdict(int)
		total_size = used_size = free_size = 0
		if os.path.exists(path):
			for root, dirs, files in os.walk(path):
				for f in files:
					ext = os.path.splitext(f)[1].lower() or 'no_ext'
					file_types[ext] += 1
		return {
			'path': path,
			'type': self._get_type_for_path(path),
			'total_gb': usage['total_gb'],
			'used_gb': usage['used_gb'],
			'free_gb': usage['free_gb'],
			'percent_used': (usage['used_gb'] / usage['total_gb'] * 100) if usage['total_gb'] else 0,
			'file_types': dict(file_types)
		}

	def _get_type_for_path(self, path):
		for loc in self.locations:
			if loc['path'] == path:
				return loc['type']
		return 'Unknown'

	def ai_cleanup(self):
		# Simulate AI-powered cleanup
		cleaned = 0
		for loc in self.locations:
			path = loc['path']
			if os.path.exists(path):
				for root, dirs, files in os.walk(path):
					for f in files:
						if f.endswith('.tmp') or f.startswith('~'):
							try:
								os.remove(os.path.join(root, f))
								cleaned += 1
							except Exception:
								pass
		return f"AI Cleanup complete. {cleaned} temporary files removed."

	def ai_analyze_storage(self):
		# Simulate AI analysis
		analysis = "=== AI Storage Analysis ===\n"
		for loc in self.locations:
			usage = self._get_usage(loc['path'])
			analysis += f"{loc['type']} ({loc['path']}): {usage['used_gb']:.1f} GB used, {usage['free_gb']:.1f} GB free\n"
		analysis += "\nRecommendations:\n"
		for loc in self.locations:
			if self._get_usage(loc['path'])['free_gb'] < 1:
				analysis += f"- Consider cleaning up {loc['type']} ({loc['path']})\n"
		return analysis
