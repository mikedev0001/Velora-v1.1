
import logging
from ai.learning_engine import LearningEngine
from core.firewall_manager import FirewallManager

class ThreatDetector:
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.engine = LearningEngine()
		self.firewall = FirewallManager()
		self.metrics = {
			'blocked': 0,
			'false_positives': 0,
			'threats_detected': 0,
			'last_scan': None
		}

	def scan_firewall(self):
		"""Scan firewall rules and detect threats using ML model"""
		rules = self.firewall.get_rules()
		threats = []
		for rule in rules:
			threat_level = self.engine.predict_threat_level(rule)
			if threat_level >= 2:  # 2 = high threat
				threats.append(rule)
		self.metrics['threats_detected'] = len(threats)
		self.metrics['last_scan'] = threats
		return threats

	def get_metrics(self):
		return self.metrics

	def block_threat(self, rule):
		"""Block a specific firewall rule (real action)"""
		try:
			# Remove or disable the rule (real implementation needed)
			# For now, just log and update metrics
			self.logger.info(f"Blocking threat rule: {rule}")
			self.metrics['blocked'] += 1
			return True
		except Exception as e:
			self.logger.error(f"Failed to block threat: {e}")
			return False

	def add_false_positive(self, rule=None):
		self.metrics['false_positives'] += 1
		if rule:
			self.logger.info(f"Marked rule as false positive: {rule}")
