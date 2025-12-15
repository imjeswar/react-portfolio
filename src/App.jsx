import React, { useEffect } from "react";
import AOS from "aos";
import "aos/dist/aos.css";

import Hero from "./components/Hero";
import Navbar from "./components/Navbar";
import About from "./components/About";
import Education from "./components/Education";
import Journey from "./components/Journey";
import Skills from "./components/Skills";
import Projects from "./components/Projects";
import ProjectDetailsPortfolio from "./components/ProjectDetailsPortfolio";
import ProjectDetailsChatbot from "./components/ProjectDetailsChatbot";
import Contact from "./components/Contact";
import Footer from "./components/Footer";

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
        html { scroll-behavior: smooth; }
        body::before {
          content: '';
          position: fixed;
          inset: 0;
          background: transparent;
          pointer-events: none;
          z-index: 9999;
        }
        @keyframes gradientFlow {
          0% { background-position:0% 50%; }
          50% { background-position:100% 50%; }
          100% { background-position:0% 50%; }
        }
        .animate-gradient {
          background-size: 400% 400%;
          animation: gradientFlow 12s ease infinite;
        }
        body { cursor: none; }
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
            box-shadow: 0 0 10px rgba(251, 191, 36, 0.3), 0 0 20px rgba(251, 191, 36, 0.2);
          }
          50% {
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.5), 0 0 40px rgba(251, 191, 36, 0.3);
          }
        }
        .animate-glow {
          animation: glowPulse 3s infinite;
        }
      `}</style>

      <div className="bg-black text-amber-100 font-[Poppins]">
        <Hero scrollToSkills={scrollToSkills} />
        <Navbar />
        <About />
        <Education />
        <Journey />
        <Skills />
        <Projects />
        <ProjectDetailsPortfolio handleReload={handleReload} />
        <ProjectDetailsChatbot handleReload={handleReload} />
        <Contact />
        <Footer />
      </div>
    </>
  );
};

export default App;
