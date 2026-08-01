#!/usr/bin/env python3
# bot_antautosurf_complete.py
# BOT COMPLETO: ProxyScrape (100 proxy) → Browser-USE (fallback) → Request Dirette

import requests
import time
import logging
import re
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# 🔧 CONFIGURAZIONE
# ============================================================

# 🔥 100 PROXY DI PROXYSCRAPE
PROXYSCRAPE_LIST = [
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.43.190:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.252.171:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.32.85:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.48.208:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.42.199:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.39.185:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.21.196:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.14.254:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.3.169:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@193.56.28.124:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.34.92:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.51.46:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.43.13:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.28.203:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.232.26:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.174.73:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.27.236:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.1.250:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.167.19.18:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.43.3:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.189.1:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.245.26:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.55.49:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.253.210:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.36.176:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.238.37:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.34.21:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.36.122:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.47.73:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.11.245:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.20.87:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.231.208:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.41.221:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.1.198:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.22.10:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.178.206:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.164.36:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.236.234:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.182.0:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.55.63:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.189.172:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.49.68:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.30.128:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.34.51:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@195.63.31.110:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.239.217:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.167.19.210:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.52.201:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.20.121:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.45.250:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.183.220:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.13.141:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.234.91:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.227.28:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.233.30:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.169.125:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.63.146:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.46.186:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.238.76:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@217.181.91.68:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.44.77:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.53.250:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.38.189:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.52.109:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.4.45:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.6.112:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.188.162:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.5.19:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.168.90:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.22.163:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.10.14:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.22.90:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.56.156:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.40.156:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.240.189:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.183.95:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.41.110:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.38.67:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.8.19:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.235.160:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.53.90:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.167.25.58:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.41.182:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.175.134:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.63.116:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@45.3.62.83:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.177.110:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@209.50.191.47:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.250.175:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.225.45:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@151.123.177.189:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.60.161:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.40.52:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.239.26:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@65.111.25.234:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.41.236:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.63.1:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@104.207.62.200:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@216.26.225.59:3129",
    "yxgoqj9ooo9c:zbznhcy7jx6kkwq@195.63.31.153:3129"
]

# Account Antautosurf
ANTA_USER = "luigitaschi@gmail.com"
ANTA_PASS = "carxzava"

# Browser-USE API Key (fallback)
BROWSER_USE_KEY = "bu_vpqaFMR7fG2iGto2Z9oLXXL8M3Fkm25Y87_BwKp2aAU"

# ============================================================
# ROTAZIONE PROXY
# ============================================================

class ProxyRotator:
    """Gestisce la rotazione dei proxy per evitare ripetizioni"""
    
    def __init__(self, proxy_list):
        self.proxies = []
        for p in proxy_list:
            parsed = self.parse_proxy(p)
            if parsed:
                self.proxies.append(parsed)
        self.index = 0
        self.used = set()
    
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
        if not self.proxies:
            return None
        
        for i in range(len(self.proxies)):
            idx = (self.index + i) % len(self.proxies)
            proxy = self.proxies[idx]
            host = proxy['host']
            
            if host not in self.used:
                self.index = idx + 1
                self.used.add(host)
                return proxy
        
        self.used.clear()
        proxy = self.proxies[self.index % len(self.proxies)]
        self.index += 1
        return proxy

# ============================================================
# LIVELLO 1: PROXYSCRAPE
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
    
    for i in range(20):
        proxy = rotator.get_next()
        if not proxy:
            break
        
        result = test_proxy(proxy)
        if result['success']:
            print(f"   ✅ Proxy funzionante: {proxy['host']} ({result['time']:.2f}s)")
            return proxy
        
        print(f"   ❌ Proxy morto: {proxy['host']}")
    
    print("   ❌ Nessun proxy funzionante")
    return None

def get_csrf_with_proxy(proxy):
    """Tenta di ottenere CSRF usando il proxy"""
    
    print("🌐 Navigo su Antautosurf con proxy...")
    
    session = requests.Session()
    if proxy:
        session.proxies.update({'http': proxy['http'], 'https': proxy['https']})
    
    try:
        response = session.get("https://antautosurf.com/", timeout=30)
        print(f"   📡 Status: {response.status_code}")
        
        if response.status_code != 200:
            return None, session
        
        # Cerca CSRF
        csrf_match = re.search(r'csrf_token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)', response.text)
        if csrf_match:
            csrf = csrf_match.group(1)
            print(f"   ✅ CSRF trovato: {csrf}")
            return csrf, session
        
        # Prova login
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
# LIVELLO 2: BROWSER-USE (FALLBACK)
# ============================================================

async def get_csrf_with_browseruse_async():
    """Usa Browser-USE per ottenere il CSRF (fallback)"""
    
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
            
            # Inserisci email
            email_input = await page.query_selector('input[name="bitcoinwallet"]')
            if email_input:
                await email_input.fill(ANTA_USER)
                print("   ✅ Email inserita")
            
            # Clicca Enter
            enter_btn = await page.query_selector('input[value*="Enter"]')
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
    """Wrapper sincrono per Browser-USE"""
    return asyncio.run(get_csrf_with_browseruse_async())

# ============================================================
# REQUEST DIRETTE (SENZA PROXY)
# ============================================================

def make_direct_request(csrf_token, session):
    """Fai una request diretta (senza proxy) con il CSRF"""
    
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
# BOT PRINCIPALE
# ============================================================

def main():
    print("="*60)
    print("  🤖 BOT ANTAUTOSURF COMPLETO")
    print("="*60)
    print("   Livello 1: ProxyScrape (100 proxy)")
    print("   Livello 2: Browser-USE (fallback)")
    print("   Request: Dirette (senza proxy)")
    print("="*60)
    print(f"   Utente: {ANTA_USER}")
    print("="*60)
    
    # Inizializza rotatore proxy
    rotator = ProxyRotator(PROXYSCRAPE_LIST)
    print(f"📋 {len(rotator.proxies)} proxy pronti")
    
    # ============================================================
    # LIVELLO 1: PROXYSCRAPE
    # ============================================================
    
    proxy = get_working_proxy(rotator)
    csrf = None
    session = None
    
    if proxy:
        csrf, session = get_csrf_with_proxy(proxy)
    
    # ============================================================
    # LIVELLO 2: BROWSER-USE (FALLBACK)
    # ============================================================
    
    if not csrf:
        print("\n" + "="*60)
        print("  ⚠️ PROXY FALLITO, PASSO A BROWSER-USE")
        print("="*60)
        csrf = get_csrf_with_browseruse()
    
    # ============================================================
    # REQUEST DIRETTE
    # ============================================================
    
    if not csrf:
        print("\n❌ Impossibile ottenere CSRF")
        return
    
    print(f"\n🔑 CSRF: {csrf}")
    
    if not session:
        session = requests.Session()
    
    result = make_direct_request(csrf, session)
    
    if result:
        print("\n" + "="*60)
        print("  🎯 BOT COMPLETATO CON SUCCESSO!")
        print("="*60)
        print(f"📄 Response: {result[:500]}...")
    else:
        print("\n" + "="*60)
        print("  ❌ BOT FALLITO")
        print("="*60)

if __name__ == "__main__":
    main()
