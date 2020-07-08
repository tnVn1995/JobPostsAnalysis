# Job Post Analysis

  It is within the nature of the tech industry to continuously renew itself. It is of vital importance that businesses capitalize on the new trend to prosper and disrupt the status quo. This principle also applies to tech employees. The ability to capitalize on the new trend will reward them highly. Covid-19 brings about unparalleled challenges to the U.S economy as the whole and to the tech industry in particular. How do tech job seekers prosper during this difficult time? One way to capture and take advantage of the new trend in tech is to analyze companies' behavior. One important aspect is their hiring practices. I'll be performing text analysis of job postings from Indeed to see the trend in tech industry by states in the U.S

# Data

  Data is scraped directly from [Indeed](https://www.indeed.com/) using BeautifulSoup and Python. The data include two files. The IndeedJobPosts.csv file contains information about job title, company name, location and the url link for job description. The JobDescription contains information about the job description for each url link from the IndeedJobPosts.csv. The job postings are scraped within a valid time period defined by Indeed (jobs that are still valid).
