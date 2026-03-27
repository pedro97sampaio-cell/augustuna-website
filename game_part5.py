#!/usr/bin/env python3
# Part 5: HUD, Game Over screen, High Scores, Pause, Cosmetics, main render, input, loop
import os
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '404.html'), 'a', encoding='utf-8')
f.write(r'''
// ═══════════════════════════════════════
// HUD DRAWING
// ═══════════════════════════════════════
function drawHUD(){
  // Score (Roman + Arabic)
  ctx.textAlign='right';ctx.fillStyle=C.GOLD;
  ctx.font='700 28px "Cinzel",serif';
  let scoreStr=G.score>9999?toRoman(Math.min(G.score,39999)):toRoman(G.score);
  ctx.fillText(scoreStr,C.W-30,40);
  ctx.fillStyle=C.CREAM;ctx.font='400 14px "Cinzel",serif';
  ctx.fillText(String(G.score),C.W-30,58);
  // Era label
  ctx.fillStyle=C.TERRA;ctx.font='400 12px "Cinzel",serif';
  ctx.fillText(ERAS[G.era].label,C.W-30,75);
  // Speed era
  let speedLabel=G.speed<7?'ANDANTE':G.speed<11?'ALLEGRO':G.speed<15?'PRESTO':'FURIOSO';
  ctx.fillText(speedLabel,C.W-30,90);
  // Combo
  if(G.comboCount>1){
    ctx.textAlign='center';ctx.fillStyle=C.GOLD;
    ctx.font='700 24px "Cinzel",serif';
    ctx.fillText('×'+toRoman(G.comboCount),C.W/2,50);
  }
  // Near miss
  if(G.nearMissTimer>0){
    ctx.globalAlpha=G.nearMissTimer;ctx.textAlign='center';
    ctx.fillStyle=C.GOLD;ctx.font='700 30px "Cinzel Decorative",serif';
    ctx.fillText(G.nearMissText,C.W/2,C.H*0.4);ctx.globalAlpha=1;
  }
  // Power cooldown indicator (bottom-left)
  let pcx=60,pcy=C.H-60,pr=28;
  // Circle bg
  ctx.beginPath();ctx.arc(pcx,pcy,pr,0,Math.PI*2);
  ctx.fillStyle='rgba(26,10,0,0.7)';ctx.fill();
  ctx.strokeStyle=C.CREAM+'66';ctx.lineWidth=2;ctx.stroke();
  // Mini character
  ctx.save();ctx.beginPath();ctx.arc(pcx,pcy,pr-4,0,Math.PI*2);ctx.clip();
  drawCharacter(pcx,pcy+15,G.selectedChar,G.equippedSkin[G.selectedChar],0.6,0);
  ctx.restore();
  // Cooldown arc
  if(!G.powerReady&&!G.powerActive){
    let cd=CHARS[G.selectedChar].powerCD;
    let progress=1-G.powerTimer/cd;
    ctx.beginPath();ctx.moveTo(pcx,pcy);
    ctx.arc(pcx,pcy,pr,-Math.PI/2,-Math.PI/2+progress*Math.PI*2);
    ctx.closePath();ctx.fillStyle=C.GOLD+'44';ctx.fill();
    ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;
    ctx.beginPath();ctx.arc(pcx,pcy,pr,-Math.PI/2,-Math.PI/2+progress*Math.PI*2);ctx.stroke();
  }
  if(G.powerReady){
    ctx.strokeStyle=C.GOLD;ctx.lineWidth=3;ctx.shadowColor=C.GOLD;ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(pcx,pcy,pr,0,Math.PI*2);ctx.stroke();ctx.shadowBlur=0;
    ctx.fillStyle=C.GOLD;ctx.font='700 9px "Cinzel",serif';ctx.textAlign='center';
    ctx.fillText('PRONTO',pcx,pcy+pr+14);
  }
  if(G.powerActive){
    ctx.strokeStyle='#FF4444';ctx.lineWidth=3;
    ctx.beginPath();ctx.arc(pcx,pcy,pr,0,Math.PI*2);ctx.stroke();
    ctx.fillStyle=C.CREAM;ctx.font='400 10px "Cinzel",serif';ctx.textAlign='center';
    ctx.fillText(G.powerDuration.toFixed(1)+'s',pcx,pcy+pr+14);
  }
  // Era name
  ctx.textAlign='left';ctx.fillStyle=C.CREAM+'88';ctx.font='400 11px "Cinzel",serif';
  ctx.fillText('ERA: '+ERAS[G.era].name,15,25);
  // Glory Surge
  if(G.glorySurge){
    ctx.textAlign='center';ctx.fillStyle=C.GOLD;
    ctx.font='700 20px "Cinzel",serif';
    ctx.fillText('⚡ GLORY SURGE ×2 ⚡',C.W/2,100);
  }
  // Chaos Mode
  if(G.chaosMode){
    ctx.textAlign='center';ctx.fillStyle='#FF2200';
    ctx.font='700 20px "Cinzel",serif';
    ctx.fillText('🔥 CHAOS MODE 🔥',C.W/2,100);
  }
  // Triumphus
  if(G.triumphus){
    ctx.strokeStyle=C.GOLD;ctx.lineWidth=4;ctx.strokeRect(5,5,C.W-10,C.H-10);
    ctx.textAlign='center';ctx.fillStyle=C.GOLD;
    ctx.font='700 24px "Cinzel Decorative",serif';
    ctx.fillText('TRIUMPHUS!',C.W/2,100);
  }
  // Era 5 gold border
  if(G.era===4){
    ctx.strokeStyle=C.GOLD+'66';ctx.lineWidth=3;
    ctx.strokeRect(3,3,C.W-6,C.H-6);
  }
}

// ═══════════════════════════════════════
// ERA TRANSITION FLASH
// ═══════════════════════════════════════
function drawEraFlash(){
  if(G.eraFlashTimer<=0)return;
  let a=Math.min(1,G.eraFlashTimer/1.5);
  ctx.globalAlpha=a*0.3;ctx.fillStyle='#FFFFFF';ctx.fillRect(0,0,C.W,C.H);
  ctx.globalAlpha=a;ctx.textAlign='center';ctx.fillStyle=C.GOLD;
  ctx.font='900 64px "Cinzel Decorative",serif';
  ctx.fillText(G.eraFlashName,C.W/2,C.H/2);
  ctx.fillStyle=C.CREAM;ctx.font='400 20px "Cinzel",serif';
  ctx.fillText(ERAS[G.era].sub,C.W/2,C.H/2+45);
  ctx.globalAlpha=1;
}

// ═══════════════════════════════════════
// GAME OVER SCREEN
// ═══════════════════════════════════════
function drawGameOver(){
  ctx.fillStyle='rgba(26,10,0,0.85)';ctx.fillRect(0,0,C.W,C.H);
  // Red vignette
  let vg=ctx.createRadialGradient(C.W/2,C.H/2,C.W*0.2,C.W/2,C.H/2,C.W*0.7);
  vg.addColorStop(0,'transparent');vg.addColorStop(1,'rgba(139,0,0,0.4)');
  ctx.fillStyle=vg;ctx.fillRect(0,0,C.W,C.H);

  ctx.textAlign='center';
  ctx.fillStyle=C.TERRA;ctx.font='900 48px "Cinzel Decorative",serif';
  ctx.fillText('CAIU EM BATALHA',C.W/2,120);
  // Score
  ctx.fillStyle=C.GOLD;ctx.font='700 36px "Cinzel",serif';
  ctx.fillText(toRoman(Math.min(G.score,39999)),C.W/2,190);
  ctx.fillStyle=C.CREAM;ctx.font='400 18px "Cinzel",serif';
  ctx.fillText(G.score+' pontos',C.W/2,220);
  // Stats
  let stats=[
    ['Distância',Math.floor(G.distance)+'m'],
    ['Barris Saltados',String(G.barrelsDodged)],
    ['Poderes Usados',String(G.powersUsed)],
    ['Lauréis',String(G.laurelsCollected)],
    ['Era',ERAS[G.era].name]
  ];
  stats.forEach((s,i)=>{
    ctx.fillStyle=C.CREAM+'AA';ctx.font='400 14px "Cinzel",serif';
    ctx.textAlign='left';ctx.fillText(s[0],C.W/2-120,270+i*25);
    ctx.textAlign='right';ctx.fillStyle=C.GOLD;ctx.fillText(s[1],C.W/2+120,270+i*25);
  });
  // Name entry
  if(G.enteringName){
    ctx.textAlign='center';ctx.fillStyle=C.GOLD;
    ctx.font='700 20px "Cinzel",serif';
    ctx.fillText('INSCRIÇÃO NA HISTÓRIA',C.W/2,420);
    // Stone input
    ctx.fillStyle='#3A2A1A';
    let iw=300,ih=40,ix=(C.W-iw)/2,iy=440;
    ctx.fillRect(ix,iy,iw,ih);ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;ctx.strokeRect(ix,iy,iw,ih);
    ctx.fillStyle=C.CREAM;ctx.font='700 18px "Cinzel",serif';
    let displayName=G.nameEntry+(Math.floor(Date.now()/500)%2===0?'|':'');
    ctx.fillText(displayName,C.W/2,iy+27);
    ctx.fillStyle=C.CREAM+'88';ctx.font='400 12px "Cinzel",serif';
    ctx.fillText('Escreve o teu nome e prime ENTER',C.W/2,iy+ih+20);
  }
  // Buttons
  let btnY=G.enteringName?520:430;
  // RENASCER button
  ctx.fillStyle='#3A2A1A';let bw=180,bh=45;
  ctx.fillRect(C.W/2-bw-20,btnY,bw,bh);ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;
  ctx.strokeRect(C.W/2-bw-20,btnY,bw,bh);
  ctx.fillStyle=C.GOLD;ctx.font='700 16px "Cinzel",serif';ctx.textAlign='center';
  ctx.fillText('RENASCER',C.W/2-bw/2-20,btnY+30);
  // GLÓRIA button
  ctx.fillStyle='#3A2A1A';
  ctx.fillRect(C.W/2+20,btnY,bw,bh);ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;
  ctx.strokeRect(C.W/2+20,btnY,bw,bh);
  ctx.fillStyle=C.GOLD;ctx.fillText('GLÓRIA ETERNA',C.W/2+bw/2+20,btnY+30);
  // High scores table inline
  drawHighScoresTable(C.W/2,btnY+80,false);
  // Store button positions for click handling
  G._goBtns={
    restart:{x:C.W/2-bw-20,y:btnY,w:bw,h:bh},
    scores:{x:C.W/2+20,y:btnY,w:bw,h:bh}
  };
}

function drawHighScoresTable(cx,sy,fullScreen){
  if(fullScreen){ctx.fillStyle='rgba(26,10,0,0.92)';ctx.fillRect(0,0,C.W,C.H)}
  ctx.textAlign='center';
  if(fullScreen){
    ctx.fillStyle=C.GOLD;ctx.font='700 30px "Cinzel Decorative",serif';
    ctx.fillText('GLÓRIA ETERNA',cx,60);sy=100;
  }
  // Table
  let tw=500,th=Math.min(G.highScores.length*30+40,340);
  let tx=cx-tw/2;
  ctx.fillStyle='#2A1A0A';ctx.fillRect(tx,sy,tw,th);
  ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;ctx.strokeRect(tx,sy,tw,th);
  // Header
  ctx.fillStyle=C.GOLD;ctx.font='700 13px "Cinzel",serif';
  ctx.textAlign='left';ctx.fillText('#',tx+15,sy+25);
  ctx.fillText('NOME',tx+50,sy+25);
  ctx.textAlign='right';ctx.fillText('PONTOS',tx+tw-20,sy+25);
  // Entries
  G.highScores.slice(0,10).forEach((h,i)=>{
    let ey=sy+50+i*28;
    let icon=i===0?'🏆':i===1?'🥈':i===2?'🥉':'';
    ctx.textAlign='left';ctx.fillStyle=i<3?C.GOLD:C.CREAM;
    ctx.font='400 13px "Cinzel",serif';
    ctx.fillText(icon+(i+1),tx+15,ey);
    ctx.fillText(h.name,tx+50,ey);
    ctx.textAlign='right';ctx.fillText(String(h.score),tx+tw-20,ey);
  });
  if(G.highScores.length===0){
    ctx.textAlign='center';ctx.fillStyle=C.CREAM+'66';ctx.font='400 14px "Cinzel",serif';
    ctx.fillText('Nenhum registo ainda',cx,sy+60);
  }
  if(fullScreen){
    // Back button
    let bw2=160,bh2=40,bx2=cx-bw2/2,by2=sy+th+20;
    ctx.fillStyle='#3A2A1A';ctx.fillRect(bx2,by2,bw2,bh2);
    ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;ctx.strokeRect(bx2,by2,bw2,bh2);
    ctx.fillStyle=C.GOLD;ctx.font='700 14px "Cinzel",serif';ctx.textAlign='center';
    ctx.fillText('VOLTAR',cx,by2+27);
    G._hsBackBtn={x:bx2,y:by2,w:bw2,h:bh2};
  }
}

// ═══════════════════════════════════════
// PAUSE SCREEN
// ═══════════════════════════════════════
function drawPause(){
  ctx.fillStyle='rgba(26,10,0,0.8)';ctx.fillRect(0,0,C.W,C.H);
  ctx.textAlign='center';ctx.fillStyle=C.GOLD;
  ctx.font='900 42px "Cinzel Decorative",serif';
  ctx.fillText('PAUSA',C.W/2,150);
  let items=['[P/ESC] Continuar','[R] Reiniciar','[M] Som: '+(G.muted?'OFF':'ON'),'[Q] Menu Principal'];
  items.forEach((t,i)=>{
    ctx.fillStyle=C.CREAM;ctx.font='400 18px "Cinzel",serif';
    ctx.fillText(t,C.W/2,250+i*40);
  });
  // Touch buttons
  let bw=200,bh=45,bx=C.W/2-bw/2;
  ['CONTINUAR','REINICIAR','MENU'].forEach((label,i)=>{
    let by=420+i*60;
    ctx.fillStyle='#3A2A1A';ctx.fillRect(bx,by,bw,bh);
    ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;ctx.strokeRect(bx,by,bw,bh);
    ctx.fillStyle=C.GOLD;ctx.font='700 14px "Cinzel",serif';
    ctx.fillText(label,C.W/2,by+30);
  });
  G._pauseBtns=[
    {x:bx,y:420,w:bw,h:bh,action:'resume'},
    {x:bx,y:480,w:bw,h:bh,action:'restart'},
    {x:bx,y:540,w:bw,h:bh,action:'menu'}
  ];
}

''')
f.close()
print("Part 5 written")
