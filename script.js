/* ============================================
   AUGUSTUNA — JavaScript
   SPA Routing, Cart, Dropdowns, Animations
   ============================================ */

document.addEventListener('DOMContentLoaded', async () => {
  // --- Pre-loader Animation ---
  const loaderWrapper = document.getElementById('loader-wrapper');
  const progressBar = document.getElementById('loaderProgressBar');
  if (loaderWrapper && progressBar) {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 15 + 5; 
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
      }
      progressBar.style.width = progress + '%';
    }, 150);
  }

  await fetchWebsiteData();

  if (loaderWrapper) {
    setTimeout(() => {
      document.body.classList.add('loaded');
    }, 400); 
  }

  // Initialize icons - Huge Icons are font-based, no initialization needed for <i> classes
  // But we'll keep a placeholder if needed for other systems


  initRouter();
  initNavigation();
  initDropdowns();
  initScrollAnimations();
  initCounters();
  initMembers();
  initNewsTabs();
  initGenericTabs();
  initCart();

  console.log('🎵 Augustuna — Website carregado com sucesso!');
});

/* ============================================
   GLOBAL DATA FETCHING
   ============================================ */
let MEMBERS_DATA = [];
let ATUACOES_DATA = { festivais_concurso: [], festivais_convite: [], outras: [] };
let NOTICIAS_DATA = [];
let EVENTOS_DATA = { magna_augusta: [], festa_semina: [] };
let LOJA_DATA = [];
let CONTACTOS_DATA = null;

async function fetchWebsiteData() {
  try {
    const urls = [
      'data/membros.json',
      'data/atuacoes.json',
      'data/noticias.json',
      'data/eventos.json',
      'data/loja.json',
      'data/contactos.json',
      'data/layout.json'
    ];
    
    // Add cache buster
    const fetches = urls.map(url => fetch(url + '?t=' + new Date().getTime()).then(res => res.json()).catch(() => ({})));
    const [membros, atuacoes, noticias, eventos, loja, contactos, layout] = await Promise.all(fetches);

    // Reorder sections based on layout data
    if (layout && layout.order) {
      applyLayoutOrder(layout.order);
    }

    // Flatten members for script.js structure
    MEMBERS_DATA = (membros.geracoes || []).reduce((acc, g) => {
      const gMembers = (g.elementos || []).map(m => ({
        name: m.nome,
        alcunha: m.alcunha,
        instrumento: m.instrumento,
        curso: m.curso || '',
        data: m.data_passagem || '',
        evento: m.evento || '',
        foto: m.foto || '',
        geracao: g.nome
      }));
      return acc.concat(gMembers);
    }, []);

    ATUACOES_DATA = atuacoes;
    NOTICIAS_DATA = noticias;
    EVENTOS_DATA = eventos;
    LOJA_DATA = loja;
    CONTACTOS_DATA = contactos;

    renderNoticias();
    renderEventos();
    renderAtuacoes();
    renderLoja();
    renderContactos();
  } catch(e) {
    console.error('Failed to load website data:', e);
  }
}

/* ============================================
   DYNAMIC RENDERERS
   ============================================ */
function renderNoticias() {
  const container = document.getElementById('newsContent');
  if (!container) return;
  
  container.innerHTML = NOTICIAS_DATA.map(n => {
    let tagClass = 'tag-blue';
    let icon = '<i class="hugeicons-stroke-rounded-award-01" style="width:64px;height:64px;color:var(--dourado);opacity:0.5;"></i>';
    let bgColors = '#3A5A2A, #1A3A1A';
    
    if (n.categoria === 'destaque') {
      tagClass = '';
      icon = '<img src="Logo oficial 2.png" alt="30 Anos" style="max-width:60%;height:auto;opacity:0.8;">';
      bgColors = '#1B3A5C, #0A1628';
    } else if (n.categoria === 'recrutamento') {
      tagClass = 'tag-green';
      icon = '<i class="hugeicons-stroke-rounded-user-group" style="width:64px;height:64px;color:var(--dourado);opacity:0.5;"></i>';
      bgColors = '#8B1A1A, #5a1010';
    } else if (n.categoria === 'cultura') {
      tagClass = 'tag-blue';
      icon = '<i class="hugeicons-stroke-rounded-calendar-01" style="width:64px;height:64px;color:var(--dourado);opacity:0.5;"></i>';
      bgColors = '#1B3A5C, #0A1628';
    }
    
    const imageHTML = n.imagem ? 
      `<img src="${n.imagem}" alt="${n.titulo}" style="width:100%;height:100%;object-fit:cover;">` : 
      `<div style="width:100%;height:100%;background:linear-gradient(135deg, ${bgColors});display:flex;align-items:center;justify-content:center;">${icon}</div>`;

    return `
      <div class="news-card-v2" data-category="${n.categoria || 'all'}">
        <div class="news-card-v2-image">
          <span class="news-card-tag ${tagClass}">${n.categoria ? (n.categoria.charAt(0).toUpperCase() + n.categoria.slice(1)) : 'Notícia'}</span>
          ${imageHTML}
        </div>
        <div class="news-card-v2-body">
          <div class="news-card-date">${n.data}</div>
          <h4>${n.titulo}</h4>
          <p>${n.corpo}</p>
        </div>
      </div>
    `;
  }).join('');
}

function renderEventos() {
  function renderDropdownLayout(containerId, dataArray, prefixLabel) {
    const container = document.getElementById(containerId);
    if (!container || !dataArray || !dataArray.length) return;

    // Sort dataArray by edition or year (optional, but good for dropdown)
    // We assume dataArray is already ordered from newest to oldest or vice versa

    let html = `
      <div class="event-dropdown-wrapper" style="text-align: center; margin-bottom: 3rem;">
        <label style="display: block; color: var(--dourado); margin-bottom: 0.5rem; font-weight: 600;">Escolha a Edição:</label>
        <select class="event-select-dropdown" onchange="switchEventContent('${containerId}', this.value)" style="background: var(--bg-dark); color: white; border: 1px solid var(--dourado); padding: 0.8rem 1.5rem; border-radius: 8px; font-family: 'Helvetica', sans-serif; min-width: 250px;">
          ${dataArray.map((m, i) => {
            const label = m.edicao + (m.ano && m.ano !== 0 ? ` (${m.ano})` : '');
            return `<option value="${i}">${label}</option>`;
          }).join('')}
        </select>
      </div>

      <div class="event-display-area" id="${containerId}-display">
        ${renderSingleEventContent(dataArray[0], prefixLabel)}
      </div>
    `;

    container.innerHTML = html;
    
    // Store data in a window variable for the switch function
    window[`${containerId}_DATA`] = dataArray;
    window[`${containerId}_PREFIX`] = prefixLabel;
  }

  renderDropdownLayout('magnaAugustaContent', EVENTOS_DATA.magna_augusta, 'Magna Augusta');
  renderDropdownLayout('festaSeminaContent', EVENTOS_DATA.festa_semina, 'Festa do Semina');
}

function renderSingleEventContent(m, prefixLabel) {
  if (!m) return '';
  return `
    <div class="event-detail-view reveal shadow-hover">
      <div class="event-detail-poster">
        <img src="${m.imagem || 'Logo oficial 2.png'}" alt="${prefixLabel} ${m.edicao}">
      </div>
      <div class="event-detail-info">
        <div class="event-detail-prefix">${prefixLabel}</div>
        <h3 class="event-detail-title">Edição ${m.edicao} ${m.ano && m.ano !== 0 ? `(${m.ano})` : ''}</h3>
        <div class="event-detail-description">${m.descricao}</div>
      </div>
    </div>
  `;
}

window.switchEventContent = function(containerId, index) {
  const display = document.getElementById(`${containerId}-display`);
  const data = window[`${containerId}_DATA`][index];
  const prefix = window[`${containerId}_PREFIX`];
  
  if (display && data) {
    display.style.opacity = '0';
    setTimeout(() => {
      display.innerHTML = renderSingleEventContent(data, prefix);
      display.style.opacity = '1';
    }, 300);
  }
};

/* ============================================
   LAYOUT ORDERING
   ============================================ */
function applyLayoutOrder(order) {
  const sectionMap = {
    'Hero': 'page-home',
    'Notícias': 'page-noticias',
    'História': 'page-formacao',
    'Traje': 'page-traje',
    'Augustunos': 'page-membros',
    'Reportório': 'page-musica',
    'Magna Augusta': 'page-magna-augusta',
    'Festa do Semina': 'page-festa-semina',
    'Atuações': ['page-festivais-concurso', 'page-festivais-convite', 'page-outras-atuacoes'],
    'Loja': 'page-marketplace',
    'Contactos': 'page-contactos'
  };

  const body = document.body;
  const sections = order.flatMap(name => sectionMap[name] || []);
  
  // Reorder Sections in DOM
  sections.forEach(id => {
    const el = document.getElementById(id);
    if (el) body.appendChild(el); 
  });

  // Reorder Navigation Menu
  const navMenu = document.querySelector('.nav-links');
  if (navMenu) {
    const navLinks = Array.from(navMenu.children);
    order.forEach(name => {
      const targetIds = Array.isArray(sectionMap[name]) ? sectionMap[name] : [sectionMap[name]];
      const link = navLinks.find(l => {
        const dp = l.getAttribute('data-page');
        if (dp && targetIds.some(id => id.replace('page-','') === dp)) return true;
        const subPages = Array.from(l.querySelectorAll('[data-page]')).map(a => a.getAttribute('data-page'));
        return targetIds.some(id => subPages.includes(id.replace('page-','')));
      });
      if (link) navMenu.appendChild(link);
    });
  }
}

function renderAtuacoes() {
  function renderList(containerId, dataArray) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // Sort array by date descending
    const monthMap = {"JAN":1,"FEV":2,"MAR":3,"ABR":4,"MAI":5,"JUN":6,"JUL":7,"AGO":8,"SET":9,"OUT":10,"NOV":11,"DEZ":12};
    let sortedData = [...dataArray].sort((a, b) => {
      const p1 = a.data.split(' ');
      const p2 = b.data.split(' ');
      
      const y1 = parseInt(p1[p1.length - 1] || '0', 10);
      const y2 = parseInt(p2[p2.length - 1] || '0', 10);
      if (y1 !== y2) return y2 - y1; // descending year
      
      const m1 = p1.length > 1 ? (monthMap[p1[p1.length - 2].toUpperCase()] || 0) : 0;
      const m2 = p2.length > 1 ? (monthMap[p2[p2.length - 2].toUpperCase()] || 0) : 0;
      if (m1 !== m2) return m2 - m1; // descending month
      
      const d1 = p1.length > 2 ? parseInt(p1[0], 10) : 0;
      const d2 = p2.length > 2 ? parseInt(p2[0], 10) : 0;
      return d2 - d1; // descending day
    });

    let currentYear = '';
    let html = '';
    
    sortedData.forEach(item => {
      const parts = item.data.split(' ');
      const yr = parts[parts.length - 1]; 
      const isYearOnly = parts.length === 1;
      
      const day = isYearOnly ? '--' : parts[0];
      const month = isYearOnly ? '--' : parts.length > 1 ? parts[1] : '';
      
      if (yr !== currentYear) {
        html += `<div class="performance-year-divider">${yr}</div>`;
        currentYear = yr;
      }
      
      html += `
        <div class="performance-item">
          <div class="performance-date">
            <div class="performance-day">${day}</div>
            <div class="performance-month">${month}</div>
          </div>
          <div class="performance-info">
            <h4>${item.titulo}</h4>
            <p>${item.descricao || ''}</p>
            <div class="performance-location">
              <i class="hugeicons-stroke-rounded-location-01" style="width:14px;height:14px;"></i> ${item.localizacao}
            </div>
          </div>
        </div>
      `;
    });
    
    container.innerHTML = html;
  }

  renderList('concursoContent', ATUACOES_DATA.festivais_concurso);
  renderList('conviteContent', ATUACOES_DATA.festivais_convite);
  renderList('outrasContent', ATUACOES_DATA.outras);
}

function renderLoja() {
  const container = document.getElementById('lojaContent');
  if (!container) return;

  container.innerHTML = LOJA_DATA.map(p => {
    let sizeSelector = '';
    if (p.tamanhos && Array.isArray(p.tamanhos) && p.tamanhos.length > 0) {
      sizeSelector = `
          <div class="size-selector">
            <label style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.3rem; display: block;">Tamanho:</label>
            <select class="size-select" style="width:100%; padding: 0.5rem; background: var(--bg-dark); border: 1px solid #333; color: white; border-radius: 4px; margin-bottom: 1rem;">
              <option value="">Selecionar...</option>
              ${p.tamanhos.map(s => `<option value="${s}">${s}</option>`).join('')}
            </select>
          </div>
      `;
    }

    return `
    <div class="shop-card" data-product-id="${p.id}" data-product-name="${p.nome}" data-product-price="${p.preco}" style="display: flex; flex-direction: column; height: 100%;">
      <div class="shop-card-image" style="background: url('${p.imagem || 'Logo oficial 2.png'}') center/cover; background-size: contain; background-repeat: no-repeat; background-color: var(--card-bg);">
        <div class="shop-card-badge">Merch</div>
      </div>
      <div class="shop-card-body" style="display: flex; flex-direction: column; flex-grow: 1;">
        <h4>${p.nome}</h4>
        <div class="price" style="font-size: 1.3rem; font-weight: 700; color: #000000; margin-bottom: 0.75rem;">€${p.preco.toFixed(2).replace('.', ',')}</div>
        <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1rem; line-height: 1.4;">
          ${p.descricao || 'Produto oficial Augustuna.'}
        </p>
        ${sizeSelector}
        <button class="btn btn-secondary" style="width: 100%; padding: 0.6rem; border-radius: 4px; font-weight: bold; border: 1px solid var(--dourado); margin-top: auto;" onclick="addToCart(this)">
          Adicionar
        </button>
      </div>
    </div>
  `;}).join('');
}

/* ============================================
   SPA ROUTER
   ============================================ */
function initRouter() {
  // Handle all data-page clicks
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('[data-page]');
    if (trigger) {
      e.preventDefault();
      const page = trigger.getAttribute('data-page');
      navigateTo(page);

      // Close mobile menu if open
      const mobile = document.getElementById('navMobile');
      const hamburger = document.getElementById('navHamburger');
      const overlay = document.getElementById('navMobileOverlay');
      if (mobile && mobile.classList.contains('active')) {
        mobile.classList.remove('active');
        if (hamburger) hamburger.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        document.body.style.overflow = '';
      }

      // Close bottom nav submenus
      const menuSobreNos = document.getElementById('menuSobreNos');
      const menuAtuacoes = document.getElementById('menuAtuacoes');
      if (menuSobreNos) menuSobreNos.classList.remove('active');
      if (menuAtuacoes) menuAtuacoes.classList.remove('active');
    }
  });

  // Handle browser back/forward
  window.addEventListener('popstate', (e) => {
    const page = e.state?.page || 'home';
    showPage(page, false);
  });

  // Initial page from URL hash
  const hash = window.location.hash.replace('#', '') || 'home';
  showPage(hash, false);
}

function navigateTo(page) {
  showPage(page, true);
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showPage(page, pushState = true) {
  const pageId = `page-${page}`;
  const target = document.getElementById(pageId);

  if (!target) {
    // Fallback to home
    showPage('home', pushState);
    return;
  }

  // Hide all pages
  document.querySelectorAll('.page-section').forEach(section => {
    section.classList.remove('active');
  });

  // Show target page
  target.classList.add('active');

  // Update URL
  if (pushState) {
    history.pushState({ page }, '', `#${page}`);
  }

  // Update active nav link
  updateActiveNav(page);

  // Re-initialize animations for the new page
  setTimeout(() => {
    initScrollAnimations();
    initCounters();
    // Huge Icons are font-based, no initialization needed
  }, 100);

  // Show/hide footer (always visible except on home)
  const footer = document.getElementById('footer');
  if (footer) {
    footer.style.display = page === 'home' ? 'none' : 'block';
  }
}

function updateActiveNav(page) {
  // Remove all active states
  document.querySelectorAll('.nav-link, .nav-bottom-link').forEach(link => {
    link.classList.remove('active');
  });

  // Map sub-pages to parent nav items
  const parentMap = {
    'formacao': 'sobre-nos',
    'traje': 'sobre-nos',
    'membros': 'sobre-nos',
    'musica': 'sobre-nos',
    'magna-augusta': 'sobre-nos',
    'festivais-concurso': 'atuacoes',
    'festivais-convite': 'atuacoes',
    'outras-atuacoes': 'atuacoes'
  };

  // Try to highlight the matching link
  document.querySelectorAll('[data-page]').forEach(link => {
    if (link.getAttribute('data-page') === page) {
      if (link.classList.contains('nav-link') || link.classList.contains('nav-bottom-link')) {
        link.classList.add('active');
      }
    }
  });

  // Highlight parent dropdown trigger for sub-pages
  const parent = parentMap[page];
  if (parent) {
    document.querySelectorAll('.nav-dropdown-trigger').forEach(trigger => {
      const text = trigger.textContent.trim().toLowerCase();
      if (parent === 'sobre-nos' && text.includes('sobre')) {
        trigger.classList.add('active');
      }
      if (parent === 'atuacoes' && text.includes('atua')) {
        trigger.classList.add('active');
      }
    });
  }
}

/* ============================================
   NAVIGATION
   ============================================ */
function initNavigation() {
  const nav = document.getElementById('nav');
  const hamburger = document.getElementById('navHamburger');
  const mobile = document.getElementById('navMobile');

  // Scroll effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  });

  // Hamburger toggle (Kept safe if it ever returns)
  if (hamburger && mobile) {
    const overlay = document.getElementById('navMobileOverlay');

    const closeMobile = () => {
      hamburger.classList.remove('active');
      mobile.classList.remove('active');
      if (overlay) overlay.classList.remove('active');
      document.body.style.overflow = '';
    };

    const openMobile = () => {
      hamburger.classList.add('active');
      mobile.classList.add('active');
      if (overlay) overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    };

    hamburger.addEventListener('click', () => {
      if (mobile.classList.contains('active')) {
        closeMobile();
      } else {
        openMobile();
      }
    });

    // Close on overlay click
    if (overlay) {
      overlay.addEventListener('click', closeMobile);
    }
  }

  /* Bottom Nav Dropdowns */
  const bottomSobreNos = document.getElementById('navBottomSobreNos');
  const menuSobreNos = document.getElementById('menuSobreNos');
  const bottomAtuacoes = document.getElementById('navBottomAtuacoes');
  const menuAtuacoes = document.getElementById('menuAtuacoes');

  function closeAllBottomMenus() {
    if (menuSobreNos) menuSobreNos.classList.remove('active');
    if (menuAtuacoes) menuAtuacoes.classList.remove('active');
  }

  if (bottomSobreNos && menuSobreNos) {
    bottomSobreNos.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const isActive = menuSobreNos.classList.contains('active');
      closeAllBottomMenus();
      if (!isActive) menuSobreNos.classList.add('active');
    });
  }

  if (bottomAtuacoes && menuAtuacoes) {
    bottomAtuacoes.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const isActive = menuAtuacoes.classList.contains('active');
      closeAllBottomMenus();
      if (!isActive) menuAtuacoes.classList.add('active');
    });
  }

  // Close menus when clicking anywhere else
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-bottom-item')) {
      closeAllBottomMenus();
    }
  });
}

/* ============================================
   DROPDOWNS
   ============================================ */
function initDropdowns() {
  // Desktop dropdowns (hover already in CSS, this adds click support)
  document.querySelectorAll('.nav-dropdown-trigger').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
    });
  });

  // Mobile dropdowns
  document.querySelectorAll('.nav-mobile-dropdown-trigger').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const menu = trigger.nextElementSibling;
      if (menu) {
        menu.classList.toggle('open');
        // Rotate chevron
        const chevron = trigger.querySelector('i');
        if (chevron) {
          chevron.style.transform = menu.classList.contains('open') ? 'rotate(180deg)' : '';
        }
      }
    });
  });
}

/* ============================================
   SHOPPING CART
   ============================================ */
let cart = [];

function initCart() {
  const checkoutForm = document.getElementById('checkoutForm');
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      if (cart.length === 0) {
        alert("O teu carrinho está vazio!");
        return;
      }
      
      // Initialize EmailJS with the Public Key
      emailjs.init("4GmdocNDaZch7KCVE");

      emailjs.send('service_4cidzzm', 'template_wemhxna', emailParams)
        .then(() => {
          // Success Callback
          cart = [];
          updateCartUI();
          checkoutForm.reset();
          submitBtn.innerHTML = 'Confirmar Encomenda';
          submitBtn.disabled = false;
          
          triggerSuccessAnimation();
          navigateTo('obrigado');
        })
        .catch((error) => {
          console.error("Erro ao enviar email:", error);
          alert("Ocorreu um erro ao processar a tua encomenda. Por favor tenta novamente ou contacta-nos diretamente.");
          submitBtn.innerHTML = 'Confirmar Encomenda';
          submitBtn.disabled = false;
        });
    });
  }
}

function addToCart(buttonElement) {
  const card = buttonElement.closest('.shop-card');
  if (!card) return;

  const id = card.dataset.productId;
  const name = card.dataset.productName;
  const price = parseFloat(card.dataset.productPrice);

  let size = null;
  const sizeSelect = card.querySelector('.size-select');
  if (sizeSelect) {
    size = sizeSelect.value;
    if (!size) {
      alert('Por favor, seleciona um tamanho antes de adicionar ao carrinho.');
      return;
    }
  }

  // Check if already in cart tracking ID + Size
  const existing = cart.find(item => item.id === id && item.size === size);
  if (existing) {
    existing.qty++;
  } else {
    cart.push({ id, name, price, qty: 1, size });
  }

  updateCartUI();

  // Button feedback
  const originalText = buttonElement.innerHTML;
  buttonElement.innerHTML = 'Adicionado!';
  buttonElement.style.background = '#27AE60';
  buttonElement.style.color = 'white';
  buttonElement.disabled = true;

  setTimeout(() => {
    buttonElement.innerHTML = originalText;
    buttonElement.style.background = '';
    buttonElement.style.color = '';
    buttonElement.disabled = false;
    // Huge Icons are font-based, no re-initialization needed
  }, 1500);
}

function removeFromCart(id, size = null) {
  cart = cart.filter(item => !(item.id === id && item.size === size));
  updateCartUI();
}

function updateCartUI() {
  const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
  const totalPrice = cart.reduce((sum, item) => sum + item.price * item.qty, 0);

  // Update badges
  document.querySelectorAll('.nav-cart-badge').forEach(badge => {
    badge.textContent = totalItems;
    badge.setAttribute('data-count', totalItems);
    badge.style.display = totalItems === 0 ? 'none' : 'flex';
  });

  // Update cart page
  const cartItems = document.getElementById('cartItems');
  const cartEmpty = document.getElementById('cartEmpty');
  const cartTotal = document.getElementById('cartTotal');
  const cartTotalPrice = document.getElementById('cartTotalPrice');

  if (!cartItems) return;

  if (cart.length === 0) {
    cartEmpty.style.display = 'block';
    cartItems.innerHTML = '';
    cartTotal.style.display = 'none';
  } else {
    cartEmpty.style.display = 'none';
    cartTotal.style.display = 'block';
    cartTotalPrice.textContent = `€${totalPrice.toFixed(2).replace('.', ',')}`;

    cartItems.innerHTML = cart.map(item => `
      <div class="cart-item">
        <div class="cart-item-info">
          <h4>${item.name}${item.size ? ` (Tamanho: ${item.size})` : ''}</h4>
          <p>€${item.price.toFixed(2).replace('.', ',')} × ${item.qty}</p>
        </div>
        <button class="cart-item-remove" onclick="removeFromCart('${item.id}', ${item.size ? `'${item.size}'` : null})">
          <i class="hugeicons-stroke-rounded-delete-02" style="width:18px;height:18px;"></i>
        </button>
      </div>
    `).join('');

    // Icons handled by font CSS
  }
}

// Checkout Success Animation
function triggerSuccessAnimation(callback) {
  // Play 'Tcharaaam' sound effect
  const audio = new Audio('https://actions.google.com/sounds/v1/cartoon/trumpet_fanfare.ogg');
  audio.volume = 0.6;
  audio.play().catch(e => console.log('Audio auto-play prevented:', e));

  // Fire confetti from edges
  const duration = 2000;
  const end = Date.now() + duration;

  (function frame() {
      // Check if confetti library exists, if not fallback to nothing or DOM confetti
      if (typeof confetti === 'function') {
          confetti({
              particleCount: 5,
              angle: 60,
              spread: 55,
              origin: { x: 0 },
              colors: ['#c9a84c', '#1b3a5c', '#ffffff']
          });
          confetti({
              particleCount: 5,
              angle: 120,
              spread: 55,
              origin: { x: 1 },
              colors: ['#c9a84c', '#1b3a5c', '#ffffff']
          });
      } else {
          // Fallback DOM based confetti just in case
          const conf = document.createElement('div');
          conf.className = 'dom-confetti';
          conf.style.position = 'fixed';
          const colors = ['#c9a84c', '#1b3a5c', '#ffffff'];
          conf.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
          conf.style.left = Math.random() * 100 + 'vw';
          conf.style.top = '-20px';
          conf.style.width = '10px';
          conf.style.height = '10px';
          conf.style.zIndex = '9999';
          document.body.appendChild(conf);
          setTimeout(() => conf.remove(), 2000);
      }

      if (Date.now() < end) {
          requestAnimationFrame(frame);
      }
  }());

  // Finish and invoke callback
  setTimeout(() => {
      if (callback) callback();
  }, 2000);
}

// Make functions globally available
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;

/* ============================================
   SCROLL ANIMATIONS
   ============================================ */
function initScrollAnimations() {
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .stagger-children');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0, rootMargin: '0px 0px -50px 0px' });

  reveals.forEach(el => {
    // Reset for re-observation on page change
    if (!el.classList.contains('active')) {
      observer.observe(el);
    }
  });
}

/* ============================================
   ANIMATED COUNTERS
   ============================================ */
function initCounters() {
  const counters = document.querySelectorAll('.hero-stat-number[data-count]');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        entry.target.dataset.counted = 'true';
        animateCounter(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => {
    if (!counter.dataset.counted) {
      observer.observe(counter);
    }
  });
}

function animateCounter(element) {
  const target = parseInt(element.dataset.count);
  const duration = 2000;
  const start = performance.now();
  const suffix = target >= 100 ? '+' : '';

  function update(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(target * easeOut);

    element.textContent = current + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}

/* ============================================
   MEMBERS DATA & RENDERING
   ============================================ */
/* MEMBERS_DATA is populated dynamically by fetchWebsiteData */

const GENERATION_ORDER = ['Fundadores', '2ª Geração', '3ª Geração', '4ª Geração', '5ª Geração', '6ª Geração', '7ª Geração', '8ª Geração', '9ª Geração', '10ª Geração', '11ª Geração', '12ª Geração', '13ª Geração', '14ª Geração', '15ª Geração', '16ª Geração', '17ª Geração', '18ª Geração', '19ª Geração', '20ª Geração', '21ª Geração'];

let activeGenFilters = [];
let activeInstFilters = [];
let currentSort = 'generation';

function initMembers() {
  const container = document.getElementById('membersContent');
  if (!container) return;

  // Build filter options
  const gens = [...new Set(MEMBERS_DATA.map(m => m.geracao))];
  gens.sort((a, b) => GENERATION_ORDER.indexOf(a) - GENERATION_ORDER.indexOf(b));
  const insts = [...new Set(MEMBERS_DATA.flatMap(m => m.instrumento.split('/').map(i => i.trim())))].sort();

  const genContainer = document.getElementById('filterGeneration');
  const instContainer = document.getElementById('filterInstrument');
  if (genContainer) {
    genContainer.innerHTML = gens.map(g => `<label class="filter-option"><input type="checkbox" value="${g}"> ${g}</label>`).join('');
    genContainer.addEventListener('change', () => { activeGenFilters = [...genContainer.querySelectorAll('input:checked')].map(i => i.value); renderMembers(); });
  }
  if (instContainer) {
    instContainer.innerHTML = insts.map(i => `<label class="filter-option"><input type="checkbox" value="${i}"> ${i}</label>`).join('');
    instContainer.addEventListener('change', () => { activeInstFilters = [...instContainer.querySelectorAll('input:checked')].map(i => i.value); renderMembers(); });
  }

  // Sort buttons
  document.querySelectorAll('.sort-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentSort = btn.dataset.sort;
      renderMembers();
    });
  });

  // Clear filters
  const clearBtn = document.getElementById('clearFilters');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      activeGenFilters = [];
      activeInstFilters = [];
      document.querySelectorAll('.filter-option input').forEach(i => i.checked = false);
      renderMembers();
    });
  }

  renderMembers();
}

function renderMembers() {
  const container = document.getElementById('membersContent');
  if (!container) return;

  let filtered = MEMBERS_DATA.filter(m => {
    if (activeGenFilters.length && !activeGenFilters.includes(m.geracao)) return false;
    if (activeInstFilters.length) {
      const memberInsts = m.instrumento.split('/').map(i => i.trim());
      if (!activeInstFilters.some(f => memberInsts.includes(f))) return false;
    }
    return true;
  });

  // Sort
  if (currentSort === 'alpha-asc') filtered.sort((a, b) => a.name.localeCompare(b.name, 'pt'));
  else if (currentSort === 'alpha-desc') filtered.sort((a, b) => b.name.localeCompare(a.name, 'pt'));
  else if (currentSort === 'date-asc') filtered.sort((a, b) => (a.data || '').localeCompare(b.data || ''));
  else if (currentSort === 'date-desc') filtered.sort((a, b) => (b.data || '').localeCompare(a.data || ''));
  else filtered.sort((a, b) => GENERATION_ORDER.indexOf(a.geracao) - GENERATION_ORDER.indexOf(b.geracao));

  // Group by generation if sorting by generation
  if (currentSort === 'generation') {
    const groups = {};
    filtered.forEach(m => { (groups[m.geracao] = groups[m.geracao] || []).push(m); });
    const orderedGens = Object.keys(groups).sort((a, b) => GENERATION_ORDER.indexOf(a) - GENERATION_ORDER.indexOf(b));
    container.innerHTML = orderedGens.map(gen => `
      <div class="generation-group">
        <div class="generation-header">
          <h3>${gen}</h3>
          <div class="gen-line"></div>
          <span class="gen-count">${groups[gen].length} tuno${groups[gen].length !== 1 ? 's' : ''}</span>
        </div>
        <div class="generation-members">${groups[gen].map(renderMemberCard).join('')}</div>
      </div>
    `).join('');
  } else {
    container.innerHTML = `<div class="generation-members">${filtered.map(renderMemberCard).join('')}</div>`;
    if (!filtered.length) container.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:3rem;">Nenhum membro encontrado com os filtros selecionados.</p>';
  }

  // Icons handled by font CSS
}

function renderMemberCard(m) {
  const initials = m.alcunha ? m.alcunha.charAt(0).toUpperCase() : m.name.charAt(0).toUpperCase();
  const instruments = m.instrumento.split('/').map(i => `<span class="instrument-badge">${i.trim()}</span>`).join('');
  const dateStr = m.data ? new Date(m.data).getFullYear() : '';
  
  const avatarHTML = m.foto ? 
    `<img src="${m.foto}" alt="${m.name}" class="member-card-v2-img">` :
    `<div class="member-card-v2-avatar">${initials}</div>`;

  return `
    <div class="member-card-v2">
      <div class="member-card-v2-header">
        ${avatarHTML}
        <div class="member-card-v2-name">
          <h4>${m.name}</h4>
          ${m.alcunha ? `<span class="alcunha">"${m.alcunha}"</span>` : ''}
        </div>
      </div>
      <div class="member-card-v2-meta">
        ${m.curso ? `<span><i class="hugeicons-stroke-rounded-graduation-cap" style="width:12px;height:12px;"></i> ${m.curso}</span>` : ''}
        ${m.evento ? `<span><i class="hugeicons-stroke-rounded-calendar-01" style="width:12px;height:12px;"></i> ${m.evento}${dateStr ? ' (' + dateStr + ')' : ''}</span>` : ''}
      </div>
      <div class="member-card-v2-badges">${instruments}</div>
    </div>
  `;
}

/* ============================================
   NEWS TABS
   ============================================ */
function initNewsTabs() {
  document.querySelectorAll('.news-tab:not(.generic-tab)').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.news-tab:not(.generic-tab)').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.dataset.filter;
      document.querySelectorAll('.news-card-v2').forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
}

/* ============================================
   GENERIC TABS
   ============================================ */
function initGenericTabs() {
  const tabGroups = document.querySelectorAll('.tab-group');
  tabGroups.forEach(group => {
    const tabs = group.querySelectorAll('.generic-tab');
    const contents = group.querySelectorAll('.generic-tab-content');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const targetId = tab.dataset.target;
        contents.forEach(content => {
          if (content.id === targetId) {
            content.classList.remove('hidden');
            // small delay to trigger reflow and css transition if any
            setTimeout(() => {
              content.style.opacity = '1';
            }, 50);
          } else {
            content.classList.add('hidden');
            content.style.opacity = '0';
          }
        });
      });
    });
  });
}

/* ============================================
   CONTACTOS (DYNAMIC RENDER)
   ============================================ */
function renderContactos() {
  if (!CONTACTOS_DATA) return;

  const socialContainer = document.getElementById('socialLinksContent');
  if (socialContainer) {
    const s = CONTACTOS_DATA.redes_sociais;
    socialContainer.innerHTML = `
      <a href="${s.youtube || '#'}" target="_blank" class="social-link-card">
        <div class="social-icon-box youtube">
          <i class="hugeicons-stroke-rounded-youtube" style="width:24px;height:24px;"></i>
        </div>
        <span>YouTube</span>
      </a>
      <a href="${s.instagram || '#'}" target="_blank" class="social-link-card">
        <div class="social-icon-box instagram">
          <i class="hugeicons-stroke-rounded-instagram" style="width:24px;height:24px;"></i>
        </div>
        <span>Instagram</span>
      </a>
      <a href="${s.facebook || '#'}" target="_blank" class="social-link-card">
        <div class="social-icon-box facebook">
          <i class="hugeicons-stroke-rounded-facebook-01" style="width:24px;height:24px;"></i>
        </div>
        <span>Facebook</span>
      </a>
      <a href="${s.linkedin || '#'}" target="_blank" class="social-link-card">
        <div class="social-icon-box linkedin">
          <i class="hugeicons-stroke-rounded-linkedin-01" style="width:24px;height:24px;"></i>
        </div>
        <span>LinkedIn</span>
      </a>
      <a href="${s.spotify || '#'}" target="_blank" class="social-link-card">
        <div class="social-icon-box spotify" style="background: rgba(30, 215, 96, 0.1); color: #1DB954;">
          <i class="hugeicons-stroke-rounded-music-01" style="width:32px;height:32px;"></i>
        </div>
        <span>Spotify</span>
      </a>
    `;
  }

  const dirigentesContainer = document.getElementById('dirigentesContent');
  if (dirigentesContainer && CONTACTOS_DATA.dirigentes) {
    dirigentesContainer.innerHTML = `
      <div class="personal-contact-card">
        <div class="personal-contact-icon email-icon" style="background: var(--azul-profundo);">
          <i class="hugeicons-stroke-rounded-mail-01" style="width:24px;height:24px;color:#ffffff;"></i>
        </div>
        <h4>Email Geral</h4>
        <p class="personal-contact-desc">Para questões gerais e informações</p>
        <a href="mailto:${CONTACTOS_DATA.informacoes_gerais.email || 'augustunataum@gmail.com'}" class="personal-contact-action">${CONTACTOS_DATA.informacoes_gerais.email || 'augustunataum@gmail.com'}</a>
      </div>
      ${CONTACTOS_DATA.dirigentes.map(d => `
        <div class="personal-contact-card">
          <div class="personal-contact-icon person-icon" style="background: var(--azul-profundo);">
            <i class="hugeicons-stroke-rounded-user" style="width:24px;height:24px;color:#ffffff;"></i>
          </div>
          <h4>${d.cargo}</h4>
          <p class="personal-contact-name">${d.nome}</p>
          <a href="tel:${d.telefone.replace(/ /g, '')}" class="personal-contact-action">
            ${d.telefone}
          </a>
        </div>
      `).join('')}
    `;
  }

  const infoGeraisContainer = document.getElementById('infogeraisContent');
  if (infoGeraisContainer) {
    const info = CONTACTOS_DATA.informacoes_gerais;
    infoGeraisContainer.innerHTML = `
      <div class="contact-info-item">
        <div class="contact-info-icon">
          <i class="hugeicons-stroke-rounded-location-01" style="width:20px;height:20px;"></i>
        </div>
        <div>
          <h4>Morada</h4>
          <p>${info.morada || 'Universidade do Minho<br>Campus de Gualtar, Braga'}</p>
        </div>
      </div>
      <div class="contact-info-item">
        <div class="contact-info-icon">
          <i class="hugeicons-stroke-rounded-mail-01" style="width:20px;height:20px;"></i>
        </div>
        <div>
          <h4>Email</h4>
          <p>${info.email || 'augustunataum@gmail.com'}</p>
        </div>
      </div>
      <div class="contact-info-item">
        <div class="contact-info-icon">
          <i class="hugeicons-stroke-rounded-phone-01" style="width:20px;height:20px;"></i>
        </div>
        <div>
          <h4>Telefone</h4>
          <p>${info.telefone || '+351 931 311 840'}</p>
        </div>
      </div>
    `;
  }

  // Icons handled by font CSS
}
