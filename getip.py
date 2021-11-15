
"""
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()
"""

from pyngrok import ngrok

ssh_tunnel = ngrok.connect(8485, 'tcp')

print(ssh_tunnel)
