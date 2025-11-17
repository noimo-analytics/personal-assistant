from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
import os
import requests
from langchain.agents import Tool
from langchain_core.tools import StructuredTool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime



load_dotenv(override=True)
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"
serper = GoogleSerperAPIWrapper()

async def playwright_tools():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright


def push(text: str):
    """Send a push notification to the user"""
    requests.post(pushover_url, data = {"token": pushover_token, "user": pushover_user, "message": text})
    return "success"


def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="outputs")
    return toolkit.get_tools()


async def other_tools():
    push_tool = Tool(
        name="send_push_notification", 
        func=push, 
        description="Use this tool when you want to send a push notification"
    )
    file_tools = get_file_tools()

    search_tool =Tool(
        name="search",
        func=serper.run,
        description="Use this tool when you want to get the results of an online web search"
    )

    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    python_repl = PythonREPLTool()
    
    return file_tools + [push_tool, search_tool, python_repl,  wiki_tool]

# --- Google Calendar integration ---

def _get_calendar_service():
    creds = Credentials.from_authorized_user_file(
        os.getenv("GOOGLE_TOKEN_PATH", "token.json"),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    return build("calendar", "v3", credentials=creds)


def create_calendar_event(summary: str, start_iso: str, end_iso: str, description: str = "", calendar_id: str = None) -> str:
    try:
        cal_id = calendar_id or os.getenv("GOOGLE_CALENDAR_ID", "primary")
        service = _get_calendar_service()
        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_iso},
            "end":   {"dateTime": end_iso},
        }
        created = service.events().insert(calendarId=cal_id, body=event).execute()
        return f"Event created: {created.get('htmlLink')}"
    except Exception as e:
        return f"Error creating calendar event: {str(e)}"


def list_upcoming_events(calendar_id: str = None, max_results: int = 5) -> str:
    cal_id = calendar_id or os.getenv("GOOGLE_CALENDAR_ID", "primary")
    service = _get_calendar_service()
    now = datetime.utcnow().isoformat() + "Z"
    events_result = (
        service.events()
        .list(calendarId=cal_id, timeMin=now, maxResults=max_results, singleEvents=True, orderBy="startTime")
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
        return "No upcoming events found."
    lines = []
    for evt in events:
        start = evt["start"].get("dateTime", evt["start"].get("date"))
        lines.append(f"{start} — {evt['summary']}")
    return "\n".join(lines)


def calendar_tools() -> list[Tool]:
    return [
        StructuredTool.from_function(
            func=create_calendar_event,
            name="create_calendar_event",
            description="Create a new calendar event. Requires: summary (event title), start_iso (RFC3339 format like '2025-05-20T15:00:00+05:30'), end_iso (RFC3339 format). Optional: description (event description), calendar_id (calendar ID, defaults to primary)."
        ),
        StructuredTool.from_function(
            func=list_upcoming_events,
            name="list_upcoming_events",
            description="List upcoming events on the specified or primary calendar. Optional: calendar_id (calendar ID, defaults to primary), max_results (number of events to return, defaults to 5)."
        ),
    ]

