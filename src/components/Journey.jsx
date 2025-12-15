import React from "react";

const Journey = () => (
  <section
    id="journey"
    className="max-w-5xl mx-auto my-16 p-8 bg-gray-900/80 backdrop-blur-md rounded-2xl shadow-xl border border-amber-400/30 hover:shadow-amber-400/70 transition duration-500 transform hover:-translate-y-2"
    data-aos="fade-up"
  >
    <h2 className="text-3xl font-bold border-b-2 border-amber-300 pb-2 mb-6 text-amber-200 tracking-wide">
      My Journey
    </h2>

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
        className="bg-gray-800/90 p-6 rounded-xl shadow-md border border-amber-400/20 hover:shadow-amber-300 hover:scale-105 transition duration-300 text-center"
        data-aos="zoom-in"
      >
        ⚡ <h4 className="mt-2 font-semibold text-amber-200">Full-Stack</h4>
        <p className="text-sm text-gray-300">Responsive apps.</p>
      </div>
      <div
        className="bg-gray-800/90 p-6 rounded-xl shadow-md border border-amber-400/20 hover:shadow-amber-300 hover:scale-105 transition duration-300 text-center"
        data-aos="zoom-in"
        data-aos-delay="100"
      >
        🤖 <h4 className="mt-2 font-semibold text-amber-200">
          AI &amp; Innovation
        </h4>
        <p className="text-sm text-gray-300">Prompt Engineering.</p>
      </div>
      <div
        className="bg-gray-800/90 p-6 rounded-xl shadow-md border border-amber-400/20 hover:shadow-amber-300 hover:scale-105 transition duration-300 text-center"
        data-aos="zoom-in"
        data-aos-delay="200"
      >
        🚀 <h4 className="mt-2 font-semibold text-amber-200">
          Problem Solving
        </h4>
        <p className="text-sm text-gray-300">Coding challenges.</p>
      </div>
      <div
        className="bg-gray-800/90 p-6 rounded-xl shadow-md border border-amber-400/20 hover:shadow-amber-300 hover:scale-105 transition duration-300 text-center"
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
