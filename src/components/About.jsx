import React from "react";

const About = () => (
  <section
    id="about"
    className="w-full p-6 md:p-12 premium-glass animate-glow rounded-3xl"
    data-aos="fade-up"
  >
    <div className="relative group inline-block mb-8">
      <h2 className="text-4xl font-bold text-amber-200 tracking-wide heading-shine pb-2">
        About Me
      </h2>
      <span className="absolute bottom-0 left-0 w-0 h-[3px] bg-gradient-to-r from-amber-400 to-amber-200 transition-all duration-500 group-hover:w-full group-hover:shadow-[0_0_12px_#fbbf24] shadow-[0_0_6px_#fbbf24]" />
    </div>

    <p className="text-gray-300 leading-relaxed hover:text-white transition duration-300">
      I’m Jeswar A M, a passionate web developer and AI enthusiast who loves
      transforming ideas into impactful digital solutions. I focus on building
      clean, scalable, and user-friendly applications using modern tools and
      frameworks. Driven by curiosity, I constantly explore AI and automation to
      unlock creativity and smarter innovation. For me, technology is more than
      code — it’s about growth, collaboration, and creating a real difference.
    </p>
  </section>
);

export default About;
