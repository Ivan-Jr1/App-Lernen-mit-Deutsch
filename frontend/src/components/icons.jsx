// Ícones em SVG inline — evita uma dependência de biblioteca de ícones.
// Todos herdam a cor do texto (stroke="currentColor") e o tamanho via classe.

const base = {
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.75,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  viewBox: '0 0 24 24',
}

export const CardsIcon = (props) => (
  <svg {...base} {...props}>
    <rect x="3" y="5" width="18" height="13" rx="2" />
    <path d="M3 10h18" />
  </svg>
)

export const ChatIcon = (props) => (
  <svg {...base} {...props}>
    <path d="M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H9l-4 4V6z" />
  </svg>
)

export const ChartIcon = (props) => (
  <svg {...base} {...props}>
    <path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />
  </svg>
)

export const SunIcon = (props) => (
  <svg {...base} {...props}>
    <circle cx="12" cy="12" r="4" />
    <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
  </svg>
)

export const MoonIcon = (props) => (
  <svg {...base} {...props}>
    <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
  </svg>
)

export const LogoutIcon = (props) => (
  <svg {...base} {...props}>
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />
  </svg>
)

export const FlameIcon = (props) => (
  <svg {...base} fill="currentColor" stroke="none" viewBox="0 0 24 24" {...props}>
    <path d="M12 2c1 3-1 5-2.5 6.5C8 10 7 11.6 7 13.5A5 5 0 0 0 17 14c0-2-1-3.5-2-5 .5 1 .5 2 0 2.8.8-3-1-6-3-9.8z" />
  </svg>
)
