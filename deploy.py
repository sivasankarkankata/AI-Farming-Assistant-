# deploy.py
import subprocess
import sys
import os
import time
import webbrowser
import platform

def check_ngrok():
    try:
        subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def start_app_with_ngrok():
    print("🌾 AI Farming Assistant - Global Deployment")
    print("="*50)
    
    # Check ngrok
    if not check_ngrok():
        print("❌ Ngrok not found!")
        print("📥 Install from: https://ngrok.com/download")
        return
    
    # Start Flask app in background
    print("🚀 Starting Flask application...")
    flask_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)
    
    # Start ngrok
    print("🔄 Creating public tunnel...")
    ngrok_process = subprocess.Popen(
        ['ngrok', 'http', '5000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(3)
    
    # Get public URL
    try:
        import requests
        response = requests.get('http://localhost:4040/api/tunnels')
        data = response.json()
        public_url = data['tunnels'][0]['public_url']
        
        print("\n✅ SUCCESS! Your app is now live!")
        print("="*50)
        print(f"🌐 Public URL: {public_url}")
        print("="*50)
        print("\n📱 Share this URL with anyone in India:")
        print(f"🔗 {public_url}")
        print("\n🔒 HTTPS secured")
        print("⚡ Fast connection via ngrok")
        print("\n⚠️  Keep this terminal window open")
        print("⚠️  Press Ctrl+C to stop")
        
        # Open in browser
        webbrowser.open(public_url)
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            flask_process.terminate()
            ngrok_process.terminate()
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    start_app_with_ngrok()