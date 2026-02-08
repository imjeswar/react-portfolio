import React from "react";

const Internship = () => {
    return (
        <section
            id="internship"
            className="w-full p-6 md:p-12 premium-glass animate-glow rounded-3xl"
            data-aos="fade-up"
        >
            <div className="relative group inline-block mb-10">
                <h2 className="text-4xl font-bold text-amber-200 tracking-wide heading-shine pb-2">
                    Internship Experience
                </h2>
                <span className="absolute bottom-0 left-0 w-0 h-[3px] bg-gradient-to-r from-amber-400 to-amber-200 transition-all duration-500 group-hover:w-full group-hover:shadow-[0_0_12px_#fbbf24] shadow-[0_0_6px_#fbbf24]" />
            </div>

            <div className="relative pl-8 space-y-10">
                {/* Custom Gradient Line */}
                <div className="absolute left-0 top-0 w-1 h-full bg-gradient-to-b from-transparent via-amber-300 to-transparent shadow-[0_0_10px_rgba(251,191,36,0.5)]" />

                <div className="relative group">
                    <div className="absolute -left-[2.15rem] top-8 w-4 h-4 rounded-full bg-amber-300 border-2 border-black animate-pulse shadow-[0_0_15px_rgba(251,191,36,0.8)] z-10" />
                    <div className="premium-glass animate-glow p-8 rounded-3xl transition duration-300">
                        <h3 className="text-xl font-bold text-amber-200">
                            Web Developer Intern
                        </h3>
                        <p className="text-amber-100 font-semibold">
                            The Pinnacle | Remote | Coimbatore
                        </p>
                        <p className="text-sm text-gray-400">September 2025 – Present</p>

                        <p className="mt-4 text-gray-300 leading-relaxed text-lg">
                            Contributed to the development of internal web applications and product features
                            while assisting in UI design improvements, collaborated with a remote development
                            team using version control tools and participated in content analysis tasks, and
                            gained hands-on experience with real-world development workflows, technical
                            documentation, and effective team collaboration.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default Internship;
