"use client";

import { useState } from "react";
import { Loader2, Search, User, ExternalLink, Briefcase } from "lucide-react";

export default function Dashboard() {
  const [jdText, setJdText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const analyzeJob = async () => {
    if (!jdText) return;
    setIsLoading(true);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append("raw_text", jdText);

      const response = await fetch("http://localhost:8000/ingest", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Pipeline failed", error);
      alert("Failed to connect to the backend. Is FastAPI running?");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
          <Search className="text-blue-600" />
          RecruitAI Intelligence
        </h1>
        <p className="text-gray-500">Automated Sourcing & Ranking Pipeline</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* LEFT COLUMN: INPUT */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-semibold mb-4">1. Paste Job Description</h2>
            <textarea
              className="w-full h-64 p-4 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none resize-none text-sm text-gray-700"
              placeholder="e.g., We need a Senior ML Engineer with 4+ years of Python and PyTorch in Bengaluru..."
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
            <button
              onClick={analyzeJob}
              disabled={isLoading || !jdText}
              className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg flex justify-center items-center gap-2 transition disabled:opacity-50"
            >
              {isLoading ? (
                <>
                  <Loader2 className="animate-spin w-5 h-5" /> Processing Pipeline...
                </>
              ) : (
                "Run Sourcing Pipeline"
              )}
            </button>
          </div>

          {/* PARSED DATA WIDGET */}
          {results?.parsed_jd && (
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h2 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4 flex items-center gap-2">
                <Briefcase size={16} /> Extracted Parameters
              </h2>
              <div className="space-y-3 text-sm">
                <p><strong>Role:</strong> {results.parsed_jd.title}</p>
                <p><strong>Location:</strong> {results.parsed_jd.location}</p>
                <p><strong>Experience:</strong> {results.parsed_jd.min_years_experience}+ years</p>
                <div>
                  <strong>Top Skills:</strong>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {results.parsed_jd.required_skills.map((skill: string, i: number) => (
                      <span key={i} className="bg-blue-50 text-blue-700 px-2 py-1 rounded-md text-xs font-semibold">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: RANKED CANDIDATES */}
        <div className="lg:col-span-2">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 min-h-[500px]">
            <h2 className="text-xl font-semibold mb-6 border-b pb-4">
              2. AI-Ranked Candidates
            </h2>
            
            {!results && !isLoading && (
              <div className="text-center text-gray-400 mt-20">
                <User className="w-16 h-16 mx-auto mb-4 opacity-20" />
                <p>Paste a job description to initiate the sourcing sequence.</p>
              </div>
            )}

            <div className="space-y-4">
              {results?.ranked_candidates?.map((candidate: any, index: number) => (
                <div key={index} className="p-4 border rounded-lg hover:border-blue-300 transition group flex flex-col sm:flex-row justify-between gap-4">
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg">
                      {candidate.title || "Unknown Candidate"}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                      {candidate.snippet}
                    </p>
                    <a 
                      href={candidate.profile_url} 
                      target="_blank" 
                      className="text-blue-600 text-sm font-medium mt-3 inline-flex items-center gap-1 opacity-0 group-hover:opacity-100 transition"
                    >
                      View Profile <ExternalLink size={14} />
                    </a>
                  </div>
                  
                  {/* Score Badge */}
                  <div className="flex-shrink-0 flex items-start">
                    <div className={`px-3 py-2 rounded-lg text-center ${
                      candidate.match_score > 70 ? 'bg-green-50 text-green-700' : 'bg-yellow-50 text-yellow-700'
                    }`}>
                      <span className="block text-2xl font-bold">{candidate.match_score.toFixed(0)}%</span>
                      <span className="text-xs uppercase font-semibold">Match</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}