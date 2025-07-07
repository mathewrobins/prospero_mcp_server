import socketserver
import json
from prospero_client import ProsperoClient
import yaml

class MCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        prospero = ProsperoClient()
        
        # Receive data from Smithery.ai
        data = self.request.recv(1024).decode('utf-8').strip()
        if not data:
            return
        
        try:
            # Parse JSON request
            payload = json.loads(data)
            domain = payload.get("domain")
            first_name = payload.get("first_name")
            last_name = payload.get("last_name")
            
            # Validate input
            if not all([domain, first_name, last_name]):
                response = {"error": "Missing required fields"}
            else:
                # Fetch email from Prospero
                result = prospero.find_email(domain, first_name, last_name)
                response = {
                    "domain": domain,
                    "first_name": first_name,
                    "last_name": last_name,
                    "result": result
                }
        except json.JSONDecodeError:
            response = {"error": "Invalid JSON format"}
        
        # Send response to Smithery.ai
        self.request.sendall(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    HOST = config['server']['host']
    PORT = config['server']['port']
    
    server = socketserver.TCPServer((HOST, PORT), MCPHandler)
    print(f"MCP Server running on {HOST}:{PORT}")
    server.serve_forever()