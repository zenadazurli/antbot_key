# bot.py
# ============================================================
# BOT CON ROTAZIONE KEY
# ============================================================

import time
import logging
import random
import requests
from datetime import datetime
from config import BOT_KEYS, SLEEP_INTERVAL, MAX_RETRIES, TIMEOUT, REQUEST_DELAY, LOG_LEVEL

# Configura logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class BrowserUseBot:
    """Bot con rotazione di 10 API Key"""
    
    def __init__(self):
        self.keys = BOT_KEYS
        self.current_key_index = 0
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.key_usage = {key: 0 for key in self.keys}
        
        logger.info(f"🚀 Bot avviato con {len(self.keys)} key in rotazione")
        logger.info(f"📋 Key: {', '.join([k[:15] + '...' for k in self.keys])}")
    
    def get_next_key(self):
        """Restituisce la prossima key in rotazione (round-robin)"""
        key = self.keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        self.key_usage[key] = self.key_usage.get(key, 0) + 1
        return key
    
    def get_random_key(self):
        """Restituisce una key casuale"""
        key = random.choice(self.keys)
        self.key_usage[key] = self.key_usage.get(key, 0) + 1
        return key
    
    def make_request(self, url, method="GET", data=None, headers=None):
        """Effettua una richiesta con rotazione key e retry"""
        
        key = self.get_next_key()
        self.total_requests += 1
        
        # Headers base
        base_headers = {
            "X-Browser-Use-API-Key": key,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        if headers:
            base_headers.update(headers)
        
        # Tentativi con retry
        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"🔄 Tentativo {attempt + 1}/{MAX_RETRIES} con key: {key[:15]}...")
                
                if method.upper() == "GET":
                    response = requests.get(url, headers=base_headers, timeout=TIMEOUT)
                elif method.upper() == "POST":
                    response = requests.post(url, json=data, headers=base_headers, timeout=TIMEOUT)
                else:
                    response = requests.request(method, url, json=data, headers=base_headers, timeout=TIMEOUT)
                
                if response.status_code == 200:
                    self.successful_requests += 1
                    logger.info(f"✅ Richiesta OK (key: {key[:15]}...) - Status: {response.status_code}")
                    return response.json() if response.text else None
                else:
                    logger.warning(f"⚠️ Status {response.status_code} con key: {key[:15]}...")
                    
                    # Se 401 o 403, la key potrebbe essere scaduta
                    if response.status_code in [401, 403]:
                        logger.warning(f"🔑 Key {key[:15]}... potrebbe essere scaduta! Passo alla prossima.")
                        key = self.get_next_key()  # Passa alla prossima key
                        base_headers["X-Browser-Use-API-Key"] = key
                        continue
                    
                    # Se 429, troppe richieste
                    if response.status_code == 429:
                        logger.warning(f"⏳ Rate limit! Aspetto 5 secondi...")
                        time.sleep(5)
                        continue
                    
                    return None
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏰ Timeout con key: {key[:15]}... (tentativo {attempt + 1})")
                if attempt == MAX_RETRIES - 1:
                    self.failed_requests += 1
                    return None
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Errore: {e} (tentativo {attempt + 1})")
                if attempt == MAX_RETRIES - 1:
                    self.failed_requests += 1
                    return None
                time.sleep(2)
        
        self.failed_requests += 1
        return None
    
    def test_keys(self):
        """Testa tutte le key per verificare che funzionino"""
        
        logger.info("🧪 Test di tutte le key...")
        
        url = "https://api.browser-use.com/api/v2/profiles?pageNumber=1&pageSize=100"
        
        for i, key in enumerate(self.keys):
            headers = {
                "X-Browser-Use-API-Key": key,
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    logger.info(f"   ✅ Key {i+1}: {key[:15]}... FUNZIONA")
                else:
                    logger.warning(f"   ⚠️ Key {i+1}: {key[:15]}... STATUS {response.status_code}")
            except Exception as e:
                logger.error(f"   ❌ Key {i+1}: {key[:15]}... ERRORE: {e}")
            
            time.sleep(0.5)
    
    def get_stats(self):
        """Restituisce le statistiche del bot"""
        return {
            "total_requests": self.total_requests,
            "successful": self.successful_requests,
            "failed": self.failed_requests,
            "success_rate": round(self.successful_requests / max(1, self.total_requests) * 100, 2),
            "key_usage": self.key_usage
        }
    
    def run(self):
        """Ciclo principale del bot"""
        
        logger.info("🔄 Avvio ciclo principale...")
        
        # Test iniziale delle key
        self.test_keys()
        
        while True:
            try:
                # Qui metti la logica principale del bot
                # Esempio: chiamata a un endpoint
                result = self.make_request("https://api.browser-use.com/api/v2/profiles?pageNumber=1&pageSize=100")
                
                if result:
                    logger.info(f"📊 Profili trovati: {len(result.get('items', []))}")
                
                # Mostra statistiche ogni 10 cicli
                if self.total_requests % 10 == 0 and self.total_requests > 0:
                    stats = self.get_stats()
                    logger.info(f"📊 Statistiche: {stats['successful']}/{stats['total_requests']} successi ({stats['success_rate']}%)")
                
                # Attesa prima del prossimo ciclo
                logger.debug(f"⏳ Attesa {SLEEP_INTERVAL} secondi...")
                time.sleep(SLEEP_INTERVAL)
                
            except KeyboardInterrupt:
                logger.info("🛑 Bot fermato dall'utente")
                break
                
            except Exception as e:
                logger.error(f"❌ Errore nel ciclo principale: {e}")
                time.sleep(10)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("  🤖 BROWSER-USE BOT (10 KEY IN ROTAZIONE)")
    print("="*60)
    
    bot = BrowserUseBot()
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot fermato")
    finally:
        stats = bot.get_stats()
        print("\n" + "="*60)
        print("  📊 STATISTICHE FINALI")
        print("="*60)
        print(f"   Richieste totali: {stats['total_requests']}")
        print(f"   Successi: {stats['successful']}")
        print(f"   Falliti: {stats['failed']}")
        print(f"   Tasso di successo: {stats['success_rate']}%")
        print("="*60)