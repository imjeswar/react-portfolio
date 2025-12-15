import React from "react";

const ProjectDetailsChatbot = ({ handleReload }) => (
  <section id="project3-details" className="py-16 bg-black scroll-mt-20">
    <div className="max-w-5xl mx-auto flex flex-col md:flex-row-reverse items-center gap-10 bg-gray-900 p-6 rounded-lg border border-amber-300 shadow-lg hover:shadow-[0_0_25px_rgba(251,191,36,0.6)] transition duration-300">
      {/* Image (Right) */}
      <div className="md:w-1/2 flex justify-center">
        <img
          src="robot.png"
          className="max-w-sm rounded-lg border border-gray-700"
          alt="Chatbot"
        />
      </div>

      {/* Text (Left) */}
      <div className="md:w-1/2 text-center md:text-left">
        <h3 className="text-2xl font-bold mb-4 text-amber-100">Chatbot App</h3>
        <p className="text-gray-300 mb-6">
          An AI-powered chatbot application using Python and Gemini API,
          deployed on Streamlit for interactive usage.
        </p>
        <div className="flex gap-4 justify-center md:justify-start">
          <a
            href="#"
            onClick={handleReload}
            className="px-6 py-2 bg-amber-300 text-black rounded-lg hover:bg-amber-400 transition"
          >
            Live Demo
          </a>

          <a
            href="https://chatbot-demo.netlify.app"
            target="_blank"
            rel="noreferrer"
            className="px-6 py-2 bg-amber-300 text-black rounded-lg hover:bg-amber-400 transition"
          >
            Live Demo
          </a>
        </div>
      </div>
    </div>
  </section>
);

export default ProjectDetailsChatbot;
