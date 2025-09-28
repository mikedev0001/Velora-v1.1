import os
import json
import subprocess
import time
import psutil
import logging
from threading import Thread

class LauncherManager:
	def __init__(self, config):
		self.logger = logging.getLogger(__name__)
		self.config = config
		self.applications = []
		self.running = {}
		self._load_applications()

	def _load_applications(self):
		# Load from config or file (simulate for now)
		apps_conf = self.config.get('applications', {})
		self.applications = apps_conf.get('list', [])

	def get_applications(self):
		return self.applications

	def add_application(self, app_data):
		# Add or update application
		for app in self.applications:
			if app['name'] == app_data['name']:
				app.update(app_data)
				self._save()
				return
		self.applications.append(app_data)
		self._save()

	def get_application(self, name):
		for app in self.applications:
			if app['name'] == name:
				return app
		return None

	def launch_application(self, name):
		app = self.get_application(name)
		if not app or not os.path.exists(app['path']):
			return False, "Application not found or path invalid"
		try:
			args = [app['path']]
			if app.get('arguments'):
				args += app['arguments'].split()
			proc = subprocess.Popen(args)
			self.running[name] = {
				'pid': proc.pid,
				'start_time': time.time(),
				'process': proc
			}
			app['running'] = True
			self._save()
			return True, f"Launched {name} (PID {proc.pid})"
		except Exception as e:
			return False, str(e)

	def stop_application(self, name):
		if name in self.running:
			proc = self.running[name]['process']
			try:
				proc.terminate()
				proc.wait(timeout=5)
			except Exception:
				proc.kill()
			del self.running[name]
			app = self.get_application(name)
			if app:
				app['running'] = False
			self._save()
			return True
		return False

	def get_running_applications(self):
		running_apps = []
		for name, info in self.running.items():
			app = self.get_application(name)
			if app:
				pid = info['pid']
				try:
					p = psutil.Process(pid)
					cpu = p.cpu_percent(interval=0.1)
					mem = p.memory_info().rss / (1024 * 1024)  # MB
					uptime = int(time.time() - info['start_time'])
				except Exception:
					cpu = 'N/A'
					mem = 'N/A'
					uptime = 'N/A'
				running_apps.append({
					'name': name,
					'pid': pid,
					'uptime': f"{uptime}s",
					'cpu': cpu,
					'memory': mem
				})
		return running_apps

	def import_system_applications(self):
		# Real import: scan Start Menu and Program Files for .exe files (Windows only)
		import glob
		import platform
		imported = 0
		if platform.system() == 'Windows':
			# Scan Start Menu
			start_menu = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs')
			for exe in glob.glob(start_menu + '/**/*.lnk', recursive=True):
				name = os.path.splitext(os.path.basename(exe))[0]
				app_data = {
					'name': name,
					'path': exe,
					'type': 'Executable',
					'arguments': '',
					'auto_start': False
				}
				self.add_application(app_data)
				imported += 1
			# Scan Program Files
			for pf in [os.environ.get('ProgramFiles'), os.environ.get('ProgramFiles(x86)')]:
				if pf:
					for exe in glob.glob(pf + '/**/*.exe', recursive=True):
						name = os.path.splitext(os.path.basename(exe))[0]
						app_data = {
							'name': name,
							'path': exe,
							'type': 'Executable',
							'arguments': '',
							'auto_start': False
						}
						self.add_application(app_data)
						imported += 1
		return imported

	def ai_optimize_launch_order(self):
		# Real optimization: sort by memory usage (lowest first)
		apps = self.get_running_applications()
		if not apps:
			return "No running applications to optimize."
		sorted_apps = sorted(apps, key=lambda x: x['memory'] if isinstance(x['memory'], (int, float)) else float('inf'))
		result = "Recommended launch order (least memory usage first):\n"
		for app in sorted_apps:
			result += f"{app['name']} (PID {app['pid']}): {app['memory']} MB RAM\n"
		return result

	def _save(self):
		# Save to config or file (simulate)
		self.config.set('applications.list', self.applications)
