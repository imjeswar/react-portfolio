import React from "react";

const skills = [
  ["HTML", "https://cdn-icons-png.flaticon.com/512/174/174854.png"],
  ["CSS", "https://cdn-icons-png.flaticon.com/512/732/732190.png"],
  ["JavaScript", "https://cdn-icons-png.flaticon.com/512/5968/5968292.png"],
  ["Python", "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"],
  ["C", "https://cdn-icons-png.flaticon.com/512/3665/3665923.png"],
  ["Java", "https://cdn-icons-png.flaticon.com/512/226/226777.png"],
  ["GitHub", "https://cdn-icons-png.flaticon.com/512/733/733553.png"],
  ["Tailwind", "https://cdn.worldvectorlogo.com/logos/tailwind-css-2.svg"],
  ["VS Code", "https://cdn-icons-png.flaticon.com/512/906/906324.png"],
];

const Skills = () => (
  <section
    id="skills"
    className="py-10 mb-12 bg-gray-900 text-center max-w-4xl mx-auto rounded-lg shadow-lg p-6 border-2 border-amber-400/50 transition hover:shadow-[0_0_40px_rgba(251,191,36,0.7)]"
    data-aos="fade-up"
  >
    <h2 className="text-3xl font-bold mb-4 text-amber-100 border-b-2 border-amber-300/70 pb-2 inline-block">
      Skills
    </h2>

    <div className="flex flex-wrap justify-center gap-6 mt-6">
      {skills.map(([name, src]) => (
        <div key={name} className="flex flex-col items-center">
          {/* dark rounded bg + smaller icon */}
          <div className="p-3 rounded-full bg-black/80 flex items-center justify-center shadow-md">
            <img src={src} className="w-8 h-8" alt={name} />
          </div>
          <span className="text-amber-200 text-sm mt-2">{name}</span>
        </div>
      ))}
    </div>
  </section>
);

export default Skills;
