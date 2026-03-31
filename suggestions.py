def generate_suggestions(missing_skills, experience, job_match=None):
    suggestions = []

    # 1. Missing Skill Suggestions
    if missing_skills:
        suggestions.append(f"Consider learning or adding these missing skills: {', '.join(missing_skills[:5])}.")

    # 2. Experience Level Suggestions
    if experience < 2:
        suggestions.append("Highlight academic projects, bootcamps, and internships to compensate for lower total years of experience.")
    elif experience >= 5:
        suggestions.append("Quantify your achievements (e.g. 'Improved efficiency by 20%') since you have mid-to-senior level experience.")

    # 3. Job Match Specific Suggestions
    if job_match:
        suggestions.append(f"Your profile strongly aligns with {job_match['job_title']} in {job_match['category']}. Tailor your summary to highlight this domain.")

    # 4. Action Verbs Rule
    suggestions.append("Ensure every bullet point starts with a strong action verb like Designed, Engineered, Overheaded, Directed, Negotiated.")

    return suggestions