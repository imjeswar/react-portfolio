import React from "react";

const ProjectDetailsChatbot = ({ handleReload }) => (
  <section id="project3-details" className="w-full scroll-mt-20">
    <div className="flex flex-col md:flex-row items-center gap-10 premium-glass animate-glow p-8 md:p-12 rounded-3xl shadow-lg transition duration-300">
      {/* Image (Left) */}
      <div className="md:w-1/2 flex justify-center">
        <img
          src="robot.png"
          className="max-w-sm rounded-lg border border-gray-700"
          alt="Chatbot"
        />
      </div>

      {/* Text (Right) */}
      <div className="md:w-1/2 text-center md:text-left">
        <h3 className="text-2xl font-bold mb-4 text-amber-100 heading-shine">Chatbot App</h3>
        <p className="text-gray-300 mb-6 font-medium">
          An AI-powered chatbot application using Python and Gemini API,
          deployed on Streamlit for interactive usage.
        </p>
        <div className="flex gap-4 justify-center md:justify-start">
          <a
            href="https://github.com/imjeswar/chatbot-app"
            target="_blank"
            rel="noreferrer"
            className="px-6 py-2 bg-gray-900 border border-amber-300 rounded-lg hover:bg-amber-200 hover:text-black transition font-semibold"
          >
            View Code
          </a>

          <a
            href="https://chatbot-demo.netlify.app"
            target="_blank"
            rel="noreferrer"
            className="px-6 py-2 bg-amber-300 text-black rounded-lg hover:bg-amber-400 transition font-semibold"
          >
            Live Demo
          </a>
        </div>
      </div>
    </div>
  </section>
);

export default ProjectDetailsChatbot;
