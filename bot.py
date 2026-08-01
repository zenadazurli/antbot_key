#!/usr/bin/env python3
# bot_antautosurf_complete.py
# BOT COMPLETO: ProxyScrape → Browser-USE → Start Surf → Loop infinito

import asyncio
import requests
import time
import re
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# 🔧 CONFIGURAZIONE
# ============================================================

ANTA_USER = "luigitaschi@gmail.com"
ANTA_PASS = "carxzava"

# Browser-USE Key (fallback)
BROWSER_USE_KEY = "bu_vpqaFMR7fG2iGto2Z9oLXXL8M3Fkm25Y87_BwKp2aAU"

# 🔥 100 PROXY DI PROXYSCRAPE
PROXYSCRAPE_LIST = [
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.43.190:3129",
    # ... tutti i 100 proxy
]

# ============================================================
# SMART PROXY ROTATOR
# ============================================================

class SmartProxyRotator:
    def __init__(self, proxy_list):
        self.proxies = []
        self.failed = set()
        self.used = set()
        self.current_index = 0
        
        for p in proxy_list:
            parsed = self.parse_proxy(p)
            if parsed:
                self.proxies.append(parsed)
        self.working_proxies = self.proxies.copy()
    
    def parse_proxy(self, proxy_str):
        try:
            auth, host = proxy_str.split('@')
            user, password = auth.split(':')
            return {
                'http': f'http://{user}:{password}@{host}',
                'https': f'http://{user}:{password}@{host}',
                'host': host
            }
        except:
            return None
    
    def get_next(self):
        if not self.working_proxies:
            self.working_proxies = self.proxies.copy()
            self.failed.clear()
        
        for i in range(len(self.working_proxies)):
            idx = (self.current_index + i) % len(self.working_proxies)
            proxy = self.working_proxies[idx]
            
            if proxy['host'] not in self.used and proxy['host'] not in self.failed:
                self.current_index = idx + 1
                self.used.add(proxy['host'])
                return proxy
        
        self.used.clear()
        proxy = self.working_proxies[self.current_index % len(self.working_proxies)]
        self.current_index += 1
        return proxy
    
    def mark_failed(self, proxy):
        if proxy and proxy['host'] not in self.failed:
            self.failed.add(proxy['host'])
            self.used.discard(proxy['host'])
            self.working_proxies = [p for p in self.working_proxies if p['host'] != proxy['host']]
            print(f"   🚫 Proxy {proxy['host']} marcato come fallito")
    
    def get_stats(self):
        return {
            'total': len(self.proxies),
            'working': len(self.working_proxies),
            'failed': len(self.failed),
            'used': len(self.used)
        }

# ============================================================
# TEST PROXY
# ============================================================

def test_proxy(proxy):
    try:
        start = time.time()
        r = requests.get('http://httpbin.org/ip', 
                        proxies={'http': proxy['http'], 'https': proxy['https']}, 
                        timeout=10)
        if r.status_code == 200:
            return {'success': True, 'proxy': proxy, 'time': time.time()-start}
    except:
        pass
    return {'success': False}

def get_working_proxy(rotator):
    print("🔍 ProxyScrape: cerco proxy funzionante...")
    
    for i in range(30):
        proxy = rotator.get_next()
        if not proxy:
            break
        
        result = test_proxy(proxy)
        if result['success']:
            print(f"   ✅ Proxy funzionante: {proxy['host']} ({result['time']:.2f}s)")
            return proxy
        else:
            rotator.mark_failed(proxy)
            print(f"   ❌ Proxy morto: {proxy['host']}")
    
    print("   ❌ Nessun proxy funzionante")
    return None

# ============================================================
# OTTIENI CSRF CON PROXY
# ============================================================

def get_csrf_with_proxy(proxy):
    print("🌐 Navigo su Antautosurf con proxy...")
    
    session = requests.Session()
    if proxy:
        session.proxies.update({'http': proxy['http'], 'https': proxy['https']})
    
    try:
        response = session.get("https://antautosurf.com/", timeout=30)
        print(f"   📡 Status: {response.status_code}")
        
        if response.status_code != 200:
            return None, session
        
        csrf_match = re.search(r'csrf_token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)', response.text)
        if csrf_match:
            csrf = csrf_match.group(1)
            print(f"   ✅ CSRF trovato: {csrf}")
            return csrf, session
        
        print("   📝 Provo login...")
        login_data = {"bitcoinwallet": ANTA_USER}
        response = session.post("https://antautosurf.com/index.php", data=login_data, timeout=30)
        
        csrf_match = re.search(r'csrf_token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)', response.text)
        if csrf_match:
            csrf = csrf_match.group(1)
            print(f"   ✅ CSRF trovato dopo login: {csrf}")
            return csrf, session
        
        return None, session
        
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return None, session

# ============================================================
# BROWSER-USE FALLBACK
# ============================================================

async def get_csrf_with_browseruse_async():
    print("🔍 Browser-USE: fallback attivato...")
    print("   🧪 Avvio Browser-USE...")
    
    try:
        from browser_use_sdk.v3 import AsyncBrowserUse
        from playwright.async_api import async_playwright
        
        client = AsyncBrowserUse(api_key=BROWSER_USE_KEY)
        browser = await client.browsers.create()
        
        async with async_playwright() as p:
            pw_browser = await p.chromium.connect_over_cdp(browser.cdp_url)
            context = pw_browser.contexts[0]
            page = context.pages[0]
            
            print("   🌐 Apro Antautosurf...")
            await page.goto("https://antautosurf.com/")
            await page.wait_for_load_state("networkidle")
            
            email_input = await page.query_selector('input[name="bitcoinwallet"]')
            if email_input:
                await email_input.fill(ANTA_USER)
                print("   ✅ Email inserita")
            
            # Clicca su Enter & Earn Crypto
            enter_btn = await page.wait_for_selector('input[value*="Enter"]', timeout=30000)
            if enter_btn:
                await enter_btn.click()
                print("   ✅ Cliccato su Enter")
            
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            # Se richiede password
            if "Please enter Password" in await page.content():
                pass_input = await page.query_selector('input[name="password"]')
                if pass_input:
                    await pass_input.fill(ANTA_PASS)
                    print("   ✅ Password inserita")
                
                enter_btn = await page.query_selector('input[value="Enter"]')
                if enter_btn:
                    await enter_btn.click()
                    print("   ✅ Cliccato su Enter")
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
            
            # Se captcha
            if "Please Click Similar" in await page.content():
                captcha_btn = await page.query_selector('a[href*="cid="]')
                if captcha_btn:
                    await captcha_btn.click()
                    print("   ✅ Captcha risolto")
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
            
            # 🔥 CLICCA SU START SURF
            print("   🚀 Clicco su Start Surf...")
            try:
                start_btn = await page.wait_for_selector(
                    '#button1, input[value*="Start Surf"], .submit3', 
                    timeout=30000
                )
                if start_btn:
                    await start_btn.click()
                    print("   ✅ Start Surf cliccato!")
                    
                    # Aspetta che il timer inizi
                    await asyncio.sleep(3)
                    print("   ⏱️ Timer partito!")
                else:
                    print("   ⚠️ Start Surf non trovato")
            except Exception as e:
                print(f"   ⚠️ Errore Start Surf: {e}")
            
            # Cerca CSRF nella pagina
            html = await page.content()
            csrf_match = re.search(r'csrf_token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)', html)
            
            if csrf_match:
                csrf = csrf_match.group(1)
                print(f"   ✅ CSRF trovato con Browser-USE: {csrf}")
                await pw_browser.close()
                await client.browsers.stop(browser.id)
                return csrf
            
            await pw_browser.close()
            await client.browsers.stop(browser.id)
            return None
            
    except Exception as e:
        print(f"   ❌ Browser-USE fallito: {e}")
        return None

def get_csrf_with_browseruse():
    return asyncio.run(get_csrf_with_browseruse_async())

# ============================================================
# REQUEST DIRETTA
# ============================================================

def make_direct_request(csrf_token, session):
    print("\n📡 Request diretta (senza proxy)...")
    
    url = "https://antautosurf.com/index.php"
    params = {
        "bitcoinwallet": ANTA_USER,
        "csrf_token": csrf_token
    }
    
    try:
        session.proxies.clear()
        response = session.get(url, params=params, timeout=30)
        print(f"   📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Request diretta riuscita!")
            return response.text
        else:
            print(f"   ❌ Errore: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return None

# ============================================================
# SINGOLA SESSIONE
# ============================================================

def esegui_sessione():
    """Esegue una singola sessione del bot"""
    
    print("\n" + "="*60)
    print("  🤖 BOT ANTAUTOSURF - SESSIONE")
    print("="*60)
    print(f"   Utente: {ANTA_USER}")
    print("="*60)
    
    rotator = SmartProxyRotator(PROXYSCRAPE_LIST)
    print(f"📋 {len(rotator.proxies)} proxy pronti")
    
    # Livello 1: ProxyScrape
    proxy = get_working_proxy(rotator)
    csrf = None
    session = None
    browser_use_used = False
    
    if proxy:
        csrf, session = get_csrf_with_proxy(proxy)
        if not csrf:
            rotator.mark_failed(proxy)
    
    # Livello 2: Browser-USE (fallback)
    if not csrf:
        print("\n" + "="*60)
        print("  ⚠️ PROXY FALLITO, PASSO A BROWSER-USE")
        print("="*60)
        browser_use_used = True
        csrf = get_csrf_with_browseruse()
    
    # Request diretta
    if not csrf:
        print("\n❌ Impossibile ottenere CSRF")
        return False
    
    print(f"\n🔑 CSRF: {csrf}")
    
    if not session:
        session = requests.Session()
    
    result = make_direct_request(csrf, session)
    
    # Statistiche
    stats = rotator.get_stats()
    print("\n" + "="*60)
    print("  📊 STATISTICHE PROXY")
    print("="*60)
    print(f"   Proxy totali: {stats['total']}")
    print(f"   Proxy funzionanti: {stats['working']}")
    print(f"   Proxy falliti: {stats['failed']}")
    print(f"   Proxy usati: {stats['used']}")
    print(f"   Browser-USE usato: {'SI' if browser_use_used else 'NO'}")
    print("="*60)
    
    if result:
        print("\n" + "="*60)
        print("  🎯 SESSIONE COMPLETATA CON SUCCESSO!")
        print("="*60)
        return True
    else:
        print("\n" + "="*60)
        print("  ❌ SESSIONE FALLITA")
        print("="*60)
        return False

# ============================================================
# MAIN - LOOP INFINITO
# ============================================================

def main():
    print("="*60)
    print("  🤖 BOT ANTAUTOSURF (LOOP INFINITO)")
    print("="*60)
    print("   Livello 1: ProxyScrape (rotazione intelligente)")
    print("   Livello 2: Browser-USE (fallback)")
    print("   Request: Dirette (senza proxy)")
    print("   🚀 Start Surf: ATTIVO (guadagna punti!)")
    print("   Modalità: Continuo (loop infinito)")
    print("="*60)
    
    ciclo = 0
    
    while True:
        ciclo += 1
        print(f"\n🔄 CICLO {ciclo}")
        print("="*60)
        
        try:
            successo = esegui_sessione()
            
            if successo:
                print("\n⏳ Attesa 60 secondi prima del prossimo ciclo...")
                time.sleep(60)
            else:
                print("\n⏳ Attesa 30 secondi prima di riprovare...")
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 Bot fermato dall'utente")
            break
            
        except Exception as e:
            print(f"\n❌ Errore nel ciclo: {e}")
            print("⏳ Attesa 30 secondi prima di riprovare...")
            time.sleep(30)

if __name__ == "__main__":
    main()
