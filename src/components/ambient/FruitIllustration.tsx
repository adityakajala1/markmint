interface FruitIllustrationProps {
  type: "pomegranate" | "orange" | "fig" | "strawberry" | "apple" | "grapes" | "cherry" | "watermelon";
  className?: string;
}

export function FruitIllustration({ type, className = "" }: FruitIllustrationProps) {
  
  const getSvgContent = () => {
    switch(type) {
      case "watermelon":
        return (
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-full h-full">
            {/* Watermelon Slice Arch */}
            <path d="M 10 30 A 50 50 0 0 0 90 30 Z" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M 16 30 A 44 44 0 0 0 84 30 Z" strokeLinecap="round" strokeLinejoin="round" />
            {/* Seeds */}
            <circle cx="35" cy="45" r="1.5" fill="currentColor" />
            <circle cx="50" cy="55" r="1.5" fill="currentColor" />
            <circle cx="65" cy="45" r="1.5" fill="currentColor" />
            <circle cx="42" cy="36" r="1.5" fill="currentColor" />
            <circle cx="58" cy="36" r="1.5" fill="currentColor" />
            {/* Vintage hatching marks */}
            <path d="M 20 40 L 25 45 M 80 40 L 75 45 M 50 70 L 50 75" strokeWidth="0.5" />
          </svg>
        );
      case "pomegranate":
        return (
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-full h-full">
            {/* Pomegranate Body */}
            <circle cx="50" cy="55" r="35" />
            {/* Crown */}
            <path d="M 40 20 L 35 5 L 50 15 L 65 5 L 60 20 Z" strokeLinejoin="round" />
            {/* Cutaway showing seeds */}
            <path d="M 30 45 C 50 25, 75 40, 70 70 C 50 85, 25 70, 30 45 Z" strokeDasharray="2 2" />
            <circle cx="45" cy="50" r="2" fill="currentColor" />
            <circle cx="55" cy="55" r="2" fill="currentColor" />
            <circle cx="48" cy="62" r="2" fill="currentColor" />
            <circle cx="60" cy="48" r="2" fill="currentColor" />
            {/* Engraving lines */}
            <path d="M 20 55 A 30 30 0 0 0 35 80 M 80 55 A 30 30 0 0 1 65 80" strokeWidth="0.5" />
          </svg>
        );
      case "fig":
        return (
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-full h-full">
            {/* Fig Teardrop */}
            <path d="M 50 15 C 65 15, 85 45, 80 75 C 75 95, 25 95, 20 75 C 15 45, 35 15, 50 15 Z" />
            <path d="M 45 5 L 50 15 L 55 5 Z" />
            {/* Inner flesh lines */}
            <path d="M 50 25 L 50 80 M 35 45 L 65 45 M 35 65 L 65 65" strokeWidth="0.5" strokeDasharray="4 4" />
            <circle cx="45" cy="55" r="1" fill="currentColor" />
            <circle cx="55" cy="60" r="1" fill="currentColor" />
          </svg>
        );
      case "orange":
        return (
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-full h-full">
            <circle cx="50" cy="50" r="40" />
            <circle cx="50" cy="50" r="34" />
            {/* Segments */}
            <path d="M 50 16 L 50 84 M 16 50 L 84 50 M 26 26 L 74 74 M 26 74 L 74 26" strokeWidth="1" />
            {/* Seeds */}
            <circle cx="42" cy="42" r="1.5" fill="currentColor" />
            <circle cx="58" cy="58" r="1.5" fill="currentColor" />
          </svg>
        );
      case "grapes":
        return (
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-full h-full">
            <path d="M 40 10 Q 50 0 60 10 L 50 20 Z" />
            <circle cx="50" cy="30" r="10" />
            <circle cx="35" cy="40" r="10" />
            <circle cx="65" cy="40" r="10" />
            <circle cx="42" cy="55" r="10" />
            <circle cx="58" cy="55" r="10" />
            <circle cx="50" cy="70" r="10" />
            {/* Highlights */}
            <path d="M 48 24 A 5 5 0 0 1 54 26" strokeWidth="0.5" />
            <path d="M 40 49 A 5 5 0 0 1 46 51" strokeWidth="0.5" />
          </svg>
        );
      default:
        // Generic leaf as fallback
        return (
          <svg viewBox="0 0 100 100" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-full h-full">
            <path d="M 20 80 C 20 40, 50 10, 80 20 C 80 60, 50 90, 20 80 Z" />
            <path d="M 20 80 L 80 20" />
            <path d="M 40 60 L 55 45 M 50 70 L 65 55 M 30 50 L 45 35" strokeWidth="0.5" />
          </svg>
        );
    }
  };

  return (
    <div className={`text-accent opacity-[0.08] pointer-events-none mix-blend-screen ${className}`}>
      {getSvgContent()}
    </div>
  );
}