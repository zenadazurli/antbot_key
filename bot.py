#!/usr/bin/env python3
# bot_antautosurf_complete.py
# BOT COMPLETO: ProxyScrape (100 proxy) → Browser-USE → Start Surf → Loop infinito

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

# ============================================================
# 🔥 100 PROXY AGGIORNATI (GENNAIO 2026)
# ============================================================

PROXYSCRAPE_LIST = [
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.47.43:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.239.104:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.172.12:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@217.181.90.251:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.168.130:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.32.175:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.57.73:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.9.66:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.50.243:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.236.9:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.26.73:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.249.47:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.48.250:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.39.220:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.10.76:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.56.160:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.182.210:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.167.25.71:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.48.82:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.55.237:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.160.11:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.185.22:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.240.42:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.40.107:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.36.201:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@151.123.176.232:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.181.6:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.40.168:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@151.123.176.108:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.29.193:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.22.174:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.246.45:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.11.56:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.42.151:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.31.105:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.40.198:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.53.111:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.50.88:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.183.59:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.246.240:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.184.63:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.230.0:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.236.71:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.238.110:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.177.238:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.14.2:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.51.239:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.188.131:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.1.5:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.22.117:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.31.208:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.232.21:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@151.123.177.216:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.10.206:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.173.158:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.162.165:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.235.71:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.234.82:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.228.26:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.167.157:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.50.248:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.37.112:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.169.19:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.249.78:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.62.246:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.253.173:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.43.184:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.5.26:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.51.13:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.249.76:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.224.5:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.60.235:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.63.174:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.38.74:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.249.106:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.4.82:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@217.181.91.147:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.37.121:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.8.30:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.169.170:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.14.137:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.9.247:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.12.4:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.53.97:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.186.64:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@216.26.247.208:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.184.140:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.10.110:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.7.201:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.51.140:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.37.99:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@104.207.45.112:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.40.164:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.160.82:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.171.160:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@45.3.52.191:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.183.220:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.170.80:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@209.50.163.32:3129",
    "3ryexlvjrecm:e78o06ke4auyk2j@65.111.13.2:3129"
]

# ============================================================
# SMART PROXY ROTATOR (MANTIENE LA STESSA LOGICA)
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
                'host': host,
                'user': user,
                'password': password
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
            
            enter_btn = await page.wait_for_selector('input[value*="Enter"]', timeout=30000)
            if enter_btn:
                await enter_btn.click()
                print("   ✅ Cliccato su Enter")
            
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
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
            
            if "Please Click Similar" in await page.content():
                captcha_btn = await page.query_selector('a[href*="cid="]')
                if captcha_btn:
                    await captcha_btn.click()
                    print("   ✅ Captcha risolto")
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
            
            # 🚀 CLICCA SU START SURF
            print("   🚀 Clicco su Start Surf...")
            try:
                start_btn = await page.wait_for_selector(
                    '#button1, input[value*="Start Surf"], .submit3', 
                    timeout=30000
                )
                if start_btn:
                    await start_btn.click()
                    print("   ✅ Start Surf cliccato!")
                    await asyncio.sleep(3)
                    print("   ⏱️ Timer partito!")
            except Exception as e:
                print(f"   ⚠️ Errore Start Surf: {e}")
            
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
    
    proxy = get_working_proxy(rotator)
    csrf = None
    session = None
    browser_use_used = False
    
    if proxy:
        csrf, session = get_csrf_with_proxy(proxy)
        if not csrf:
            rotator.mark_failed(proxy)
    
    if not csrf:
        print("\n" + "="*60)
        print("  ⚠️ PROXY FALLITO, PASSO A BROWSER-USE")
        print("="*60)
        browser_use_used = True
        csrf = get_csrf_with_browseruse()
    
    if not csrf:
        print("\n❌ Impossibile ottenere CSRF")
        return False
    
    print(f"\n🔑 CSRF: {csrf}")
    
    if not session:
        session = requests.Session()
    
    result = make_direct_request(csrf, session)
    
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
    print("   Livello 1: ProxyScrape (100 proxy, rotazione intelligente)")
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
