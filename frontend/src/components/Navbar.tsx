"use client";

import { useState } from "react";
import Link from "next/link";
import ThemeToggle from "./ThemeToggle";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const navLinks = [
    { href: "/", label: "Home" },
    { href: "/register", label: "Register" },
    { href: "/login", label: "Login" },
  ];

  return (
    <nav className="border-b border-white/10 bg-black/50 backdrop-blur dark:border-white/10 dark:bg-black/50">
      <div className="mx-auto max-w-7xl px-6">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <span className="font-mono text-sm uppercase tracking-[0.3em] text-mint">
              Stellar Pay
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden items-center gap-8 md:flex">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-sm text-slate-300 transition-colors hover:text-white dark:text-slate-300 dark:hover:text-white"
              >
                {link.label}
              </Link>
            ))}
            <ThemeToggle />
          </div>

          {/* Mobile Menu Button and Theme Toggle */}
          <div className="flex items-center gap-3 md:hidden">
            <ThemeToggle />
            <button
              onClick={toggleMenu}
              className="flex flex-col gap-1.5"
              aria-label="Toggle menu"
            >
              <span
                className={`block h-0.5 w-6 bg-white transition-all ${
                  isMenuOpen ? "translate-y-2 rotate-45" : ""
                }`}
              ></span>
              <span
                className={`block h-0.5 w-6 bg-white transition-all ${
                  isMenuOpen ? "opacity-0" : ""
                }`}
              ></span>
              <span
                className={`block h-0.5 w-6 bg-white transition-all ${
                  isMenuOpen ? "-translate-y-2 -rotate-45" : ""
                }`}
              ></span>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="border-t border-white/10 py-4 md:hidden">
            <div className="flex flex-col gap-4">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setIsMenuOpen(false)}
                  className="text-sm text-slate-300 transition-colors hover:text-white dark:text-slate-300 dark:hover:text-white"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
