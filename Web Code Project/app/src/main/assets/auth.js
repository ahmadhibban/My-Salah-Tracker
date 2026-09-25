const AuthCSS = `<style>
.a-bg{background:linear-gradient(135deg,#FFF,#E8E8E8)} .a-bg-dark{background:linear-gradient(145deg,#F9F9F9,#E3E3E3)}

/* 1. Modal Centering & Native Keyboard Handling Fix */
.a-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.65);backdrop-filter:blur(8px);display:flex;justify-content:center;align-items:center;z-index:99999;padding:15px;box-sizing:border-box;}
.a-card{position:relative;border-radius:22px;padding:26px;width:100%;max-width:320px;box-shadow:0 20px 45px rgba(0,0,0,0.35),inset 0 2px 5px #FFF;text-align:center;border:1.5px solid rgba(255,255,255,0.8);max-height:95vh;overflow-y:auto;margin:auto;}

.a-btn,.a-close,.a-copy-btn{display:flex;justify-content:center;align-items:center;cursor:pointer;border:none;transition:0.1s}
.a-close{position:absolute;top:12px;right:12px;width:32px;height:32px;border-radius:10px;background:linear-gradient(135deg,#FFF,#DFDBD2);box-shadow:inset 2px 2px 3px #FFF,inset -1px -1px 2px rgba(0,0,0,0.05),1px 1px 0 #BCB4A4,2px 2px 0 #BCB4A4,3px 4px 6px rgba(0,0,0,0.12)}
.a-close:active,.a-copy-btn:active{transform:scale(0.92);box-shadow:inset 2px 3px 5px rgba(0,0,0,0.15),inset -1px -1px 2px rgba(255,255,255,0.5)}
.a-circle{width:55px;height:55px;margin:0 auto 15px;border-radius:50%;display:flex;align-items:center;justify-content:center}
.a-c-def{background:rgba(0,0,0,0.05);box-shadow:inset 2px 3px 5px rgba(0,0,0,0.2),inset -1px -1px 3px #FFF}
.a-c-log{background:linear-gradient(135deg,#159C4C,#0F783A);box-shadow:inset 1px 2px 3px rgba(255,255,255,0.4),inset -2px -2px 4px rgba(0,0,0,0.3),0 3px 6px rgba(16,137,62,0.4)}
.a-c-dan{background:linear-gradient(135deg,#E74C3C,#B03A2E);box-shadow:inset 2px 2px 3px rgba(255,255,255,0.4),inset -2px -2px 4px rgba(0,0,0,0.2),1px 1px 0 #641E16,2px 2px 0 #641E16,4px 5px 10px rgba(0,0,0,0.3); color:#FFF; border-top:1px solid rgba(255,255,255,0.3); border-left:1px solid rgba(255,255,255,0.2)}
.a-title{color:#2D3748;margin:0 0 22px;font-size:24px;font-weight:900;font-family:'Outfit',sans-serif;text-shadow:1px 1px 0 #FFF,2px 3px 0 rgba(0,0,0,0.1),3px 5px 8px rgba(0,0,0,0.2);letter-spacing:0.5px}
.a-input{width:100%;height:50px;border-radius:14px;border:none;padding:0 16px;box-sizing:border-box;font-size:15px;font-weight:800;color:#4A5568;text-shadow:1px 1px 0 #FFF;box-shadow:inset 2px 3px 6px rgba(0,0,0,0.15),inset -1px -1px 3px #FFF;border-top:1px solid #FFF;border-left:1px solid #FFF;outline:none;margin-bottom:16px;font-family:'Plus Jakarta Sans',sans-serif}
.a-input:focus{box-shadow:inset 3px 4px 8px rgba(0,0,0,0.2),inset -1px -1px 3px #FFF}
.a-btn{width:100%;height:48px;border-radius:14px;font-weight:800;font-size:15px;font-family:'Plus Jakarta Sans',sans-serif;margin-bottom:12px;border-top:1px solid rgba(255,255,255,0.3);border-left:1px solid rgba(255,255,255,0.2)}
.a-btn-pri{background:linear-gradient(135deg,#4A89DF,#1A4B96);color:#FFF;box-shadow:inset 2px 2px 3px rgba(255,255,255,0.5),inset -2px -2px 4px rgba(0,0,0,0.2),1px 1px 0 #133366,2px 2px 0 #133366,4px 5px 10px rgba(0,0,0,0.3);text-shadow:1px 2px 2px rgba(0,0,0,0.5)}
.a-btn-sec{background:linear-gradient(135deg,#FFF,#D4D1C7);color:#444E51;box-shadow:inset 2px 3px 4px #FFF,inset -1px -1px 3px rgba(0,0,0,0.05),1px 1px 0 #BCB8A7,2px 2px 0 #BCB8A7,3px 3px 0 #BCB8A7,4px 5px 10px rgba(0,0,0,0.15);text-shadow:1px 1px 1px #FFF}
.a-btn:active{transform:scale(0.96)} .a-btn-sec:active{transform:translateY(3px) scale(0.98);box-shadow:inset 2px 3px 6px rgba(0,0,0,0.12),inset -2px -2px 4px rgba(255,255,255,0.8),0 0 0 #BCB8A7,1px 2px 4px rgba(0,0,0,0.1)}
.a-btn-pri:active,.a-c-dan:active{box-shadow:inset 2px 3px 6px rgba(0,0,0,0.3),inset -1px -1px 2px rgba(255,255,255,0.2),1px 1px 0 currentColor}
.a-link{font-size:13px;font-weight:800;color:#6C7A80;cursor:pointer;margin-top:6px;text-shadow:1px 1px 0 #FFF} .a-link span{color:#1A4B96;text-decoration:underline} .a-link:active{transform:scale(0.95)}
.a-sync{border-radius:16px;padding:14px;margin-bottom:24px;box-shadow:inset 2px 2px 3px #FFF,inset -1px -1px 2px rgba(0,0,0,0.05),1px 1px 0 #C9C9C9,2px 2px 0 #C9C9C9,3px 4px 8px rgba(0,0,0,0.15);border-top:1px solid #FFF;border-left:1px solid #FFF}
</style>`;

const AuthHTML = `
<div x-show="isAuthModalOpen" class="a-overlay" style="display:none;" x-transition.opacity x-cloak>
  <div class="a-card a-bg-dark" @click.stop>
    
    <button type="button" class="a-close" @click="isAuthModalOpen=false" x-show="!isLogoutConfirmOpen">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6C7A80" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(1px 1px 0px #FFF)"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
    </button>
    
    <div x-show="!isLoggedIn">
      <div class="a-circle a-c-def"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6C7A80" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
      <h3 class="a-title" x-text="authMode==='signup'?'Create Account':'Welcome Back'"></h3>
      
      <input type="email" id="authEmailInput" class="a-input a-bg" :style="genPass?'opacity:0.8;pointer-events:none;':''" placeholder="Email Address" x-model="authEmail" :readonly="genPass!==''">
      <input x-show="authMode==='login'" id="authPassInput" type="password" class="a-input a-bg" placeholder="Password" x-model="authPass">
      
      <div x-show="authMode==='signup' && genPass" style="position:relative; margin-bottom:16px;">
        <input type="text" class="a-input a-bg" style="padding-right:48px;font-family:monospace;color:#1A4B96;letter-spacing:1px;margin-bottom:0;" :value="genPass" readonly>
        <button type="button" @click="copyPass()" class="a-copy-btn" style="position:absolute;right:5px;top:5px;width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#FFF,#DFDBD2);box-shadow:inset 1px 1px 2px #FFF,inset -1px -1px 2px rgba(0,0,0,0.05),1px 1px 2px rgba(0,0,0,0.12);">
          <svg x-show="!isCopied" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3B75C6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <svg x-show="isCopied" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#159C4C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
        </button>
      </div>
      
      <button type="button" class="a-btn a-btn-pri" x-show="authMode==='signup' && !genPass" @click.prevent="genAcc()" x-text="isLoading?'Checking...':'Generate Password'"></button>
      <button type="button" class="a-btn" :class="forceConf?'a-c-dan':'a-btn-pri'" x-show="authMode==='signup' && genPass" @click.prevent="compSignup()" x-text="forceConf?'Confirm Without Copying?':'Login & Continue'"></button>
      <button type="button" class="a-btn a-btn-pri" x-show="authMode==='login'" @click.prevent="login()" x-text="isLoading?'Logging in...':'Login'"></button>
      
      <div class="a-link" @click="authMode=(authMode==='signup')?'login':'signup'" x-show="!genPass">
        <span x-show="authMode==='signup'">Already have an account? Login</span><span x-show="authMode==='login'">Don't have an account? Create one</span>
      </div>
    </div>
    
    <div x-show="isLoggedIn && !isLogoutConfirmOpen">
      <div class="a-circle a-c-log"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
      <h3 class="a-title" style="margin-bottom:5px;">Profile</h3>
      <p style="font-size:14px;font-weight:900;color:#4A5568;margin-bottom:22px;text-shadow:1px 1px 0 #FFF;letter-spacing:0.5px;" x-text="regEmail"></p>
      
      <div class="a-sync a-bg">
        <div style="display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:6px;">
          <div style="width:8px;height:8px;border-radius:50%;" :style="navigator.onLine?'background:#159C4C;box-shadow:0 0 5px #159C4C;':'background:#e74c3c;box-shadow:0 0 5px #e74c3c;'"></div>
          <span style="font-size:13px;font-weight:900;color:#4A5568;text-shadow:1px 1px 0 #FFF;" x-text="navigator.onLine?'Cloud Syncing Active':'Offline Mode'"></span>
        </div>
        <p style="font-size:11px;font-weight:700;color:#8A9499;margin:0;text-shadow:1px 1px 0 #FFF;">Last Synced: <span x-text="lastSyncTime"></span></p>
      </div>
      
      <button type="button" class="a-btn a-c-dan" style="margin-bottom:0;" @click="isLogoutConfirmOpen=true;">Logout</button>
    </div>
    
    <div x-show="isLoggedIn && isLogoutConfirmOpen">
      <div class="a-circle a-c-dan" style="width:50px;height:50px;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div>
      <h3 class="a-title" style="margin-bottom:8px;font-size:20px;">Logout?</h3>
      <p style="color:#6C7A80;font-size:13px;font-weight:700;margin:0 0 24px;line-height:1.4;">Your local data will be cleared. Restore anytime by logging in.</p>
      <div style="display:flex;gap:10px;">
        <button type="button" class="a-btn a-btn-sec" style="margin:0;" @click="isLogoutConfirmOpen=false;">Cancel</button>
        <button type="button" class="a-btn a-c-dan" style="margin:0;" @click="logoutAccount()">Yes, Logout</button>
      </div>
    </div>
    
  </div>
</div>`;
document.addEventListener("DOMContentLoaded",()=>document.body.insertAdjacentHTML('beforeend',AuthCSS+AuthHTML));
const FB="https://mysalahtracker-49a76-default-rtdb.firebaseio.com/users/";
window.getAuthLogic=()=>({
  isAuthModalOpen:!1, isLogoutConfirmOpen:!1, isLoggedIn:localStorage.getItem('isLoggedIn')==='true',
  regEmail:localStorage.getItem('regEmail')||'', regPass:localStorage.getItem('regPass')||'',
  authEmail:'', authPass:'', authMode:'signup', genPass:'', isCopied:!1, forceConf:!1, isLoading:!1,
  lastSyncTime:localStorage.getItem('lastSyncTime')||'Never', syncInterval:null, 
  get sMail(){return this.authEmail.trim().toLowerCase().replace(/\./g,"_dot_").replace(/@/g,"_at_")}, 
  get rsMail(){return this.regEmail.trim().toLowerCase().replace(/\./g,"_dot_").replace(/@/g,"_at_")},
  initAuth(){if(this.isLoggedIn)this.fetchCloudData();window.addEventListener('online',()=>{if(this.isLoggedIn)this.forceCloudSync()})},
  openAuthModal(){
      this.isAuthModalOpen=!0;
      this.isLogoutConfirmOpen=!1;
      this.authMode=this.regPass?'login':'signup';
      this.authEmail=this.regEmail;
      this.authPass=this.genPass='';
      this.isCopied=this.forceConf=this.isLoading=!1;
  },
  async genAcc(){
      let emailNode = document.getElementById('authEmailInput');
      if (emailNode && emailNode.value) this.authEmail = emailNode.value;
      if(!this.authEmail.includes('@'))return alert('Valid email required.');
      this.isLoading=!0;
      try{let r=await fetch(FB+this.sMail+"/auth.json"),d=await r.json();if(d&&d.password){alert('Account exists! Please Login.');this.authMode='login';}else{let p='',c='ABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$*';for(let i=0;i<12;i++){if(i>0&&i%4===0)p+='-';p+=c.charAt(Math.floor(Math.random()*c.length))}this.genPass=p}}catch(e){alert('Network error!')}this.isLoading=!1},
  copyPass(){let t=this.genPass,s=()=>{this.isCopied=!0;this.forceConf=!1;setTimeout(()=>this.isCopied=!1,2000)},ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";document.body.appendChild(ta);ta.select();try{document.execCommand('copy');s()}catch(e){if(navigator.clipboard)navigator.clipboard.writeText(t).then(s)}document.body.removeChild(ta)},
  async compSignup(){if(!this.isCopied&&!this.forceConf){this.forceConf=!0;setTimeout(()=>this.forceConf=!1,3000);return}try{await fetch(FB+this.sMail+"/auth.json",{method:'PUT',body:JSON.stringify({password:this.genPass})});this.regEmail=this.authEmail.trim().toLowerCase();this.regPass=this.genPass;localStorage.setItem('regEmail',this.regEmail);localStorage.setItem('regPass',this.regPass);this.isLoggedIn=!0;localStorage.setItem('isLoggedIn','true');this.isAuthModalOpen=!1;this.forceCloudSync()}catch(e){alert('Firebase connection failed.')}},
  async login(){
      let emailNode = document.getElementById('authEmailInput');
      let passNode = document.getElementById('authPassInput');
      if (emailNode && emailNode.value) this.authEmail = emailNode.value;
      if (passNode && passNode.value) this.authPass = passNode.value;

      this.authEmail = this.authEmail.trim().toLowerCase();
      if(!this.authEmail.includes('@'))return alert('Valid email required.');
      this.isLoading=!0;
      try{
          let r=await fetch(FB+this.sMail+"/auth.json");
          if (!r.ok) throw new Error("Connection failed");
          let d=await r.json();
          if(d && d.password===this.authPass.trim()){
              this.regEmail=this.authEmail;
              this.regPass=this.authPass.trim();
              localStorage.setItem('regEmail',this.regEmail);
              localStorage.setItem('regPass',this.regPass);
              this.isLoggedIn=!0;
              localStorage.setItem('isLoggedIn','true');
              this.isAuthModalOpen=!1;
              await this.fetchCloudData();
          } else {
              alert('Invalid Credentials!');
          }
      }catch(e){
          alert('Login failed: ' + e.message);
      }
      this.isLoading=!1;
  },
  logoutAccount(){this.isLoggedIn=!1;localStorage.setItem('isLoggedIn','false');localStorage.removeItem('regEmail');localStorage.removeItem('regPass');if(window.appRef)window.appRef.db={};localStorage.removeItem('prayer_db');location.reload()},
  async fetchCloudData(){if(!navigator.onLine)return;try{let r=await fetch(FB+this.rsMail+"/db.json"),d=await r.json();if(d){if(window.appRef)window.appRef.db={...d};localStorage.setItem('prayer_db',JSON.stringify(d));this.lastSyncTime=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});localStorage.setItem('lastSyncTime',this.lastSyncTime)}}catch(e){}},
  async forceCloudSync(){if(!navigator.onLine||!this.isLoggedIn)return;try{await fetch(FB+this.rsMail+"/db.json",{method:'PUT',body:JSON.stringify(window.appRef?window.appRef.db:JSON.parse(localStorage.getItem('prayer_db')))});this.lastSyncTime=new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});localStorage.setItem('lastSyncTime',this.lastSyncTime)}catch(e){}}
});
