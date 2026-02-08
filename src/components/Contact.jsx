import React, { useState } from "react";

const Contact = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus(null);

    try {
      await fetch(
        "https://script.google.com/macros/s/AKfycbzlKNtiFj-noyFY-ZF5NdBDvIH9ielnPF5KrXWkhadHUyYlyeUZVyJZxhPvpCcR7d8b5Q/exec",
        {
          method: "POST",
          mode: "no-cors",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: formData.name,
            email: formData.email,
            subject: formData.subject,
            message: formData.message,
          }),
        }
      );

      // With no-cors, we can't read the response, so we assume success if no error is thrown
      setStatus("success");
      setFormData({
        name: "",
        email: "",
        subject: "",
        message: "",
      });
    } catch (err) {
      console.error(err);
      setStatus("error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="contact" className="py-16 w-full flex flex-col items-center">
      <h2 className="text-3xl font-bold mb-12 text-amber-100 border-b-2 border-amber-300/70 pb-2 inline-block">
        Let&apos;s Start a Conversation
      </h2>

      <div className="w-full md:w-3/4 lg:w-2/3 premium-glass animate-glow p-8 md:p-12 rounded-3xl shadow-xl">
        <form className="space-y-4" onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Your Name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full p-3 rounded bg-black text-white border border-amber-400/40"
          />

          <input
            type="email"
            name="email"
            placeholder="Your Email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full p-3 rounded bg-black text-white border border-amber-400/40"
          />

          <input
            type="text"
            name="subject"
            placeholder="Subject"
            value={formData.subject}
            onChange={handleChange}
            required
            className="w-full p-3 rounded bg-black text-white border border-amber-400/40"
          />

          <textarea
            name="message"
            placeholder="Message"
            rows={5}
            value={formData.message}
            onChange={handleChange}
            required
            className="w-full p-3 rounded bg-black text-white border border-amber-400/40"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 premium-glass animate-glow text-amber-200 font-bold rounded-xl hover:text-white transition-all duration-300 disabled:opacity-60"
          >
            {loading ? "Sending..." : "Send Message"}
          </button>
        </form>

        {status === "success" && (
          <p className="mt-4 text-green-400 text-sm">
            ✅ Message sent successfully!
          </p>
        )}

        {status === "error" && (
          <p className="mt-4 text-red-400 text-sm">
            ❌ Something went wrong. Try again.
          </p>
        )}
      </div>

      {/* Contact Icons */}
      <div className="flex justify-center gap-6 mt-8">
        <a href="https://wa.me/917904181537" target="_blank" rel="noreferrer">
          <img
            src="https://cdn-icons-png.flaticon.com/512/733/733585.png"
            className="w-10 h-10 hover:scale-110 transition"
            alt="WhatsApp"
          />
        </a>
        <a
          href="https://instagram.com/imjeswar"
          target="_blank"
          rel="noreferrer"
        >
          <img
            src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png"
            className="w-10 h-10 hover:scale-110 transition"
            alt="Instagram"
          />
        </a>
        <a href="https://github.com/imjeswar" target="_blank" rel="noreferrer">
          <img
            src="https://cdn-icons-png.flaticon.com/512/733/733553.png"
            className="w-10 h-10 hover:scale-110 transition"
            alt="GitHub"
          />
        </a>
        <a
          href="https://linkedin.com/in/imjeswar"
          target="_blank"
          rel="noreferrer"
        >
          <img
            src="https://cdn-icons-png.flaticon.com/512/733/733561.png"
            className="w-10 h-10 hover:scale-110 transition"
            alt="LinkedIn"
          />
        </a>
        <a href="mailto:imjeswar@gmail.com">
          <img
            src="https://cdn-icons-png.flaticon.com/512/732/732200.png"
            className="w-10 h-10 hover:scale-110 transition"
            alt="Email"
          />
        </a>
      </div>
    </section>
  );
};

export default Contact;
