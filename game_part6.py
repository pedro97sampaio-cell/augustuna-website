#!/usr/bin/env python3
# Part 6: Main render, input handling, event loop, closing tags
import os
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '404.html'), 'a', encoding='utf-8')
f.write(r'''
// ═══════════════════════════════════════
// COSMETICS SCREEN
// ═══════════════════════════════════════
function drawCosmetics(){
  ctx.fillStyle='rgba(26,10,0,0.92)';ctx.fillRect(0,0,C.W,C.H);
  let ci=G.showCosmeticsFor>=0?G.showCosmeticsFor:G.selectedChar;
  ctx.textAlign='center';ctx.fillStyle=C.GOLD;
  ctx.font='700 30px "Cinzel Decorative",serif';
  ctx.fillText('TRAJES — '+CHARS[ci].sub.toUpperCase(),C.W/2,60);
  let sw=180,sh=220,gap=30;
  let startX=(C.W-(sw*4+gap*3))/2;
  G._cosButtons=[];
  for(let i=0;i<4;i++){
    let sx=startX+i*(sw+gap),sy=100;
    let unlocked=G.unlockedSkins[ci][i];
    let equipped=G.equippedSkin[ci]===i;
    ctx.fillStyle=unlocked?(equipped?'#2A3A2A':'#2A1A0A'):'#1A1A1A';
    ctx.fillRect(sx,sy,sw,sh);ctx.strokeStyle=equipped?C.GOLD:C.CREAM+'44';
    ctx.lineWidth=equipped?3:1;ctx.strokeRect(sx,sy,sw,sh);
    if(unlocked){
      drawCharacter(sx+sw/2,sy+sh*0.5,ci,i,1.5,0);
      ctx.fillStyle=C.GOLD;ctx.font='700 14px "Cinzel",serif';
      ctx.fillText(SKINS[ci][i].n,sx+sw/2,sy+sh-30);
      if(equipped){ctx.fillStyle='#55AA55';ctx.fillText('✓ EQUIPADO',sx+sw/2,sy+sh-10)}
    }else{
      ctx.fillStyle='#333';ctx.font='400 40px serif';ctx.fillText('?',sx+sw/2,sy+sh/2);
      ctx.fillStyle=C.CREAM+'66';ctx.font='400 12px "Cinzel",serif';
      ctx.fillText(SKINS[ci][i].s+' pts',sx+sw/2,sy+sh-20);
    }
    if(unlocked)G._cosButtons.push({x:sx,y:sy,w:sw,h:sh,skin:i,char:ci});
  }
  // Back button
  let bw=160,bh=40,bx=C.W/2-bw/2,by=350;
  ctx.fillStyle='#3A2A1A';ctx.fillRect(bx,by,bw,bh);
  ctx.strokeStyle=C.GOLD;ctx.lineWidth=2;ctx.strokeRect(bx,by,bw,bh);
  ctx.fillStyle=C.GOLD;ctx.font='700 14px "Cinzel",serif';
  ctx.fillText('VOLTAR',C.W/2,by+27);
  G._cosBackBtn={x:bx,y:by,w:bw,h:bh};
}

// ═══════════════════════════════════════
// MAIN RENDER
// ═══════════════════════════════════════
function render(){
  ctx.save();
  // Screen shake
  if(G.shakeTimer>0){
    let sx=(Math.random()-0.5)*G.shakeIntensity*2;
    let sy=(Math.random()-0.5)*G.shakeIntensity*2;
    ctx.translate(sx,sy);
  }
  ctx.clearRect(0,0,C.W,C.H);

  switch(G.state){
    case C.STATES.LOADING:
      drawLoadingScreen();break;
    case C.STATES.CHAR_SELECT:
      drawCharSelect();break;
    case C.STATES.COSMETICS:
      drawCharSelect();drawCosmetics();break;
    case C.STATES.PLAYING:
      drawBackground();
      // Draw barrels
      G.barrels.forEach(b=>drawBarrel(b.x,b.y,b.rot));
      // Draw laurels
      G.laurels.forEach(l=>drawLaurel(l.x,l.y,l.rot));
      // Draw player
      drawCharacter(G.playerX,G.playerY,G.selectedChar,G.equippedSkin[G.selectedChar],1,G.runFrame,G.powerActive);
      drawParticles();
      drawHUD();
      drawEraFlash();
      break;
    case C.STATES.PAUSED:
      drawBackground();
      G.barrels.forEach(b=>drawBarrel(b.x,b.y,b.rot));
      drawCharacter(G.playerX,G.playerY,G.selectedChar,G.equippedSkin[G.selectedChar],1,G.runFrame);
      drawHUD();drawPause();break;
    case C.STATES.GAME_OVER:
      drawBackground();drawGameOver();break;
    case C.STATES.HIGH_SCORES:
      drawHighScoresTable(C.W/2,50,true);break;
  }
  // Fade overlay
  if(G.fadeAlpha>0&&G.fadeAlpha<1||(G.fadeDir!==0)){
    ctx.fillStyle=`rgba(26,10,0,${clamp(G.fadeAlpha,0,1)})`;
    ctx.fillRect(-20,-20,C.W+40,C.H+40);
  }
  ctx.restore();
}

// ═══════════════════════════════════════
// MAIN LOOP
// ═══════════════════════════════════════
function gameLoop(timestamp){
  if(!G.lastTime)G.lastTime=timestamp;
  G.dt=Math.min((timestamp-G.lastTime)/1000,0.05);
  G.lastTime=timestamp;
  // Fade
  if(G.fadeDir!==0){
    G.fadeAlpha+=G.fadeDir*G.dt/(G.fadeDur||0.5);
    if(G.fadeDir>0&&G.fadeAlpha>=1){G.fadeDir=0;if(G.fadeCB){G.fadeCB();G.fadeCB=null;G.fadeDir=-1}}
    if(G.fadeDir<0&&G.fadeAlpha<=0){G.fadeDir=0;G.fadeAlpha=0}
  }
  if(G.state===C.STATES.PLAYING)updateGameplay(G.dt);
  if(G.state===C.STATES.CHAR_SELECT||G.state===C.STATES.COSMETICS)G.runFrame++;
  updateDrone();
  render();
  requestAnimationFrame(gameLoop);
}

// ═══════════════════════════════════════
// INPUT HANDLING
// ═══════════════════════════════════════
function getCanvasPos(e){
  let r=canvas.getBoundingClientRect();
  let scaleX=C.W/r.width,scaleY=C.H/r.height;
  let clientX,clientY;
  if(e.touches){clientX=e.touches[0].clientX;clientY=e.touches[0].clientY}
  else{clientX=e.clientX;clientY=e.clientY}
  return{x:(clientX-r.left)*scaleX,y:(clientY-r.top)*scaleY};
}

function tryJump(){
  initAudio();
  if(G.state===C.STATES.PLAYING){
    if(G.onGround||G.coyoteFrames>0){
      G.velY=C.JUMP_VEL;G.onGround=false;G.coyoteFrames=0;sfxJump();
    }else{G.jumpBufferFrames=C.JUMP_BUFFER}
  }
}

function hitTest(pos,btn){
  return btn&&pos.x>=btn.x&&pos.x<=btn.x+btn.w&&pos.y>=btn.y&&pos.y<=btn.y+btn.h;
}

canvas.addEventListener('mousedown',e=>{
  let pos=getCanvasPos(e);
  G.mouseDown=true;G.mouseDownTime=Date.now();
  if(G.state===C.STATES.CHAR_SELECT){
    // Check character panels
    let panelW=300,panelH=440,gap=50;
    let startX=(C.W-(panelW*3+gap*2))/2;
    for(let i=0;i<3;i++){
      let px=startX+i*(panelW+gap),py=100;
      if(pos.x>=px&&pos.x<=px+panelW&&pos.y>=py&&pos.y<=py+panelH){
        G.selectedChar=i;
        // Check cosmetics icon
        if(pos.x>=px+panelW-45&&pos.y>=py+panelH-30){
          G.showCosmeticsFor=i;G.state=C.STATES.COSMETICS;
        }
      }
    }
    // Start button
    let btnW=320,btnH=50,btnX=(C.W-btnW)/2,btnY=C.H-80;
    if(pos.x>=btnX&&pos.x<=btnX+btnW&&pos.y>=btnY&&pos.y<=btnY+btnH){
      startFade(1,0.5,()=>startGame());
    }
  }else if(G.state===C.STATES.COSMETICS){
    if(G._cosButtons)(G._cosButtons||[]).forEach(b=>{if(hitTest(pos,b)){G.equippedSkin[b.char]=b.skin;save()}});
    if(hitTest(pos,G._cosBackBtn))G.state=C.STATES.CHAR_SELECT;
  }else if(G.state===C.STATES.PLAYING){
    tryJump();
  }else if(G.state===C.STATES.PAUSED){
    (G._pauseBtns||[]).forEach(b=>{
      if(hitTest(pos,b)){
        if(b.action==='resume')G.state=C.STATES.PLAYING;
        if(b.action==='restart')startGame();
        if(b.action==='menu'){G.state=C.STATES.CHAR_SELECT}
      }
    });
  }else if(G.state===C.STATES.GAME_OVER){
    if(G._goBtns){
      if(hitTest(pos,G._goBtns.restart)){if(!G.enteringName)startFade(1,0.3,()=>startGame())}
      if(hitTest(pos,G._goBtns.scores))G.state=C.STATES.HIGH_SCORES;
    }
  }else if(G.state===C.STATES.HIGH_SCORES){
    if(hitTest(pos,G._hsBackBtn))G.state=C.STATES.GAME_OVER;
  }
});

canvas.addEventListener('mouseup',e=>{
  if(G.mouseDown&&G.state===C.STATES.PLAYING){
    let held=(Date.now()-G.mouseDownTime)/1000;
    if(held>=1&&G.powerReady)activatePower();
  }
  G.mouseDown=false;
});

canvas.addEventListener('mousemove',e=>{
  if(G.state===C.STATES.CHAR_SELECT){
    let pos=getCanvasPos(e);
    let panelW=300,panelH=440,gap=50;
    let startX=(C.W-(panelW*3+gap*2))/2;
    G.hoverChar=-1;
    for(let i=0;i<3;i++){
      let px=startX+i*(panelW+gap);
      if(pos.x>=px&&pos.x<=px+panelW&&pos.y>=100&&pos.y<=100+panelH)G.hoverChar=i;
    }
  }
});

// Touch
canvas.addEventListener('touchstart',e=>{
  e.preventDefault();
  let fakeEvent={clientX:e.touches[0].clientX,clientY:e.touches[0].clientY,touches:e.touches};
  canvas.dispatchEvent(new MouseEvent('mousedown',{clientX:e.touches[0].clientX,clientY:e.touches[0].clientY}));
},{passive:false});
canvas.addEventListener('touchend',e=>{
  e.preventDefault();
  canvas.dispatchEvent(new MouseEvent('mouseup',{}));
},{passive:false});

// Mobile jump button
document.getElementById('mobile-jump').addEventListener('touchstart',e=>{
  e.preventDefault();e.stopPropagation();tryJump();
},{passive:false});

// Keyboard
document.addEventListener('keydown',e=>{
  if(G.enteringName){
    if(e.key==='Enter'&&G.nameEntry.length>0){submitHighScore();return}
    if(e.key==='Backspace'){G.nameEntry=G.nameEntry.slice(0,-1);return}
    if(e.key.length===1&&G.nameEntry.length<15){G.nameEntry+=e.key.toUpperCase();return}
    return;
  }
  if(e.code==='Space'||e.code==='ArrowUp'){
    e.preventDefault();
    if(G.state===C.STATES.PLAYING){
      if(!G.spaceDown){G.spaceDown=true;G.spaceDownTime=Date.now();tryJump()}
    }
    if(G.state===C.STATES.GAME_OVER&&!G.enteringName)startFade(1,0.3,()=>startGame());
  }
  if(e.code==='KeyP'||e.code==='Escape'){
    if(G.state===C.STATES.PLAYING)G.state=C.STATES.PAUSED;
    else if(G.state===C.STATES.PAUSED)G.state=C.STATES.PLAYING;
  }
  if(e.code==='KeyM'){
    G.muted=!G.muted;
    document.getElementById('mute-btn').textContent=G.muted?'♪̸':'♪';
  }
  if(e.code==='KeyR'&&G.state===C.STATES.PAUSED)startGame();
  if(e.code==='KeyQ'&&G.state===C.STATES.PAUSED)G.state=C.STATES.CHAR_SELECT;
  if(e.code==='Enter'&&G.state===C.STATES.CHAR_SELECT)startFade(1,0.5,()=>startGame());
});
document.addEventListener('keyup',e=>{
  if(e.code==='Space'){
    if(G.spaceDown&&G.state===C.STATES.PLAYING){
      let held=(Date.now()-G.spaceDownTime)/1000;
      if(held>=1&&G.powerReady)activatePower();
    }
    G.spaceDown=false;
  }
});

// Mute button
document.getElementById('mute-btn').addEventListener('click',()=>{
  G.muted=!G.muted;
  document.getElementById('mute-btn').textContent=G.muted?'🔇':'♪';
});

// Visibility change - pause
document.addEventListener('visibilitychange',()=>{
  if(document.hidden&&G.state===C.STATES.PLAYING)G.state=C.STATES.PAUSED;
});

// Resize
function resize(){
  let vw=window.innerWidth,vh=window.innerHeight;
  let ratio=C.W/C.H;
  let w,h;
  if(vw/vh>ratio){h=vh;w=h*ratio}else{w=vw;h=w/ratio}
  canvas.style.width=w+'px';canvas.style.height=h+'px';
}
window.addEventListener('resize',resize);resize();

// ═══════════════════════════════════════
// INIT
// ═══════════════════════════════════════
G.loadStart=Date.now();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
''')
f.close()
print("Part 6 written - file complete!")
