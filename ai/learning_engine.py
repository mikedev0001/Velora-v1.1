import json
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import threading
import time
import logging
from collections import deque
from ai.data_ingestion import DataIngestion

class LearningEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.learning_active = False
        self.learning_thread = None
        
        # Data storage
        self.firewall_patterns = deque(maxlen=10000)
        self.server_patterns = deque(maxlen=5000)
        self.user_behavior = deque(maxlen=2000)
        
        # ML models
        self.threat_model = None
        self.optimization_model = None
        self.user_pattern_model = None
        
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models or initialize new ones"""
        try:
            with open('data/models/threat_model.pkl', 'rb') as f:
                self.threat_model = pickle.load(f)
            with open('data/models/optimization_model.pkl', 'rb') as f:
                self.optimization_model = pickle.load(f)
            self.logger.info("AI models loaded successfully")
        except FileNotFoundError:
            self.initialize_models()
    
    def initialize_models(self):
        """Initialize new ML models"""
        self.threat_model = RandomForestClassifier(n_estimators=100)
        self.optimization_model = KMeans(n_clusters=5)
        self.user_pattern_model = RandomForestClassifier(n_estimators=50)
        self.logger.info("New AI models initialized")
    
    def start_continuous_learning(self):
        """Start continuous learning in background thread"""
        if not self.learning_active:
            self.learning_active = True
            self.learning_thread = threading.Thread(target=self._learning_loop, daemon=True)
            self.learning_thread.start()
            self.logger.info("Continuous learning started")
    
    def stop_continuous_learning(self):
        """Stop continuous learning"""
        self.learning_active = False
        if self.learning_thread:
            self.learning_thread.join(timeout=5)
        self.logger.info("Continuous learning stopped")
    
    def _learning_loop(self):
        """Main learning loop running in background"""
        while self.learning_active:
            try:
                self.analyze_patterns()
                time.sleep(60)  # Learn every minute
            except Exception as e:
                self.logger.error(f"Learning loop error: {e}")
                time.sleep(300)  # Wait 5 minutes on error
    
    def analyze_patterns(self):
        """Analyze collected patterns for insights"""
        if len(self.firewall_patterns) > 100:
            self._analyze_firewall_patterns()
        
        if len(self.server_patterns) > 50:
            self._analyze_server_patterns()
        
        if len(self.user_behavior) > 100:
            self._analyze_user_behavior()
    
    def _analyze_firewall_patterns(self):
        """Analyze firewall patterns for threat detection"""
        # Convert patterns to features
        features = []
        labels = []
        
        for pattern in self.firewall_patterns:
            features.append([
                pattern.get('port', 0),
                pattern.get('protocol', 0),
                pattern.get('frequency', 0),
                pattern.get('source_diversity', 0)
            ])
            labels.append(pattern.get('threat_level', 0))
        
        if len(features) > 10:
            X = np.array(features)
            y = np.array(labels)
            self.threat_model.partial_fit(X, y, classes=[0, 1, 2])
    
    def _analyze_server_patterns(self):
        """Analyze server usage patterns for optimization"""
        features = []
        for pattern in self.server_patterns:
            features.append([
                pattern.get('cpu_usage', 0),
                pattern.get('memory_usage', 0),
                pattern.get('active_connections', 0),
                pattern.get('request_rate', 0)
            ])
        
        if len(features) > 5:
            X = np.array(features)
            self.optimization_model.partial_fit(X)
    
    def _analyze_user_behavior(self):
        """Learn user behavior patterns"""
        # Implement user behavior analysis
        pass
    

    def add_firewall_event(self, event_data):
        """Add real firewall event for learning (ingest live data)"""
        event_data['timestamp'] = datetime.now().isoformat()
        self.firewall_patterns.append(event_data)
        # Optionally trigger learning immediately
        if len(self.firewall_patterns) > 100:
            self._analyze_firewall_patterns()

    def add_server_metric(self, metric_data):
        """Add real server metrics for learning (ingest live data)"""
        metric_data['timestamp'] = datetime.now().isoformat()
        self.server_patterns.append(metric_data)
        if len(self.server_patterns) > 50:
            self._analyze_server_patterns()
    
    def predict_threat_level(self, rule_data):
        """Predict threat level for new rule"""
        from sklearn.utils.validation import check_is_fitted
        try:
            check_is_fitted(self.threat_model)
            features = np.array([[
                rule_data.get('port', 0),
                rule_data.get('protocol', 0),
                rule_data.get('frequency', 1),
                rule_data.get('source_diversity', 1)
            ]])
            return self.threat_model.predict(features)[0]
        except Exception:
            return 1  # Medium threat by default
    
    def get_server_optimization(self, server_data):
        """Get optimization suggestions for server"""
        if self.optimization_model:
            features = np.array([[
                server_data.get('cpu_usage', 0),
                server_data.get('memory_usage', 0),
                server_data.get('connections', 0),
                server_data.get('request_rate', 0)
            ]])
            cluster = self.optimization_model.predict(features)[0]
            return self._get_optimization_for_cluster(cluster)
        return {"suggestion": "Monitor performance"}
    
    def _get_optimization_for_cluster(self, cluster):
        """Get optimization suggestions based on cluster"""
        optimizations = {
            0: {"suggestion": "Optimal performance", "action": "maintain"},
            1: {"suggestion": "High CPU usage", "action": "scale_up"},
            2: {"suggestion": "High memory usage", "action": "optimize_memory"},
            3: {"suggestion": "Low utilization", "action": "scale_down"},
            4: {"suggestion": "Network bottleneck", "action": "optimize_network"}
        }
        return optimizations.get(cluster, {"suggestion": "Monitor"})
    
    def retrain_models(self):
        """Retrain models with all available data (real, not simulated)"""
        self.logger.info("Retraining AI models with all available data...")
        # Full retraining using all collected data
        if self.firewall_patterns:
            self._analyze_firewall_patterns()
        if self.server_patterns:
            self._analyze_server_patterns()
        # User behavior retraining can be added here
        self.save_models()
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            with open('data/models/threat_model.pkl', 'wb') as f:
                pickle.dump(self.threat_model, f)
            with open('data/models/optimization_model.pkl', 'wb') as f:
                pickle.dump(self.optimization_model, f)
            self.logger.info("AI models saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving models: {e}")
    
    def ingest_from_internet(self, dataset_urls=None, threat_feeds=None, api_keys=None):
        """Fetch and learn from internet datasets and threat feeds."""
        ingestion = DataIngestion()
        all_data = []
        if dataset_urls:
            for url in dataset_urls:
                all_data.extend(ingestion.fetch_public_dataset(url))
        if threat_feeds:
            for i, feed in enumerate(threat_feeds):
                key = api_keys[i] if api_keys and i < len(api_keys) else None
                all_data.extend(ingestion.fetch_threat_feed(feed, api_key=key))
        # Example: treat all_data as firewall patterns for now
        for entry in all_data:
            self.add_firewall_event(entry)
        self.logger.info(f"Ingested {len(all_data)} records from internet sources.")
        self.retrain_models()