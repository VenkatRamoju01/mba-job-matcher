from openai import OpenAI
import json

client = OpenAI(api_key="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")

# --- DATA INPUTS ---
# Later, we will automate this. For now, we paste text here.
my_resume = """
PROFESSIONAL SUMMARY 
Product analytics and systems professional with 4.5 years of experience driving data-driven decision making across digital platforms and 
large-scale infrastructure systems. Experienced in experimentation frameworks, predictive modeling, and scalable analytics systems to 
improve product performance. Strong first-principles problem solver collaborating with product, engineering, and business teams. 
WORK EXPERIENCE                                                             
Google | Performance Lead, YouTube Support Analytics                                                                                                 
August 25- Present   
Lead analytics and experimentation initiatives to improve YouTube Help Center performance, user experience, and operational decision-making 
across global support operations, partnering with product and operations teams. 
● Designed and prototyped a predictive classification model (AUC 0.71) using behavioral signals to estimate user effort, enabling scalable 
evaluation metrics for experimentation across YouTube Help Center product improvements. 
● Designed a quasi-experimental evaluation framework (difference-in-differences) to measure the impact of Help Center updates, 
identifying a 10% reduction in support contacts alongside a 7% rise in extreme dissatisfaction driven by case-mix changes. 
● Analyzed the end-to-end funnel of the YouTube account recovery chatbot, identifying >50% early-stage user drop-offs and <1% full 
self-recovery, segmenting behavior across creator cohorts to inform workflow redesign priorities. 
● Led development of a centralized product performance dashboard for YouTube Help Center, integrating behavioral and feedback signals 
to monitor thousands of articles and prioritize content improvements. 
● Built analytics pipelines transforming large-scale support logs into operational dashboards used by product, vendor, and GTM teams to 
monitor launches and support system performance. 
Accordion India |  Business Manager (Analytics), Data & Analytics Practice                                                                                      
April 24- August 25 
Led analytics engagement for a $100B+ AUM private equity client, managing a team of 8 analysts delivering decision-support systems for 
portfolio strategy and executive performance reviews across 80+ B2B SaaS companies. 
● Analyzed technology spend and GenAI adoption across portfolio companies, identifying seven-figure vendor consolidation opportunities 
and informing portfolio cost optimization initiatives. 
● Designed a portfolio-wide “Metrics That Matter” performance scorecard, consolidating financial and operating KPIs to benchmark 
companies and identify operational underperformance. 
● Built an acquisition benchmarking application integrating Power Apps, workflow automation, and BI dashboards to enable deal teams to 
compare potential targets against portfolio peers. 
● Automated portfolio-wide data collection and reporting workflows, reducing a week-long manual reporting process to a single day and 
enabling near real-time dashboard refreshes. 
Hindustan Petroleum Corporation Limited | Operations Officer                                                                                                    
September 20- April 23   
Managed operations for a 133 km petroleum pipeline transporting ₹10 crore/hour fuel throughput, leading 5 officers and 15 vendors while 
safeguarding ₹400 crore in critical infrastructure assets. 
● Led deployment of an ML-based alarm classification system for pipeline monitoring by defining model requirements, coordinating vendor 
development, and overseeing evaluation, reducing false alerts by 50% and improving response efficiency by 22%. 
● Implemented automated PLC-based control of drag-reducing additive injection, reducing chemical consumption and generating ₹40L 
annual cost savings. 
● Redesigned nighttime pipeline security operations by piloting vehicle-based patrol systems, reducing manpower requirements 88% and 
delivering ₹50L annual savings while improving guard safety and response coverage. 
● Identified structural exposure risk at a canal-crossing pipeline segment and led a ₹30L mitigation project, preventing potential ₹4Cr fuel 
theft risk and eliminating recurring maintenance costs. 
● Resolved politically sensitive ~1 lakh sq ft pipeline corridor encroachment, coordinating with legal teams, police, and district authorities to 
protect critical infrastructure. 
EDUCATION 
Indian School of Business (ISB) 
PGP in Finance & IT management 
Indian Institute of Technology Hyderabad 
Skills:  
B. Tech in Civil Engineering 
3.6/4  
9.2/10 - Institute Silver Medalist   
April 23 - April 24 
August 16 - May 20 
SQL, Python, Applied ML, Product Analytics, Experimentation & A/B Testing, Power BI, Tableau, Excel, Workflow Automation, Power Apps
"""

job_description = """

 Program Manager, VCP  at Amazon

About the job
DESCRIPTION

DESCRIPTION

Amazon.com, Inc. (NASDAQ:AMZN), a Fortune 500 company based in Seattle, opened on the World Wide Web in July 1995 and today offers Earth's Biggest Selection. Amazon.com, Inc. seeks to be Earth's most customer-centric company, where customers can find and discover anything they might want to buy online, and endeavors to offer its customers the lowest possible prices. Today, we operate retail websites in nine countries, offering millions of products in more than 40 categories worldwide, and we still like to work hard, have fun and make history!

Amazon Vendor Services (AVS), in partnership with Retail Business Services (RBS), offers a premium B2B consulting program to help leading vendors maximize their success on the Amazon marketplace. The Vendor Consultant Program (VCP) provides hands-on strategic guidance, operational support, and performance optimization for key vendor partners. As part of this service, experienced consultants work directly with vendors to streamline logistics, enhance product content, optimize advertising, and drive greater sales growth on the Amazon platform. Vendors enrolled in the VCP benefit from dedicated account management, data-driven recommendations, and customized consulting to navigate the complexities of the vendor-Amazon relationship. This paid program is designed for vendors seeking a competitive edge and deeper integration with Amazon's systems and processes.

Vendor Consultant Program (VCP) is looking for a highly skilled and analytical Program Manager, with a passion for making an impact through innovation and delivering solutions at scale. This role offers a unique opportunity to support our growing business while driving large scale, high visibility projects such as HOTW automation, UDE and process improvement initiatives with substantial internal and external impact.

Key job responsibilities as Program Manager in VCP are.

 Ambiguity Management: You will be working in new environment where there is no clear ‘right’ path or solution defined earlier.
 Program Development: Developing the strategy to improve the business metrics and align with leadership.
 Building HOTW Solutions: Developing tech-first solutions for reducing the manual dependency to drive cost-effective and centralized teams.
 UDE: Diving deep on the data, analyzing trends, inputs to provide data driven solutions to permanently eliminate the defects upstream.
 Stakeholder Management: Understand partner teams’ problems, identify sweet spots to enable premium relationship with key high-level stakeholders such as category leaders, country managers of new MP launches.
 Deliver Results: Work backwards from the business impact and customer experience to define the steps to followed

Candidate Profile:

The successful candidate will have program management skill with the ability to conduct in-depth analyses, think big and identify game-changing opportunities. In addition, you will be expected to deliver solutions and programs that are technology based, highly scalable, secure, and flexible - all while maintaining customer and business partner focus. You will work with internal and external stakeholders to identify, define, and specify solutions meeting our customers and selling partner’s needs.

The individual would have targets on process standardization, automation and business metrics. Would engage with the business and support/service teams and build customer confidence through quality delivery, robust processes and sound reporting metrics. The individual would be responsible and be a point of escalation for the delivery by the teams working with him/her.

Basic Qualifications

 3+ years of program or project management experience
 3+ years of working cross functionally with tech and non-tech teams experience
 3+ years of defining and implementing process improvement initiatives using data and metrics experience
 Knowledge of Excel (Pivot Tables, VLookUps) at an advanced level
 Experience defining program requirements and using data and metrics to determine improvements

Preferred Qualifications

 Experience with SQL queries
 Project management certificate
 Lean Six Sigma certificate – GB or BB
 Master's degree

BASIC QUALIFICATIONS

 3+ years of program or project management experience
 3+ years of working cross functionally with tech and non-tech teams experience
 3+ years of defining and implementing process improvement initiatives using data and metrics experience
 Knowledge of Excel (Pivot Tables, VLookUps) at an advanced level and SQL
 Experience defining program requirements and using data and metrics to determine improvements

PREFERRED QUALIFICATIONS

 Master's degree
"""

# --- THE SYSTEM PROMPT ---
system_message = """
You are an expert Career Coach for Tier-1 MBA graduates. 
Your task is to compare a Resume against a Job Description.
Identify exactly what is missing and provide a Match Score.
Output ONLY in JSON format.
"""

# --- THE USER PROMPT ---
user_message = f"""
RESUME: {my_resume}
JOB DESCRIPTION: {job_description}

Please provide:
1. match_score (0-100)
2. missing_skills (list)
3. experience_gaps (list)
4. tailoring_tip (1 sentence on how to rewrite a bullet point to fit this JD)
"""

print("Analyzing the match... please wait.")

try:
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
      ],
      response_format={ "type": "json_object" } # This forces the AI to give us a clean JSON
    )
    
    # Parse and print the result
    result = json.loads(response.choices[0].message.content)
    print("\n--- ANALYSIS COMPLETE ---")
    print(json.dumps(result, indent=2)) # This makes the JSON look pretty

except Exception as e:
    print(f"Error: {e}")