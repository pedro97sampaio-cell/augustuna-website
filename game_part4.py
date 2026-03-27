#!/usr/bin/env python3
# Part 4: Core gameplay loop, collision, scoring, powers, HUD
import os
f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '404.html'), 'a', encoding='utf-8')
f.write(r'''
// ═══════════════════════════════════════
// GAMEPLAY UPDATE
// ═══════════════════════════════════════
function startGame(){
  G.state=C.STATES.PLAYING;G.score=0;G.distance=0;G.speed=C.START_SPEED;
  G.velY=0;G.onGround=true;G.barrels=[];G.particles=[];G.laurels=[];
  G.comboCount=0;G.comboTimer=0;G.powerReady=true;G.powerTimer=0;
  G.powerActive=false;G.slowTimeActive=false;G.invincibleActive=false;
  G.era=0;G.eraFlashTimer=0;G.gameTime=0;G.speedIncTimer=0;G.spawnTimer=2;
  G.barrelsDodged=0;G.powersUsed=0;G.laurelsCollected=0;
  G.glorySurge=false;G.chaosMode=false;G.triumphus=false;
  G.nearMissTimer=0;G.scrollX=0;G.shakeTimer=0;G.runFrame=0;
  G.playerY=C.H*C.GROUND_Y;G.squashTimer=0;G.stretchTimer=0;
  // Apply Tuno speed bonus
  if(G.selectedChar===2)G.speed*=1.1;
  initAudio();startDrone();
  sfxEraTransition();
  G.eraFlashTimer=2;G.eraFlashName=ERAS[0].name;
}

function spawnBarrel(){
  let groundY=C.H*C.GROUND_Y;
  let type=0; // 0=single,1=double,2=cluster
  if(G.score>=1500&&Math.random()>0.6)type=2;
  else if(G.score>=500&&Math.random()>0.5)type=1;
  let count=type===0?1:type===1?2:3;
  for(let i=0;i<count;i++){
    G.barrels.push({x:C.W+60+i*55,y:groundY-18,rot:0,w:30,h:36,scored:false});
  }
}

function spawnLaurel(){
  let groundY=C.H*C.GROUND_Y;
  G.laurels.push({x:C.W+50,y:groundY-80-Math.random()*40,rot:0});
}

function activatePower(){
  if(!G.powerReady||G.powerActive)return;
  G.powerReady=false;G.powerActive=true;G.powersUsed++;
  let ch=G.selectedChar;
  if(ch===0){
    // Hiper Salto - massive jump
    G.velY=C.JUMP_VEL*3;G.onGround=false;
    spawnParticle(G.playerX,G.playerY,'#4A2A6A',15,5,1);
    sfxPowerSeminoide();
    G.powerActive=false;G.powerTimer=CHARS[0].powerCD;
  }else if(ch===1){
    // Slow Time
    G.slowTimeActive=true;G.powerDuration=4;
    spawnParticle(G.playerX,G.playerY,'#3A5ADA',15,5,1);
    sfxPowerSemina();
  }else{
    // Invencível
    G.invincibleActive=true;G.powerDuration=5;
    spawnParticle(G.playerX,G.playerY,C.GOLD,20,6,1);
    sfxPowerTuno();
  }
}

function updateGameplay(dt){
  let effDt=dt;
  if(G.slowTimeActive)effDt*=0.3;
  G.gameTime+=dt;G.scrollX+=G.speed*effDt*60;
  // Speed increase
  G.speedIncTimer+=dt;
  if(G.speedIncTimer>=10){G.speedIncTimer=0;G.speed=Math.min(C.MAX_SPEED,G.speed+0.15)}
  // Score
  G.distance+=G.speed*effDt*60;
  G.score=Math.floor(G.distance/10);
  // Combo decay
  if(G.comboTimer>0){G.comboTimer-=dt;if(G.comboTimer<=0)G.comboCount=0}
  // Era check
  let newEra=getEra();
  if(newEra!==G.era){
    G.era=newEra;G.eraFlashTimer=2.5;G.eraFlashName=ERAS[newEra].name;
    screenShake(8,0.5);sfxEraTransition();
  }
  // Power cooldown
  if(!G.powerReady&&!G.powerActive){
    G.powerTimer-=dt;if(G.powerTimer<=0){G.powerReady=true;G.powerTimer=0}
  }
  // Power duration
  if(G.powerActive){
    G.powerDuration-=dt;
    if(G.powerDuration<=0){
      G.powerActive=false;G.slowTimeActive=false;G.invincibleActive=false;
      G.powerTimer=CHARS[G.selectedChar].powerCD;
    }
  }
  // Gravity & Jump
  G.velY+=C.GRAVITY*effDt*60;
  G.playerY+=G.velY*effDt*60;
  let groundY=C.H*C.GROUND_Y;
  if(G.playerY>=groundY){
    if(!G.onGround){
      G.squashTimer=0.1;sfxLand();
      if(G.jumpBufferFrames>0){G.velY=C.JUMP_VEL;G.onGround=false;sfxJump()}
      else{G.onGround=true;G.comboTimer=0.5}
    }
    G.playerY=groundY;G.velY=0;
    if(G.onGround)G.coyoteFrames=C.COYOTE;
  }else{
    G.onGround=false;
    if(G.coyoteFrames>0)G.coyoteFrames--;
  }
  // Stretch at peak
  if(!G.onGround&&Math.abs(G.velY)<2)G.stretchTimer=0.08;
  // Timers
  if(G.squashTimer>0)G.squashTimer-=dt;
  if(G.stretchTimer>0)G.stretchTimer-=dt;
  if(G.jumpBufferFrames>0)G.jumpBufferFrames--;
  // Run animation
  if(G.onGround){G.runTimer+=dt;if(G.runTimer>0.05){G.runTimer=0;G.runFrame++}}
  // Barrel spawn
  G.spawnTimer-=dt;
  let minSpawn=Math.max(0.6,1.2-G.speed*0.03);
  let maxSpawn=Math.max(1.5,3.5-G.speed*0.08);
  if(G.chaosMode){minSpawn=0.2;maxSpawn=0.5}
  if(G.spawnTimer<=0){spawnBarrel();G.spawnTimer=rnd(minSpawn,maxSpawn)}
  // Laurel spawn
  if(Math.random()<0.0005*effDt*60&&G.laurels.length===0)spawnLaurel();
  // Update barrels
  for(let i=G.barrels.length-1;i>=0;i--){
    let b=G.barrels[i];
    let bSpeed=G.speed*effDt*60;
    // Seminoide passive: shockwave slows barrels
    if(G.selectedChar===0&&!G.onGround){
      let dist=Math.abs(b.x-G.playerX);
      if(dist<150)bSpeed*=0.8;
    }
    b.x-=bSpeed;b.rot+=0.05*effDt*60;
    // Collision
    let px=G.playerX,py=G.playerY-30;
    let hitW=G.selectedChar===1?12:16,hitH=45;
    if(b.x>px-hitW&&b.x<px+hitW&&py+hitH>b.y-b.h/2&&py<b.y+b.h/2){
      if(G.invincibleActive){
        // Barrel explodes
        spawnParticle(b.x,b.y,C.BARREL_WOOD,12,6,0.8);
        spawnParticle(b.x,b.y,'#FFFFFF',5,4,0.5);
        sfxBarrelBreak();G.barrels.splice(i,1);G.barrelsDodged++;continue;
      }else{
        // Game over
        gameOver();return;
      }
    }
    // Near miss detection
    if(!b.scored&&b.x<px-20){
      b.scored=true;G.barrelsDodged++;G.score+=50;
      // Near miss bonus
      let nearDist=Math.abs((py+hitH)-(b.y-b.h/2));
      if(nearDist<15&&!G.onGround){G.nearMissTimer=1;G.nearMissText='VICTÓRIA!';G.score+=25}
      if(!G.onGround){G.comboCount++;G.comboTimer=2}
    }
    if(b.x<-50){G.barrels.splice(i,1)}
  }
  // Update laurels
  for(let i=G.laurels.length-1;i>=0;i--){
    let l=G.laurels[i];l.x-=G.speed*effDt*60;l.rot+=0.02;
    let collectRad=G.selectedChar===1?40:30;
    if(Math.abs(l.x-G.playerX)<collectRad&&Math.abs(l.y-(G.playerY-30))<collectRad){
      G.laurelsCollected++;G.score+=200;
      spawnParticle(l.x,l.y,C.GOLD,20,5,1);sfxCollect();
      G.laurels.splice(i,1);
      if(G.powerReady)activatePower();
    }else if(l.x<-50){G.laurels.splice(i,1)}
  }
  // Special events
  if(G.era>=2&&!G.glorySurge&&Math.random()<0.0002){
    G.glorySurge=true;G.glorySurgeTimer=10;
  }
  if(G.glorySurge){G.glorySurgeTimer-=dt;if(G.glorySurgeTimer<=0)G.glorySurge=false}
  if(G.era>=3&&!G.chaosMode&&Math.random()<0.0001){
    G.chaosMode=true;G.chaosTimer=5;
  }
  if(G.chaosMode){G.chaosTimer-=dt;if(G.chaosTimer<=0){G.chaosMode=false;G.score+=1000}}
  if(G.era>=4&&!G.triumphus&&Math.random()<0.00008){
    G.triumphus=true;G.triumphusTimer=8;G.invincibleActive=true;G.powerDuration=8;
  }
  if(G.triumphus){G.triumphusTimer-=dt;if(G.triumphusTimer<=0)G.triumphus=false}
  // Near miss timer
  if(G.nearMissTimer>0)G.nearMissTimer-=dt;
  // Shake
  if(G.shakeTimer>0)G.shakeTimer-=dt;
  // Era flash
  if(G.eraFlashTimer>0)G.eraFlashTimer-=dt;
  // Skin unlocks
  for(let c=0;c<3;c++){
    for(let s=0;s<4;s++){
      if(!G.unlockedSkins[c][s]&&G.score>=SKINS[c][s].s){
        G.unlockedSkins[c][s]=true;save();
      }
    }
  }
  updateParticles(dt);
}

function gameOver(){
  G.state=C.STATES.GAME_OVER;sfxGameOver();screenShake(10,0.5);
  if(G.score>G.bestScore)G.bestScore=G.score;
  // Check high score
  G.newHighIdx=-1;G.enteringName=false;G.nameEntry='';
  if(G.highScores.length<10||G.score>G.highScores[G.highScores.length-1].score){
    G.newHighIdx=G.highScores.findIndex(h=>G.score>h.score);
    if(G.newHighIdx===-1)G.newHighIdx=G.highScores.length;
    if(G.newHighIdx<5)G.enteringName=true;
  }
  save();
}

function submitHighScore(){
  let entry={name:G.nameEntry||'ANONYMVS',score:G.score,char:CHARS[G.selectedChar].sub,era:ERAS[G.era].name};
  G.highScores.splice(G.newHighIdx,0,entry);
  if(G.highScores.length>10)G.highScores.pop();
  G.enteringName=false;save();
}

''')
f.close()
print("Part 4 written")
