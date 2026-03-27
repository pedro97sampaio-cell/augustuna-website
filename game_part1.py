#!/usr/bin/env python3
# Part 1: HTML shell, CSS, Loading Screen, Character Select
import os
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '404.html'), 'w', encoding='utf-8')
f.write(r'''<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">
<title>AUGUSTUNA: Rumo à Bracara Augusta</title>
<link rel="icon" type="image/x-icon" href="Logo oficial 2.png">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Cinzel+Decorative:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#1A0A00;overflow:hidden;font-family:'Cinzel',serif;width:100vw;height:100vh;display:flex;justify-content:center;align-items:center}
#gc{position:relative;width:100vw;height:100vh;overflow:hidden}
canvas{display:block;width:100%;height:100%;image-rendering:auto}
#mute-btn{position:fixed;top:15px;right:15px;z-index:1000;background:none;border:2px solid #D4AF37;color:#D4AF37;font-family:'Cinzel',serif;font-size:18px;width:40px;height:40px;cursor:pointer;border-radius:50%;display:flex;align-items:center;justify-content:center;opacity:0.7;transition:opacity 0.3s}
#mute-btn:hover{opacity:1}
#mobile-jump{display:none;position:fixed;bottom:30px;right:30px;z-index:999;width:80px;height:80px;border-radius:50%;background:rgba(212,175,55,0.25);border:2px solid rgba(212,175,55,0.5);color:#D4AF37;font-family:'Cinzel',serif;font-size:12px;cursor:pointer;-webkit-tap-highlight-color:transparent}
@media(max-width:768px),(hover:none){#mobile-jump{display:flex;align-items:center;justify-content:center}}
</style>
</head>
<body>
<div id="gc"><canvas id="c"></canvas></div>
<button id="mute-btn" title="Mute (M)">♪</button>
<button id="mobile-jump">SALTAR</button>
<script>
'use strict';
// ═══════════════════════════════════════
// CONSTANTS & CONFIG
// ═══════════════════════════════════════
const C={
  TERRA:'#C1440E',CREAM:'#F5E6C8',BLACK:'#1A0A00',GOLD:'#D4AF37',
  DARK_PURPLE:'#1a0a2e',BROWN:'#8B4513',BARREL_WOOD:'#A0522D',
  W:1280,H:720,GROUND_Y:0.75,
  GRAVITY:0.6,JUMP_VEL:-14,MAX_SPEED:18,START_SPEED:5,
  COYOTE:6,JUMP_BUFFER:8,
  STATES:{LOADING:0,CHAR_SELECT:1,PLAYING:2,PAUSED:3,GAME_OVER:4,HIGH_SCORES:5,COSMETICS:6}
};
const CHARS=[
  {name:'ΣΕΜΙΝΟΕΙΔΗΣ',sub:'Seminoide',jump:4,speed:2,endurance:3,
   color:'#2A1A0A',accent:'#4A2A1A',power:'HIPER SALTO',powerCD:15,
   desc:'Salto massivo 3x altura',passiveDesc:'Ondas de choque atrasam barris 20%'},
  {name:'ΣΕΜΙΝΑ',sub:'Semina',jump:3,speed:3,endurance:4,
   color:'#3A5A7A',accent:'#5A7A5A',power:'SLOW TIME',powerCD:18,
   desc:'Tudo abranda a 30% por 4s',passiveDesc:'Recolha +15% hitbox'},
  {name:'ΤΟΥΝΟΣ',sub:'Tuno',jump:2,speed:4,endurance:2,
   color:'#1A1A1A',accent:'#D4AF37',power:'INVENCÍVEL',powerCD:20,
   desc:'Invencível por 5s, barris explodem',passiveDesc:'Velocidade base +10%'}
];
const SKINS=[
  [{n:'Default',s:0},{n:'Aurum',s:1000},{n:'Spectral',s:3000},{n:'Imperator',s:6000}],
  [{n:'Default',s:0},{n:'Bardo',s:1000},{n:'Temporal',s:3000},{n:'Musa',s:6000}],
  [{n:'Default',s:0},{n:'Dourado',s:1000},{n:'Sombrio',s:3000},{n:'Augustus',s:6000}]
];
const ERAS=[
  {name:'REPÚBLICA',sub:'Roma Aeterna',minScore:0,maxScore:499,sky1:'#1a0a2e',sky2:'#C1440E',label:'ANDANTE'},
  {name:'IMPÉRIO',sub:'Gloria Imperii',minScore:500,maxScore:1499,sky1:'#2a1a3e',sky2:'#E8A317',label:'ALLEGRO'},
  {name:'EXPANSÃO',sub:'Mare Nostrum',minScore:1500,maxScore:2999,sky1:'#3a2a1e',sky2:'#FFD700',label:'PRESTO'},
  {name:'DECADÊNCIA',sub:'Finis Romae',minScore:3000,maxScore:5999,sky1:'#2A0A1E',sky2:'#8B0000',label:'FURIOSO'},
  {name:'BRACARA AUGUSTA',sub:'Triumphus Aeternus',minScore:6000,maxScore:Infinity,sky1:'#0A2A0A',sky2:'#D4AF37',label:'FURIOSO'}
];

// ═══════════════════════════════════════
// CANVAS & STATE SETUP
// ═══════════════════════════════════════
const canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
canvas.width=C.W;canvas.height=C.H;

let G={
  state:C.STATES.LOADING,loadProgress:0,loadStart:0,
  selectedChar:0,equippedSkin:[0,0,0],
  score:0,distance:0,barrelsDodged:0,powersUsed:0,laurelsCollected:0,
  speed:C.START_SPEED,playerX:120,playerY:C.H*C.GROUND_Y,
  velY:0,onGround:true,coyoteFrames:0,jumpBufferFrames:0,
  squashTimer:0,stretchTimer:0,
  barrels:[],particles:[],laurels:[],bgEvents:[],
  comboCount:0,comboTimer:0,
  powerReady:true,powerTimer:0,powerActive:false,powerDuration:0,
  slowTimeActive:false,invincibleActive:false,
  era:0,eraFlashTimer:0,eraFlashName:'',
  glorySurge:false,glorySurgeTimer:0,
  chaosMode:false,chaosTimer:0,
  triumphus:false,triumphusTimer:0,
  nearMissTimer:0,nearMissText:'',
  gameTime:0,speedIncTimer:0,
  spawnTimer:2,lastBarrelScore:0,
  scrollX:0,
  mouseDown:false,mouseDownTime:0,
  spaceDown:false,spaceDownTime:0,
  highScores:[],unlockedSkins:[[true,false,false,false],[true,false,false,false],[true,false,false,false]],
  bestScore:0,
  muted:false,bgMusicStarted:false,
  runFrame:0,runTimer:0,
  hoverChar:-1,
  charSelectScroll:0,
  dt:0,lastTime:0,
  shakeTimer:0,shakeIntensity:0,
  fadeAlpha:0,fadeDir:0,fadeCB:null,
  nameEntry:'',enteringName:false,newHighIdx:-1,
  showCosmeticsFor:-1,
};

// Load saved data
try{
  let d=JSON.parse(localStorage.getItem('augustuna_save')||'{}');
  if(d.highScores)G.highScores=d.highScores;
  if(d.unlockedSkins)G.unlockedSkins=d.unlockedSkins;
  if(d.bestScore)G.bestScore=d.bestScore;
  if(d.equippedSkin)G.equippedSkin=d.equippedSkin;
}catch(e){}

function save(){
  try{localStorage.setItem('augustuna_save',JSON.stringify({
    highScores:G.highScores,unlockedSkins:G.unlockedSkins,
    bestScore:G.bestScore,equippedSkin:G.equippedSkin
  }))}catch(e){}
}

// ═══════════════════════════════════════
// WEB AUDIO
// ═══════════════════════════════════════
let audioCtx=null;
function initAudio(){if(!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)()}
function playTone(freq,dur,type='sine',vol=0.15){
  if(G.muted||!audioCtx)return;
  let o=audioCtx.createOscillator(),g=audioCtx.createGain();
  o.type=type;o.frequency.value=freq;
  g.gain.setValueAtTime(vol,audioCtx.currentTime);
  g.gain.exponentialRampToValueAtTime(0.001,audioCtx.currentTime+dur);
  o.connect(g);g.connect(audioCtx.destination);
  o.start();o.stop(audioCtx.currentTime+dur);
}
function sfxJump(){playTone(440,0.12,'sine',0.1);playTone(660,0.08,'sine',0.08)}
function sfxLand(){playTone(80,0.1,'sawtooth',0.12)}
function sfxCollect(){playTone(523,0.1,'sine',0.12);setTimeout(()=>playTone(659,0.1,'sine',0.12),80);setTimeout(()=>playTone(784,0.15,'sine',0.12),160)}
function sfxBarrelBreak(){if(G.muted||!audioCtx)return;let b=audioCtx.createBufferSource(),buf=audioCtx.createBuffer(1,audioCtx.sampleRate*0.2,audioCtx.sampleRate),d=buf.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=(Math.random()*2-1)*Math.exp(-i/1000);b.buffer=buf;let g=audioCtx.createGain();g.gain.value=0.15;b.connect(g);g.connect(audioCtx.destination);b.start();playTone(60,0.3,'sawtooth',0.1)}
function sfxPowerSeminoide(){playTone(55,0.5,'sawtooth',0.15);playTone(65,0.4,'sine',0.1)}
function sfxPowerSemina(){[784,659,523,440,349].forEach((f,i)=>setTimeout(()=>playTone(f,0.15,'sine',0.1),i*80))}
function sfxPowerTuno(){[330,415,494,659].forEach((f,i)=>setTimeout(()=>playTone(f,0.08,'sawtooth',0.08),i*30))}
function sfxEraTransition(){[262,330,392,523].forEach((f,i)=>setTimeout(()=>playTone(f,0.3,'sawtooth',0.12),i*100))}
function sfxGameOver(){[392,349,330,262].forEach((f,i)=>setTimeout(()=>playTone(f,0.4,'sine',0.1),i*200))}
let dronOsc=null,dronGain=null;
function startDrone(){
  if(!audioCtx||dronOsc)return;
  dronOsc=audioCtx.createOscillator();dronGain=audioCtx.createGain();
  dronOsc.type='sine';dronOsc.frequency.value=55;
  dronGain.gain.value=G.muted?0:0.03;
  dronOsc.connect(dronGain);dronGain.connect(audioCtx.destination);dronOsc.start();
}
function updateDrone(){if(dronGain)dronGain.gain.value=G.muted?0:0.03}

// ═══════════════════════════════════════
// UTILITY
// ═══════════════════════════════════════
function toRoman(n){
  if(n<=0||n>99999)return String(n);
  const v=[1000,900,500,400,100,90,50,40,10,9,5,4,1],
        r=['M','CM','D','CD','C','XC','L','XL','X','IX','V','IV','I'];
  let s='';for(let i=0;i<v.length;i++)while(n>=v[i]){s+=r[i];n-=v[i]}return s;
}
function lerp(a,b,t){return a+(b-a)*t}
function clamp(v,mn,mx){return Math.max(mn,Math.min(mx,v))}
function rnd(a,b){return a+Math.random()*(b-a)}
function drawMeander(x,y,w,h,sz=12,color=C.GOLD){
  ctx.strokeStyle=color;ctx.lineWidth=2;
  let steps=Math.floor(w/sz);
  ctx.beginPath();
  for(let i=0;i<steps;i++){
    let bx=x+i*sz,d=(i%4);
    if(d===0){ctx.moveTo(bx,y);ctx.lineTo(bx+sz,y)}
    else if(d===1){ctx.lineTo(bx+sz,y+h*0.5);ctx.lineTo(bx,y+h*0.5)}
    else if(d===2){ctx.lineTo(bx,y+h);ctx.lineTo(bx+sz,y+h)}
    else{ctx.lineTo(bx+sz,y+h*0.5);ctx.lineTo(bx+sz+sz*0.1,y)}
  }
  ctx.stroke();
}
function drawMeanderBorder(x,y,w,h,sz,color){
  drawMeander(x,y,w,sz,sz,color);
  drawMeander(x,y+h-sz,w,sz,sz,color);
  ctx.save();ctx.translate(x,y);ctx.rotate(Math.PI/2);drawMeander(0,0,h,sz,sz,color);ctx.restore();
  ctx.save();ctx.translate(x+w,y);ctx.rotate(Math.PI/2);drawMeander(0,-sz,h,sz,sz,color);ctx.restore();
}
function screenShake(intensity=5,dur=0.3){G.shakeTimer=dur;G.shakeIntensity=intensity}
function startFade(dir,dur,cb){G.fadeAlpha=dir>0?0:1;G.fadeDir=dir;G.fadeDur=dur;G.fadeCB=cb}

// ═══════════════════════════════════════
// PARTICLE SYSTEM
// ═══════════════════════════════════════
function spawnParticle(x,y,color,count=5,spread=3,life=0.6){
  for(let i=0;i<count;i++)G.particles.push({x,y,vx:rnd(-spread,spread),vy:rnd(-spread-2,-0.5),life,maxLife:life,color,size:rnd(2,5)});
}
function updateParticles(dt){
  for(let i=G.particles.length-1;i>=0;i--){
    let p=G.particles[i];p.x+=p.vx;p.y+=p.vy;p.vy+=0.1;p.life-=dt;
    if(p.life<=0)G.particles.splice(i,1);
  }
}
function drawParticles(){
  G.particles.forEach(p=>{
    ctx.globalAlpha=clamp(p.life/p.maxLife,0,1);
    ctx.fillStyle=p.color;
    ctx.fillRect(p.x-p.size/2,p.y-p.size/2,p.size,p.size);
  });
  ctx.globalAlpha=1;
}

''')
f.close()
print("Part 1 written")
