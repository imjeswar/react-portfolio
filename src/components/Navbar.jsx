import React from "react";

const Navbar = () => {
  const navItems = [
    ["About", "#about"],
    ["Education", "#education"],
    ["My Journey", "#journey"],
    ["Skills", "#skills"],
    ["Projects", "#projects"],
    ["Contact", "#contact"],
  ];

  return (
    <nav className="sticky top-0 z-[100] w-full flex justify-center py-4 px-4 overflow-visible">
      <div className="premium-glass animate-glow rounded-full px-4 md:px-8 py-3 ring-1 ring-white/5 transition-all duration-300 hover:border-amber-400/40">
        <ul className="flex items-center justify-center gap-2 md:gap-8">
          {navItems.map(([label, href]) => (
            <li key={href}>
              <a
                href={href}
                className="relative text-xs md:text-sm font-medium text-amber-100/70 hover:text-amber-300 transition-all duration-300 group px-2 md:px-3 py-1.5"
              >
                {label}
                {/* Neon Underline Effect */}
                <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-gradient-to-r from-amber-400 to-amber-200 transition-all duration-300 group-hover:w-full group-hover:shadow-[0_0_8px_#fbbf24] shadow-[0_0_4px_#fbbf24]" />
                {/* Background Glow on Hover */}
                <span className="absolute inset-0 bg-amber-400/5 rounded-lg scale-0 group-hover:scale-100 transition-transform duration-300 -z-10" />
              </a>
            </li>
          ))}
        </ul>
      </div>

      <style>{`
        /* Smooth scrolling adjustment for fixed header */
        html {
          scroll-padding-top: 100px;
        }

        @keyframes nav-glow {
          0%, 100% { box-shadow: 0 8px 32px 0 rgba(0,0,0,0.8); }
          50% { box-shadow: 0 8px 32px 0 rgba(251,191,36,0.1); }
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
