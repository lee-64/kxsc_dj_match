import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { Analytics } from "@vercel/analytics/react"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "DJ Match — KXSC Radio",
  description: "DJ Match app by KXSC Radio",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <div className="min-h-screen bg-gradient-to-br from-neutral-900 via-black to-neutral-900 text-white">
          {/* Logo and Header */}
          <div className="absolute top-0 left-0 right-0 p-4">
            <div className="flex items-center justify-between mr-8">
              <div className="flex items-center gap-4">
                <img
                  src="/kxsc_temp_logo.png"
                  alt="Header logo"
                  className="w-16 h-16 object-contain"
                />
                <Link href="/"
                  className="underline underline-offset-2 font-mono text-3xl tracking-wider italic font-bold bg-gradient-to-r from-purple-400 via-red-400 to-orange-400 bg-clip-text text-transparent cursor-pointer">
                  KXSC DJ MATCH
                </Link>
              </div>
              <Link href="https://kxsc.org"
                className="md:text-xl lg:text-2xl xl:text-2xl underline underline-offset-2 font-mono tracking-wider italic font-bold text-gray-300 cursor-pointer">
                kxsc.org
              </Link>
            </div>
          </div>

          {/* Main Content */}
          <div className="container mx-auto px-4 py-12 pt-32">
            <main>
              {children}
              <Analytics />
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}