import React from "react";

const ProjectDetailsResume = ({ handleReload }) => (
    <section id="project4-details" className="w-full scroll-mt-20 group">
        <div className="flex flex-col md:flex-row-reverse items-center gap-10 premium-glass animate-glow p-6 md:p-12 rounded-3xl shadow-lg hover:shadow-[0_0_25px_rgba(251,191,36,0.6)] transition duration-300">
            {/* Image (Right) */}
            <div className="w-full md:w-1/2 flex justify-center mb-8 md:mb-0">
                <img
                    src="computer1.png"
                    className="w-full max-w-[400px] aspect-[4/3] object-contain rounded-xl border border-amber-300/20 shadow-2xl shadow-amber-900/40"
                    alt="AI Resume Analyzer"
                />
            </div>

            {/* Text (Left) */}
            <div className="md:w-1/2 text-center md:text-left">
                <h3 className="text-2xl font-bold mb-4 text-amber-100">
                    AI Resume Analyzer
                </h3>
                <p className="text-gray-300 mb-6">
                    Analyzes resumes using AI and NLP techniques.
                    Extracts skills, keywords, and experience from resume content.
                    Provides feedback to improve resume strength and job relevance.
                </p>
                <div className="flex gap-4 justify-center md:justify-start">
                    <a
                        href="https://github.com/imjeswar/ai-resume-analyzer.git"
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

export default ProjectDetailsResume;
