import { useState } from "react";
import InputForm from "./components/InputForm";
import ResultDashboard from "./components/ResultDashboard";
import { analyzeStudent } from "./services/api";

function normalizeWeaknessResponse(response) {
  return {
    concept_level: response?.concept_level ?? "Weak",
    concept_confidence: response?.concept_confidence ?? 100,
    burnout_risk: response?.burnout_risk ?? "N/A",
    burnout_confidence: response?.burnout_confidence ?? 0,
    readiness_score: response?.readiness_score ?? 0,
    readiness_band: response?.readiness_band ?? "N/A",
    risk_reasoning: response?.risk_reasoning ?? [],
    recommendations: response?.recommendations ?? {
      study_plan: [],
      focus_area: "Only concept weakness is available from this endpoint.",
      rest_advice: "Use /predict/burnout for burnout-specific guidance.",
    },
  };
}

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async (payload) => {
    setLoading(true);
    setError("");

    try {
      const response = await analyzeStudent(payload);
      setResult(normalizeWeaknessResponse(response));
    } catch (err) {
      setResult(null);
      setError(err.message || "Failed to analyze student");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <main className="mx-auto max-w-6xl px-4 py-10 md:px-8">
        <header className="mb-8 text-center">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-emerald-600">MindLearn AI</p>
          <h1 className="mt-2 text-3xl font-bold text-slate-900 md:text-4xl">Student Intelligence Dashboard</h1>
          <p className="mt-2 text-sm text-slate-600 md:text-base">
            Predict concept strength, burnout risk, and readiness with explainable recommendations.
          </p>
        </header>

        <div className="space-y-6">
          <InputForm onSubmit={handleAnalyze} loading={loading} />

          {error ? (
            <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm font-medium text-rose-700 shadow-sm">
              {error}
            </div>
          ) : null}

          {loading ? (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
                <p className="text-sm text-slate-700">Analyzing student performance...</p>
              </div>
            </div>
          ) : null}

          {!loading && result ? <ResultDashboard result={result} /> : null}
        </div>
      </main>
    </div>
  );
}
