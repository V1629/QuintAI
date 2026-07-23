import { useState } from 'react';
import BoidsEcosystem from '../components/animata/background/BoidsEcosystem';
import GithubCardSkew from '../components/animata/card/GithubCardSkew';

/* ── Feature card icons (SVG, no emojis) ── */
function IconBolt() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#818cf8" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
  );
}
function IconTarget() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#818cf8" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" />
    </svg>
  );
}
function IconZap() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#818cf8" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M5 12H3l9-9v6h7l-9 9v-6H5z" />
    </svg>
  );
}

const features = [
  {
    title: 'Multi-Model Routing',
    desc: 'Queries dispatched to GPT-4, Claude, Gemini simultaneously for maximum coverage.',
    Icon: IconBolt,
  },
  {
    title: 'Best Answer Selection',
    desc: 'Agentic pipeline picks the highest quality response automatically — no manual review.',
    Icon: IconTarget,
  },
  {
    title: 'Zero Config Setup',
    desc: 'One API call routes across all models with smart fallback and zero configuration.',
    Icon: IconZap,
  },
];

const NAV_LINKS = ['Features', 'Models', 'Docs', 'GitHub'];

/* ── Sibling-focus nav with React state ── */
function NavLinks({ onQueryOpen }) {
  const [hovered, setHovered] = useState(null);
  return (
    <nav style={{ display: 'flex', alignItems: 'center' }} aria-label="Main navigation">
      {NAV_LINKS.map((label) => {
        const isActive = hovered === label;
        const isDim = hovered !== null && !isActive;
        const href =
          label === 'GitHub'
            ? 'https://github.com/V1629/QuintAI'
            : label === 'Docs'
            ? '#features'
            : `#${label.toLowerCase()}`;
        return (
          <a
            key={label}
            href={href}
            target={label === 'GitHub' ? '_blank' : undefined}
            rel={label === 'GitHub' ? 'noreferrer' : undefined}
            onClick={label === 'Docs' ? (e) => { e.preventDefault(); onQueryOpen(); } : undefined}
            onMouseEnter={() => setHovered(label)}
            onMouseLeave={() => setHovered(null)}
            style={{
              color: '#cbd5e1',
              textDecoration: 'none',
              fontSize: '0.875rem',
              fontWeight: 450,
              padding: '8px 18px',
              borderRadius: '6px',
              opacity: isDim ? 0.3 : 1,
              transition: 'opacity 0.2s ease-out',
              letterSpacing: '0.01em',
              cursor: 'pointer',
            }}
          >
            {label}
          </a>
        );
      })}
    </nav>
  );
}

/* ── Query Modal ── */
function QueryModal({ onClose }) {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'https://quintai-backend.onrender.com';
      const res = await fetch(`${apiUrl}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question.trim() }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to reach the backend. Is the server running on port 5000?');
    } finally {
      setLoading(false);
    }
  };

  return (
    /* backdrop */
    <div
      onClick={onClose}
      style={{
        position: 'fixed', inset: 0, zIndex: 1000,
        background: 'rgba(0,0,0,0.7)',
        backdropFilter: 'blur(6px)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: '24px',
      }}
    >
      {/* panel */}
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: '100%', maxWidth: '680px', maxHeight: '80vh',
          background: 'rgba(15,15,25,0.95)',
          border: '1px solid rgba(255,255,255,0.12)',
          borderRadius: '20px',
          boxShadow: '0 24px 80px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.1)',
          display: 'flex', flexDirection: 'column',
          overflow: 'hidden',
        }}
      >
        {/* header */}
        <div style={{ padding: '20px 24px', borderBottom: '1px solid rgba(255,255,255,0.07)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div style={{ color: '#fff', fontWeight: 700, fontSize: '1rem' }}>Ask QuintAI</div>
            <div style={{ color: '#4b5563', fontSize: '0.75rem', marginTop: '2px' }}>Routes across GPT-4, Claude, Gemini and more</div>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)', color: '#9ca3af', width: '32px', height: '32px', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1rem' }}
          >
            ✕
          </button>
        </div>

        {/* body */}
        <div style={{ padding: '20px 24px', overflowY: 'auto', flex: 1 }}>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'flex', gap: '10px' }}>
              <input
                autoFocus
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ask anything…"
                disabled={loading}
                style={{
                  flex: 1,
                  background: 'rgba(255,255,255,0.05)',
                  border: '1px solid rgba(255,255,255,0.12)',
                  borderRadius: '10px',
                  padding: '12px 16px',
                  color: '#f1f5f9',
                  fontSize: '0.9rem',
                  outline: 'none',
                  fontFamily: 'inherit',
                }}
                onFocus={(e) => { e.target.style.borderColor = 'rgba(99,102,241,0.5)'; }}
                onBlur={(e) => { e.target.style.borderColor = 'rgba(255,255,255,0.12)'; }}
              />
              <button
                type="submit"
                disabled={loading || !question.trim()}
                style={{
                  background: loading || !question.trim() ? '#374151' : '#6366f1',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '10px',
                  padding: '12px 20px',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: loading || !question.trim() ? 'not-allowed' : 'pointer',
                  whiteSpace: 'nowrap',
                  transition: 'background 0.2s',
                  minWidth: '90px',
                }}
              >
                {loading ? 'Routing…' : 'Send →'}
              </button>
            </div>
          </form>

          {/* Loading state */}
          {loading && (
            <div style={{ marginTop: '24px', color: '#6b7280', fontSize: '0.85rem', textAlign: 'center', padding: '20px' }}>
              <div style={{ marginBottom: '8px', fontSize: '1.4rem' }}>⟳</div>
              Routing your question across all models…
            </div>
          )}

          {/* Error */}
          {error && (
            <div style={{ marginTop: '20px', background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: '10px', padding: '14px 16px', color: '#fca5a5', fontSize: '0.85rem' }}>
              {error}
            </div>
          )}

          {/* Results */}
          {result && (
            <div style={{ marginTop: '20px' }}>
              {/* Judge's answer */}
              <div style={{ background: 'rgba(99,102,241,0.08)', border: '1px solid rgba(99,102,241,0.25)', borderRadius: '12px', padding: '16px', marginBottom: '16px' }}>
                <div style={{ color: '#a5b4fc', fontSize: '0.7rem', fontWeight: 600, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '8px' }}>Best Answer</div>
                <p style={{ color: '#f1f5f9', fontSize: '0.9rem', lineHeight: 1.7 }}>{result.judge_decision}</p>
              </div>

              {/* Individual agent responses */}
              <div style={{ color: '#4b5563', fontSize: '0.7rem', fontWeight: 600, letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: '10px' }}>All Agent Responses</div>
              {result.agent_responses?.map((agent, i) => (
                <div
                  key={i}
                  style={{
                    background: 'rgba(255,255,255,0.03)',
                    border: `1px solid ${agent.status === 'error' ? 'rgba(239,68,68,0.2)' : 'rgba(255,255,255,0.07)'}`,
                    borderRadius: '10px',
                    padding: '12px 14px',
                    marginBottom: '8px',
                  }}
                >
                  <div style={{ color: agent.status === 'error' ? '#f87171' : '#818cf8', fontSize: '0.72rem', fontWeight: 600, marginBottom: '6px' }}>{agent.agent}</div>
                  <p style={{ color: '#6b7280', fontSize: '0.82rem', lineHeight: 1.6 }}>{agent.response}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/* ── Main landing page ── */
export default function QuintAILanding() {
  const [modalOpen, setModalOpen] = useState(false);

  const openModal = () => setModalOpen(true);
  const closeModal = () => setModalOpen(false);

  return (
    <div style={{ minHeight: '100vh', position: 'relative', background: '#050508', fontFamily: "'Inter', system-ui, sans-serif" }}>

      {/* ── Global styles ── */}
      <style>{`
        .glass-card {
          background: rgba(255, 255, 255, 0.08);
          backdrop-filter: blur(13px);
          -webkit-backdrop-filter: blur(13px);
          border-radius: 20px;
          border: 1px solid rgba(255, 255, 255, 0.18);
          box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.22),
            inset 0 -1px 0 rgba(255, 255, 255, 0.06);
          position: relative;
          overflow: hidden;
        }
        .glass-card::before {
          content: '';
          position: absolute;
          top: 0; left: 0; right: 0;
          height: 1px;
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent);
          pointer-events: none;
        }
        .glass-card::after {
          content: '';
          position: absolute;
          top: 0; left: 0;
          width: 1px; height: 100%;
          background: linear-gradient(180deg, rgba(255,255,255,0.55), transparent, rgba(255,255,255,0.15));
          pointer-events: none;
        }
        @keyframes scrollBounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(7px); }
        }
        @keyframes glowPulse {
          0%, 100% {
            text-shadow:
              0 0 20px rgba(129,140,248,0.8),
              0 0 40px rgba(129,140,248,0.5),
              0 0 80px rgba(99,102,241,0.3);
          }
          50% {
            text-shadow:
              0 0 30px rgba(167,139,250,1),
              0 0 60px rgba(129,140,248,0.8),
              0 0 120px rgba(99,102,241,0.5);
          }
        }
        input::placeholder { color: #4b5563; }
      `}</style>

      {/* ── Boids background (pointer-events:none is set inside the component) ── */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 0, pointerEvents: 'none' }}>
        <BoidsEcosystem
          count={80}
          background="#050508"
          palette={['#6366f1', '#818cf8', '#4f46e5', '#a5b4fc']}
          cursorRadius={100}
          className="!rounded-none"
        />
      </div>

      {/* ── Navbar ── */}
      <header
        style={{
          position: 'sticky', top: 0, zIndex: 50,
          background: 'rgba(5,5,8,0.75)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          borderBottom: '1px solid rgba(255,255,255,0.07)',
          padding: '0 32px', height: '60px',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        }}
      >
        <span style={{ color: '#fff', fontWeight: 700, fontSize: '1.15rem', letterSpacing: '-0.01em', userSelect: 'none' }}>
          Quint<span style={{ color: '#818cf8' }}>AI</span>
        </span>

        <NavLinks onQueryOpen={openModal} />

        <button
          id="navbar-get-started"
          onClick={openModal}
          style={{
            background: '#6366f1', color: '#fff', border: 'none',
            padding: '8px 18px', borderRadius: '8px',
            fontSize: '0.85rem', fontWeight: 600, cursor: 'pointer',
            transition: 'background 0.2s, transform 0.15s',
          }}
          onMouseEnter={e => { e.currentTarget.style.background = '#4f46e5'; e.currentTarget.style.transform = 'scale(1.04)'; }}
          onMouseLeave={e => { e.currentTarget.style.background = '#6366f1'; e.currentTarget.style.transform = 'scale(1)'; }}
        >
          Get Started
        </button>
      </header>

      {/* ── Hero ── */}
      <section style={{ position: 'relative', zIndex: 10, minHeight: 'calc(100vh - 60px)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 24px' }}>
        <div style={{ background: 'rgba(99,102,241,0.12)', border: '1px solid rgba(99,102,241,0.35)', color: '#a5b4fc', fontSize: '0.75rem', fontWeight: 500, borderRadius: '9999px', padding: '5px 14px', marginBottom: '28px', letterSpacing: '0.04em' }}>
          Multi-Model Agentic Pipeline
        </div>

        <h1 style={{ fontSize: 'clamp(2.6rem, 6vw, 4rem)', fontWeight: 800, color: '#fff', marginBottom: '20px', maxWidth: '52rem', lineHeight: 1.08, letterSpacing: '-0.03em' }}>
          Query Smarter Across{' '}
          <span style={{ background: 'linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #c4b5fd 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
            Every Model
          </span>
        </h1>

        <p style={{ color: '#6b7280', fontSize: '1.1rem', maxWidth: '32rem', marginBottom: '44px', lineHeight: 1.75 }}>
          QuintAI routes your questions intelligently across GPT-4, Claude, Gemini
          and more — returning the best answer, every time.
        </p>

        <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap', justifyContent: 'center' }}>
          <button
            id="hero-start-querying"
            onClick={openModal}
            style={{
              background: '#6366f1', color: '#fff', border: 'none',
              padding: '13px 30px', borderRadius: '10px',
              fontSize: '0.95rem', fontWeight: 600, cursor: 'pointer',
              transition: 'transform 0.2s, background 0.2s, box-shadow 0.2s',
              boxShadow: '0 0 24px rgba(99,102,241,0.35)',
            }}
            onMouseEnter={e => { e.currentTarget.style.background = '#4f46e5'; e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 0 36px rgba(99,102,241,0.55)'; }}
            onMouseLeave={e => { e.currentTarget.style.background = '#6366f1'; e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 0 24px rgba(99,102,241,0.35)'; }}
          >
            Start Querying
          </button>
          <a
            id="hero-view-github"
            href="https://github.com"
            target="_blank"
            rel="noreferrer"
            style={{
              background: 'transparent', color: '#e2e8f0',
              border: '1px solid rgba(255,255,255,0.15)',
              padding: '13px 30px', borderRadius: '10px',
              fontSize: '0.95rem', fontWeight: 600,
              textDecoration: 'none', display: 'inline-block',
              transition: 'transform 0.2s, background 0.2s, border-color 0.2s',
            }}
            onMouseEnter={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.06)'; e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)'; e.currentTarget.style.transform = 'translateY(-2px)'; }}
            onMouseLeave={e => { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.borderColor = 'rgba(255,255,255,0.15)'; e.currentTarget.style.transform = 'translateY(0)'; }}
          >
            View on GitHub
          </a>
        </div>

        <div style={{ marginTop: '72px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '5px', opacity: 0.3, animation: 'scrollBounce 2.2s ease-in-out infinite' }}>
          <span style={{ color: '#94a3b8', fontSize: '0.62rem', letterSpacing: '0.18em', textTransform: 'uppercase' }}>Scroll</span>
          <svg width="14" height="14" fill="none" stroke="#94a3b8" strokeWidth="2" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </section>

      {/* ── Features ── */}
      <section id="features" style={{ position: 'relative', zIndex: 10, padding: '100px 24px' }}>
        <h2 style={{ color: '#fff', fontSize: '2rem', fontWeight: 700, textAlign: 'center', marginBottom: '10px', letterSpacing: '-0.02em' }}>
          Why QuintAI
        </h2>
        <p style={{ color: '#4b5563', textAlign: 'center', marginBottom: '52px', maxWidth: '26rem', marginLeft: 'auto', marginRight: 'auto', fontSize: '0.9rem', lineHeight: 1.7 }}>
          Built for developers who need reliable, intelligent multi-model orchestration without the overhead.
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px', maxWidth: '960px', margin: '0 auto' }}>
          {features.map(({ title, desc, Icon }) => (
            <GithubCardSkew key={title} className="glass-card" style={{ padding: '36px 32px' }}>
              <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(129,140,248,0.1)', border: '1px solid rgba(129,140,248,0.2)' }}>
                <Icon />
              </div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#f1f5f9', marginBottom: '10px', letterSpacing: '-0.01em' }}>{title}</h3>
              <p style={{ color: '#6b7280', fontSize: '0.88rem', lineHeight: 1.7 }}>{desc}</p>
            </GithubCardSkew>
          ))}
        </div>
      </section>

      {/* ── Powered by — glowing V ── */}
      <section id="models" style={{ position: 'relative', zIndex: 10, padding: '60px 24px 100px', textAlign: 'center' }}>
        <p style={{ color: '#374151', fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.18em', marginBottom: '32px' }}>
          Powered by
        </p>
        <div style={{ fontSize: '8rem', fontWeight: 900, lineHeight: 1, letterSpacing: '-0.05em', color: '#818cf8', animation: 'glowPulse 3s ease-in-out infinite', userSelect: 'none' }}>
          V
        </div>
      </section>

      {/* ── Footer ── */}
      <footer style={{ position: 'relative', zIndex: 10, borderTop: '1px solid rgba(255,255,255,0.05)', padding: '24px 32px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: '#374151', fontSize: '0.75rem' }}>
        <span>© 2026 Quint<span style={{ color: '#6366f1' }}>AI</span>. All rights reserved.</span>
        <span>Multi-model agentic QA pipeline</span>
      </footer>

      {/* ── Query Modal ── */}
      {modalOpen && <QueryModal onClose={closeModal} />}
    </div>
  );
}