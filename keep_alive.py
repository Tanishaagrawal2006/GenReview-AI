import time
import requests
import threading

def ping_server(url, interval=840):
    """
    Pings the specified URL every 'interval' seconds (default 14 minutes).
    Render free instances spin down after 15 minutes of inactivity.
    """
    while True:
        try:
            time.sleep(interval)
            response = requests.get(url)
            print(f"[Keep-Alive] Pinged {url} - Status Code: {response.status_code}")
        except Exception as e:
            print(f"[Keep-Alive] Error pinging server: {e}")

def keep_alive(url="https://restaurant-review-bpdu.onrender.com"):
    """
    Starts a background thread that continually pings the server.
    Call this function from your main app entry point (e.g., at the end of app.py).
    
    Example:
    from keep_alive import keep_alive
    keep_alive("https://my-reviewflow-app.onrender.com")
    """
    thread = threading.Thread(target=ping_server, args=(url,))
    thread.daemon = True
    thread.start()
    print(f"[Keep-Alive] Started background ping thread for {url}")

if __name__ == "__main__":
   
    import os
    app_url = os.getenv("RENDER_EXTERNAL_URL", "https://your-app-name.onrender.com")
    print(f"Starting standalone keep-alive script for {app_url}...")
    ping_server(app_url)
