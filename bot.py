#!/usr/bin/env python3
# bot_antautosurf_final.py
# BOT DEFINITIVO: ProxyFinder (100 proxy) + Auto-Generazione API Key

import asyncio
import requests
import time
import re
import json
import random
import subprocess
import sys
import os
from datetime import datetime

# ============================================================
# 🔧 CONFIGURAZIONE
# ============================================================

ANTA_USER = "luigitaschi@gmail.com"
ANTA_PASS = "carxzava"

# ============================================================
# 🔥 100 PROXY PROXYSCRAPE
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
# PROXY MANAGER CON CACHE DEI FALLITI
# ============================================================

class ProxyManager:
    def __init__(self, proxy_list):
        self.proxies = []
        self.failed_proxies = set()  # Proxy che hanno fallito su Antautosurf
        self.blacklisted = set()      # Proxy che hanno già fallito molte volte
        self.current_index = 0
        self.stats = {'tested': 0, 'working': 0, 'failed': 0}
        
        for p in proxy_list:
            parsed = self.parse_proxy(p)
            if parsed:
                self.proxies.append(parsed)
        
        print(f"📋 {len(self.proxies)} proxy caricati")
    
    def parse_proxy(self, proxy_str):
        try:
            auth, host = proxy_str.split('@')
            user, password = auth.split(':')
            return {
                'http': f'http://{user}:{password}@{host}',
                'https': f'http://{user}:{password}@{host}',
                'host': host,
                'user': user,
                'password': password,
                'fail_count': 0
            }
        except:
            return None
    
    def get_next_proxy(self):
        """Ottiene il prossimo proxy NON fallito"""
        # Salta proxy già falliti o blacklistati
        for i in range(len(self.proxies)):
            idx = (self.current_index + i) % len(self.proxies)
            proxy = self.proxies[idx]
            
            if proxy['host'] not in self.failed_proxies and proxy['host'] not in self.blacklisted:
                self.current_index = (idx + 1) % len(self.proxies)
                return proxy
        
        # Se tutti sono falliti, resetta
        print("   🔄 Tutti i proxy falliti, reset...")
        self.failed_proxies.clear()
        self.current_index = 0
        return self.proxies[0] if self.proxies else None
    
    def mark_failed(self, proxy, reason=""):
        """Marca un proxy come fallito"""
        if proxy and proxy['host'] not in self.failed_proxies:
            self.failed_proxies.add(proxy['host'])
            self.stats['failed'] += 1
            print(f"   🚫 Proxy {proxy['host']} fallito: {reason}")
    
    def test_proxy(self, proxy):
        """Testa il proxy su Antautosurf"""
        try:
            session = requests.Session()
            session.proxies.update({'http': proxy['http'], 'https': proxy['https']})
            session.timeout = 15
            
            response = session.get("https://antautosurf.com/", timeout=15)
            
            if response.status_code == 200 and ("bitcoinwallet" in response.text or "csrf_token" in response.text):
                return {'success': True, 'proxy': proxy, 'session': session}
            else:
                return {'success': False, 'reason': f'Status {response.status_code}'}
                
        except requests.exceptions.ProxyError:
            return {'success': False, 'reason': 'ProxyError'}
        except requests.exceptions.ConnectTimeout:
            return {'success': False, 'reason': 'ConnectTimeout'}
        except requests.exceptions.ReadTimeout:
            return {'success': False, 'reason': 'ReadTimeout'}
        except Exception as e:
            return {'success': False, 'reason': str(e)[:50]}
    
    def find_working_proxy(self, max_tests=30):
        """Trova un proxy funzionante"""
        print("🔍 Cerco proxy funzionante su Antautosurf...")
        
        tested = 0
        while tested < max_tests:
            proxy = self.get_next_proxy()
            if not proxy:
                break
            
            tested += 1
            self.stats['tested'] += 1
            print(f"   🧪 Test {tested}/{max_tests}: {proxy['host']}...", end=" ")
            
            result = self.test_proxy(proxy)
            
            if result['success']:
                print("✅ OK!")
                self.stats['working'] += 1
                return result['proxy'], result['session']
            else:
                print(f"❌ {result.get('reason', 'fallito')}")
                self.mark_failed(proxy, result.get('reason', ''))
        
        print("   ❌ Nessun proxy funzionante trovato")
        return None, None

# ============================================================
# GENERATORE API KEY BROWSER-USE (AUTO)
# ============================================================

def genera_nuova_api_key():
    """Genera una nuova API Key Browser-USE"""
    print("   🔑 Generazione nuova API Key...")
    
    try:
        # Esegue lo script di generazione
        result = subprocess.run(
            [sys.executable, 'browseruse_full_automation_headless.py', '--headless'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            # Legge il file account.json
            try:
                with open('account.json', 'r') as f:
                    data = json.load(f)
                    api_key = data.get('api_key')
                    if api_key:
                        print(f"   ✅ Nuova API Key generata: {api_key[:20]}...")
                        return api_key
            except:
                pass
        
        print(f"   ❌ Generazione fallita: {result.stderr[:100]}")
        return None
        
    except Exception as e:
        print(f"   ❌ Errore generazione: {e}")
        return None

# ============================================================
# BROWSER-USE CON ROTAZIONE API KEY
# ============================================================

class BrowserUseManager:
    def __init__(self):
        self.keys = []
        self.current_key = None
        self.failed_keys = set()
        self.keys_file = 'browseruse_keys.json'
        self.load_keys()
    
    def load_keys(self):
        """Carica le API Key dal file"""
        try:
            if os.path.exists(self.keys_file):
                with open(self.keys_file, 'r') as f:
                    self.keys = json.load(f)
                print(f"📂 Caricate {len(self.keys)} API Key")
            else:
                print("📂 Nessuna API Key salvata")
                self.keys = []
        except:
            self.keys = []
    
    def save_keys(self):
        """Salva le API Key"""
        try:
            with open(self.keys_file, 'w') as f:
                json.dump(self.keys, f, indent=2)
        except:
            pass
    
    def add_key(self, api_key):
        """Aggiunge una nuova API Key"""
        if api_key not in self.keys:
            self.keys.append(api_key)
            self.save_keys()
            return True
        return False
    
    def get_next_key(self):
        """Ottiene la prossima API Key disponibile"""
        if not self.keys:
            print("   🔑 Genero nuova API Key (pool vuoto)...")
            new_key = genera_nuova_api_key()
            if new_key:
                self.add_key(new_key)
                return new_key
            return None
        
        for key in self.keys:
            if key not in self.failed_keys:
                self.current_key = key
                return key
        
        # Tutte le key fallite, proviamo a generarne una nuova
        print("   🔑 Tutte le key fallite, genero nuova...")
        new_key = genera_nuova_api_key()
        if new_key:
            self.add_key(new_key)
            return new_key
        
        return None
    
    def mark_failed(self, key):
        """Marca una key come fallita"""
        if key and key not in self.failed_keys:
            self.failed_keys.add(key)
            print(f"   🚫 API Key {key[:20]}... fallita")

# ============================================================
# BROWSER-USE FALLBACK
# ============================================================

async def get_csrf_with_browseruse_async(api_key, anta_user, anta_pass):
    """Ottiene CSRF usando Browser-USE"""
    print(f"   🧪 Browser-USE: {api_key[:20]}...")
    
    try:
        from browser_use_sdk.v3 import AsyncBrowserUse
        from playwright.async_api import async_playwright
        
        client = AsyncBrowserUse(api_key=api_key)
        browser = await client.browsers.create()
        
        async with async_playwright() as p:
            pw_browser = await p.chromium.connect_over_cdp(browser.cdp_url)
            context = pw_browser.contexts[0]
            page = context.pages[0]
            
            await page.goto("https://antautosurf.com/")
            await page.wait_for_load_state("networkidle")
            
            email_input = await page.query_selector('input[name="bitcoinwallet"]')
            if email_input:
                await email_input.fill(anta_user)
            
            enter_btn = await page.wait_for_selector('input[value*="Enter"]', timeout=30000)
            if enter_btn:
                await enter_btn.click()
            
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)
            
            if "Please enter Password" in await page.content():
                pass_input = await page.query_selector('input[name="password"]')
                if pass_input:
                    await pass_input.fill(anta_pass)
                
                enter_btn = await page.query_selector('input[value="Enter"]')
                if enter_btn:
                    await enter_btn.click()
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
            
            if "Please Click Similar" in await page.content():
                captcha_btn = await page.query_selector('a[href*="cid="]')
                if captcha_btn:
                    await captcha_btn.click()
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)
            
            # Start Surf
            try:
                start_btn = await page.wait_for_selector(
                    '#button1, input[value*="Start Surf"], .submit3', 
                    timeout=30000
                )
                if start_btn:
                    await start_btn.click()
                    await asyncio.sleep(3)
            except:
                pass
            
            html = await page.content()
            csrf_match = re.search(r'csrf_token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)', html)
            
            if csrf_match:
                csrf = csrf_match.group(1)
                print(f"   ✅ CSRF: {csrf}")
                await pw_browser.close()
                await client.browsers.stop(browser.id)
                return csrf
            
            await pw_browser.close()
            await client.browsers.stop(browser.id)
            return None
            
    except Exception as e:
        error_msg = str(e)
        if "402" in error_msg or "credits" in error_msg.lower() or "balance" in error_msg.lower():
            print(f"   💰 Saldo esaurito per key {api_key[:20]}...")
            return "NO_CREDITS"
        else:
            print(f"   ❌ Errore: {error_msg[:80]}")
            return None

def get_csrf_with_browseruse(api_key, anta_user, anta_pass):
    """Wrapper sincrono per Browser-USE"""
    result = asyncio.run(get_csrf_with_browseruse_async(api_key, anta_user, anta_pass))
    
    # Se "NO_CREDITS", marcalo come fallito
    if result == "NO_CREDITS":
        return None
    return result

# ============================================================
# OTTIENI CSRF
# ============================================================

def get_csrf_with_proxy(proxy, session, anta_user):
    """Ottiene CSRF usando il proxy"""
    try:
        response = session.get("https://antautosurf.com/", timeout=30)
        
        if response.status_code != 200:
            return None
        
        csrf_match = re.search(r'csrf_token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)', response.text)
        if csrf_match:
            return csrf_match.group(1)
        
        # Prova login
        login_data = {"bitcoinwallet": anta_user}
        response = session.post("https://antautosurf.com/index.php", data=login_data, timeout=30)
        
        csrf_match = re.search(r'csrf_token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]+)', response.text)
        if csrf_match:
            return csrf_match.group(1)
        
        return None
        
    except Exception as e:
        return None

# ============================================================
# MAIN SESSIONE
# ============================================================

def esegui_sessione():
    """Esegue una sessione del bot"""
    
    print("\n" + "="*60)
    print(f"  🤖 SESSIONE - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    # 1. PROXY
    proxy_manager = ProxyManager(PROXYSCRAPE_LIST)
    proxy, session = proxy_manager.find_working_proxy(max_tests=30)
    csrf = None
    browser_use_used = False
    browser_manager = BrowserUseManager()
    
    if proxy and session:
        csrf = get_csrf_with_proxy(proxy, session, ANTA_USER)
        if not csrf:
            proxy_manager.mark_failed(proxy, "CSRF non trovato")
    
    # 2. BROWSER-USE FALLBACK
    if not csrf:
        print("\n" + "="*60)
        print("  ⚠️ PROXY FALLITO, PASSO A BROWSER-USE")
        print("="*60)
        
        max_attempts = 5
        for attempt in range(max_attempts):
            api_key = browser_manager.get_next_key()
            if not api_key:
                print("   ❌ Nessuna API Key disponibile")
                break
            
            browser_use_used = True
            print(f"\n   🔑 Tentativo {attempt+1}/{max_attempts}")
            csrf = get_csrf_with_browseruse(api_key, ANTA_USER, ANTA_PASS)
            
            if csrf:
                print(f"   ✅ Browser-USE OK con key: {api_key[:20]}...")
                break
            else:
                browser_manager.mark_failed(api_key)
                print(f"   ⚠️ Tentativo {attempt+1} fallito")
                time.sleep(3)
    
    if not csrf:
        print("\n❌ Impossibile ottenere CSRF")
        return False
    
    # 3. REQUEST DIRETTA
    print(f"\n🔑 CSRF: {csrf}")
    
    if not session:
        session = requests.Session()
    
    try:
        session.proxies.clear()
        response = session.get(
            "https://antautosurf.com/index.php",
            params={"bitcoinwallet": ANTA_USER, "csrf_token": csrf},
            timeout=30
        )
        
        if response.status_code == 200:
            print("   ✅ Request diretta riuscita!")
            print("\n" + "="*60)
            print("  🎯 SESSIONE COMPLETATA!")
            print("="*60)
            
            # Statistiche
            print(f"\n📊 STATISTICHE:")
            print(f"   Proxy testati: {proxy_manager.stats['tested']}")
            print(f"   Proxy funzionanti: {proxy_manager.stats['working']}")
            print(f"   Proxy falliti: {proxy_manager.stats['failed']}")
            print(f"   Browser-USE usato: {'SI' if browser_use_used else 'NO'}")
            print(f"   API Key disponibili: {len(browser_manager.keys)}")
            print("="*60)
            return True
        else:
            print(f"   ❌ Errore: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Errore: {e}")
        return False

# ============================================================
# MAIN - LOOP INFINITO
# ============================================================

def main():
    print("="*60)
    print("  🤖 BOT ANTAUTOSURF FINALE")
    print("="*60)
    print(f"   📧 Account: {ANTA_USER}")
    print(f"   🌐 Proxy: {len(PROXYSCRAPE_LIST)} proxy")
    print(f"   🔑 Browser-USE: Auto-generazione")
    print("   🚀 Start Surf: ATTIVO")
    print("   ♾️ Modalità: Continuo")
    print("="*60)
    
    ciclo = 0
    
    while True:
        ciclo += 1
        print(f"\n🔄 CICLO {ciclo}")
        print("="*60)
        
        try:
            successo = esegui_sessione()
            
            if successo:
                print("\n⏳ Attesa 60 secondi...")
                time.sleep(60)
            else:
                print("\n⏳ Attesa 30 secondi...")
                time.sleep(30)
                
        except KeyboardInterrupt:
            print("\n🛑 Fermato")
            break
        except Exception as e:
            print(f"\n❌ Errore: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
