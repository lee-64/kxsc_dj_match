import React from "react";

export default function Hero({ header, description, fullWidth = false }) {
    return (
        <div className="text-center mb-8 relative">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 via-red-500/10 to-orange-500/10 blur-3xl -z-10"/>
            <div
                className={`backdrop-blur-sm bg-white/5 border border-white/10 rounded-2xl p-8 shadow-2xl ${
                    fullWidth ? '' : 'max-w-2xl mx-auto'
                }`}>
                <h2 className="text-4xl sm:text-5xl md:text-6xl lg:text-6xl xl:text-7xl font-bold mb-4 font-mono tracking-tight break-words">
                    {header}
                </h2>
                <span className="text-sm sm:text-md md:text-lg lg:text-lg xl:text-xl font-mono text-gray-300 mb-12 max-w-2xl mx-auto leading-relaxed">
                    {description}
                </span>
            </div>
        </div>
    );
}