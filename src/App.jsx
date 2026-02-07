import React, { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

import Hero from "./components/Hero";
import Navbar from "./components/Navbar";
import About from "./components/About";
import Education from "./components/Education";
import Journey from "./components/Journey";
import Internship from "./components/Internship";
import Skills from "./components/Skills";
import Projects from "./components/Projects";
import ProjectDetailsPortfolio from "./components/ProjectDetailsPortfolio";
import ProjectDetailsChatbot from "./components/ProjectDetailsChatbot";
import ProjectDetailsHealth from "./components/ProjectDetailsHealth";
import ProjectDetailsResume from "./components/ProjectDetailsResume";
import ProjectDetailsInkify from "./components/ProjectDetailsInkify";
import ProjectDetailsEcommerce from "./components/ProjectDetailsEcommerce";
import Contact from "./components/Contact";
import Footer from "./components/Footer";
import Background from "./components/Background";

const App = () => {
  useEffect(() => {
    // AOS init
    AOS.init({ duration: 1000, once: true });

    // === CUSTOM CURSOR ===
    const dot = document.createElement("div");
    dot.className = "cursor-dot";
    document.body.appendChild(dot);

    const trailCount = 6;
    const trails = [];
    const trailPos = [];
    for (let i = 0; i < trailCount; i++) {
      const t = document.createElement("div");
      t.className = `cursor-trail trail-${i}`;
      document.body.appendChild(t);
      trails.push(t);
      trailPos.push({ x: window.innerWidth / 2, y: window.innerHeight / 2 });
    }

    const mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    const pos = { x: mouse.x, y: mouse.y };

    const handleMouseMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });

    const mainLerp = 0.35;
    const baseTrailLerp = 0.12;
    let animationFrameId;

    const animate = () => {
      pos.x += (mouse.x - pos.x) * mainLerp;
      pos.y += (mouse.y - pos.y) * mainLerp;

      dot.style.transform = `translate(${pos.x}px, ${pos.y}px) translate(-50%, -50%)`;

      let prevX = pos.x;
      let prevY = pos.y;

      for (let i = 0; i < trails.length; i++) {
        const lerp = Math.max(0.02, baseTrailLerp - i * 0.012);
        trailPos[i].x += (prevX - trailPos[i].x) * lerp;
        trailPos[i].y += (prevY - trailPos[i].y) * lerp;
        prevX = trailPos[i].x;
        prevY = trailPos[i].y;

        const t = trails[i];
        t.style.transform = `translate(${trailPos[i].x}px, ${trailPos[i].y}px) translate(-50%, -50%)`;
        const baseSize = 22;
        const scale = 1 - i * 0.08;
        t.style.width = Math.max(6, baseSize * scale) + "px";
        t.style.height = Math.max(6, baseSize * scale) + "px";
      }

      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);

    const interactiveSel = "a, button, input, textarea, select, label";
    const interactiveEls = document.querySelectorAll(interactiveSel);

    const handleEnter = () => dot.classList.add("enlarge");
    const handleLeave = () => dot.classList.remove("enlarge");

    interactiveEls.forEach((el) => {
      el.addEventListener("mouseenter", handleEnter);
      el.addEventListener("mouseleave", handleLeave);
    });

    const handleMouseDown = () => dot.classList.add("shrink");
    const handleMouseUp = () => dot.classList.remove("shrink");

    document.addEventListener("mousedown", handleMouseDown);
    document.addEventListener("mouseup", handleMouseUp);

    // Smooth scroll for internal links (same as your script)
    const anchors = document.querySelectorAll('a[href^="#"]');
    const onClickAnchor = (e) => {
      const targetId = e.currentTarget.getAttribute("href");
      if (!targetId || targetId === "#") return;
      const targetEl = document.querySelector(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: "smooth" });
      }
    };
    anchors.forEach((a) => a.addEventListener("click", onClickAnchor));

    // Skill bars animation (kept from original; harmless even if unused)
    const animateSkills = () => {
      const bars = document.querySelectorAll(".skill-bar");
      bars.forEach((bar) => {
        const rect = bar.getBoundingClientRect();
        if (rect.top < window.innerHeight - 50) {
          bar.style.width = bar.dataset.percentage;
        }
      });
    };
    window.addEventListener("scroll", animateSkills);
    window.addEventListener("load", animateSkills);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mousedown", handleMouseDown);
      document.removeEventListener("mouseup", handleMouseUp);
      anchors.forEach((a) => a.removeEventListener("click", onClickAnchor));
      window.removeEventListener("scroll", animateSkills);
      window.removeEventListener("load", animateSkills);
      interactiveEls.forEach((el) => {
        el.removeEventListener("mouseenter", handleEnter);
        el.removeEventListener("mouseleave", handleLeave);
      });
      cancelAnimationFrame(animationFrameId);
      dot.remove();
      trails.forEach((t) => t.remove());
    };
  }, []);

  const scrollToSkills = () => {
    const el = document.getElementById("skills");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  const handleReload = (e) => {
    e.preventDefault();
    window.location.reload();
  };

  return (
    <>
      {/* Global CSS from your <style> and glow animation */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700;800;900&family=Manrope:wght@300;400;500;600;700;800&family=Sora:wght@400;500;600;700;800&family=Syne:wght@400;500;600;700;800&display=swap');
        
        html { scroll-behavior: smooth; }
        body { 
          cursor: none; 
          background: black; 
          font-family: 'Manrope', sans-serif;
          overflow-x: hidden;
          color: #fef3c7; /* text-amber-50 */
        }
        h1, h2, h3, h4, h5, h6 {
          font-family: 'Syne', sans-serif;
        }
        .font-name {
          font-family: 'Lexend', sans-serif;
        }
        body::before {
          content: '';
          position: fixed;
          inset: 0;
          background: transparent;
          pointer-events: none;
          z-index: 9999;
        }
        .cursor-dot {
          position: fixed; top:0; left:0; width:10px; height:10px;
          border-radius:50%;
          background: radial-gradient(circle at 30% 30%, rgba(255,215,0,0.98) 0%, rgba(255,215,0,0.72) 30%, rgba(255,215,0,0.16) 60%, transparent 85%);
          pointer-events:none;
          transform: translate(-50%, -50%);
          transition: width .12s ease, height .12s ease, opacity .12s ease, transform .12s ease;
          z-index:11000;
          box-shadow:0 8px 26px rgba(255,215,0,0.12);
          mix-blend-mode: screen;
          opacity:0.98;
        }
        .cursor-trail {
          position: fixed; top:0; left:0; width:22px; height:22px;
          border-radius:50%;
          background: radial-gradient(circle at 30% 30%, rgba(255,215,0,0.32) 0%, rgba(255,215,0,0.08) 50%, transparent 85%);
          pointer-events:none;
          transform: translate(-50%, -50%);
          z-index:10990;
          mix-blend-mode:screen;
          transition: opacity .15s linear;
        }
        .trail-0{opacity:.85}.trail-1{opacity:.62}.trail-2{opacity:.45}.trail-3{opacity:.3}.trail-4{opacity:.2}.trail-5{opacity:.12}
        .cursor-dot.enlarge{width:18px;height:18px}
        .cursor-dot.shrink{transform:translate(-50%,-50%) scale(0.85)}
        body::before{z-index:10000;}
        .skill-bar { width: 0%; height: 0.75rem; background-color: #fbbf24; border-radius: 0.375rem; transition: width 1.5s ease-in-out; }
        .skill-icon { transition: transform 0.3s ease, filter 0.3s ease; }
        .skill-icon:hover { transform: scale(1.25); filter: drop-shadow(0 0 10px #fbbf24); }

        @keyframes glowPulse {
          0%, 100% {
            border-color: rgba(251, 191, 36, 0.2);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8), 0 0 15px rgba(251, 191, 36, 0.1);
          }
          50% {
            border-color: rgba(251, 191, 36, 0.5);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8), 0 0 30px rgba(251, 191, 36, 0.3);
          }
        }
        .animate-glow {
          animation: glowPulse 5s ease-in-out infinite;
        }
        .premium-glass {
          background: rgba(10, 10, 10, 0.45); 
          backdrop-filter: blur(28px);
          border: 1px solid rgba(251, 191, 36, 0.1);
          box-shadow: 
            0 20px 50px -10px rgba(0, 0, 0, 0.8),
            inset 0 0 0 1px rgba(255, 255, 255, 0.05);
          position: relative;
          z-index: 1;
          transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .premium-glass:hover {
          border-color: rgba(251, 191, 36, 0.4);
          box-shadow: 
            0 25px 60px -5px rgba(0, 0, 0, 0.9), 
            0 0 30px rgba(251, 191, 36, 0.2),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1);
          transform: translateY(-5px) scale(1.005);
        }
        .premium-glass::before {
          content: "";
          position: absolute;
          inset: 0;
          border-radius: inherit;
          padding: 1px;
          background: linear-gradient(to bottom right, rgba(251,191,36,0.3), transparent, rgba(251,191,36,0.1));
          -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
          mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
          -webkit-mask-composite: xor;
          mask-composite: exclude;
          pointer-events: none;
          opacity: 0.5;
          transition: opacity 0.4s ease;
        }
        .premium-glass:hover::before {
          opacity: 1;
        }
        .heading-shine {
          background: linear-gradient(90deg, #fbbf24, #fcd34d, #fbbf24);
          background-size: 200% auto;
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          transition: all 0.5s ease;
        }
        .heading-shine:hover {
          background-position: right center;
          text-shadow: 0 0 20px rgba(251, 191, 36, 0.4);
        }
      `}</style>

      <div className="relative text-amber-100 space-y-20 pb-20">
        <Background />
        <Hero scrollToSkills={scrollToSkills} />
        <Navbar />
        <div className="max-w-5xl mx-auto space-y-20 px-4 shadow-none">
          <About />
          <Education />
          <Journey />
          <Internship />
          <Skills />
          <Projects />
          {/* Alternating Layout Verification: L, R, L, R, L, R */}
          <ProjectDetailsPortfolio handleReload={handleReload} /> {/* L */}
          <ProjectDetailsEcommerce handleReload={handleReload} /> {/* R */}
          <ProjectDetailsChatbot handleReload={handleReload} />   {/* L */}
          <ProjectDetailsHealth handleReload={handleReload} />    {/* R */}
          <ProjectDetailsResume handleReload={handleReload} />    {/* L */}
          <ProjectDetailsInkify handleReload={handleReload} />    {/* R */}
          <Contact />
        </div>
        <Footer />
      </div>
    </>
  );
};

export default App;
