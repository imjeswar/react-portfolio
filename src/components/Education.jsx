import React from "react";

const Education = () => (
  <section
    id="education"
    className="max-w-4xl mx-auto my-16 p-8 bg-gray-900/80 backdrop-blur-md rounded-2xl shadow-xl border border-amber-400/30 hover:shadow-amber-400/70 transition duration-500 transform hover:-translate-y-2"
    data-aos="fade-up"
  >
    <h2 className="text-3xl font-bold border-b-2 border-amber-300 pb-2 mb-8 text-amber-200 tracking-wide">
      Education
    </h2>

    <div className="relative border-l-4 border-amber-300 pl-6 space-y-10">
      {/* College */}
      <div className="relative group">
        <div className="absolute -left-3 top-2 w-5 h-5 rounded-full bg-amber-300 border-4 border-gray-900 animate-pulse" />
        <div className="bg-gray-800/90 p-6 rounded-xl shadow-md border border-amber-400/20 group-hover:shadow-amber-300 group-hover:scale-[1.02] transition duration-300">
          <h3 className="text-xl font-bold text-amber-200">
            B.Tech in Artificial Intelligence &amp; Data Science
          </h3>
          <p className="text-amber-100">
            Dhanalakshmi Srinivasan University, Trichy
          </p>
          <p className="text-sm text-gray-400">Pre-final Year | 2022 – 2026</p>
          <p className="mt-2 text-gray-300">
            Currently pursuing with focus on Artificial Intelligence, Data
            Science, and modern applications in AI.
          </p>
        </div>
      </div>

      {/* School */}
      <div className="relative group">
        <div className="absolute -left-3 top-2 w-5 h-5 rounded-full bg-amber-300 border-4 border-gray-900 animate-pulse" />
        <div className="bg-gray-800/90 p-6 rounded-xl shadow-md border border-amber-400/20 group-hover:shadow-amber-300 group-hover:scale-[1.02] transition duration-300">
          <h3 className="text-xl font-bold text-amber-200">
            Higher Secondary Education
          </h3>
          <p className="text-amber-100">
            Sri Bala Vidhyamandhir Matric Hr. Sec. School, Trichy
          </p>
          <p className="text-sm text-gray-400">Completed in 2022</p>
          <p className="mt-2 text-gray-300">
            Scored <strong>72%</strong> in Class 12
          </p>
        </div>
      </div>
    </div>
  </section>
);

export default Education;
