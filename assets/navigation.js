/* Call after rendering the navigation and day sections. No trip data is embedded. */
function initTripNavigation({days,formatDate=value=>value,navigate}={}){
 const button=document.getElementById('quick-day-button'),menu=document.getElementById('quick-day-menu'),top=document.getElementById('back-top');
 if(!button||!menu)throw new Error('Approved floating navigation markup is missing');
 const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 menu.innerHTML='<p class="day-menu-heading">JUMP TO A DAY</p><a class="day-bubble" data-quick-day href="#days"><span class="day-bubble-number">☷</span><span class="day-bubble-copy"><b>All days</b><small>Explore the complete itinerary</small></span></a>'+(days||[]).map(d=>`<a class="day-bubble" data-quick-day href="#day-${Number(d.n)}"><span class="day-bubble-number">${String(d.n).padStart(2,'0')}</span><span class="day-bubble-copy"><b>${esc(d.city)}</b><small>Day ${Number(d.n)} · ${esc(formatDate(d.date))}</small></span><span class="day-bubble-arrow" aria-hidden="true">↗</span></a>`).join('');
 function toggle(open,focus=false){menu.hidden=!open;button.setAttribute('aria-expanded',String(open));menu.querySelectorAll('a').forEach(a=>a.classList.toggle('is-current',a.hash===location.hash));if(open&&focus)menu.querySelector('a')?.focus()}
 function go(hash){if(navigate)navigate(hash);else{const element=document.getElementById(hash.slice(1));if(element){if(element.tagName==='DETAILS')element.open=true;element.closest('details')?.setAttribute('open','');element.scrollIntoView({behavior:'smooth',block:'start'})}}}
 button.addEventListener('click',()=>toggle(menu.hidden,true));
 button.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();toggle(true,true)}});
 menu.addEventListener('keydown',e=>{const links=[...menu.querySelectorAll('a')],i=links.indexOf(document.activeElement);if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();links[(i+(e.key==='ArrowDown'?1:-1)+links.length)%links.length]?.focus()}});
 document.addEventListener('click',e=>{const day=e.target.closest('[data-quick-day]');if(day){e.preventDefault();toggle(false);if(location.hash!==day.hash)history.pushState(null,'',day.hash);go(day.hash)}else if(!e.target.closest('.floating-day-picker'))toggle(false)});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){toggle(false);button.focus()}});
 window.addEventListener('hashchange',()=>toggle(false));
 top?.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));
 const links=[...document.querySelectorAll('.trip-sidebar nav a')];
 function setActive(hash){links.forEach(a=>{const active=a.hash===hash;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')})}
 const observer=new IntersectionObserver(entries=>{for(const entry of entries)if(entry.isIntersecting)setActive('#'+entry.target.id)},{rootMargin:'-15% 0px -65% 0px'});
 links.forEach(a=>{const section=document.getElementById(a.hash.slice(1));if(section)observer.observe(section);a.addEventListener('click',()=>setActive(a.hash))});
 setActive(location.hash||'#overview');
 return {close:()=>toggle(false),setActive};
}
