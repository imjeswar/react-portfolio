import React from "react";

const Navbar = () => (
  <nav className="sticky top-0 bg-black/90 backdrop-blur-md py-4 z-50 shadow-lg">
    <ul className="flex justify-center gap-6 md:gap-10">
      {[
        ["About", "#about"],
        ["Education", "#education"],
        ["My Journey", "#journey"],
        ["Skills", "#skills"],
        ["Projects", "#projects"],
        ["Contact", "#contact"],
      ].map(([label, href]) => (
        <li key={href}>
          <a
            href={href}
            className="relative px-4 py-2 font-semibold text-amber-200 transition group"
          >
            {label}
            <span className="absolute left-0 bottom-0 w-0 h-0.5 bg-amber-300 transition-all group-hover:w-full" />
          </a>
        </li>
      ))}
    </ul>
  </nav>
);

export default Navbar;
