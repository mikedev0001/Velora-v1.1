
from ai.learning_engine import LearningEngine
from ai.threat_detector import ThreatDetector

class Recommendations:
	def __init__(self):
		self.engine = LearningEngine()
		self.detector = ThreatDetector()
		self.recommendations = []

	def generate(self):
		"""Generate actionable recommendations based on real data and model outputs"""
		self.recommendations.clear()
		# Threat-based recommendations
		threats = self.detector.scan_firewall()
		if threats:
			for rule in threats:
				self.recommendations.append({
					'type': 'threat',
					'message': f"High-risk firewall rule detected: {rule}",
					'action': 'Review or block this rule.'
				})
		# Storage/optimization recommendations
		# (Assume server_data is available from somewhere, e.g., monitoring)
		# Example:
		# server_data = {'cpu_usage': 80, 'memory_usage': 90, 'connections': 100, 'request_rate': 200}
		# opt = self.engine.get_server_optimization(server_data)
		# self.recommendations.append({'type': 'optimization', 'message': opt['suggestion'], 'action': opt['action']})
		return self.recommendations

	def add(self, rec):
		self.recommendations.append(rec)

	def get_all(self):
		return self.recommendations
