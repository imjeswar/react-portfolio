import React, { useState, useEffect, useRef } from "react";

const SOURCE_LABELS = {
  "about_me": "About Me", "about": "About Me",
  "projects": "Projects",
  "certifications": "Certifications",
  "skills": "Skills",
  "education": "Education",
  "experience": "Experience",
  "contact": "Contact",
};

const getSourceLabel = (source = "") => {
  const key = Object.keys(SOURCE_LABELS).find((k) => source.toLowerCase().includes(k));
  return key ? SOURCE_LABELS[key] : source.replace(".md", "").replace(/_/g, " ");
};

const SUGGESTED = [
  "Tell me about yourself",
  "What projects have you built?",
  "Explain the AI Resume Analyzer",
  "What certifications do you have?",
  "How can I contact Jeswar?",
];

const CONTACT_PATTERNS = [
  { test: /linkedin\.com/i,        label: "LinkedIn",  url: "https://www.linkedin.com/in/jeswar-am/" },
  { test: /github\.com\/imjeswar/i, label: "GitHub",   url: "https://github.com/imjeswar" },
  { test: /wa\.me|whatsapp/i,      label: "WhatsApp", url: "https://wa.me/917904181537" },
  { test: /imjeswar@gmail|mailto/i, label: "Email",    url: "mailto:imjeswar@gmail.com" },
];

const extractContactLinks = (content = "", sources = []) => {
  const hay = content + " " + sources.map((s) => JSON.stringify(s)).join(" ");
  return CONTACT_PATTERNS.filter(({ test }) => test.test(hay));
};

const renderMarkdown = (text = "") => {
  if (!text) return "";
  let html = text
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/\*\*(.*?)\*\*/g, "<strong class='text-amber-200'>$1</strong>")
    .replace(/`(.*?)`/g, "<code class='bg-amber-400/10 px-1 rounded text-amber-300 text-[10px] font-mono'>$1</code>")
    .replace(/\[(.*?)\]\((.*?)\)/g, "<a href='$2' target='_blank' rel='noopener noreferrer' class='text-amber-400 underline underline-offset-2 hover:text-amber-300 transition-colors'>$1</a>")
    .replace(/^---$/gm, "<div class='border-t border-white/8 my-2.5'></div>");

  const lines = html.split("\n");
  let inList = false;
  const processed = lines.map((line) => {
    const t = line.trim();
    if (t.startsWith("- ") || t.startsWith("* ")) {
      const item = t.substring(2);
      const pre = inList ? "" : (inList = true, "<ul class='space-y-1 pl-3 my-1.5 border-l-2 border-amber-400/20'>");
      return pre + `<li class='text-[11px] leading-relaxed'>${item}</li>`;
    }
    if (inList) { inList = false; return "</ul>" + line; }
    return line;
  });
  let out = processed.join("\n");
  if (inList) out += "</ul>";
  return <span dangerouslySetInnerHTML={{ __html: out }} />;
};

export default function ChatbotWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const endRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (open) {
      endRef.current?.scrollIntoView({ behavior: "smooth" });
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [messages, open]);

  const executeAction = (action) => {
    if (typeof action !== "string") return;
    if (action.startsWith("scroll:")) {
      document.getElementById(action.split(":")[1])?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const send = async (text) => {
    text = (text || input).trim();
    if (!text || busy) return;
    setInput("");

    setMessages((p) => [...p, { role: "user", content: text }]);
    setBusy(true);

    const history = messages
      .filter((m) => m.content && !m.content.startsWith("⚠️") && !m.isStreaming)
      .map(({ role, content }) => ({ role, content }));

    const id = Date.now();
    setMessages((p) => [...p, { id, role: "assistant", content: "", sources: [], isStreaming: true }]);

    try {
      const res = await fetch("https://react-portfolio-1-r0cj.onrender.com/api/portfolio/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text, history }),
      });
      if (!res.ok) throw new Error();

      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "", sources = [];

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        for (const line of dec.decode(value, { stream: true }).split("\n")) {
          if (!line.trim().startsWith("data: ")) continue;
          try {
            const p = JSON.parse(line.trim().slice(6));
            if (p.sources) sources = p.sources;
            if (p.actions) p.actions.forEach(executeAction);
            if (p.text) {
              buf += p.text;
              setMessages((prev) => prev.map((m) => m.id === id ? { ...m, content: buf, sources } : m));
            }
          } catch { /* partial */ }
        }
      }
      setMessages((p) => p.map((m) => m.id === id ? { ...m, isStreaming: false } : m));
    } catch {
      setMessages((p) => p.map((m) =>
        m.id === id ? { ...m, content: "⚠️ Backend unreachable. Make sure the server is running on port 8000.", isStreaming: false } : m
      ));
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      {/* ── Floating Button ── */}
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label="Portfolio AI"
        style={{ position: "fixed", bottom: "1.75rem", right: "1.75rem", zIndex: 9999 }}
        className="group relative w-12 h-12 rounded-2xl bg-[#0e0e10] border border-amber-400/30 hover:border-amber-400/60 shadow-[0_8px_32px_rgba(0,0,0,0.6),0_0_0_1px_rgba(251,191,36,0.06)] hover:shadow-[0_8px_40px_rgba(251,191,36,0.18)] flex items-center justify-center transition-all duration-300 cursor-pointer"
      >
        <span className={`text-amber-400 text-lg transition-all duration-300 ${open ? "rotate-45 scale-90" : "group-hover:scale-110"}`}>
          {open ? "✕" : "◈"}
        </span>
        {!open && (
          <span className="absolute top-0.5 right-0.5 w-2 h-2 bg-emerald-400 rounded-full border border-black/60" />
        )}
      </button>

      {/* ── Chat Window ── */}
      <div
        style={{
          position: "fixed",
          bottom: "5.25rem",
          right: "1.75rem",
          zIndex: 9998,
          width: "346px",
          maxWidth: "calc(100vw - 2rem)",
          height: "480px",
          maxHeight: "calc(100vh - 8rem)",
          pointerEvents: open ? "all" : "none",
          transform: open ? "translateY(0) scale(1)" : "translateY(12px) scale(0.96)",
          opacity: open ? 1 : 0,
          transformOrigin: "bottom right",
          transition: "transform 0.22s cubic-bezier(0.34,1.4,0.64,1), opacity 0.18s ease",
        }}
        className="flex flex-col bg-[#0b0b0d] rounded-2xl overflow-hidden border border-white/7 shadow-[0_40px_100px_rgba(0,0,0,0.9),0_0_0_1px_rgba(255,255,255,0.03)]"
      >

        {/* ── Header ── */}
        <div className="flex items-center justify-between px-4 py-3 shrink-0 bg-gradient-to-b from-white/4 to-transparent border-b border-white/5">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-xl bg-gradient-to-br from-amber-400/20 to-amber-600/10 border border-amber-400/20 flex items-center justify-center">
              <span className="text-amber-400 text-[11px]">◈</span>
            </div>
            <div>
              <p className="text-[12px] font-semibold text-white/90 leading-none tracking-wide">Portfolio AI</p>
              <div className="flex items-center gap-1 mt-0.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
                <span className="text-[9px] text-white/30 font-medium">Online</span>
              </div>
            </div>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="w-6 h-6 rounded-lg flex items-center justify-center text-white/25 hover:text-white/70 hover:bg-white/6 transition cursor-pointer text-xs"
          >
            ✕
          </button>
        </div>

        {/* ── Messages ── */}
        <div className="flex-1 overflow-y-auto px-3 py-3 space-y-4 scrollbar-none">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col justify-between py-2">
              {/* Welcome */}
              <div className="space-y-2 text-center px-2">
                <div className="w-10 h-10 mx-auto rounded-2xl bg-gradient-to-br from-amber-400/15 to-amber-600/5 border border-amber-400/15 flex items-center justify-center text-xl">
                  ◈
                </div>
                <p className="text-[11px] text-white/40 leading-relaxed">
                  Ask me anything about <span className="text-amber-400/70 font-medium">Jeswar's</span> portfolio — projects, skills, certifications, and more.
                </p>
              </div>

              {/* Suggested Questions */}
              <div className="space-y-1.5">
                <p className="text-[9px] uppercase tracking-[0.15em] text-white/20 font-semibold px-0.5">Suggested</p>
                {SUGGESTED.map((q) => (
                  <button
                    key={q}
                    onClick={() => send(q)}
                    className="w-full text-left px-3 py-2 rounded-xl bg-white/3 hover:bg-white/5 border border-white/5 hover:border-amber-400/15 text-[11px] text-white/45 hover:text-white/75 transition-all cursor-pointer flex items-center justify-between group"
                  >
                    <span>{q}</span>
                    <span className="text-white/15 group-hover:text-amber-400/50 transition-colors text-[10px]">↵</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"} gap-2`}>

                {/* Assistant icon */}
                {msg.role === "assistant" && (
                  <div className="shrink-0 w-5 h-5 mt-0.5 rounded-lg bg-amber-400/10 border border-amber-400/15 flex items-center justify-center text-[8px] text-amber-400/70">
                    ◈
                  </div>
                )}

                <div className={`max-w-[82%] flex flex-col gap-1.5 ${msg.role === "user" ? "items-end" : "items-start"}`}>

                  {/* Bubble */}
                  <div className={`rounded-2xl text-[11px] leading-relaxed px-3 py-2 ${
                    msg.role === "user"
                      ? "bg-amber-400 text-black font-semibold rounded-tr-sm"
                      : "bg-white/5 border border-white/7 text-white/70 rounded-tl-sm"
                  }`}>
                    {msg.content ? (
                      msg.role === "assistant" ? renderMarkdown(msg.content) : msg.content
                    ) : (
                      <span className="flex items-center gap-1 px-1 py-0.5">
                        {[0, 120, 240].map((d) => (
                          <span key={d} className="w-1 h-1 bg-amber-400/50 rounded-full animate-bounce" style={{ animationDelay: `${d}ms` }} />
                        ))}
                      </span>
                    )}
                  </div>

                  {/* Contact action links */}
                  {msg.role === "assistant" && !msg.isStreaming && msg.content && (() => {
                    const links = extractContactLinks(msg.content, msg.sources);
                    return links.length > 0 ? (
                      <div className="flex flex-wrap gap-1">
                        {links.map(({ label, url }) => (
                          <a
                            key={label}
                            href={url}
                            target={url.startsWith("mailto") ? "_self" : "_blank"}
                            rel="noopener noreferrer"
                            className="px-2.5 py-1 text-[9px] font-semibold tracking-wide rounded-full bg-amber-400/8 hover:bg-amber-400/15 border border-amber-400/20 hover:border-amber-400/40 text-amber-300 hover:text-amber-200 transition-all cursor-pointer"
                          >
                            {label} ↗
                          </a>
                        ))}
                      </div>
                    ) : null;
                  })()}

                  {/* Source chips */}
                  {msg.role === "assistant" && !msg.isStreaming && msg.sources?.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {msg.sources.map((s, si) => {
                        const label = getSourceLabel(s.filename || s.source || "");
                        const href = s.url || s.github;
                        return (
                          <a
                            key={si}
                            href={href || undefined}
                            target={href ? "_blank" : undefined}
                            rel={href ? "noopener noreferrer" : undefined}
                            className={`text-[8px] px-1.5 py-0.5 rounded bg-white/3 border border-white/7 text-white/25 font-mono transition-all ${href ? "hover:text-amber-400/60 hover:border-amber-400/20 cursor-pointer" : "cursor-default"}`}
                          >
                            {label}{href ? " ↗" : ""}
                          </a>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          <div ref={endRef} />
        </div>

        {/* ── Quick chips ── */}
        <div className="px-3 pt-1 pb-0 flex gap-1.5 overflow-x-auto scrollbar-none shrink-0">
          {[
            ["Projects", "What projects have you built?"],
            ["Skills", "What are your skills?"],
            ["Contact", "How can I contact Jeswar?"],
            ["Certs", "What certifications do you have?"],
          ].map(([label, q]) => (
            <button
              key={label}
              onClick={() => send(q)}
              className="shrink-0 px-2.5 py-1 text-[9px] font-bold uppercase tracking-wider rounded-full bg-white/3 hover:bg-white/5 border border-white/6 hover:border-white/10 text-white/30 hover:text-white/55 transition cursor-pointer"
            >
              {label}
            </button>
          ))}
        </div>

        {/* ── Input ── */}
        <div className="p-3 shrink-0">
          <div className={`flex items-center gap-2 rounded-xl border px-3 py-2 transition-all duration-200 ${
            busy ? "bg-white/2 border-white/5" : "bg-white/4 border-white/8 focus-within:border-amber-400/35 focus-within:bg-amber-400/3 focus-within:shadow-[0_0_0_3px_rgba(251,191,36,0.06)]"
          }`}>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send()}
              placeholder="Ask anything about Jeswar…"
              disabled={busy}
              className="flex-1 bg-transparent text-[11px] text-white/70 placeholder-white/18 outline-none min-w-0"
            />
            <button
              onClick={() => send()}
              disabled={!input.trim() || busy}
              className="shrink-0 w-6 h-6 rounded-lg flex items-center justify-center bg-amber-400 disabled:bg-white/6 text-black disabled:text-white/20 text-xs font-bold transition-all hover:bg-amber-300 active:scale-90 cursor-pointer disabled:cursor-not-allowed"
            >
              ↑
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
