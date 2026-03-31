import json
import os
import random

def generate_job_data():
    domains = {
        "Technology": {
            "sub_categories": ["Software Engineering", "Data Science", "Cloud Computing", "Cybersecurity", "IT Support"],
            "base_skills": ["Python", "Java", "SQL", "Git", "Problem Solving", "Communication", "Agile"],
            "base_tools": ["Jira", "VS Code", "Slack"],
            "roles": [
                ("Software Developer", ["JavaScript", "React", "Node.js", "API Design", "Docker", "Algorithms"]),
                ("Data Scientist", ["Machine Learning", "Statistics", "Pandas", "TensorFlow", "Data Visualization", "R"]),
                ("Cloud Architect", ["AWS", "Azure", "Kubernetes", "Terraform", "Linux", "Networking"]),
                ("Frontend Engineer", ["HTML", "CSS", "React", "Vue", "Typescript", "UI/UX", "Webpack"]),
                ("Backend Engineer", ["Python", "Django", "FastAPI", "PostgreSQL", "Redis", "Microservices"]),
                ("Cybersecurity Analyst", ["SIEM", "Penetration Testing", "Network Security", "Linux", "Firewalls", "Incident Response"]),
                ("DevOps Engineer", ["CI/CD", "Jenkins", "Ansible", "Docker", "Kubernetes", "AWS", "Bash"]),
                ("IT Support Specialist", ["Windows Server", "Active Directory", "Troubleshooting", "Hardware", "Networking", "Customer Service"]),
            ]
        },
        "Healthcare": {
            "sub_categories": ["Nursing", "Medicine", "Administration", "Therapy"],
            "base_skills": ["Patient Care", "Empathy", "Communication", "Critical Thinking", "Medical Knowledge"],
            "base_tools": ["EHR Software", "Medical Equipment"],
            "roles": [
                ("Registered Nurse", ["Vitals Monitoring", "Medication Administration", "CPR", "Patient Assessment"]),
                ("Medical Assistant", ["Phlebotomy", "Scheduling", "Triage", "EMR"]),
                ("Physician", ["Diagnosis", "Treatment Planning", "Surgery", "Pharmacology", "Anatomy"]),
                ("Healthcare Administrator", ["Budgeting", "Compliance", "Operations Management", "Medical Billing"]),
                ("Physical Therapist", ["Rehabilitation", "Kinesiology", "Exercise Prescription", "Injury Prevention"])
            ]
        },
        "Finance": {
            "sub_categories": ["Accounting", "Investment Banking", "Financial Planning"],
            "base_skills": ["Analytical Skills", "Attention to Detail", "Communication", "Microsoft Excel", "Mathematics"],
            "base_tools": ["Bloomberg Terminal", "Excel", "SAP"],
            "roles": [
                ("Accountant", ["Financial Reporting", "Taxation", "Auditing", "QuickBooks", "GAAP"]),
                ("Financial Analyst", ["Financial Modeling", "Forecasting", "Valuation", "Corporate Finance", "Data Analysis"]),
                ("Investment Banker", ["M&A", "Capital Markets", "Pitch Books", "Due Diligence"]),
                ("Financial Advisor", ["Wealth Management", "Retirement Planning", "Portfolio Management", "Sales"])
            ]
        },
        "Business & Management": {
            "sub_categories": ["Operations", "Project Management", "Consulting"],
            "base_skills": ["Leadership", "Communication", "Problem Solving", "Strategic Planning", "Time Management"],
            "base_tools": ["Microsoft Office", "Trello", "Asana"],
            "roles": [
                ("Project Manager", ["Agile", "Scrum", "Risk Management", "Budgeting", "Stakeholder Management"]),
                ("Business Analyst", ["Requirements Gathering", "Process Modeling", "Data Analysis", "SQL", "Tableau"]),
                ("Operations Manager", ["Supply Chain", "Logistics", "Process Improvement", "Six Sigma", "Vendor Management"]),
                ("Management Consultant", ["Strategy", "Change Management", "Financial Analysis", "Client Relations"])
            ]
        },
        "Sales & Marketing": {
            "sub_categories": ["Digital Marketing", "B2B Sales", "Content Creation"],
            "base_skills": ["Communication", "Negotiation", "Creativity", "Data Analysis", "Customer Relationship Management"],
            "base_tools": ["Salesforce", "HubSpot", "Google Analytics"],
            "roles": [
                ("Marketing Manager", ["SEO", "SEM", "Content Strategy", "Email Marketing", "Social Media", "Campaign Management"]),
                ("Sales Executive", ["Lead Generation", "Closing", "B2B", "Account Management", "Cold Calling"]),
                ("Content Writer", ["Copywriting", "SEO", "Editing", "Blogging", "Research"]),
                ("SEO Specialist", ["Keyword Research", "On-Page SEO", "Off-Page SEO", "Google Search Console", "Link Building"])
            ]
        },
        "Engineering": {
            "sub_categories": ["Mechanical", "Civil", "Electrical"],
            "base_skills": ["Mathematics", "Physics", "Problem Solving", "AutoCAD", "Project Management"],
            "base_tools": ["AutoCAD", "SolidWorks", "MATLAB"],
            "roles": [
                ("Mechanical Engineer", ["Thermodynamics", "CAD/CAM", "Manufacturing Processes", "Material Science", "Finite Element Analysis"]),
                ("Civil Engineer", ["Structural Design", "Construction Management", "Surveying", "Geotechnical Engineering"], ),
                ("Electrical Engineer", ["Circuit Design", "Power Systems", "PLC", "Control Systems", "Electronics"])
            ]
        },
        "Design & Arts": {
            "sub_categories": ["UX/UI Design", "Graphic Design", "Animation"],
            "base_skills": ["Creativity", "Visual Communication", "Attention to Detail", "Typography", "Color Theory"],
            "base_tools": ["Figma", "Adobe Creative Suite"],
            "roles": [
                ("UX/UI Designer", ["Wireframing", "Prototyping", "User Research", "Usability Testing", "Interaction Design"]),
                ("Graphic Designer", ["Illustration", "Branding", "Layout Design", "Photoshop", "Illustrator"]),
                ("3D Animator", ["Maya", "Blender", "Character Animation", "Rigging", "Rendering"])
            ]
        },
        "Human Resources": {
            "sub_categories": ["Talent Acquisition", "HR Operations", "Training"],
            "base_skills": ["Communication", "Empathy", "Conflict Resolution", "Organization"],
            "base_tools": ["Workday", "BambooHR"],
            "roles": [
                ("HR Manager", ["Employee Relations", "Performance Management", "Compliance", "Benefits Administration"]),
                ("Technical Recruiter", ["Sourcing", "Interviewing", "Applicant Tracking Systems", "Negotiation", "Market Research"])
            ]
        }
    }

    job_dataset = []
    job_id_counter = 1000
    all_skills = set()

    # Generate exact roles + programmatic variations
    for domain, data in domains.items():
        for role_name, specific_skills in data["roles"]:
            
            # Base Role
            job = {
                "job_id": f"PI-{job_id_counter}",
                "job_title": role_name,
                "category": domain,
                "sub_category": random.choice(data["sub_categories"]),
                "skills": list(set(data["base_skills"] + specific_skills)),
                "soft_skills": [s for s in data["base_skills"] if "Communication" in s or "Problem" in s or "Empathy" in s or "Leadership" in s or "Critical" in s],
                "tools": data["base_tools"],
                "experience_levels": ["Entry", "Mid", "Senior"],
                "keywords": [role_name.lower()] + [s.lower() for s in specific_skills]
            }
            job_dataset.append(job)
            all_skills.update(job["skills"])
            job_id_counter += 1

            # Variation: Senior Role
            senior_job = job.copy()
            senior_job["job_id"] = f"PI-{job_id_counter}"
            senior_job["job_title"] = f"Senior {role_name}"
            senior_job["skills"] = list(set(senior_job["skills"] + ["Leadership", "Mentoring", "Architecture", "Strategy"]))
            senior_job["experience_levels"] = ["Senior", "Lead"]
            job_dataset.append(senior_job)
            all_skills.update(senior_job["skills"])
            job_id_counter += 1

            # Variation: Lead Role
            lead_job = job.copy()
            lead_job["job_id"] = f"PI-{job_id_counter}"
            lead_job["job_title"] = f"Lead {role_name}"
            lead_job["skills"] = list(set(lead_job["skills"] + ["Team Management", "Budgeting", "Cross-functional Leadership"]))
            lead_job["experience_levels"] = ["Lead", "Manager"]
            job_dataset.append(lead_job)
            all_skills.update(lead_job["skills"])
            job_id_counter += 1
            
            # Variation: Junior/Associate Role
            junior_job = job.copy()
            junior_job["job_id"] = f"PI-{job_id_counter}"
            junior_job["job_title"] = f"Junior {role_name}"
            junior_job["experience_levels"] = ["Entry"]
            job_dataset.append(junior_job)
            job_id_counter += 1

    os.makedirs('data', exist_ok=True)
    
    with open('data/job_categories.json', 'w', encoding='utf-8') as f:
        json.dump(job_dataset, f, indent=4)
        print(f"Generated {len(job_dataset)} job categories.")

    skills_taxonomy = {
        skill: {
            "aliases": [skill.lower(), skill.lower().replace(" ", ""), skill.lower().replace(" ", "-")],
            "category": "Technical" if skill not in ["Communication", "Problem Solving", "Empathy", "Leadership", "Attention to Detail", "Time Management", "Creativity"] else "Soft"
        }
        for skill in all_skills
    }
    
    with open('data/skills_taxonomy.json', 'w', encoding='utf-8') as f:
        json.dump(skills_taxonomy, f, indent=4)
        print(f"Generated {len(skills_taxonomy)} unique skills in taxonomy.")

if __name__ == "__main__":
    generate_job_data()
