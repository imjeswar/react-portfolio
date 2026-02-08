import React from "react";

const Journey = () => (
  <section
    id="journey"
    className="w-full p-6 md:p-12 premium-glass animate-glow rounded-3xl group"
    data-aos="fade-up"
  >
    <div className="relative inline-block mb-8">
      <h2 className="text-4xl font-bold text-amber-200 tracking-wide heading-shine pb-2">
        My Journey
      </h2>
      <span className="absolute bottom-0 left-0 w-0 h-[3px] bg-gradient-to-r from-amber-400 to-amber-200 transition-all duration-500 group-hover:w-full group-hover:shadow-[0_0_12px_#fbbf24] shadow-[0_0_6px_#fbbf24]" />
    </div>

    <p className="text-gray-300 leading-relaxed hover:text-white transition duration-300">
      I’m currently pursuing B.Tech in Artificial Intelligence &amp; Data
      Science at Dhanalakshmi Srinivasan University, Trichy (Pre-final Year).
      Over time, I’ve developed a strong passion for web programming and
      building impactful digital solutions. My curiosity pushes me to explore
      both frontend and backend development while experimenting with modern
      frameworks. I enjoy crafting efficient code and discovering ways AI can
      enhance real-world applications.
    </p>

    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8">
      <div
        className="premium-glass animate-glow p-6 rounded-xl text-center"
        data-aos="zoom-in"
      >
        ⚡ <h4 className="mt-2 font-semibold text-amber-200">Full-Stack</h4>
        <p className="text-sm text-gray-300">Responsive apps.</p>
      </div>
      <div
        className="premium-glass animate-glow p-6 rounded-xl text-center"
        data-aos="zoom-in"
        data-aos-delay="100"
      >
        🤖 <h4 className="mt-2 font-semibold text-amber-200">
          AI &amp; Innovation
        </h4>
        <p className="text-sm text-gray-300">Prompt Engineering.</p>
      </div>
      <div
        className="premium-glass animate-glow p-6 rounded-xl text-center"
        data-aos="zoom-in"
        data-aos-delay="200"
      >
        🚀 <h4 className="mt-2 font-semibold text-amber-200">
          Problem Solving
        </h4>
        <p className="text-sm text-gray-300">Coding challenges.</p>
      </div>
      <div
        className="premium-glass animate-glow p-6 rounded-xl text-center"
        data-aos="zoom-in"
        data-aos-delay="300"
      >
        🎨 <h4 className="mt-2 font-semibold text-amber-200">Creative</h4>
        <p className="text-sm text-gray-300">Interactive design.</p>
      </div>
    </div>
  </section>
);

export default Journey;
