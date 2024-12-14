import json
import os
from typing import Dict, List, Optional
from cryptfuncs import password_encrypt


class Storage:
    def __init__(self, file_path: str = 'passwords.json'):
        self.file_path = file_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        if not os.path.exists(self.file_path):
            self._save_data({'master_password': None, 'passwords': []})

    def _load_data(self) -> Dict:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            # If file is corrupted or can't be read, create a new one
            default_data = {'master_password': None, 'passwords': []}
            self._save_data(default_data)
            return default_data

    def _save_data(self, data: Dict):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save data: {str(e)}")

    def get_master_password(self) -> Optional[str]:
        data = self._load_data()
        return data['master_password']

    def set_master_password(self, password_hash: str):
        data = self._load_data()
        data['master_password'] = password_hash
        self._save_data(data)

    def get_passwords(self) -> List[Dict]:
        data = self._load_data()
        return data['passwords']

    def add_password(self, service: str, username: str, password: str, master_password: str, comments: str):
        data = self._load_data()
        data['passwords'].append({
            'service': service,
            'username': username,
            'password': password_encrypt(bytes(password, 'utf-8'),
                                         master_password).decode('utf-8'),
            'comments': password_encrypt(bytes(comments, 'utf-8'),
                                         master_password).decode('utf-8')
        })
        self._save_data(data)

    def delete_password(self, service: str, username: str) -> bool:
        data = self._load_data()
        initial_length = len(data['passwords'])
        data['passwords'] = [
            p for p in data['passwords']
            if not (p['service'] == service and p['username'] == username)
        ]
        if len(data['passwords']) < initial_length:
            self._save_data(data)
            return True
        return False
