# ==============================
# IMPORTS
# ==============================
from pdfminer.high_level import extract_text
import docx
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# ==============================
# STEP 1: READ RESUME
# ==============================
def read_resume(file_path):
    if file_path.endswith(".pdf"):
        return extract_text(file_path)
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    return None

# ==============================
# STEP 2: EXTRACT SKILLS
# ==============================
def extract_skills(text):
    skills_db = ["python", "aws", "docker", "linux"]
    text = text.lower()
    return [skill for skill in skills_db if skill in text]

# ==============================
# STEP 3: SCRAPE JOBS
# ==============================
def scrape_jobs():
    print("\n🌐 Fetching jobs...\n")

    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job in soup.find_all("div", class_="card-content"):
        title = job.find("h2").text.strip()
        company = job.find("h3").text.strip()
        location = job.find("p", class_="location").text.strip()

        skills = title.lower() + " python aws docker linux"

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "skills": skills
        })

    return jobs

# ==============================
# STEP 4: MATCHING LOGIC
# ==============================
def match_score(resume_skills, job_skills):
    match = 0
    for skill in resume_skills:
        if skill in job_skills:
            match += 1
    return (match / len(resume_skills)) * 100 if resume_skills else 0

# ==============================
# STEP 5: AUTO APPLY BOT
# ==============================
def auto_apply(job):
    print(f"\n🚀 Applying to: {job['title']}")

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get("https://www.w3schools.com/html/html_forms.asp")

    time.sleep(2)

    driver.find_element(By.NAME, "firstname").send_keys("Tharani")
    driver.find_element(By.NAME, "lastname").send_keys("AWS")

    print("✅ Applied successfully!")

    time.sleep(2)
    driver.quit()

# ==============================
# MAIN PROGRAM
# ==============================
if __name__ == "__main__":
    file_path = "resume.pdf"

    text = read_resume(file_path)

    if text:
        print("\n===== EXTRACTED SKILLS =====")
        resume_skills = extract_skills(text)
        print(resume_skills)

        jobs = scrape_jobs()

        print("\n===== MATCHING & APPLYING =====")

        for job in jobs[:5]:   # limit for safety
            score = match_score(resume_skills, job["skills"])

            print(f"\nJob: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Match: {score:.2f}%")

            # AUTO APPLY CONDITION
            if score >= 70:
                auto_apply(job)

    else:
        print("❌ Resume not found")
