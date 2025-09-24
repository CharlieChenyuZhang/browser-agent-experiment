import asyncio
import os
from browser_use import Agent, Browser, ChatOpenAI

# Get the absolute path to the resume file
resume_path = os.path.abspath("test-resume.pdf")
print(f"Resume file path: {resume_path}")

# Initialize browser with larger window for better form interaction
browser = Browser(
    headless=False,  # Show browser window
    window_size={'width': 1200, 'height': 800},  # Set larger window size
)

# Create comprehensive task for Spotify job application
task = f"""
Navigate to https://jobs.lever.co/spotify/35de0846-f4bb-4975-8f21-382b44aa0e40/apply and fill out the job application form with the following information:

1. Office location: Select the first available option from the dropdown (New York, NY or Boston, MA)

2. Resume/CV: Upload the file using the absolute path: {resume_path}

3. Fill out the required fields with placeholder information:
   - Full name: "John Doe"
   - Pronouns: Select the first option (He/him)
   - Email: "john.doe@example.com"
   - Phone: "555-123-4567"
   - Current location: "New York, NY"
   - Current company: "Tech Company Inc"

4. Optional links section (leave blank or add placeholder):
   - LinkedIn URL: "https://linkedin.com/in/johndoe"
   - GitHub URL: "https://github.com/johndoe"

5. For all demographic survey questions, select the first available option:
   - Gender: Select first option
   - Race/ethnicity: Select first option
   - Veteran status: Select first option
   - Location: Select first option

6. Check the consent checkbox for future job opportunities

7. Submit the application

Make sure to wait for each form element to load before interacting with it. Handle any dropdowns, checkboxes, and file uploads carefully.
"""

agent = Agent(
    task=task,
    browser=browser,
    llm=ChatOpenAI(model='gpt-4o-mini'),
    available_file_paths=[resume_path],  # Make the resume file available to the agent
)

async def main():
    try:
        await agent.run()
        print("Job application completed successfully!")
    except Exception as e:
        print(f"Error during application process: {e}")

if __name__ == "__main__":
    asyncio.run(main())