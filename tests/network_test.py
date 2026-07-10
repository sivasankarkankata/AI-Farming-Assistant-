# network_test.py
import socket
import requests

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

def test_connection():
    ip = get_local_ip()
    port = 5000
    
    print("🌾 AI Farming Assistant - Network Test")
    print("="*50)
    print(f"📡 Your Computer IP: {ip}")
    print(f"📱 Your Phone IP: 100.112.223.189")
    print("="*50)
    print("\n✅ To access from your phone, enter this URL:")
    print(f"🔗 http://{ip}:{port}")
    print("\n⚠️  Make sure both devices are on the same WiFi")
    print("⚠️  Your computer's firewall must allow port 5000")
    print("="*50)

if __name__ == '__main__':
    test_connection()