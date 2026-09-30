from sentence_transformers import SentenceTransformer, util
from typing import List, Dict

# Load the lightweight ML model into memory (it will download a ~90MB model on the first run)
model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_candidates(jd_requirements: dict, candidates: List[Dict[str, str]]) -> List[Dict]:
    """
    Scores and ranks candidates based on semantic similarity to the JD.
    """
    if not candidates:
        return []

    # 1. Create a dense summary of what we are looking for based on parsed AI data
    jd_summary = f"Job Title: {jd_requirements['title']}. Required Skills: {', '.join(jd_requirements['required_skills'])}. Experience: {jd_requirements['min_years_experience']} years."
    
    # 2. Create text blocks for each candidate using what we scraped
    candidate_texts = [f"{c.get('title', '')} {c.get('snippet', '')}" for c in candidates]
    
    # 3. Convert text to mathematical vectors (Embeddings)
    jd_embedding = model.encode(jd_summary, convert_to_tensor=True)
    candidate_embeddings = model.encode(candidate_texts, convert_to_tensor=True)
    
    # 4. Compute Cosine Similarity (How close are the vectors in multi-dimensional space?)
    cosine_scores = util.cos_sim(jd_embedding, candidate_embeddings)[0]
    
    # 5. Attach scores to candidate dictionaries
    for i, candidate in enumerate(candidates):
        # Convert tensor to standard float, multiply by 100 for a readable percentage score
        candidate['match_score'] = round(float(cosine_scores[i]) * 100, 2)
        
    # 6. Sort candidates highest to lowest score
    ranked_candidates = sorted(candidates, key=lambda x: x['match_score'], reverse=True)
    
    return ranked_candidates