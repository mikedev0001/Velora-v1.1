
import logging
from datetime import datetime
from ai.learning_engine import LearningEngine

class FirewallAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = LearningEngine()

    def analyze_rules(self, rules):
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_rules": len(rules),
            "threats": [],
            "recommendations": [],
        }
        for rule in rules:
            threat_level = self.engine.predict_threat_level(rule)
            if threat_level >= 2:
                analysis["threats"].append({"rule": rule, "threat_level": threat_level})

        output = (
            f"=== FIREWALL ANALYSIS ===\n"
            f"Timestamp: {analysis['timestamp']}\n"
            f"Total Rules: {analysis['total_rules']}\n\n"
            f"DETECTED THREATS:\n"
        )
        if analysis["threats"]:
            for threat in analysis["threats"]:
                output += f"⚠️  Rule: {threat['rule']} | Threat Level: {threat['threat_level']}\n"
        else:
            output += "✅ No high-risk threats detected\n"

        output += "\nRECOMMENDATIONS:\n"
        if analysis["threats"]:
            output += "🔴 High-risk rules found. Review and block as needed.\n"
        else:
            output += "🟢 Firewall configuration appears secure.\n"
        return output