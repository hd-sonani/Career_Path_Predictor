import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from predictor.models import Career

careers_data = [
    {
        "name": "Software Engineer",
        "description": "Design, develop, and maintain software systems and applications. Requires strong programming and problem-solving skills.",
        "salary": "$80,000 - $150,000",
        "skills": "Python, Java, JavaScript, Problem Solving",
        "work_type": "Hybrid/Remote"
    },
    {
        "name": "Data Scientist",
        "description": "Analyze complex datasets to derive business insights using machine learning and statistical techniques.",
        "salary": "$90,000 - $160,000",
        "skills": "Python, Data Analysis, SQL, Math",
        "work_type": "Hybrid"
    },
    {
        "name": "UX/UI Designer",
        "description": "Create intuitive and visually appealing user interfaces for digital products.",
        "salary": "$70,000 - $130,000",
        "skills": "UIUX, Graphic Design, Creativity",
        "work_type": "Hybrid/Remote"
    },
    {
        "name": "Financial Analyst",
        "description": "Analyze financial data, identify trends, and provide recommendations to improve financial performance.",
        "salary": "$65,000 - $110,000",
        "skills": "Data Analysis, Critical Thinking, Accounts",
        "work_type": "On-site/Hybrid"
    },
    {
        "name": "Marketing Manager",
        "description": "Develop and execute marketing strategies to promote products and services.",
        "salary": "$75,000 - $125,000",
        "skills": "Marketing, Communication, Leadership",
        "work_type": "Hybrid"
    },
    {
        "name": "Teacher",
        "description": "Educate students in various subjects and help them develop essential skills.",
        "salary": "$50,000 - $85,000",
        "skills": "Communication, Leadership, Problem Solving",
        "work_type": "On-site"
    },
    {
        "name": "Graphic Designer",
        "description": "Create visual concepts to communicate ideas that inspire, inform, and captivate consumers.",
        "salary": "$50,000 - $90,000",
        "skills": "Graphic Design, Creativity, Arts",
        "work_type": "Hybrid/Remote"
    },
    {
        "name": "Video Editor",
        "description": "Manipulate and edit film pieces in a way that is invisible to the audience.",
        "salary": "$55,000 - $95,000",
        "skills": "Video Editing, Creativity",
        "work_type": "Hybrid/Remote"
    },
    {
        "name": "Sales Manager",
        "description": "Lead and guide a team of sales representatives to meet or exceed sales goals.",
        "salary": "$80,000 - $140,000+",
        "skills": "Sales, Communication, Management",
        "work_type": "Hybrid"
    },
    {
        "name": "Database Administrator",
        "description": "Ensure databases run efficiently and are secure from unauthorized access.",
        "salary": "$75,000 - $120,000",
        "skills": "SQL, Problem Solving, Computer",
        "work_type": "Hybrid"
    },
    {
        "name": "HR Manager",
        "description": "Plan, direct, and coordinate the administrative functions of an organization.",
        "salary": "$70,000 - $115,000",
        "skills": "Management, Communication, Teamwork",
        "work_type": "On-site/Hybrid"
    },
    {
        "name": "Content Writer",
        "description": "Create engaging and relevant written content for websites, blogs, and marketing materials.",
        "salary": "$45,000 - $80,000",
        "skills": "Communication, Creativity, English",
        "work_type": "Remote"
    },
    {
        "name": "Business Analyst",
        "description": "Help businesses implement technology solutions in a cost-effective way by determining the requirements of a project.",
        "salary": "$75,000 - $115,000",
        "skills": "Data Analysis, Management, Communication",
        "work_type": "Hybrid"
    },
    {
        "name": "Project Manager",
        "description": "Plan, execute, and close projects, leading teams to achieve specific goals.",
        "salary": "$85,000 - $135,000",
        "skills": "Management, Leadership, Problem Solving",
        "work_type": "Hybrid"
    },
    {
        "name": "Game Developer",
        "description": "Design and develop video games for various platforms, combining programming and creativity.",
        "salary": "$70,000 - $130,000",
        "skills": "C++, Python, Problem Solving",
        "work_type": "Hybrid/Remote"
    }
]

def seed():
    for data in careers_data:
        Career.objects.get_or_create(
            name=data["name"],
            defaults={
                "description": data["description"],
                "salary": data["salary"],
                "skills": data["skills"],
                "work_type": data["work_type"]
            }
        )
    print("Database seeded with careers successfully!")

if __name__ == "__main__":
    seed()
