"""
Cloudflare Workers 临时邮箱服务
API: https://mail-api.hznan0629.cloud
"""

import requests
import time
import random
import string


class CloudflareEmailService:
    def __init__(self, api_base="https://mail-api.hznan0629.cloud"):
        self.api_base = api_base.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        })
    
    def create_email(self):
        """创建临时邮箱，返回 (email, token)"""
        # 生成随机邮箱前缀
        prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        email = f"{prefix}@hznan0629.cloud"
        
        try:
            resp = self.session.post(
                f"{self.api_base}/api/new_address",
                json={"name": prefix},
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                return email, data.get("token") or email
            else:
                raise Exception(f"创建邮箱失败: {resp.status_code} - {resp.text[:200]}")
        
        except Exception as e:
            raise Exception(f"Cloudflare 邮箱创建失败: {e}")
    
    def get_messages(self, email):
        """获取邮件列表"""
        try:
            resp = self.session.get(
                f"{self.api_base}/api/mails/{email}",
                timeout=10
            )
            
            if resp.status_code == 200:
                return resp.json()
            return []
        
        except Exception:
            return []
    
    def get_message_content(self, email, message_id):
        """获取邮件内容"""
        try:
            resp = self.session.get(
                f"{self.api_base}/api/mails/{email}/{message_id}",
                timeout=10
            )
            
            if resp.status_code == 200:
                return resp.json()
            return None
        
        except Exception:
            return None
