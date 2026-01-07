Campaign Booster (Built for Ketto Use Cases)

Campaign Booster is a small web tool designed around a simple idea:

People on Ketto often have genuine needs, but their campaign pages don’t clearly explain the story, the urgency, or how the money will be used. As a result, good fundraisers sometimes fail.

This project tries to help fix that problem before a campaign goes live.




>Why I built this<

After spending time exploring Ketto campaigns, a few patterns kept showing up:

many campaigns have very short or unclear descriptions

some don’t explain treatment costs or bills clearly

trust signals (proof, updates, transparency) are often missing

donors don’t always understand why the goal amount is required

None of this comes from bad intentions. Most people simply don’t know how to write a strong campaign page.

Campaign Booster acts like a “writing coach” for Ketto users.




>What the tool does<

A user pastes their campaign title and description, adds their goal amount, and clicks analyze.

The tool then:

Scores the campaign based on clarity, detail, urgency and transparency

Labels the trust level (High / Medium / Low)

Suggests practical improvements, written in plain language

Uses AI to produce:

a clearer, more emotional title

an improved version of the campaign story

The tool is not meant to replace the person’s story.
It simply helps them communicate better and build more trust.




>Why this matters for Ketto<

Better storytelling can mean:

higher donor confidence

more completed campaigns

fewer abandoned fundraisers

clearer expectations for both donors and campaign creators

It also reduces support overhead because users receive guidance upfront instead of asking for help after publishing.

This can complement Ketto’s existing verification and support processes.




>Tech stack<

Flask (Python backend)

HTML, CSS, JavaScript (frontend)

Google Gemini API (for rewriting suggestions)




>How to run locally<

Clone the repository

Install dependencies:

pip install -r requirements.txt


Create a .env file in the root directory:

GEMINI_API_KEY=your_api_key_here


Start the server:

python app.py


Open:

http://127.0.0.1:5000




>Deployment and security<

The API key is not stored in the codebase.

.env (local only)

environment variable on the hosting platform

never exposed on the frontend

This keeps the Gemini key safe even when deployed publicly.




>Possible future extensions (specifically for Ketto)<

Some ideas if this moves forward:

analyze real campaign drafts inside the Ketto dashboard

personalized coaching based on campaign category (medical, education, NGO, etc.)

automated trust checklist (documents, bills, updates, verification prompts)

content suggestions in Hindi and regional Indian languages

A/B testing to compare different versions of campaign stories

The goal would be to make fundraising easier, not more complicated.