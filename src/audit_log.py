import json
import os
from datetime import datetime


class AuditLog:
    def __init__(self, log_file='data/audit.log'):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log_event(self, event_type: str, username: str, status: str, details: str = ""):
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'username': username,
            'status': status,
            'details': details
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def get_user_events(self, username: str):
        events = []
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    event = json.loads(line)
                    if event['username'] == username:
                        events.append(event)
        except FileNotFoundError:
            pass
        return events

    def export_report(self, output_file='reports/security_audit.json'):
        events = []
        try:
            with open(self.log_file, 'r') as f:
                events = [json.loads(line) for line in f]
        except FileNotFoundError:
            pass
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(events, f, indent=2)
        print(f"Report exported to {output_file}")
