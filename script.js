/* ============================================
   AUGUSTUNA — JavaScript
   SPA Routing, Cart, Dropdowns, Animations
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons
  if (typeof lucide !== 'undefined') {
    try {
      lucide.createIcons();
    } catch(err) {
      console.warn('Alguns ícones Lucide não foram carregados:', err);
    }
  }

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
    if (typeof lucide !== 'undefined') {
      lucide.createIcons();
    }
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
        const chevron = trigger.querySelector('[data-lucide]');
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
      
      const submitBtn = document.getElementById('submitOrderBtn');
      submitBtn.innerHTML = '<i data-lucide="loader" class="spin"></i> A Processar...';
      submitBtn.disabled = true;

      const nomeCliente = document.getElementById('checkoutName').value;
      const email = document.getElementById('checkoutEmail').value;
      const phone = document.getElementById('checkoutPhone').value;
      const notes = document.getElementById('checkoutNotes').value;
      
      const detalhesCarrinho = cart.map(item => {
        const sizeStr = item.size ? ` - Tam: ${item.size}` : '';
        return `${item.qty}x ${item.name}${sizeStr} (€${(item.price * item.qty).toFixed(2).replace('.', ',')})`;
      }).join('\n');
      
      const valorTotal = cart.reduce((sum, item) => sum + item.price * item.qty, 0).toFixed(2).replace('.', ',') + '€';

      // Mapping variables according to task requirements
      const emailParams = {
        nome_cliente: nomeCliente,
        name: nomeCliente, // fallback for safety
        email: email,
        telefone: phone,
        detalhes_carrinho: detalhesCarrinho,
        valor_total: valorTotal,
        message: notes || 'Sem notas adicionais'
      };

      if (typeof emailjs === 'undefined') {
        alert('Serviço de email indisponível. Por favor, tenta mais tarde.');
        submitBtn.innerHTML = 'Confirmar Encomenda';
        submitBtn.disabled = false;
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
  buttonElement.innerHTML = '<i data-lucide="check" style="width:16px;height:16px;"></i> Adicionado!';
  buttonElement.style.background = '#27AE60';
  buttonElement.style.color = 'white';
  buttonElement.disabled = true;

  setTimeout(() => {
    buttonElement.innerHTML = originalText;
    buttonElement.style.background = '';
    buttonElement.style.color = '';
    buttonElement.disabled = false;
    if (typeof lucide !== 'undefined') lucide.createIcons();
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
          <i data-lucide="trash-2" style="width:18px;height:18px;"></i>
        </button>
      </div>
    `).join('');

    if (typeof lucide !== 'undefined') lucide.createIcons();
  }
}

function triggerSuccessAnimation() {
  const overlay = document.createElement('div');
  overlay.className = 'success-overlay';
  overlay.innerHTML = `
    <div class="tuno-venia-container">
      <div class="tricornio">🎓</div>
      <div class="tuno-figure">🤵</div>
    </div>
    <div class="success-text">Vénia Académica!</div>
    <div style="font-size: 1.2rem; margin-top: 1rem; color: var(--branco-perola); font-family: var(--font-body);">A tua encomenda foi recebida com sucesso.</div>
  `;
  document.body.appendChild(overlay);

  const colors = ['#D4AF37', '#1B3A5C', '#ffffff', '#e74c3c'];

  for(let i = 0; i < 150; i++) {
    const conf = document.createElement('div');
    conf.style.position = 'absolute';
    conf.style.width = (Math.random() * 8 + 4) + 'px';
    conf.style.height = (Math.random() * 8 + 4) + 'px';
    conf.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    conf.style.left = Math.random() * 100 + 'vw';
    conf.style.top = '-20px';
    conf.style.opacity = Math.random() + 0.5;
    conf.style.transform = `rotate(${Math.random() * 360}deg)`;
    conf.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
    conf.style.zIndex = '10001';
    
    // Animate falling
    const duration = Math.random() * 3 + 2;
    conf.style.animation = `fallDown ${duration}s linear forwards`;
    overlay.appendChild(conf);
  }

  setTimeout(() => {
    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.5s ease';
    setTimeout(() => overlay.remove(), 500);
  }, 4000);
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
const MEMBERS_DATA = [
  { name: "Carlos Manuel Fernandes da Silva", alcunha: "Pamelo", instrumento: "Braguesa", evento: "Fundação", data: "1996-02-28", curso: "Ensino Português - Inglês", geracao: "Fundadores" },
  { name: "Maria João Barbosa da Silva Martins", alcunha: "General", instrumento: "Estandarte", evento: "Fundação", data: "1996-02-28", curso: "Ensino Português - Inglês", geracao: "Fundadores" },
  { name: "Fernando Miguel Brito Faria", alcunha: "Aranha", instrumento: "Bandolim", evento: "Fundação", data: "1996-02-28", curso: "Engenharia de Materiais", geracao: "Fundadores" },
  { name: "Filipe Alexandre Hipólito Proença Caiado Márcia", alcunha: "Piçalho", instrumento: "Guitarra", evento: "Fundação", data: "1996-02-28", curso: "Engenharia de Materiais", geracao: "Fundadores" },
  { name: "João Manuel Araújo Cruz", alcunha: "Krika", instrumento: "Guitarra", evento: "Fundação", data: "1996-02-28", curso: "Sociologia", geracao: "Fundadores" },
  { name: "José Carlos Ferreira da Silva", alcunha: "Balastro", instrumento: "Voz", evento: "Fundação", data: "1996-02-28", curso: "Ensino Português - Inglês", geracao: "Fundadores" },
  { name: "Carlos Alberto Moreira de Araújo", alcunha: "Jumbo", instrumento: "Guitarra", evento: "Fundação", data: "1996-02-28", curso: "Ensino Português - Inglês", geracao: "Fundadores" },
  { name: "Maria de Fátima Duarte Ferreira", alcunha: "Pinypon", instrumento: "Guitarra", evento: "Fundação", data: "1996-02-28", curso: "Ensino Português - Inglês", geracao: "Fundadores" },
  { name: "Jorge Manuel Campos Pinto", alcunha: "60 Litros", instrumento: "Bandola", evento: "Fundação", data: "1996-02-28", curso: "Economia", geracao: "Fundadores" },
  { name: "Maria Vitória Sampaio de Carvalho Antunes", alcunha: "Corvo", instrumento: "Contrabaixo", evento: "Fundação", data: "1996-10-01", curso: "Economia", geracao: "Fundadores" },
  { name: "Regina Isabel da Mota Carneiro", alcunha: "Mémé", instrumento: "Guitarra", evento: "Fundação", data: "1996-02-28", curso: "Ensino Português - Inglês", geracao: "Fundadores" },
  { name: "Alexandra Maria Costa Duarte", alcunha: "Bocas", instrumento: "Pandeireta", evento: "Récita", data: "1998-12-01", curso: "Ensino Português - Inglês", geracao: "2ª Geração" },
  { name: "Catarina Adelaide Fernandes Fonseca", alcunha: "Rancha", instrumento: "Acordeão", evento: "Récita", data: "1998-12-01", curso: "Comunicação Social", geracao: "2ª Geração" },
  { name: "Mara Helena Ferreira da Silva Dória", alcunha: "Chicla", instrumento: "Cavaquinho", evento: "Récita", data: "1998-12-01", curso: "Engenharia de Materiais/Geologia", geracao: "2ª Geração" },
  { name: "Pedro Henrique Rodrigues Vale", alcunha: "Laurindo", instrumento: "Guitarra", evento: "Récita", data: "1998-12-01", curso: "Direito", geracao: "2ª Geração" },
  { name: "João Paulo Paupério", alcunha: "Tarrafal", instrumento: "Pandeireta", evento: "Sala da Tuna", data: "1999-01-01", curso: "Relações Internacionais", geracao: "2ª Geração" },
  { name: "Sónia Raquel da Costa Marques", alcunha: "XIU", instrumento: "Acordeão", evento: "", data: "2000-01-01", curso: "Comunicação Social", geracao: "3ª Geração" },
  { name: "Ana Maria Fernandes dos Santos Oliveira", alcunha: "Pissup", instrumento: "Braguesa", evento: "Velório da Gata", data: "2000-01-01", curso: "Direito", geracao: "3ª Geração" },
  { name: "Miguel Ângelo Martins da Silva Rêgo", alcunha: "Cisterna", instrumento: "Voz", evento: "Tuno Convidado", data: "2003-01-01", curso: "Engenharia Agrícola/Biologia Aplicada", geracao: "4ª Geração" },
  { name: "Rui Nuno Calisto Araujo de Melo", alcunha: "Mijeira", instrumento: "Pandeireta", evento: "Tuno Convidado", data: "2003-01-01", curso: "Engenharia Mecânica", geracao: "4ª Geração" },
  { name: "Pedro Miguel Azevedo Paredes", alcunha: "Dromedário", instrumento: "Guitarra", evento: "Tuno Convidado", data: "2003-01-01", curso: "Ensino de Biologia e Geologia", geracao: "4ª Geração" },
  { name: "Hélder Daniel Ribeiro de Carvalho", alcunha: "Jagunço", instrumento: "Estandarte", evento: "VII Festival do ISMAI", data: "2003-11-20", curso: "Gestão", geracao: "4ª Geração" },
  { name: "António Castro", alcunha: "Falo", instrumento: "Acordeão", evento: "", data: "2004-01-01", curso: "Física", geracao: "5ª Geração" },
  { name: "André Costa Cardoso", alcunha: "Bexiga", instrumento: "Contrabaixo", evento: "", data: "2004-12-09", curso: "Relações Internacionais", geracao: "5ª Geração" },
  { name: "Vasco Martins", alcunha: "Sacas", instrumento: "Bandolim", evento: "", data: "2004-12-09", curso: "Relações Internacionais", geracao: "5ª Geração" },
  { name: "Luís Filipe Pinto Pereira", alcunha: "Múmia", instrumento: "Guitarra", evento: "Récita", data: "2005-12-01", curso: "Arqueologia", geracao: "6ª Geração" },
  { name: "Afonso João Esteves Pizarro Dias", alcunha: "Rabeca", instrumento: "Violino", evento: "Jantar do Caloiro", data: "2006-10-11", curso: "Relações Internacionais", geracao: "7ª Geração" },
  { name: "Emanuel de Oliveira", alcunha: "Bush", instrumento: "Percussão", evento: "XI Aniversário da Tuna", data: "2007-03-02", curso: "Gestão", geracao: "8ª Geração" },
  { name: "Fernando Almeida Martins", alcunha: "Tachas", instrumento: "Trompete", evento: "I CIRTAV", data: "2007-06-10", curso: "Relações Internacionais", geracao: "8ª Geração" },
  { name: "Ricardo Emanuel Agostinho Coelho", alcunha: "George Michael", instrumento: "Contrabaixo", evento: "Récita", data: "2013-12-01", curso: "Línguas e Culturas Orientais", geracao: "10ª Geração" },
  { name: "José Rafael Azevedo Teixeira Gonçalves", alcunha: "Profeta", instrumento: "Guitarra", evento: "Récita", data: "2013-12-01", curso: "Ciência Política", geracao: "10ª Geração" },
  { name: "Carlos Filipe Mesquita Teixeira", alcunha: "Passos Recluso", instrumento: "Guitarra", evento: "Récita", data: "2013-12-01", curso: "Psicologia", geracao: "10ª Geração" },
  { name: "Diogo Alberto Ferreira Lima", alcunha: "Pito", instrumento: "Bandolim", evento: "Receção ao Caloiro", data: "2014-10-04", curso: "Psicologia", geracao: "11ª Geração" },
  { name: "Nuno Miguel Mota Pereira", alcunha: "Phineas", instrumento: "Bandolim", evento: "Receção ao Caloiro", data: "2014-10-04", curso: "Relações Internacionais", geracao: "11ª Geração" },
  { name: "Vitor Hugo Simões da Silva", alcunha: "Assandes", instrumento: "Guitarra", evento: "Récita", data: "2014-12-01", curso: "Línguas e Culturas Orientais", geracao: "11ª Geração" },
  { name: "Flávio António Silva Ferreira", alcunha: "Kirk", instrumento: "Braguesa", evento: "Récita", data: "2014-12-01", curso: "Engenharia Civil", geracao: "11ª Geração" },
  { name: "Eduardo Luís Carvalho Ferreira", alcunha: "Marco Paulo", instrumento: "Cavaquinho", evento: "Receção ao Caloiro", data: "2014-10-04", curso: "Direito", geracao: "11ª Geração" },
  { name: "Miguel Duarte Gonçalves Fontoura", alcunha: "Centoura", instrumento: "Acordeão", evento: "Récita", data: "2016-12-01", curso: "Administração Pública", geracao: "12ª Geração" },
  { name: "Paulo Virgílio Gonçalves Fernandes Diz", alcunha: "Silvas", instrumento: "Voz", evento: "Récita", data: "2016-12-01", curso: "Línguas e Culturas Orientais", geracao: "12ª Geração" },
  { name: "Dário Castro Dias", alcunha: "Borbogoucha", instrumento: "Percussão", evento: "Festa do Semina", data: "2017-02-14", curso: "Administração Pública", geracao: "13ª Geração" },
  { name: "Pedro Moreira Ferraz", alcunha: "Zé Miguel", instrumento: "Bandolim", evento: "Enterro da Gata", data: "2017-05-16", curso: "Direito", geracao: "13ª Geração" },
  { name: "Gonçalo Martins de Matos", alcunha: "Badjoraz", instrumento: "Voz/Cavaquinho", evento: "Enterro da Gata", data: "2017-05-16", curso: "Direito", geracao: "13ª Geração" },
  { name: "Daniel Diaz Costa", alcunha: "Cont'Aquela", instrumento: "Braguesa", evento: "III Magna Augusta", data: "2018-03-17", curso: "Engenharia Mecânica", geracao: "14ª Geração" },
  { name: "João Filipe da Silva Barros", alcunha: "Envergonhado", instrumento: "Guitarra", evento: "III Magna Augusta", data: "2018-03-17", curso: "Filosofia", geracao: "14ª Geração" },
  { name: "Afonso Miguel Capela Reis Oliveira Arantes", alcunha: "Esquivas", instrumento: "Bandolim", evento: "III Magna Augusta", data: "2018-03-17", curso: "Engenharia Mecânica", geracao: "14ª Geração" },
  { name: "António Pedro Carvalho Moreira", alcunha: "Beijo Negro", instrumento: "Guitarra", evento: "Receção ao Caloiro", data: "2018-10-04", curso: "Negócios Internacionais", geracao: "14ª Geração" },
  { name: "Diogo Miguel Rodrigues de Almeida", alcunha: "Rolhão", instrumento: "Percussão", evento: "Receção ao Caloiro", data: "2018-10-04", curso: "Marketing", geracao: "14ª Geração" },
  { name: "David Pires Barbosa", alcunha: "Dona Teresa", instrumento: "Estandarte", evento: "Récita", data: "2018-12-01", curso: "Engenharia de Sistemas & Informática", geracao: "14ª Geração" },
  { name: "Pedro Afonso Dordio Pedras", alcunha: "Mito", instrumento: "Bandolim", evento: "IV Magna Augusta", data: "2019-03-22", curso: "Negócios Internacionais", geracao: "15ª Geração" },
  { name: "João Francisco Vieira Marques Charréu", alcunha: "Caguei", instrumento: "Pandeireta", evento: "IV Magna Augusta", data: "2019-03-22", curso: "Filosofia", geracao: "15ª Geração" },
  { name: "João Carlos do Ouro Peixoto Alves Pereira", alcunha: "Paraquedista", instrumento: "Estandarte", evento: "IV Magna Augusta", data: "2019-03-22", curso: "Ciências do Ambiente", geracao: "15ª Geração" },
  { name: "Daniel Filipe Almeida Couto Correia Dias", alcunha: "Esporras", instrumento: "Bandolim", evento: "XI Collipo", data: "2020-03-06", curso: "Engenharia Biológica", geracao: "16ª Geração" },
  { name: "António Pedro Gonçalves Pereira", alcunha: "Baby Jesus", instrumento: "Acordeão", evento: "Retiro", data: "2021-07-17", curso: "Engenharia Física", geracao: "17ª Geração" },
  { name: "Elízio Maria Oliveira Verdial", alcunha: "Finch", instrumento: "Guitarra", evento: "Retiro", data: "2021-07-17", curso: "Direito", geracao: "17ª Geração" },
  { name: "Igor José Ramalho Rodrigues", alcunha: "Finoco", instrumento: "Pandeireta", evento: "Retiro", data: "2021-07-17", curso: "História", geracao: "17ª Geração" },
  { name: "Diogo Filipe Braga Baptista", alcunha: "Postas", instrumento: "Contrabaixo", evento: "Retiro", data: "2021-07-17", curso: "Gestão", geracao: "17ª Geração" },
  { name: "José João Cardoso Simões Araújo", alcunha: "Yoda", instrumento: "Braguesa", evento: "Retiro", data: "2021-07-17", curso: "Ciências do Ambiente", geracao: "17ª Geração" },
  { name: "Adão Fernandes Rocha", alcunha: "À Porta", instrumento: "Pandeireta", evento: "Receção ao Caloiro", data: "2021-11-04", curso: "Química", geracao: "17ª Geração" },
  { name: "Afonso Quintas Costeira", alcunha: "Tou", instrumento: "Percussão", evento: "Receção ao Caloiro", data: "2021-11-04", curso: "Física", geracao: "17ª Geração" },
  { name: "José Pedro Sampaio Cunha", alcunha: "Eco-Escroto", instrumento: "Contrabaixo", evento: "V Magna Augusta", data: "2022-03-25", curso: "Física", geracao: "18ª Geração" },
  { name: "Dionísio Emanuel Piairo Pereira", alcunha: "Lam'Cona", instrumento: "Bandolim", evento: "Enterro da Gata", data: "2022-05-08", curso: "História", geracao: "18ª Geração" },
  { name: "Rui Pedro Magalhães Torres", alcunha: "Avenger", instrumento: "Bandolim", evento: "Receção ao Caloiro", data: "2022-10-13", curso: "Ciências da Computação", geracao: "18ª Geração" },
  { name: "Fábio Martins Branquinho", alcunha: "Erudito", instrumento: "Estandarte", evento: "Récita", data: "2022-11-30", curso: "Arqueologia", geracao: "18ª Geração" },
  { name: "David Gonçalo Lemos Oliveira", alcunha: "Sheik", instrumento: "Cajón", evento: "Récita", data: "2022-11-30", curso: "História", geracao: "18ª Geração" },
  { name: "André Lopes Domingues", alcunha: "Timão", instrumento: "Bandolim", evento: "Récita", data: "2022-11-30", curso: "Arqueologia", geracao: "18ª Geração" },
  { name: "Bruno Francisco Carneiro de Vilhena Dias", alcunha: "Escondidinhas", instrumento: "Pandeireta", evento: "VI Magna Augusta", data: "2023-03-10", curso: "História", geracao: "19ª Geração" },
  { name: "José Filipe da Costa Ribeiro", alcunha: "Popeye", instrumento: "Guitarra", evento: "VI Magna Augusta", data: "2023-03-10", curso: "Administração Pública", geracao: "19ª Geração" },
  { name: "António Miguel Ribeiro de Freitas Mendes", alcunha: "SARS", instrumento: "Guitarra", evento: "VI Magna Augusta", data: "2023-03-10", curso: "História", geracao: "19ª Geração" },
  { name: "Guilherme Oliveira de Lourdes Coutinho", alcunha: "Alijó", instrumento: "Pandeireta", evento: "Enterro da Gata", data: "2023-05-07", curso: "Química", geracao: "19ª Geração" },
  { name: "Gonçalo Guimarães de Sequeira Braga", alcunha: "Jolinhas", instrumento: "Cavaquinho", evento: "Receção ao Caloiro", data: "2023-09-28", curso: "Engenharia Biológica", geracao: "19ª Geração" },
  { name: "Pedro Ilídio Lemos Freitas", alcunha: "Grego", instrumento: "Pandeireta", evento: "Receção ao Caloiro", data: "2023-09-28", curso: "História", geracao: "19ª Geração" },
  { name: "Diogo João Santos Brito", alcunha: "Placona", instrumento: "Estandarte", evento: "Récita", data: "2023-11-30", curso: "Arqueologia", geracao: "20ª Geração" }
];

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

  if (typeof lucide !== 'undefined') lucide.createIcons();
}

function renderMemberCard(m) {
  const initials = m.alcunha ? m.alcunha.charAt(0).toUpperCase() : m.name.charAt(0).toUpperCase();
  const instruments = m.instrumento.split('/').map(i => `<span class="instrument-badge">${i.trim()}</span>`).join('');
  const dateStr = m.data ? new Date(m.data).getFullYear() : '';
  return `
    <div class="member-card-v2">
      <div class="member-card-v2-header">
        <div class="member-card-v2-avatar">${initials}</div>
        <div class="member-card-v2-name">
          <h4>${m.name}</h4>
          ${m.alcunha ? `<span class="alcunha">"${m.alcunha}"</span>` : ''}
        </div>
      </div>
      <div class="member-card-v2-meta">
        ${m.curso ? `<span><i data-lucide="graduation-cap" style="width:12px;height:12px;"></i> ${m.curso}</span>` : ''}
        ${m.evento ? `<span><i data-lucide="calendar" style="width:12px;height:12px;"></i> ${m.evento}${dateStr ? ' (' + dateStr + ')' : ''}</span>` : ''}
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
