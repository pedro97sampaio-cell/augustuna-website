#!/usr/bin/env python3
# Part 2: Drawing functions, background, character rendering
import os
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '404.html'), 'a', encoding='utf-8')
f.write(r'''
// ═══════════════════════════════════════
// BACKGROUND RENDERING
// ═══════════════════════════════════════
function getEra(){
  for(let i=ERAS.length-1;i>=0;i--)if(G.score>=ERAS[i].minScore)return i;
  return 0;
}
function drawSky(){
  let e=ERAS[G.era];
  let grad=ctx.createLinearGradient(0,0,0,C.H*0.6);
  grad.addColorStop(0,e.sky1);grad.addColorStop(1,e.sky2);
  ctx.fillStyle=grad;ctx.fillRect(0,0,C.W,C.H*0.7);
  // Stars
  ctx.fillStyle='rgba(255,255,220,0.5)';
  for(let i=0;i<30;i++){
    let sx=(i*137+G.scrollX*0.02)%C.W,sy=20+((i*73)%200);
    let twinkle=Math.sin(G.gameTime*2+i)*0.3+0.7;
    ctx.globalAlpha=twinkle*0.4;ctx.fillRect(sx,sy,1.5,1.5);
  }
  ctx.globalAlpha=1;
}
function drawHills(){
  let ox=(-G.scrollX*0.15)%600;
  ctx.fillStyle='#1a0a2e';ctx.beginPath();ctx.moveTo(0,C.H*0.5);
  for(let x=-100;x<C.W+200;x+=60){
    let h=Math.sin((x+ox)*0.005)*60+Math.sin((x+ox)*0.012)*30;
    ctx.lineTo(x,C.H*0.45-h);
  }
  ctx.lineTo(C.W+200,C.H*0.7);ctx.lineTo(0,C.H*0.7);ctx.fill();
}
function drawFarRuins(){
  let ox=(-G.scrollX*0.3)%800;
  ctx.fillStyle='rgba(26,10,0,0.7)';
  // Aqueduct arches
  for(let i=0;i<6;i++){
    let ax=i*250+ox-200,ay=C.H*0.38;
    if(ax<-100||ax>C.W+100)continue;
    ctx.fillRect(ax,ay,20,C.H*0.35);
    ctx.fillRect(ax+230,ay,20,C.H*0.35);
    ctx.beginPath();ctx.arc(ax+125,ay+20,105,Math.PI,0);ctx.fill();
    ctx.fillRect(ax,ay,250,15);
  }
  // Glow behind
  ctx.fillStyle=C.TERRA+'33';
  ctx.fillRect(0,C.H*0.35,C.W,C.H*0.1);
}
function drawMidRuins(){
  let ox=(-G.scrollX*0.6)%900;
  ctx.fillStyle=C.CREAM+'99';
  // Columns
  for(let i=0;i<5;i++){
    let cx=i*300+ox-100,cy=C.H*0.5;
    if(cx<-80||cx>C.W+80)continue;
    // Column base
    ctx.fillRect(cx,cy,18,C.H*0.25);
    // Capital
    ctx.fillRect(cx-5,cy-5,28,8);
    // Broken top
    if(i%2===0){ctx.fillRect(cx-3,cy-15,24,12)}
  }
  ctx.strokeStyle=C.BLACK+'66';ctx.lineWidth=1.5;
  for(let i=0;i<5;i++){
    let cx=i*300+ox-100,cy=C.H*0.5;
    if(cx<-80||cx>C.W+80)continue;
    ctx.strokeRect(cx,cy,18,C.H*0.25);
  }
}
function drawGround(){
  let groundY=C.H*C.GROUND_Y;
  // Road
  ctx.fillStyle='#5A4A3A';ctx.fillRect(0,groundY,C.W,C.H-groundY);
  // Cobblestones
  let ox=(-G.scrollX*1.5)%60;
  ctx.strokeStyle='#3A2A1A';ctx.lineWidth=1;
  for(let r=0;r<3;r++){
    let rowOff=(r%2)*30;
    for(let i=-1;i<C.W/60+2;i++){
      let sx=i*60+ox+rowOff,sy=groundY+r*25+5;
      ctx.fillStyle=`hsl(25,20%,${28+((i+r)*7)%10}%)`;
      ctx.fillRect(sx,sy,55,20);
      ctx.strokeRect(sx,sy,55,20);
    }
  }
  // Mosaic border on road edges
  ctx.fillStyle=C.GOLD+'44';
  let mox=(-G.scrollX*1.5)%20;
  for(let i=-1;i<C.W/20+2;i++){
    let mx=i*20+mox;
    if(i%2===0)ctx.fillRect(mx,groundY-3,18,6);
  }
}
function drawBackground(){drawSky();drawHills();drawFarRuins();drawMidRuins();drawGround()}

// ═══════════════════════════════════════
// CHARACTER DRAWING (Procedural Sprites)
// ═══════════════════════════════════════
function drawCharacter(x,y,charIdx,skinIdx,scale=1,frame=0,powerGlow=false){
  ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);
  let ch=CHARS[charIdx],w=36,h=55;
  // Squash/stretch
  let sy=1,sx=1;
  if(G.squashTimer>0){sy=0.8;sx=1.2}
  if(G.stretchTimer>0){sy=1.15;sx=0.9}
  ctx.scale(sx,sy);
  // Power glow
  if(powerGlow){
    ctx.shadowColor=charIdx===0?'#4A2A6A':charIdx===1?'#3A5ADA':C.GOLD;
    ctx.shadowBlur=20;
  }
  // Skin color overrides
  let bodyColor=ch.color,accentColor=ch.accent,capeColor=ch.color;
  if(charIdx===0){
    if(skinIdx===1){bodyColor='#B8860B';accentColor='#FFD700'}
    else if(skinIdx===2){bodyColor='rgba(100,150,200,0.5)';accentColor='#4488FF'}
    else if(skinIdx===3){bodyColor='#1A0A00';accentColor='#C1440E'}
  }else if(charIdx===1){
    if(skinIdx===1){bodyColor='#8B2020';accentColor='#CD853F'}
    else if(skinIdx===2){bodyColor='#2244AA';accentColor='#88BBFF'}
    else if(skinIdx===3){bodyColor='#F5E6C8';accentColor='#D4AF37'}
  }else{
    if(skinIdx===1){bodyColor='#B8860B';accentColor='#FFD700'}
    else if(skinIdx===2){bodyColor='#050505';accentColor='#FF2200'}
    else if(skinIdx===3){bodyColor='#8B4513';accentColor='#D4AF37'}
  }
  // Running animation bob
  let bob=Math.sin(frame*0.3)*3;
  let legPhase=Math.sin(frame*0.4);
  // Body
  if(charIdx===0){
    // Seminoide - hooded monk
    ctx.fillStyle=bodyColor;
    ctx.beginPath();ctx.ellipse(0,-h*0.3+bob,w*0.45,h*0.55,0,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle=C.BLACK;ctx.lineWidth=2;ctx.stroke();
    // Hood point
    ctx.beginPath();ctx.moveTo(-w*0.2,-h*0.8+bob);ctx.lineTo(0,-h+bob);ctx.lineTo(w*0.2,-h*0.8+bob);ctx.fill();ctx.stroke();
    // Face
    ctx.fillStyle='#DDB892';ctx.fillRect(-8,-h*0.5+bob,16,12);
    ctx.fillStyle='#FFF';ctx.fillRect(-5,-h*0.47+bob,4,5);ctx.fillRect(2,-h*0.47+bob,4,5);
    ctx.fillStyle=C.BLACK;ctx.fillRect(-4,-h*0.46+bob,2,3);ctx.fillRect(3,-h*0.46+bob,2,3);
    // Rope belt
    ctx.strokeStyle=accentColor;ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(-w*0.3,-h*0.1+bob);ctx.lineTo(w*0.3,-h*0.1+bob);ctx.stroke();
    // Legs
    ctx.fillStyle=bodyColor;
    ctx.fillRect(-8,bob-3,7,15+legPhase*4);ctx.fillRect(2,bob-3,7,15-legPhase*4);
  }else if(charIdx===1){
    // Semina - musician
    ctx.fillStyle=bodyColor;ctx.fillRect(-w*0.35,-h*0.65+bob,w*0.7,h*0.55);
    ctx.strokeStyle=C.BLACK;ctx.lineWidth=2;ctx.strokeRect(-w*0.35,-h*0.65+bob,w*0.7,h*0.55);
    // Head
    ctx.fillStyle='#DDB892';ctx.beginPath();ctx.arc(0,-h*0.72+bob,10,0,Math.PI*2);ctx.fill();ctx.stroke();
    // Tricorn hat
    ctx.fillStyle='#2A2A3A';
    ctx.beginPath();ctx.moveTo(-14,-h*0.78+bob);ctx.lineTo(0,-h-5+bob);ctx.lineTo(14,-h*0.78+bob);ctx.closePath();ctx.fill();ctx.stroke();
    // Eyes
    ctx.fillStyle=C.BLACK;ctx.fillRect(-4,-h*0.73+bob,3,3);ctx.fillRect(2,-h*0.73+bob,3,3);
    // Guitar shape
    ctx.fillStyle='#8B4513';ctx.fillRect(w*0.2,-h*0.5+bob,5,30);
    ctx.beginPath();ctx.ellipse(w*0.22,-h*0.2+bob,8,6,0,0,Math.PI*2);ctx.fill();ctx.stroke();
    // Legs
    ctx.fillStyle=accentColor;
    ctx.fillRect(-8,bob-12,7,18+legPhase*3);ctx.fillRect(2,bob-12,7,18-legPhase*3);
  }else{
    // Tuno - caped musician
    // Cape
    ctx.fillStyle=bodyColor;
    ctx.beginPath();ctx.moveTo(-w*0.5,-h*0.7+bob);ctx.lineTo(-w*0.6,-h*0.1+bob);
    ctx.lineTo(w*0.1,-h*0.1+bob);ctx.lineTo(w*0.1,-h*0.7+bob);ctx.closePath();ctx.fill();
    ctx.strokeStyle=C.BLACK;ctx.lineWidth=2;ctx.stroke();
    // Body
    ctx.fillStyle='#2A2A2A';ctx.fillRect(-w*0.3,-h*0.65+bob,w*0.6,h*0.5);ctx.strokeRect(-w*0.3,-h*0.65+bob,w*0.6,h*0.5);
    // Head
    ctx.fillStyle='#DDB892';ctx.beginPath();ctx.arc(0,-h*0.72+bob,10,0,Math.PI*2);ctx.fill();ctx.stroke();
    // Tricorn
    ctx.fillStyle=C.BLACK;
    ctx.beginPath();ctx.moveTo(-14,-h*0.78+bob);ctx.lineTo(0,-h-8+bob);ctx.lineTo(14,-h*0.78+bob);ctx.closePath();ctx.fill();
    // Gold trim on hat
    ctx.strokeStyle=accentColor;ctx.lineWidth=1.5;ctx.stroke();
    // Eyes
    ctx.fillStyle=C.BLACK;ctx.fillRect(-4,-h*0.73+bob,3,3);ctx.fillRect(2,-h*0.73+bob,3,3);
    // Mandolin
    ctx.fillStyle='#A0522D';ctx.fillRect(w*0.15,-h*0.55+bob,4,25);
    ctx.beginPath();ctx.ellipse(w*0.17,-h*0.26+bob,7,5,0.2,0,Math.PI*2);ctx.fill();ctx.stroke();
    // Legs
    ctx.fillStyle='#1A1A1A';
    ctx.fillRect(-8,bob-12,7,18+legPhase*3);ctx.fillRect(2,bob-12,7,18-legPhase*3);
  }
  // Gold outline for era 5
  if(G.state===C.STATES.PLAYING&&G.era===4){
    ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;
    ctx.beginPath();ctx.ellipse(0,-h*0.3,w*0.55,h*0.65,0,0,Math.PI*2);ctx.stroke();
  }
  // Invincibility flash
  if(G.invincibleActive&&G.state===C.STATES.PLAYING){
    ctx.globalAlpha=0.3+Math.sin(G.gameTime*15)*0.2;
    ctx.fillStyle=C.GOLD;ctx.beginPath();ctx.ellipse(0,-h*0.3,w*0.5,h*0.6,0,0,Math.PI*2);ctx.fill();
    ctx.globalAlpha=1;
  }
  ctx.shadowBlur=0;ctx.restore();
}

''')
f.close()
print("Part 2 written")
