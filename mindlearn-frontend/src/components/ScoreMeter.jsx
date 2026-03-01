import { useEffect, useMemo, useState } from "react";

function getBandColor(band) {
  if (band === "Excellent") return "text-emerald-600";
  if (band === "Good") return "text-lime-600";
  if (band === "Moderate") return "text-amber-500";
  return "text-rose-600";
}

export default function ScoreMeter({ score = 0, band = "Moderate" }) {
  const size = 150;
  const stroke = 12;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const boundedScore = Math.max(0, Math.min(100, Number(score) || 0));

  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const start = performance.now();
    const duration = 900;

    const step = (time) => {
      const progress = Math.min((time - start) / duration, 1);
      setAnimatedScore(Number((boundedScore * progress).toFixed(1)));
      if (progress < 1) {
        requestAnimationFrame(step);
      }
    };

    requestAnimationFrame(step);
  }, [boundedScore]);

  const offset = useMemo(() => {
    return circumference - (animatedScore / 100) * circumference;
  }, [animatedScore, circumference]);

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={stroke}
            className="fill-none stroke-slate-200"
          />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            strokeWidth={stroke}
            strokeLinecap="round"
            className="fill-none stroke-emerald-500 transition-all duration-500"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
          />
        </svg>

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <p className="text-3xl font-bold text-slate-900">{Math.round(animatedScore)}%</p>
          <p className={`text-sm font-semibold ${getBandColor(band)}`}>{band}</p>
        </div>
      </div>
    </div>
  );
}
