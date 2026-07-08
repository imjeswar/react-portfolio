import React from "react";

const technicalSkills = [
  ["HTML", "https://cdn-icons-png.flaticon.com/512/174/174854.png"],
  ["CSS", "https://cdn-icons-png.flaticon.com/512/732/732190.png"],
  ["JavaScript", "https://cdn-icons-png.flaticon.com/512/5968/5968292.png"],
  ["React", "https://cdn-icons-png.flaticon.com/512/919/919851.png"],
  ["MongoDB", "https://www.vectorlogo.zone/logos/mongodb/mongodb-icon.svg"],
  ["Tailwind", "https://cdn.worldvectorlogo.com/logos/tailwind-css-2.svg"],
  ["Python", "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"],
  ["C", "https://cdn-icons-png.flaticon.com/512/3665/3665923.png"],
  ["Java", "https://cdn-icons-png.flaticon.com/512/226/226777.png"],
  ["GitHub", "https://cdn-icons-png.flaticon.com/512/733/733553.png"],
  ["VS Code", "https://cdn-icons-png.flaticon.com/512/906/906324.png"],
];

const softSkills = [
  "Communication",
  "Teamwork",
  "Problem Solving",
  "Leadership",
  "Time Management",
];

const Skills = () => {
  // Simple deterministic offset helper
  const getOffset = (name) => {
    const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    const x = (hash % 20) - 10; // -10 to 10px
    const y = ((hash * 7) % 20) - 10;
    const delay = (hash % 10) * 0.5;
    return { x, y, delay };
  };

  return (
    <section
      id="skills"
      className="py-12 w-full premium-glass animate-glow rounded-3xl p-6 md:p-12 overflow-x-hidden overflow-y-visible group"
      data-aos="fade-up"
    >
      <div className="text-center">
        <div className="relative inline-block mb-10">
          <h2 className="text-4xl font-bold text-amber-100 pb-2 heading-shine">
            Skills
          </h2>
          <span className="absolute bottom-0 left-0 w-0 h-[3px] bg-gradient-to-r from-amber-400 to-amber-200 transition-all duration-500 group-hover:w-full group-hover:shadow-[0_0_12px_#fbbf24] shadow-[0_0_6px_#fbbf24]" />
        </div>
      </div>

      <style>{`
        @keyframes skill-wave {
          0%, 100% { transform: translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(0deg); }
          33% { transform: translate(calc(var(--tw-translate-x) + 2px), calc(var(--tw-translate-y) - 10px)) rotate(2deg); }
          66% { transform: translate(calc(var(--tw-translate-x) - 2px), calc(var(--tw-translate-y) + 5px)) rotate(-2deg); }
        }
        .animate-skill-wave {
          animation: skill-wave var(--duration) ease-in-out infinite;
        }
        @media (max-width: 640px) {
          .animate-skill-wave {
            animation: none; /* Disable wave on mobile to reduce blinking */
            transform: translate(var(--tw-translate-x), var(--tw-translate-y)) !important;
          }
        }
      `}</style>

      {/* Technical Skills - Dense Swarm */}
      <div className="mb-12">
        <h3 className="text-lg font-semibold text-amber-200 mb-8 uppercase tracking-[0.3em] text-center">Tools & Technologies</h3>
        <div className="flex flex-wrap justify-center items-center gap-3 md:gap-4 max-w-3xl mx-auto px-2">
          {technicalSkills.map(([name, src]) => {
            const { x, y, delay } = getOffset(name);
            return (
              <div
                key={name}
                className="group/skill relative flex flex-col items-center gap-1.5 md:gap-2"
              >
                {/* Intense Hover Glow */}
                <div className="absolute inset-0 bg-amber-400/20 rounded-full blur-xl opacity-0 group-hover/skill:opacity-100 transition-opacity duration-300 -z-10" />

                {/* Circular Glass Icon with Wave */}
                <div
                  className="p-3.5 md:p-5 flex items-center justify-center bg-black/40 backdrop-blur-xl border border-white/20 rounded-full shadow-[0_0_15px_rgba(251,191,36,0.05)] transition-all duration-300 cursor-pointer group-hover/skill:scale-110 group-hover/skill:bg-black/60 group-hover/skill:border-amber-400/50 group-hover/skill:shadow-[0_0_20px_rgba(251,191,36,0.3)] animate-skill-wave"
                  style={{
                    '--tw-translate-x': `${x}px`,
                    '--tw-translate-y': `${y}px`,
                    '--duration': `${4 + (delay % 2)}s`,
                    animationDelay: `${delay}s`
                  }}
                >
                  <img src={src} className="w-5 h-5 md:w-6 md:h-6 object-contain brightness-110 saturate-125 drop-shadow-[0_0_5px_rgba(255,255,255,0.2)]" alt={name} />
                </div>

                {/* Fixed Bright Name Label */}
                <span className="text-[9px] md:text-[10px] text-amber-100 font-semibold uppercase tracking-widest text-center">
                  {name}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Professional Skills Section */}
      <div className="mt-16 text-center border-t border-white/5 pt-10">
        <h3 className="text-md font-semibold text-amber-200 mb-8 uppercase tracking-[0.2em]">Professional Skills</h3>
        <div className="flex flex-wrap justify-center gap-2 md:gap-3">
          {softSkills.map((skill) => (
            <div
              key={skill}
              className="px-4 py-1.5 md:px-6 md:py-2 premium-glass rounded-lg text-amber-100 text-[10px] md:text-xs font-semibold hover:text-amber-300 hover:border-amber-300/30 hover:-translate-y-1 transition-all duration-300 cursor-default"
            >
              {skill}
            </div>
          ))}
        </div>
      </div>

      <style>{`
        @keyframes skill-drift {
          0% { transform: translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(0deg); }
          100% { transform: translate(calc(var(--tw-translate-x) + 5px), calc(var(--tw-translate-y) - 5px)) rotate(3deg); }
        }
      `}</style>
    </section>
  );
};

export default Skills;
