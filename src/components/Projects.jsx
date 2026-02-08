import React from "react";

const Projects = () => (
  <section
    id="projects"
    className="py-12 w-full premium-glass animate-glow text-center rounded-3xl p-6 md:p-12"
    data-aos="fade-up"
  >
    <div className="relative group inline-block mb-10">
      <h2 className="text-4xl font-bold text-amber-100 pb-2 heading-shine">
        Projects
      </h2>
      <span className="absolute bottom-0 left-0 w-0 h-[3px] bg-gradient-to-r from-amber-400 to-amber-200 transition-all duration-500 group-hover:w-full group-hover:shadow-[0_0_12px_#fbbf24] shadow-[0_0_6px_#fbbf24]" />
    </div>

    <div className="grid md:grid-cols-3 gap-6 mt-6">
      <a
        href="#project1-details"
        className="p-4 rounded-xl premium-glass animate-glow hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
      >
        <h3 className="text-xl font-semibold mb-1 text-amber-100">
          Portfolio Website
        </h3>
        <p className="text-gray-400 text-sm">
          A personal portfolio built with HTML &amp; Tailwind.
        </p>
      </a>

      <a
        href="#project2-details"
        className="p-4 rounded-xl premium-glass animate-glow hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
      >
        <h3 className="text-xl font-semibold mb-1 text-amber-100">
          E-commerce Platform
        </h3>
        <p className="text-gray-400 text-sm">
          Full-stack app with AI suggestions.
        </p>
      </a>

      <a
        href="#project3-details"
        className="p-4 rounded-xl premium-glass animate-glow hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
      >
        <h3 className="text-xl font-semibold mb-1 text-amber-100">
          Chatbot App
        </h3>
        <p className="text-gray-400 text-sm">
          An AI chatbot built using Python &amp; API.
        </p>
      </a>

      {/* New Project 4 */}
      <a
        href="#project4-details"
        className="p-4 rounded-xl premium-glass animate-glow hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
      >
        <h3 className="text-xl font-semibold mb-1 text-amber-100">
          AI Health Assistant
        </h3>
        <p className="text-gray-400 text-sm">
          Python + Gemini API health wellness guide.
        </p>
      </a>

      {/* New Project 5 */}
      <a
        href="#project5-details"
        className="p-4 rounded-xl premium-glass animate-glow hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
      >
        <h3 className="text-xl font-semibold mb-1 text-amber-100">
          AI Resume Analyzer
        </h3>
        <p className="text-gray-400 text-sm">
          Analyzes resumes using AI and NLP techniques.
        </p>
      </a>

      {/* New Project 6 */}
      <a
        href="#project6-details"
        className="p-4 rounded-xl premium-glass animate-glow hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
      >
        <h3 className="text-xl font-semibold mb-1 text-amber-100">
          Inkify – Text to Handwriting
        </h3>
        <p className="text-gray-400 text-sm">
          Converts digital text into handwritten output.
        </p>
      </a>
    </div>
  </section>
);

export default Projects;
