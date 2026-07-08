import React from "react";

const certificationsData = [
  {
    id: "coursera-ibm-se",
    title: "Introduction to Software Engineering",
    issuer: "IBM (via Coursera)",
    date: "Jun 2026",
    fileUrl: "/certificates/Coursera%20WEVQD69GEC4M.pdf"
  },
  {
    id: "anthropic-claude",
    title: "Claude 101 Certificate",
    issuer: "Anthropic",
    date: "Jun 2026",
    fileUrl: "/certificates/Claude.101%20certificate.pdf"
  },
  {
    id: "be10x-ai-tools",
    title: "AI Tools and ChatGPT Workshop",
    issuer: "be10x",
    date: "Jun 2026",
    fileUrl: "/certificates/Certificate.pdf"
  },
  {
    id: "nptel-iitr-dl",
    title: "Deep Learning",
    issuer: "IIT Ropar (via NPTEL)",
    date: "Oct 2025",
    fileUrl: "/certificates/Deep%20Learning%20-%20IIT%20Ropar.pdf"
  },
  {
    id: "novitech-macros",
    title: "Productivity with Macros (Skill Camp)",
    issuer: "NoviTech R&D",
    date: "Aug 2025",
    fileUrl: "/certificates/JESWAR%20AM.pdf"
  },
  {
    id: "icat-participation",
    title: "Internship Common Aptitude Test (ICAT)",
    issuer: "YCAT / ICAT",
    date: "Jun 2026",
    fileUrl: "/certificates/Jeswar%20-%20Participation%20Certificate.pdf"
  },
  {
    id: "mongodb-basics",
    title: "MongoDB Basics for Students",
    issuer: "MongoDB",
    date: "Jul 2025",
    fileUrl: "/certificates/MONGO%20DB.pdf"
  },
  {
    id: "tnsc-jr-technician",
    title: "Jr. Technician (Computer Hardware & Network)",
    issuer: "TN Skill Corporation",
    date: "Jul 2026",
    fileUrl: "/certificates/TR2026-M384952.pdf"
  }
];

const Certifications = () => {
  return (
    <section
      id="certifications"
      className="py-12 w-full premium-glass animate-glow rounded-3xl p-6 md:p-12 group"
      data-aos="fade-up"
    >
      <div className="text-center mb-10">
        <div className="relative inline-block">
          <h2 className="text-4xl font-bold text-amber-100 pb-2 heading-shine">
            🏆 Certifications
          </h2>
          <span className="absolute bottom-0 left-0 w-0 h-[3px] bg-gradient-to-r from-amber-400 to-amber-200 transition-all duration-500 group-hover:w-full group-hover:shadow-[0_0_12px_#fbbf24] shadow-[0_0_6px_#fbbf24]" />
        </div>
        <p className="text-gray-400 text-sm mt-3 max-w-xl mx-auto">
          A showcase of my professional certifications, workshops, and technical specializations.
        </p>
      </div>

      {/* Grid of Certifications */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {certificationsData.map((cert) => (
          <div
            key={cert.id}
            className="p-5 rounded-xl premium-glass animate-glow flex flex-col justify-between hover:shadow-[0_0_20px_rgba(251,191,36,0.4)] hover:border-amber-400/30 transition-all duration-300 relative overflow-hidden group/card"
            data-aos="zoom-in"
          >
            {/* Background Glow Ring */}
            <div className="absolute inset-0 bg-amber-400/5 opacity-0 group-hover/card:opacity-100 transition-opacity duration-300 -z-10" />

            <div className="mb-4">
              {/* Header with Title & Date */}
              <div className="flex justify-between items-start gap-3 mb-2">
                <h3 className="text-base font-bold text-amber-100 leading-snug group-hover/card:text-amber-200 transition duration-300">
                  {cert.title}
                </h3>
                <span className="text-[9px] text-gray-400 font-bold uppercase tracking-wider bg-black/40 px-2 py-0.5 rounded-md border border-white/5 shrink-0">
                  {cert.date}
                </span>
              </div>

              <p className="text-xs text-gray-500 font-medium flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400/70 animate-pulse" />
                {cert.issuer}
              </p>
            </div>

            {/* Button directly opening the certificate file */}
            <a
              href={cert.fileUrl}
              target="_blank"
              rel="noreferrer"
              className="w-full py-1.5 bg-amber-300 text-black text-[11px] font-bold rounded-lg hover:bg-amber-400 active:scale-[0.98] transition cursor-pointer flex items-center justify-center gap-1.5 shadow-[0_4px_12px_rgba(251,191,36,0.15)]"
            >
              View Certificate
            </a>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Certifications;
