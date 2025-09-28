import http.server
import socketserver
import threading
import logging
import socket
import urllib.request
import subprocess
import shlex
from core.proxy_chain import ProxyChain

class LightHTTPServer:
    def __init__(self, port):
        self.port = port
        self.handler = http.server.SimpleHTTPRequestHandler
        self.httpd = None
        self.thread = None
        self.is_running = False
    
    def start(self, output_callback):
        def run_server():
            try:
                self.httpd = socketserver.TCPServer(("", self.port), self.handler)
                output_callback(f"HTTP server running on port {self.port}")
                output_callback(f"Serving from: http://localhost:{self.port}")
                self.is_running = True
                self.httpd.serve_forever()
            except Exception as e:
                output_callback(f"Server error: {e}")
                self.is_running = False
        
        self.thread = threading.Thread(target=run_server)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.is_running = False

class SimpleHTTPProxyHandler(http.server.SimpleHTTPRequestHandler):
    proxy_chain = None  # Set this to a ProxyChain instance if needed
    def do_GET(self):
        import urllib.request
        try:
            url = self.path
            if url.startswith('/'):
                url = url[1:]
            if not url.startswith('http'):
                self.send_error(400, 'Bad URL')
                return
            if SimpleHTTPProxyHandler.proxy_chain:
                # Use proxy chain for outgoing connection
                s = SimpleHTTPProxyHandler.proxy_chain.connect(url.split('/')[2], 80)
                s.sendall(f"GET {self.path} HTTP/1.1\r\nHost: {url.split('/')[2]}\r\n\r\n".encode())
                resp = s.recv(65536)
                self.wfile.write(resp)
                s.close()
            else:
                with urllib.request.urlopen(url) as response:
                    self.send_response(response.status)
                    for k, v in response.getheaders():
                        self.send_header(k, v)
                    self.end_headers()
                    self.wfile.write(response.read())
        except Exception as e:
            self.send_error(502, f'Proxy error: {e}')

class LightHTTPProxyServer:
    def __init__(self, port):
        self.port = port
        self.handler = SimpleHTTPProxyHandler
        self.httpd = None
        self.thread = None
        self.is_running = False
    def start(self, output_callback):
        def run_server():
            try:
                self.httpd = socketserver.TCPServer(("", self.port), self.handler)
                output_callback(f"HTTP proxy running on port {self.port}")
                self.is_running = True
                self.httpd.serve_forever()
            except Exception as e:
                output_callback(f"Proxy server error: {e}")
                self.is_running = False
        self.thread = threading.Thread(target=run_server)
        self.thread.daemon = True
        self.thread.start()
    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.is_running = False

class ServerManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.servers = {}
    
    def start_http_server(self, port, output_callback):
        if port in self.servers:
            output_callback(f"Server already running on port {port}")
            return
        
        server = LightHTTPServer(port)
        self.servers[port] = server
        server.start(output_callback)
    
    def stop_server(self, port):
        if port in self.servers:
            self.servers[port].stop()
            del self.servers[port]
    
    def launch_program_on_server(self, port, file_path, args=None, output_callback=None):
        """Launch a program or script on the server's host machine."""
        if port not in self.servers:
            if output_callback:
                output_callback(f"No server running on port {port}")
            return False
        try:
            cmd = [file_path]
            if args:
                if isinstance(args, str):
                    cmd += shlex.split(args)
                elif isinstance(args, list):
                    cmd += args
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if output_callback:
                output_callback(f"Launched program: {file_path} (PID {proc.pid}) on server port {port}")
            return True
        except Exception as e:
            if output_callback:
                output_callback(f"Failed to launch program: {e}")
            return False
    
    def start_http_proxy(self, port, output_callback, proxy_chain_config=None):
        if port in self.servers:
            output_callback(f"Server already running on port {port}")
            return
        server = LightHTTPProxyServer(port)
        if proxy_chain_config:
            SimpleHTTPProxyHandler.proxy_chain = ProxyChain(proxy_chain_config)
        self.servers[port] = server
        server.start(output_callback)