import React from "react";

const Background = () => {
  return (
    <div className="fixed inset-0 -z-10 pointer-events-none">
      <div className="absolute inset-0 bg-gradient-to-r from-black via-gray-900 to-black animate-gradient" />

      <style>{`
        @keyframes gradientFlow {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .animate-gradient {
          background-size: 400% 400%;
          animation: gradientFlow 12s ease infinite;
        }
      `}</style>
    </div>
  );
};

export default Background;
