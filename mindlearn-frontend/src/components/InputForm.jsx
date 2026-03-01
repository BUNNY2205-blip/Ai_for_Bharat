import { useState } from "react";

const initialForm = {
  accuracy: 60,
  attempts: 10,
  avg_time: 30,
  difficulty: 2,
  repeated_errors: 3,
  accuracy_trend: -8.5,
  time_increase: 12,
  consistency: 0.4,
  study_hours: 7,
};

const fields = [
  { name: "accuracy", label: "Accuracy (%)", type: "number", step: "0.1" },
  { name: "attempts", label: "Attempts", type: "number", step: "1" },
  { name: "avg_time", label: "Avg Time (s)", type: "number", step: "0.1" },
  { name: "repeated_errors", label: "Repeated Errors", type: "number", step: "1" },
  { name: "accuracy_trend", label: "Accuracy Trend", type: "number", step: "0.1" },
  { name: "time_increase", label: "Time Increase", type: "number", step: "0.1" },
  { name: "consistency", label: "Consistency (0-1)", type: "number", step: "0.01" },
  { name: "study_hours", label: "Study Hours", type: "number", step: "0.1" },
];

export default function InputForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState(initialForm);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "difficulty" ? Number(value) : Number(value),
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(formData);
  };

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-900">Student Input</h2>
      <p className="mt-1 text-sm text-slate-500">Fill metrics to generate AI analysis.</p>

      <form className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
        {fields.map((field) => (
          <label key={field.name} className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            {field.label}
            <input
              type={field.type}
              name={field.name}
              step={field.step}
              value={formData[field.name]}
              onChange={handleChange}
              className="rounded-xl border border-slate-300 px-3 py-2 text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
              required
            />
          </label>
        ))}

        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Difficulty
          <select
            name="difficulty"
            value={formData.difficulty}
            onChange={handleChange}
            className="rounded-xl border border-slate-300 px-3 py-2 text-slate-900 outline-none transition focus:border-emerald-500 focus:ring-2 focus:ring-emerald-100"
          >
            <option value={1}>1 - Easy</option>
            <option value={2}>2 - Medium</option>
            <option value={3}>3 - Hard</option>
          </select>
        </label>

        <div className="md:col-span-2 mt-2 flex justify-center md:justify-end">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center rounded-xl bg-emerald-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-emerald-400"
          >
            {loading ? "Analyzing..." : "Analyze Student"}
          </button>
        </div>
      </form>
    </section>
  );
}
