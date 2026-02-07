import React from "react";

const ProjectDetailsHealth = ({ handleReload }) => (
    <section id="project4-details" className="w-full scroll-mt-20">
        <div className="flex flex-col md:flex-row-reverse items-center gap-10 premium-glass animate-glow p-8 md:p-12 rounded-3xl shadow-lg hover:shadow-[0_0_25px_rgba(251,191,36,0.6)] transition duration-300">
            {/* Image (Left) */}
            <div className="md:w-1/2 flex justify-center">
                <img
                    src="robot.png"
                    className="max-w-sm rounded-lg border border-gray-700"
                    alt="AI Health Assistant"
                />
            </div>

            {/* Text (Right) */}
            <div className="md:w-1/2 text-center md:text-left">
                <h3 className="text-2xl font-bold mb-4 text-amber-100">
                    AI Health Assistant (Python + Gemini API)
                </h3>
                <p className="text-gray-300 mb-6">
                    Built using Python and Gemini API to handle health-related user queries.
                    Provides AI-generated suggestions and basic wellness guidance in real time.
                    Demonstrates API integration and prompt-based AI interaction.
                </p>
                <div className="flex gap-4 justify-center md:justify-start">
                    <a
                        href="https://github.com/imjeswar/streamlit-health-app.git"
                        target="_blank"
                        rel="noreferrer"
                        className="px-6 py-2 bg-gray-900 border border-amber-300 rounded-lg hover:bg-amber-200 hover:text-black transition"
                    >
                        View Code
                    </a>
                    <a
                        href="#"
                        onClick={handleReload}
                        className="px-6 py-2 bg-amber-300 text-black rounded-lg hover:bg-amber-400 transition"
                    >
                        Live Demo
                    </a>
                </div>
            </div>
        </div>
    </section>
);

export default ProjectDetailsHealth;
