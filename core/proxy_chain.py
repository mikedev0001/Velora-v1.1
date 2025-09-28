import socks
import socket
import threading

class ProxyChain:
    def __init__(self, proxies):
        """
        proxies: list of dicts, each with keys: type ('SOCKS5', 'SOCKS4', 'HTTP'), host, port, username, password
        """
        self.proxies = proxies

    def create_chain_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for proxy in self.proxies:
            proxy_type = {
                'SOCKS5': socks.SOCKS5,
                'SOCKS4': socks.SOCKS4,
                'HTTP': socks.HTTP
            }[proxy['type'].upper()]
            s = socks.socksocket()
            s.set_proxy(proxy_type, proxy['host'], int(proxy['port']), True,
                        proxy.get('username'), proxy.get('password'))
        return s

    def connect(self, dest_host, dest_port):
        s = self.create_chain_socket()
        s.connect((dest_host, dest_port))
        return s

# Example usage:
# proxies = [
#     {'type': 'SOCKS5', 'host': '127.0.0.1', 'port': 9050},
#     {'type': 'HTTP', 'host': 'proxy.example.com', 'port': 8080}
# ]
# chain = ProxyChain(proxies)
# s = chain.connect('example.com', 80)
# s.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
# print(s.recv(4096))
