# LinkedIn Job Tracker
A simple tool to save LinkedIn job listings to a Google Sheet. No coding required!


1. **Clone or download this repository.**
2. **Install Python 3.8+** (if not already installed).
3. **Install dependencies:**
	```powershell
	pip install -r requirements.txt	
	```
4. **Set up your LinkedIn credentials:**
	 - Copy `.env.example` to `.env` and fill in your LinkedIn username and password.
		 ```
4. **Add your Google service account credentials:**
	- Place your `credentials.json` in the `creds/` folder (do not share this file).
5. **Run the tool:**
	```powershell
	python src/job_tracker_gui.py
	```
	- Enter your LinkedIn username and password in the GUI when prompted.
- All jobs are saved to your Google Sheet

## Security
- Your credentials and session are stored locally and never shared.
- Never commit your `.env` or `credentials.json` to git.

## Troubleshooting
- If you see errors about missing credentials, check your `.env` and `creds/credentials.json`.
- If your LinkedIn session expires, just rerun the tool and log in again.

## License
MIT

