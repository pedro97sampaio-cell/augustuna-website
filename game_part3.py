#!/usr/bin/env python3
# Part 3: Barrel drawing, loading screen, character select, gameplay logic
import os
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '404.html'), 'a', encoding='utf-8')
f.write(r'''
// ═══════════════════════════════════════
// BARREL DRAWING
// ═══════════════════════════════════════
function drawBarrel(x,y,rot=0){
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);
  let bw=30,bh=36;
  // Main body
  ctx.fillStyle=C.BARREL_WOOD;ctx.fillRect(-bw/2,-bh/2,bw,bh);
  // Bands
  ctx.fillStyle='#4A3A2A';
  ctx.fillRect(-bw/2-2,-bh/2+4,bw+4,4);
  ctx.fillRect(-bw/2-2,bh/2-8,bw+4,4);
  // Wood grain
  ctx.strokeStyle='#6A4A2A';ctx.lineWidth=1;
  for(let i=-2;i<3;i++){ctx.beginPath();ctx.moveTo(i*6,-bh/2);ctx.lineTo(i*6,bh/2);ctx.stroke()}
  // Outline
  ctx.strokeStyle=C.BLACK;ctx.lineWidth=2.5;ctx.strokeRect(-bw/2,-bh/2,bw,bh);
  ctx.restore();
}

// ═══════════════════════════════════════
// LAUREL CROWN
// ═══════════════════════════════════════
function drawLaurel(x,y,rot=0){
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);
  ctx.strokeStyle=C.GOLD;ctx.fillStyle=C.GOLD+'CC';ctx.lineWidth=2;
  // Left branch
  for(let i=0;i<5;i++){
    let a=-Math.PI*0.3-i*0.25;
    ctx.beginPath();ctx.ellipse(Math.cos(a)*12,Math.sin(a)*12-5,5,3,a+0.5,0,Math.PI*2);ctx.fill();ctx.stroke();
  }
  // Right branch
  for(let i=0;i<5;i++){
    let a=-Math.PI*0.7+i*0.25;
    ctx.beginPath();ctx.ellipse(Math.cos(a)*12,Math.sin(a)*12-5,5,3,a-0.5,0,Math.PI*2);ctx.fill();ctx.stroke();
  }
  // Glow
  ctx.shadowColor=C.GOLD;ctx.shadowBlur=15;
  ctx.beginPath();ctx.arc(0,-5,3,0,Math.PI*2);ctx.fill();
  ctx.shadowBlur=0;ctx.restore();
}

// ═══════════════════════════════════════
// LOADING SCREEN
// ═══════════════════════════════════════
function drawLoadingScreen(){
  ctx.fillStyle=C.BLACK;ctx.fillRect(0,0,C.W,C.H);
  let t=(Date.now()-G.loadStart)/1000;
  // Animated meander border
  let borderProgress=clamp(t/1.5,0,1);
  ctx.save();ctx.globalAlpha=borderProgress;
  let bsz=16,margin=30;
  // Top
  ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;
  let topW=C.W-margin*2;
  for(let i=0;i<Math.floor(topW/bsz*borderProgress);i++){
    let bx=margin+i*bsz;
    ctx.fillStyle=C.GOLD;
    if(i%4<2)ctx.fillRect(bx,margin,bsz-1,bsz/2);
    else ctx.fillRect(bx,margin+bsz/2,bsz-1,bsz/2);
  }
  // Bottom
  for(let i=0;i<Math.floor(topW/bsz*borderProgress);i++){
    let bx=margin+i*bsz;
    if(i%4<2)ctx.fillRect(bx,C.H-margin-bsz,bsz-1,bsz/2);
    else ctx.fillRect(bx,C.H-margin-bsz/2,bsz-1,bsz/2);
  }
  ctx.restore();
  // Vase silhouette
  ctx.fillStyle=C.TERRA;
  let vx=C.W/2,vy=C.H*0.38;
  let vs=0.8+Math.sin(t*2)*0.05;
  ctx.save();ctx.translate(vx,vy);ctx.scale(vs,vs);
  ctx.beginPath();
  ctx.moveTo(-25,40);ctx.quadraticCurveTo(-35,10,-15,-10);
  ctx.lineTo(-10,-20);ctx.lineTo(-12,-30);ctx.lineTo(-8,-35);
  ctx.lineTo(8,-35);ctx.lineTo(12,-30);ctx.lineTo(10,-20);
  ctx.lineTo(15,-10);ctx.quadraticCurveTo(35,10,25,40);
  ctx.closePath();ctx.fill();
  ctx.strokeStyle=C.GOLD;ctx.lineWidth=1.5;ctx.stroke();
  // Decorative band on vase
  ctx.strokeStyle=C.CREAM+'88';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(-30,15);ctx.lineTo(30,15);ctx.stroke();
  ctx.beginPath();ctx.moveTo(-28,25);ctx.lineTo(28,25);ctx.stroke();
  ctx.restore();
  // Title
  ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillStyle=C.GOLD;ctx.font='900 56px "Cinzel Decorative",serif';
  ctx.fillText('AUGUSTUNA',C.W/2,C.H*0.58);
  // Subtitle
  ctx.fillStyle=C.CREAM;ctx.font='400 22px "Cinzel",serif';
  ctx.fillText('Rumo à Bracara Augusta',C.W/2,C.H*0.65);
  // Loading bar (Roman road)
  G.loadProgress=clamp(t/2.8,0,1);
  let barW=300,barH=20,barX=(C.W-barW)/2,barY=C.H*0.78;
  ctx.fillStyle='#2A1A0A';ctx.fillRect(barX-2,barY-2,barW+4,barH+4);
  // Stone tiles filling
  let filled=Math.floor(G.loadProgress*15);
  for(let i=0;i<15;i++){
    let tx=barX+i*(barW/15)+1;
    if(i<filled){
      ctx.fillStyle=`hsl(25,30%,${35+(i*2)%10}%)`;
      ctx.fillRect(tx,barY,barW/15-2,barH);
      ctx.strokeStyle='#3A2A1A';ctx.lineWidth=0.5;ctx.strokeRect(tx,barY,barW/15-2,barH);
    }
  }
  // Percentage
  ctx.fillStyle=C.CREAM;ctx.font='400 14px "Cinzel",serif';
  ctx.fillText(Math.floor(G.loadProgress*100)+'%',C.W/2,barY+barH+20);
  // Transition
  if(G.loadProgress>=1){
    startFade(1,0.8,()=>{G.state=C.STATES.CHAR_SELECT});
  }
}

// ═══════════════════════════════════════
// CHARACTER SELECT SCREEN
// ═══════════════════════════════════════
function drawCharSelect(){
  // Background - scrolling Roman street at low opacity
  ctx.fillStyle=C.BLACK;ctx.fillRect(0,0,C.W,C.H);
  ctx.globalAlpha=0.15;G.charSelectScroll+=0.5;drawBackground();ctx.globalAlpha=1;
  ctx.fillStyle='rgba(26,10,0,0.75)';ctx.fillRect(0,0,C.W,C.H);
  // Title
  ctx.textAlign='center';ctx.fillStyle=C.GOLD;
  ctx.font='700 36px "Cinzel Decorative",serif';
  ctx.fillText('ESCOLHE O TEU GUERREIRO',C.W/2,60);
  // Meander under title
  ctx.strokeStyle=C.GOLD+'88';ctx.lineWidth=1;
  let mw=350;
  for(let i=0;i<Math.floor(mw/12);i++){
    let mx=C.W/2-mw/2+i*12;
    if(i%4<2)ctx.fillStyle=C.GOLD+'44',ctx.fillRect(mx,75,10,4);
    else ctx.fillStyle=C.GOLD+'44',ctx.fillRect(mx,79,10,4);
  }
  // Three arched panels
  let panelW=300,panelH=440,gap=50;
  let startX=(C.W-(panelW*3+gap*2))/2;
  for(let i=0;i<3;i++){
    let px=startX+i*(panelW+gap),py=100;
    let selected=G.selectedChar===i;
    let hovered=G.hoverChar===i;
    let sc=selected?1.04:hovered?1.02:1;
    ctx.save();
    ctx.translate(px+panelW/2,py+panelH/2);ctx.scale(sc,sc);ctx.translate(-panelW/2,-panelH/2);
    // Panel bg
    let panelColor=i===0?'#3A1A0A':i===1?'#2A3A3A':'#3A2A0A';
    ctx.fillStyle=panelColor;
    // Arch shape
    ctx.beginPath();
    ctx.moveTo(0,panelH);ctx.lineTo(0,80);
    ctx.arc(panelW/2,80,panelW/2,Math.PI,0);
    ctx.lineTo(panelW,panelH);ctx.closePath();ctx.fill();
    // Border
    ctx.strokeStyle=selected?C.GOLD:C.CREAM+'66';ctx.lineWidth=selected?3:1.5;ctx.stroke();
    // Glow
    if(selected){ctx.shadowColor=C.GOLD;ctx.shadowBlur=20;ctx.stroke();ctx.shadowBlur=0}
    // Character
    drawCharacter(panelW/2,panelH*0.55,i,G.equippedSkin[i],1.8,G.runFrame);
    // Name
    ctx.fillStyle=C.GOLD;ctx.font='700 18px "Cinzel",serif';
    ctx.textAlign='center';ctx.fillText(CHARS[i].name,panelW/2,panelH*0.72);
    ctx.fillStyle=C.CREAM;ctx.font='400 14px "Cinzel",serif';
    ctx.fillText(CHARS[i].sub,panelW/2,panelH*0.76);
    // Stats
    let stats=[['SALTO',CHARS[i].jump],['VELOC.',CHARS[i].speed],['RESIST.',CHARS[i].endurance]];
    stats.forEach((s,j)=>{
      let sy=panelH*0.8+j*22;
      ctx.fillStyle=C.CREAM+'AA';ctx.font='400 11px "Cinzel",serif';
      ctx.textAlign='left';ctx.fillText(s[0],30,sy);
      for(let k=0;k<5;k++){
        ctx.fillStyle=k<s[1]?C.GOLD:'#3A3A3A';
        ctx.fillRect(120+k*18,sy-8,14,10);
      }
    });
    // Power name
    ctx.fillStyle=C.TERRA;ctx.font='700 12px "Cinzel",serif';ctx.textAlign='center';
    ctx.fillText('⚡ '+CHARS[i].power,panelW/2,panelH*0.93);
    // Cosmetics icon
    ctx.fillStyle=C.CREAM+'88';ctx.font='18px serif';
    ctx.fillText('👗',panelW-30,panelH-15);
    ctx.restore();
  }
  // Start button
  let btnW=320,btnH=50,btnX=(C.W-btnW)/2,btnY=C.H-80;
  ctx.fillStyle='#3A2A1A';ctx.fillRect(btnX,btnY,btnW,btnH);
  ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;ctx.strokeRect(btnX,btnY,btnW,btnH);
  // Stone texture
  ctx.fillStyle='#4A3A2A';
  for(let i=0;i<8;i++)ctx.fillRect(btnX+5+i*40,btnY+2,35,btnH-4);
  ctx.fillStyle=C.GOLD;ctx.font='700 20px "Cinzel",serif';ctx.textAlign='center';
  ctx.fillText('INICIAR JORNADA',C.W/2,btnY+32);
}

''')
f.close()
print("Part 3 written")
