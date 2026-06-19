#!/usr/bin/env python3

import streamlit as st
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI()

st.set_page_config(page_title="AI To-Do App", page_icon="📝", layout="centered")
st.title("📝 AI Natural Language To-Do List")
st.write("Type tasks using relative words like *'today'*, *'tomorrow'*, or *'yesterday'*!")

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

def parse_with_ai(user_input):
    """Uses OpenAI to extract task details, resolving relative dates dynamically."""
    
    # Dynamically calculate dates to give the AI accurate temporal context
    today_date = datetime.now()
    yesterday_date = today_date - timedelta(days=1)
    tomorrow_date = today_date + timedelta(days=1)
    
    # Format dates nicely for the AI context
    date_context = (
        f"Today is {today_date.strftime('%A, %B %d, %Y')}. "
        f"Yesterday was {yesterday_date.strftime('%A, %B %d, %Y')}. "
        f"Tomorrow is {tomorrow_date.strftime('%A, %B %d, %Y')}."
    )

    prompt = f"""
    You are an AI assistant for a to-do list application. Analyze the user input and break it down into tasks.
    Extract the task description, the category (e.g., Work, Personal, Shopping, Health), and the due date.
    
    Use the following exact temporal context to resolve relative date words (like 'today', 'tomorrow', 'yesterday', or days of the week):
    {date_context}
    
    If no date is mentioned at all, default the due date to "Today".
    
    Output the result as a strict JSON object with a single key "tasks" containing an array of objects. 
    Each object must have these keys: "task", "category", "due_date".
    
    User Input: "{user_input}"
    JSON:
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        result = json.loads(response.choices.message.content)
        return result.get("tasks", [])
    except Exception as e:
        st.error(f"Failed to parse task with AI: {e}")
        return []

# User Input Form
with st.form("task_form"):
    user_input = st.text_input(
        "Add a new task:", 
        placeholder="e.g., Email project reports tomorrow, or Finish gym session today"
    )
    submitted = st.form_submit_button("Add Task")

if submitted and user_input:
    with st.spinner("AI is parsing your task timeline..."):
        new_tasks = parse_with_ai(user_input)
        for t in new_tasks:
            st.session_state.tasks.append(t)
        st.success("Task(s) added successfully!")

# Display Tasks
st.subheader("Your Tasks")
if not st.session_state.tasks:
    st.info("No tasks yet. Try typing: 'Call mom tomorrow afternoon'")
else:
    for index, task in enumerate(st.session_state.tasks):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.markdown(f"**{task['task']}**")
            st.caption(f"Category: {task['category']} | Due: {task['due_date']}")
        with col2:
            if st.button("Delete", key=f"del_{index}"):
                st.session_state.tasks.pop(index)
                st.rerun()


