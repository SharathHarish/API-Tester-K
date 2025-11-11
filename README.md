API Tester – A Tkinter-Based Desktop App for API Testing

The API Tester is a lightweight, user-friendly desktop application built using Python’s Tkinter library.
It allows you to send and test REST API requests directly from your computer — no browser extensions or heavy tools like Postman required.

This project focuses on simplicity, functionality, and a clean modern interface that adapts to both light and dark themes.


---

 Project Overview

The goal of this project was to create a compact yet powerful tool that lets developers:

Test different API endpoints quickly

View all parts of the response in one place

Save frequently used requests

Export responses for documentation or debugging

Use environment variables for flexible URL management



---

 Features and Concepts Explained

 1. Modern Tkinter Interface

Tkinter is known for being simple but not always visually appealing.
To overcome that, this app uses custom themes and layout management to create a clean, modern-looking interface.
It automatically resizes to fit 90% of your screen and centers itself on startup, making it look professional and responsive on any display.


---

 2. Light & Dark Themes

Switch between light and dark modes smoothly without the UI flickering or resizing.
When you toggle the theme, the app remembers the exact geometry and reapplies it, ensuring that nothing “jumps” or shifts on screen.


---

3. API Request Support

You can test GET, POST, PUT and DELETE requests.
Each request can include:

Custom headers (key-value pairs)

JSON request body

URLs with placeholders like {{base_url}}, which automatically replace values from the default environment file.


For example, if your default.json file contains:

{
  "base_url": "https://jsonplaceholder.typicode.com"
}

Then a request to:

{{base_url}}/posts/1

will automatically resolve to:

https://jsonplaceholder.typicode.com/posts/1


---

4. Unified Response Output

Instead of splitting results into multiple tabs, the API Tester shows everything — status code, response headers, and response body — in a single output box.
This helps you analyze everything in one glance without switching between views.
If the body contains valid JSON, it’s automatically formatted for readability.


---

5. Request History

Every request you send is saved in the history panel on the left.
You can double-click any entry to replay the same request instantly.
The app stores up to 20 recent requests and automatically saves them in /data/history.json, so your history persists between sessions.


---

6. Save Requests to Collections

If you have a request you want to reuse later, you can click the Save button.
The app will save it as a JSON file inside /collections/, including its method, URL, headers, and body.
You can easily organize and reload your saved API calls later.


---

7. Export Response

Every response you receive can be exported to a text or JSON file for documentation or debugging.
The Export Response button sits neatly on the top-right corner of the response area and saves the entire output — including status, headers, and body — in one click.


---

8. Clear Fields

The Clear button resets all inputs and outputs, so you can start a new test instantly without relaunching the app.


---

9. Environment Variables (Hidden but Functional)

Instead of showing an environment dropdown, the app silently loads a file named:

/environments/default.json

This allows you to define key-value pairs (like base_url or auth_token) that can be used in any request without cluttering the interface.


---

10. Error Handling & Stability

The app uses Python’s requests library and handles most common errors gracefully:

Invalid JSON bodies

Network timeouts

Connection errors

Non-JSON responses


If something goes wrong, you’ll see a clear error message in the response box instead of a crash.

---

<img width="1536" height="1024" alt="file_00000000a8dc7209bf0af5a153652493 (1)" src="https://github.com/user-attachments/assets/ab352b60-4c80-4035-a713-ac74ceb71774" />

Tech Stack

Component	Description

Language	Python 3.8+
GUI Framework	Tkinter
Networking	Requests
Storage	JSON Files (History, Collections, Environment)



---

📂 Project Structure

API-Tester/
│
├── main.py                  # Main application file
│
├── environments/
│   └── default.json         # Environment variables (hidden, used in backend)
│
├── collections/             # Saved API requests
│
├── data/
│   └── history.json         # Request history storage
│
└── README.md                # Project documentation


---

🧠 Challenges Faced

1. Making Tkinter Look Modern

Tkinter doesn’t have built-in dark mode or styling like modern UI frameworks.
It took a lot of fine-tuning with colors, padding, and font styles to make it visually appealing.

2. Preventing Layout Shifts

When toggling between light and dark themes, the UI initially “jumped” due to re-rendering.
I solved this by locking the window geometry before applying the new theme and restoring it afterward.

3. Merging Response Tabs into One View

The first version had separate tabs for Raw, JSON, and Headers.
They worked, but switching between them felt clunky.
Combining them into one view required careful formatting but made the app much easier to use.

4. Handling Multiple Content Types

Not all APIs return JSON — some return plain text or HTML.
To prevent the app from crashing, I added a fallback mechanism that prints the response as text if JSON parsing fails.

5. Keeping It Lightweight

I wanted to keep the project dependency-free except for requests, so I avoided external libraries for theming or layout.
This made the code more educational and easy for others to understand.


---

Installation (Single EXE File)

You don’t need to install Python or any libraries.
The entire app is packaged into one single .exe file for easy use.

 Windows Installation Steps

1. Download the file

Go to the Releases section of this repository.

Download the file named K API Tester.exe.



2. Run the app

Double-click on K API Tester.exe.

The application will open instantly — no installation or setup needed.



3. Automatic setup (first launch)

The app will automatically create the following folders (if they don’t already exist):

/environments
/collections
/data

These are used for saving your request history, environment variables, and saved collections.



4. Start Testing APIs!

Enter a URL, choose a method (GET, POST, PUT, DELETE, PATCH), and click Send.

You’ll see the response, status, and headers in a single output window.
--

📜 License

This project is licensed under the MIT License — you are free to use, modify, and distribute it for personal or commercial purposes.


---

🏁 Final Note

This project was an exciting journey in combining GUI development and API testing in Python.
It started as a small experiment to simplify API debugging and evolved into a full-fledged desktop application.

The biggest takeaway was that even with a simple toolkit like Tkinter, it’s possible to create elegant, functional, and professional-grade tools with the right design mindset.
