import React from "react";

const ProjectDetailsResume = () => (
    <section id="project4-details" className="w-full scroll-mt-20 group">
        <div className="flex flex-col md:flex-row-reverse items-center gap-10 premium-glass animate-glow p-6 md:p-12 rounded-3xl shadow-lg hover:shadow-[0_0_25px_rgba(251,191,36,0.6)] transition duration-300">
            {/* Image (Right) */}
            <div className="w-full md:w-1/2 flex justify-center mb-8 md:mb-0">
                <img
                    src="computer1.png"
                    className="w-full max-w-[400px] h-auto rounded-xl border border-amber-300/20 shadow-2xl shadow-amber-900/40"
                    alt="AI Resume Screening Simulator — ATS Optimizer"
                />
            </div>

            {/* Text (Left) */}
            <div className="md:w-1/2 text-center md:text-left">
                <h3 className="text-2xl font-bold mb-4 text-amber-100 heading-shine">
                    AI Resume Screening Simulator
                </h3>
                <p className="text-gray-300 mb-6 font-medium">
                    ATS Resume Optimizer &amp; Screening Simulator that parses resumes, matches keywords against job descriptions, and provides actionable suggestions to boost score.
                </p>
                <div className="flex gap-4 justify-center md:justify-start">
                    <a
                        href="#contact"
                        className="px-6 py-2 bg-gray-900 border border-amber-300 rounded-lg hover:bg-amber-200 hover:text-black transition font-semibold"
                    >
                        View Code
                    </a>
                    <a
                        href="https://ats-resume-rho.vercel.app/"
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

export default ProjectDetailsResume;
