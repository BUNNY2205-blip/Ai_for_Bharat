const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://44.200.74.235:8000").replace(/\/$/, "");

console.log("API_BASE_URL:", API_BASE_URL);
console.log("VITE_API_BASE_URL env:", import.meta.env.VITE_API_BASE_URL);

/**
 * Call concept weakness endpoint.
 * @param {Object} payload
 * @returns {Promise<Object>}
 */
export async function analyzeStudent(payload) {
  const url = `${API_BASE_URL}/api/v1/predict/analysis`;
  console.log("Fetching from:", url);
  
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let detail = "Request failed";

    try {
      const data = await response.json();
      if (typeof data?.detail === "string") {
        detail = data.detail;
      } else if (Array.isArray(data?.detail)) {
        detail = data.detail.map((item) => item?.msg || "Invalid input").join(", ");
      }
    } catch {
      detail = `Request failed with status ${response.status}`;
    }

    throw new Error(detail);
  }

  return response.json();
}
