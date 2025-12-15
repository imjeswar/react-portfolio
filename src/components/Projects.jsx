import React from "react";

const Projects = () => (
  <section
    id="projects"
    className="py-12 bg-gray-900 text-center max-w-5xl mx-auto rounded-lg shadow-lg p-6 border-2 border-amber-400/50 transition hover:shadow-[0_0_40px_rgba(251,191,36,0.7)]"
    data-aos="fade-up"
  >
    <h2 className="text-3xl font-bold mb-4 text-amber-100 border-b-2 border-amber-300/70 pb-2 inline-block">
      Projects
    </h2>

    <div className="grid md:grid-cols-3 gap-6 mt-6">
      <a
        href="#project1-details"
        className="p-4 rounded-lg border-2 border-amber-200 hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
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
        className="p-4 rounded-lg border-2 border-amber-200 hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
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
        className="p-4 rounded-lg border-2 border-amber-200 hover:shadow-[0_0_25px_rgba(251,191,36,0.8)] transition duration-300"
      >
        <h3 className="text-xl font-semibold mb-1 text-amber-100">
          Chatbot App
        </h3>
        <p className="text-gray-400 text-sm">
          An AI chatbot built using Python &amp; API.
        </p>
      </a>
    </div>
  </section>
);

export default Projects;
