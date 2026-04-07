import React, { useState, useEffect, createContext, useContext } from 'react';
import { Moon, Sun, Ticket, ChevronRight, MapPin, Clock, User, CheckCircle, Info, HelpCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';

// --- Theme Context ---
const ThemeContext = createContext();

const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('dark');
  
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// --- Mock Data ---
const CINEMAS = [
  "NOS Forum Madeira", "NOS Évora Plaza", "NOS Mar Algarve Shopping", 
  "NOS Glicínias", "NOS Forum Viseu", "NOS Braga Parque", 
  "NOS Nosso Shopping", "NOS Gaia Shopping", "NOS Mar Matosinhos Shopping", 
  "NOS Colombo", "NOS Almada Forum", "NOS Alvaláxia"
];

// --- Components ---

const Navbar = () => {
  const { theme, toggleTheme } = useContext(ThemeContext);
  
  return (
    <nav style={{
      position: 'fixed', top: 0, width: '100%', zIndex: 1000,
      padding: '24px 0', transition: 'all 0.3s ease',
      background: 'rgba(var(--bg-primary-rgb), 0.8)',
      backdropFilter: 'blur(10px)', borderBottom: '1px solid var(--border-color)'
    }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px', height: '40px', borderRadius: '50%',
            background: 'linear-gradient(45deg, var(--nos-magenta), var(--nos-blue))',
            display: 'flex', justifyContent: 'center', alignItems: 'center'
          }}>
            <Ticket color="white" size={24} />
          </div>
          <span style={{ fontSize: '24px', fontWeight: '800', letterSpacing: '-1px' }}>NOS <span className="premium-gradient-text">CINEMAS</span></span>
        </div>
        
        <button onClick={toggleTheme} style={{
          padding: '10px', borderRadius: '50%', background: 'var(--bg-secondary)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          transition: 'var(--transition-smooth)'
        }}>
          {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
        </button>
      </div>
    </nav>
  );
};

const Hero = ({ onStart }) => {
  return (
    <section style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center',
      paddingTop: '100px', position: 'relative', overflow: 'hidden'
    }}>
      {/* Background Image / Overlay */}
      <div style={{
        position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
        backgroundImage: `url('/eyes_wide_shut_hero.png')`,
        backgroundSize: 'cover', backgroundPosition: 'center',
        opacity: 0.4, zIndex: -1
      }} />
      <div style={{
        position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
        background: 'linear-gradient(to bottom, transparent, var(--bg-primary))',
        zIndex: -1
      }} />

      <div className="container">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          style={{ maxWidth: '700px' }}
        >
          <span style={{
            textTransform: 'uppercase', letterSpacing: '4px', fontSize: '14px',
            fontWeight: '600', color: 'var(--nos-magenta)', marginBottom: '16px', display: 'block'
          }}>Dia Mundial do Cinema • 5 Novembro 2026</span>
          
          <h1 style={{ fontSize: 'clamp(48px, 8vw, 84px)', fontWeight: '800', lineHeight: '1', marginBottom: '24px' }}>
            EYES WIDE <span className="premium-gradient-text">SHUT</span>
          </h1>
          
          <p style={{ fontSize: '18px', color: 'var(--text-secondary)', marginBottom: '40px', lineHeight: '1.6' }}>
            Assista à obra-prima de Stanley Kubrick na tela grande. 
            Uma noite de mistério e fidelidade. Registe-se agora para ganhar uma experiência exclusiva NOS Cinemas.
          </p>
          
          <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
            <button 
              onClick={onStart}
              className="glass-card"
              style={{
                padding: '16px 40px', background: 'var(--nos-magenta)', color: 'white',
                fontWeight: '700', borderRadius: '100px', display: 'flex', alignItems: 'center',
                gap: '8px', boxShadow: '0 10px 20px rgba(230, 0, 126, 0.3)',
                transition: 'var(--transition-smooth)'
              }}
              onMouseEnter={(e) => e.target.style.transform = 'translateY(-4px)'}
              onMouseLeave={(e) => e.target.style.transform = 'translateY(0)'}
            >
              Participar agora <ChevronRight size={20} />
            </button>
            
            <button 
              style={{
                padding: '16px 40px', background: 'var(--bg-secondary)',
                fontWeight: '600', borderRadius: '100px', border: '1px solid var(--border-color)',
                transition: 'var(--transition-smooth)'
              }}
            >
              Ver Detalhes
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

const BookingFlow = ({ isOpen, onClose }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    cinema: '',
    session: '',
    name: '',
    email: '',
    phone: ''
  });

  const nextStep = () => setStep(s => s + 1);
  const prevStep = () => setStep(s => s - 1);

  const handleFinish = () => {
    confetti({
      particleCount: 150, spread: 70, origin: { y: 0.6 },
      colors: ['#E6007E', '#005CB9', '#FFD500']
    });
    nextStep();
  };

  const steps = [
    { title: "Localização", icon: <MapPin size={18} /> },
    { title: "Sessão", icon: <Clock size={18} /> },
    { title: "Registo", icon: <User size={18} /> },
    { title: "Sucesso", icon: <CheckCircle size={18} /> }
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          style={{
            position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
            background: 'rgba(0,0,0,0.8)', backdropFilter: 'blur(8px)',
            zIndex: 2000, display: 'flex', justifyContent: 'center', alignItems: 'center',
            padding: '20px'
          }}
        >
          <motion.div 
            initial={{ scale: 0.9, y: 20 }}
            animate={{ scale: 1, y: 0 }}
            className="glass-card"
            style={{
              width: '100%', maxWidth: '900px', maxHeight: '90vh',
              overflow: 'hidden', display: 'flex', flexDirection: 'column'
            }}
          >
            {/* Header / Stepper */}
            <div style={{ padding: '32px', borderBottom: '1px solid var(--border-color)', background: 'rgba(var(--bg-secondary-rgb), 0.5)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <h2 style={{ fontSize: '24px', fontWeight: '700' }}>Reserva de Bilhetes</h2>
                <button onClick={onClose} style={{ color: 'var(--text-secondary)' }}>✕ Fechar</button>
              </div>
              
              <div style={{ display: 'flex', gap: '8px' }}>
                {steps.map((s, i) => (
                  <div key={i} style={{ 
                    flex: 1, height: '4px', borderRadius: '2px',
                    background: i + 1 <= step ? 'var(--nos-magenta)' : 'var(--border-color)',
                    transition: 'all 0.5s ease'
                  }} />
                ))}
              </div>
            </div>

            {/* Content */}
            <div style={{ padding: '40px', overflowY: 'auto', flex: 1 }}>
              <AnimatePresence mode="wait">
                {step === 1 && (
                  <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
                    <h3 style={{ marginBottom: '24px' }}>Escolha o seu Cinema NOS</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '12px' }}>
                      {CINEMAS.map(c => (
                        <button 
                          key={c}
                          onClick={() => { setFormData({...formData, cinema: c}); nextStep(); }}
                          style={{
                            padding: '16px', borderRadius: '12px', textAlign: 'left',
                            background: formData.cinema === c ? 'rgba(230, 0, 126, 0.1)' : 'var(--bg-secondary)',
                            border: `1px solid ${formData.cinema === c ? 'var(--nos-magenta)' : 'var(--border-color)'}`,
                            transition: 'all 0.2s ease'
                          }}
                        >
                          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                            <MapPin size={16} color={formData.cinema === c ? 'var(--nos-magenta)' : 'var(--text-secondary)'} />
                            <span style={{ fontSize: '14px', fontWeight: '500' }}>{c}</span>
                          </div>
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}

                {step === 2 && (
                  <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
                    <h3>Selecione o Horário (5 Nov)</h3>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '32px' }}>Vagas limitadas para as primeiras 5 inscrições por sessão.</p>
                    <div style={{ display: 'flex', gap: '20px' }}>
                      {["19h00", "22h00"].map(t => (
                        <button 
                          key={t}
                          onClick={() => { setFormData({...formData, session: t}); nextStep(); }}
                          style={{
                            flex: 1, padding: '32px', borderRadius: '20px',
                            background: 'var(--bg-secondary)', border: '1px solid var(--border-color)',
                            textAlign: 'center'
                          }}
                        >
                          <Clock size={32} style={{ marginBottom: '12px', color: 'var(--nos-magenta)' }} />
                          <div style={{ fontSize: '24px', fontWeight: '700' }}>{t}</div>
                          <div style={{ fontSize: '12px', opacity: 0.6 }}>Sessão Especial</div>
                        </button>
                      ))}
                    </div>
                    <button onClick={prevStep} style={{ marginTop: '32px', opacity: 0.6 }}>← Voltar</button>
                  </motion.div>
                )}

                {step === 3 && (
                  <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
                    <h3>Dados Pessoais</h3>
                    <p style={{ marginBottom: '32px', color: 'var(--text-secondary)' }}>Preencha para receber o seu bilhete duplo gratuito.</p>
                    <div style={{ display: 'grid', gap: '20px' }}>
                        <div className="input-group">
                            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px' }}>Nome Completo</label>
                            <input 
                              type="text" placeholder="Seu nome"
                              value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})}
                              style={{ width: '100%', padding: '16px', borderRadius: '12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', color: 'inherit' }} 
                            />
                        </div>
                        <div className="input-group">
                            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px' }}>E-mail</label>
                            <input 
                              type="email" placeholder="email@exemplo.com"
                              value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})}
                              style={{ width: '100%', padding: '16px', borderRadius: '12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', color: 'inherit' }} 
                            />
                        </div>
                        <div className="input-group">
                            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px' }}>Telemóvel</label>
                            <input 
                              type="tel" placeholder="912 345 678"
                              value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})}
                              style={{ width: '100%', padding: '16px', borderRadius: '12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', color: 'inherit' }} 
                            />
                        </div>
                    </div>
                    <div style={{ marginTop: '40px', display: 'flex', justifyContent: 'space-between' }}>
                        <button onClick={prevStep} style={{ opacity: 0.6 }}>← Voltar</button>
                        <button 
                          onClick={handleFinish}
                          style={{ padding: '16px 40px', background: 'var(--nos-magenta)', color: 'white', borderRadius: '100px', fontWeight: '700' }}
                        >
                          Confirmar Registo
                        </button>
                    </div>
                  </motion.div>
                )}

                {step === 4 && (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
                    style={{ textAlign: 'center', padding: '20px 0' }}
                  >
                    <div style={{ 
                      width: '80px', height: '80px', background: '#4BDB65', 
                      borderRadius: '50%', display: 'inline-flex', alignItems: 'center', 
                      justifyContent: 'center', marginBottom: '24px', color: 'white',
                      boxShadow: '0 0 40px rgba(75, 219, 101, 0.4)'
                    }}>
                      <CheckCircle size={40} />
                    </div>
                    <h2 style={{ fontSize: '32px', marginBottom: '12px' }}>Inscrição Concluída!</h2>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '40px' }}>
                      Enviamos um e-mail de confirmação para <b>{formData.email}</b>.<br/>
                      Apresente o QR Code abaixo na bilheteira do <b>{formData.cinema}</b>.
                    </p>
                    
                    <div style={{ 
                      padding: '30px', background: 'white', borderRadius: '24px', 
                      display: 'inline-block', position: 'relative',
                      boxShadow: '0 20px 50px rgba(0,0,0,0.1)'
                    }}>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=NOS-EYES-WIDE-SHUT-CONFIRMED" alt="QR Code" />
                        <div style={{ marginTop: '12px', color: '#121212', fontWeight: '700', fontSize: '14px' }}>#NOS-2026-EWSHUT</div>
                    </div>

                    <div style={{ marginTop: '48px', display: 'flex', gap: '16px', justifyContent: 'center' }}>
                        <button onClick={onClose} style={{ padding: '16px 32px', border: '1px solid var(--border-color)', borderRadius: '100px' }}>
                            Concluir
                        </button>
                        <button style={{ padding: '16px 32px', background: 'var(--nos-blue)', color: 'white', borderRadius: '100px' }}>
                            Guardar no Wallet
                        </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

const Footer = () => (
  <footer style={{ padding: '80px 0', borderTop: '1px solid var(--border-color)', background: 'var(--bg-secondary)' }}>
    <div className="container" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '40px' }}>
      <div>
        <h4 style={{ marginBottom: '24px', fontSize: '20px' }}>NOS <span className="premium-gradient-text">CINEMAS</span></h4>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', lineHeight: '1.8' }}>
          Líder em entretenimento em Portugal. Experiências únicas desde 1999.
        </p>
      </div>
      <div>
        <h5 style={{ marginBottom: '20px' }}>Links Úteis</h5>
        <ul style={{ display: 'grid', gap: '12px', color: 'var(--text-secondary)', fontSize: '14px' }}>
          <li>Cartão NOS</li>
          <li>Em Cartaz</li>
          <li>Próximas Estreias</li>
          <li>Cinemas & Horários</li>
        </ul>
      </div>
      <div>
        <h5 style={{ marginBottom: '20px' }}>Apoio</h5>
        <ul style={{ display: 'grid', gap: '12px', color: 'var(--text-secondary)', fontSize: '14px' }}>
          <li>Ajuda & FAQ</li>
          <li>Termos e Condições</li>
          <li>Política de Privacidade</li>
          <li>Contactos</li>
        </ul>
      </div>
      <div>
        <h5 style={{ marginBottom: '20px' }}>Notas Académicas</h5>
        <p style={{ color: 'var(--text-secondary)', fontSize: '12px' }}>
          Projeto Multimedia II • IPCA <br/>
          Design Gráfico (PL) — 3º ano <br/>
          © 2026 Todos os direitos reservados.
        </p>
      </div>
    </div>
  </footer>
);

export default function App() {
  const [isBookingOpen, setIsBookingOpen] = useState(false);

  return (
    <ThemeProvider>
      <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <Navbar />
        <main>
          <Hero onStart={() => setIsBookingOpen(true)} />
          
          <section id="info" style={{ padding: '120px 0' }}>
            <div className="container">
              <div style={{ textAlign: 'center', marginBottom: '80px' }}>
                <h2 style={{ fontSize: '40px', fontWeight: '800', marginBottom: '16px' }}>Como <span className="premium-gradient-text">Funciona</span></h2>
                <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto' }}>Aproveite o Dia Mundial do Cinema com a NOS. Simples, rápido e exclusivo.</p>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px' }}>
                {[
                  { icon: <Ticket color="var(--nos-magenta)" />, title: "Bilhete Duplo", text: "Registe-se e receba um bilhete duplo para a sessão especial de Eyes Wide Shut." },
                  { icon: <Info color="var(--nos-blue)" />, title: "Menu Grátis", text: "Na compra de um bilhete, o menu de pipocas e bebida é por nossa conta." },
                  { icon: <HelpCircle color="var(--nos-yellow)" />, title: "Exclusivo Web", text: "Válido apenas para os primeiros 5 registos online por sessão em cinemas aderentes." }
                ].map((item, i) => (
                  <motion.div 
                    key={i} whileHover={{ y: -10 }}
                    className="glass-card" style={{ padding: '40px' }}
                  >
                    <div style={{ marginBottom: '20px' }}>{item.icon}</div>
                    <h3 style={{ marginBottom: '16px' }}>{item.title}</h3>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>{item.text}</p>
                  </motion.div>
                ))}
              </div>
            </div>
          </section>
        </main>
        <Footer />
        <BookingFlow isOpen={isBookingOpen} onClose={() => setIsBookingOpen(false)} />
      </div>
    </ThemeProvider>
  );
}
