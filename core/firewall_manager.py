import platform
import subprocess
import logging

class FirewallManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.system = platform.system()
        self.rules = []
        
    def get_rules(self):
        # Mock implementation - replace with actual firewall commands
        if not self.rules:
            self.rules = [
                {"port": 80, "protocol": "tcp", "action": "ALLOW", "source": "0.0.0.0/0"},
                {"port": 443, "protocol": "tcp", "action": "ALLOW", "source": "0.0.0.0/0"},
                {"port": 22, "protocol": "tcp", "action": "ALLOW", "source": "192.168.1.0/24"},
            ]
        return self.rules
    
    def add_rule(self, rule_text, action):
        try:
            # Parse rule text (e.g., "80/tcp")
            parts = rule_text.split('/')
            port = int(parts[0])
            protocol = parts[1] if len(parts) > 1 else 'tcp'
            
            new_rule = {
                "port": port,
                "protocol": protocol,
                "action": action,
                "source": "0.0.0.0/0"
            }
            
            self.rules.append(new_rule)
            self.logger.info(f"Added rule: {new_rule}")
            
            # Here you would add actual firewall rules based on OS
            if self.system == "Windows":
                self._add_windows_rule(port, protocol, action)
            elif self.system == "Linux":
                self._add_linux_rule(port, protocol, action)
                
        except Exception as e:
            self.logger.error(f"Error adding rule: {e}")
            raise
    
    def _add_windows_rule(self, port, protocol, action):
        # Windows firewall commands
        pass
    
    def _add_linux_rule(self, port, protocol, action):
        # iptables/ufw commands
        pass