async function setupPlanner(id,endpoint,mode){
 const form=document.getElementById(id), target=document.getElementById("results"); if(!form)return;
 form.addEventListener("submit",async e=>{
  e.preventDefault(); target.innerHTML='<div class="empty">Generating your plan…</div>';
  try{
   let r;
   if(mode==="multipart") r=await fetch(endpoint,{method:"POST",body:new FormData(form)});
   else r=await fetch(endpoint,{method:"POST",body:new URLSearchParams(new FormData(form)),headers:{"Content-Type":"application/x-www-form-urlencoded"}});
   const d=await r.json(); if(!r.ok)throw Error(d.detail||"Request failed"); renderRecommendations(target,d);
  }catch(err){target.innerHTML=`<div class="empty">Could not generate the plan: ${esc(err.message)}</div>`}
 })
}
function esc(v){return String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
function renderRecommendations(t,d){
 const alloc=Object.entries(d.allocation||{}).map(([k,v])=>`<span class="pill">${esc(k)}: ₹${Number(v).toLocaleString("en-IN")}</span>`).join("");
 const recs=(d.recommendations||[]).map(r=>`<article class="recommendation"><div class="result-head"><div><h3>${esc(r.name)}</h3><div class="rec-meta">${esc(r.category)} · ${esc(r.platform)}</div></div><div class="rec-price">₹${Number(r.estimated_price).toLocaleString("en-IN")}</div></div><p>${esc(r.reason)}</p><a class="rec-link" target="_blank" rel="noopener noreferrer" href="${esc(r.search_url)}">Search on ${esc(r.platform)} →</a></article>`).join("");
 t.innerHTML=`<div class="result-head"><div><h2>Your plan</h2><p>${esc(d.summary)}</p></div><span class="ai-badge">${d.ai_generated?"AI generated":"Fallback plan"}</span></div><div class="allocation">${alloc}</div>${recs}<p class="form-note">Saved as history #${d.history_id}. Prices are estimates.</p>`;
}
