import React from "react";

const Hero = ({ scrollToSkills }) => {
  return (
    <div className="flex flex-col md:flex-row items-center justify-center min-h-screen py-12 md:py-0 text-center px-6">
      {/* Left: Text */}
      <div className="md:w-1/2 flex flex-col items-center md:items-start text-center md:text-left">
        <h1 className="text-4xl sm:text-5xl md:text-7xl font-extrabold tracking-tight">
          Hi, I'm <span className="text-amber-300 font-name">Jeswar</span>
        </h1>
        <h2 className="text-2xl mt-4 text-amber-200 font-semibold uppercase tracking-widest">
          Web Developer &amp; AI Enthusiast
        </h2>
        <p className="max-w-xl mt-4 text-amber-100">
          Crafting digital experiences with modern web technologies and
          exploring AI to build solutions that matter.
        </p>
        <div className="flex gap-4 mt-6">
          <a
            href="#projects"
            className="px-5 py-2.5 md:px-6 md:py-3 rounded-full font-bold bg-amber-200 text-black hover:bg-white transition text-sm md:text-base"
          >
            ⚡ Explore My Work
          </a>
          <a
            href="#contact"
            className="px-5 py-2.5 md:px-6 md:py-3 rounded-full font-bold bg-amber-200 text-black hover:bg-white transition text-sm md:text-base"
          >
            📩 Get In Touch
          </a>
        </div>
        <div className="flex gap-6 mt-8">
          <a
            href="https://wa.me/917904181537"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-full bg-gray-900 hover:bg-amber-200 hover:text-black transition"
          >
            📱
          </a>
          <a
            href="mailto:imjeswar@gmail.com"
            className="p-3 rounded-full bg-gray-900 hover:bg-amber-200 hover:text-black transition"
          >
            ✉
          </a>
          <a
            href="https://linkedin.com/in/yourprofile"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-full bg-gray-900 hover:bg-amber-200 hover:text-black transition"
          >
            💼
          </a>
          <a
            href="https://github.com/yourusername"
            target="_blank"
            rel="noreferrer"
            className="p-3 rounded-full bg-gray-900 hover:bg-amber-200 hover:text-black transition"
          >
            💻
          </a>
        </div>
      </div>

      {/* Right: Image + Skills */}
      <div className="md:w-1/2 mt-10 md:mt-0 flex flex-col items-center">
        <img
          src="jeswar1.png"
          alt="Jeswar A M"
          className="max-h-[320px] md:max-h-[480px] object-contain drop-shadow-2xl"
        />

        {/* Skills Icons Row – smaller icons + dark circular background */}
        <div className="flex flex-wrap justify-center gap-4 mt-6">
          {[
            [
              "HTML",
              "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
            ],
            [
              "CSS",
              "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg",
            ],
            [
              "JavaScript",
              "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
            ],
            [
              "Python",
              "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
            ],
            [
              "Java",
              "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
            ],
            [
              "C",
              "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg",
            ],
            [
              "GitHub",
              "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg",
              "invert",
            ],
          ].map(([title, src, extra]) => (
            <button
              key={title}
              type="button"
              onClick={scrollToSkills}
              className="p-2.5 md:p-3 rounded-full bg-gray-900/90 hover:bg-amber-200 transition flex items-center justify-center"
              title={title}
            >
              <img
                src={src}
                alt={title}
                className={`w-7 h-7 skill-icon ${extra === "invert" ? "invert" : ""}`}
              />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Hero;
