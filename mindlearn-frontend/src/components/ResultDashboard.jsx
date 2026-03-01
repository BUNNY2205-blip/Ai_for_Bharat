import { useEffect, useState } from "react";
import ScoreMeter from "./ScoreMeter";

function badgeClass(type, value) {
  if (type === "concept") {
    if (value === "Strong") return "bg-emerald-100 text-emerald-700";
    if (value === "Moderate") return "bg-amber-100 text-amber-700";
    return "bg-rose-100 text-rose-700";
  }

  if (value === "Low") return "bg-emerald-100 text-emerald-700";
  if (value === "Medium") return "bg-amber-100 text-amber-700";
  return "bg-rose-100 text-rose-700";
}

function Card({ title, children }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="text-base font-semibold text-slate-900">{title}</h3>
      <div className="mt-4">{children}</div>
    </div>
  );
}

export default function ResultDashboard({ result }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(false);
    const id = setTimeout(() => setVisible(true), 60);
    return () => clearTimeout(id);
  }, [result]);

  if (!result) return null;

  return (
    <section
      className={`transition-all duration-500 ${
        visible ? "translate-y-0 opacity-100" : "translate-y-3 opacity-0"
      }`}
    >
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card title="Concept Analysis">
          <div className="flex items-center justify-between gap-3">
            <span className={`rounded-full px-3 py-1 text-sm font-semibold ${badgeClass("concept", result.concept_level)}`}>
              {result.concept_level}
            </span>
            <p className="text-sm text-slate-600">Confidence: <span className="font-semibold text-slate-900">{result.concept_confidence}%</span></p>
          </div>
        </Card>

        <Card title="Burnout Analysis">
          <div className="flex items-center justify-between gap-3">
            <span className={`rounded-full px-3 py-1 text-sm font-semibold ${badgeClass("burnout", result.burnout_risk)}`}>
              {result.burnout_risk}
            </span>
            <p className="text-sm text-slate-600">Confidence: <span className="font-semibold text-slate-900">{result.burnout_confidence}%</span></p>
          </div>
        </Card>

        <Card title="Readiness Score">
          <div className="flex justify-center">
            <ScoreMeter score={result.readiness_score} band={result.readiness_band} />
          </div>
        </Card>
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card title="Risk Reasoning">
          {result.risk_reasoning?.length ? (
            <ul className="list-disc space-y-2 pl-5 text-sm text-slate-700">
              {result.risk_reasoning.map((reason, index) => (
                <li key={`${reason}-${index}`}>{reason}</li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-slate-600">No major risk signals detected.</p>
          )}
        </Card>

        <Card title="Recommendations">
          <div className="space-y-3">
            <div className="rounded-xl bg-slate-50 p-3">
              <p className="text-sm font-semibold text-slate-900">Study Plan</p>
              <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-700">
                {(result.recommendations?.study_plan || []).map((item, index) => (
                  <li key={`${item}-${index}`}>{item}</li>
                ))}
              </ul>
            </div>

            <div className="rounded-xl bg-slate-50 p-3">
              <p className="text-sm font-semibold text-slate-900">Focus Areas</p>
              <p className="mt-1 text-sm text-slate-700">{result.recommendations?.focus_area}</p>
            </div>

            <div className="rounded-xl bg-slate-50 p-3">
              <p className="text-sm font-semibold text-slate-900">Rest Advice</p>
              <p className="mt-1 text-sm text-slate-700">{result.recommendations?.rest_advice}</p>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
}
