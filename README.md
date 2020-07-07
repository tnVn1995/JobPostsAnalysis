# Job Post Analysis

  It is within the nature of the tech industry to continuously renew itself. It is of vital importance that businesses capitalize on the new trend to prosper and disrupt the status quo. For example, Apple Iphone when first introduced, revolutionized the mobile industry. Amazon cloud infrastructures redefine how companies approach training and deploying their models. Understanding new trend in technology, in my opinion, can be done by analyzing two sources. One from job postings and the other from research papers. The job postings provide data about the trend in technical tools while the research papers provide the trend in technical areas of research. In this data analysis, I'll work on job postings scraped from Indeed as it is publicly available. I'll be focusing on a limited number of job postings for: data scientist, machine learning engineer, software engineer and data analyst because I believe these roles will mirror the technical requirements from research areas of the near future.

# Data

  Data is scraped directly from [Indeed](https://www.indeed.com/) using BeautifulSoup and Python. The data include two files. The IndeedJobPosts.csv file contains information about job title, company name, location and the url link for job description. The JobDescription contains information about the job description for each url link from the IndeedJobPosts.csv
