
import numpy as np
from sklearn.ensemble import IsolationForest

class PatternAnalyzer:
	def __init__(self):
		self.anomaly_model = IsolationForest(n_estimators=100, contamination=0.05)
		self.trained = False

	def fit(self, patterns):
		"""Train anomaly detector on patterns (list of dicts)"""
		X = self._extract_features(patterns)
		if len(X) > 10:
			self.anomaly_model.fit(X)
			self.trained = True

	def detect_anomalies(self, patterns):
		"""Detect anomalies in new patterns"""
		if not self.trained:
			return []
		X = self._extract_features(patterns)
		preds = self.anomaly_model.predict(X)
		anomalies = [p for p, pred in zip(patterns, preds) if pred == -1]
		return anomalies

	def _extract_features(self, patterns):
		# Example: extract numeric features from pattern dicts
		features = []
		for p in patterns:
			features.append([
				p.get('port', 0),
				p.get('protocol', 0) if isinstance(p.get('protocol', 0), (int, float)) else 0,
				p.get('frequency', 0),
				p.get('source_diversity', 0),
				p.get('cpu_usage', 0),
				p.get('memory_usage', 0),
				p.get('active_connections', 0),
				p.get('request_rate', 0)
			])
		return np.array(features)
