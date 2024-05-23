import streamlit as st
from langchain.llms import GooglePalm
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from dotenv import load_dotenv
import os

"""
playbook.py : This file helps the sales person for tasks such answering sales question , craft persuasive pitch, product description
, and sales play
"""

load_dotenv()

def get_LLM_response(query,task):
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=os.environ['GOOGLE_API_KEY'])
    examples = []

    if task == "Answer a sales question":
            examples = [
                {
                    "query": "What closing techniques are most effective?",
                    "answer": "In my experience, the most effective closing techniques combine clarity about next steps with building value for the customer. Consider options like the 'assumptive close' ('Let's schedule a follow-up meeting to discuss the contract details') or the 'urgency close' ('These limited-time offers won't last long, are you ready to secure yours?') while addressing any remaining concerns."
                },
                {
                    "query": "How can I motivate my sales team?",
                    "answer": "Motivating your sales team requires a multi-pronged approach. Recognition and rewards for achievement are crucial, but fostering a collaborative environment and providing ongoing coaching and development opportunities are equally important. Consider gamification techniques, commission structures, and team-building exercises to keep them engaged."
                },
                {
                    "query": "How can I identify sales objections effectively?",
                    "answer": "Active listening and open-ended questions are key to identifying sales objections effectively. Let your customer fully express their concerns, then paraphrase and clarify to ensure you understand their perspective. This helps you tailor your responses and address their specific worries."
                },
            ]
    elif task == "Craft a persuasive pitch":
            examples = [
                {
                    "query": "Product: CRM software",
                    "answer": "Imagine streamlining your sales process with a powerful CRM system. Our software will help you manage leads, track opportunities, and nurture customer relationships, ultimately boosting your closing rates. Let's discuss how it can save you time and increase your sales!"
                },
                {
                    "query": "Service: Marketing automation",
                    "answer": "Stop wasting time on manual marketing tasks! Our marketing automation platform can personalize campaigns, automate lead nurturing, and improve your marketing ROI. Let's see how it can free you up to focus on closing deals."
                },
                {
                    "query": "Product: Productivity app",
                    "answer": "Feeling overwhelmed with tasks and deadlines? Our productivity app is your solution. Increase your focus, organize your workflow, and achieve more in less time. Imagine the impact on your sales goals! Let's explore how it can make you a more efficient salesperson."
                },
            ]
    elif task == "Write a product description":
        examples = [
            {
                "query": "Product: CRM software",
                "answer": "**Introducing Acme CRM, the all-in-one solution to streamline your sales process and boost your bottom line!** Manage leads, track opportunities, nurture customer relationships, and close more deals with ease. Acme CRM empowers sales teams of all sizes to become more efficient and effective. Let's discuss how it can transform your sales pipeline!"
            },
            {
                "query": "Product: High-performance laptop",
                "answer": "**Unleash your productivity with the blazing-fast Nova X laptop.** Edit videos seamlessly, render complex 3D models in record time, and power through demanding applications. Designed for professionals who demand the best, Nova X features cutting-edge technology and a sleek, durable build. Experience the difference a high-performance laptop can make in your workflow. Let's find the perfect configuration for your needs."
            },
            {
                "query": "Product: Wireless noise-canceling headphones",
                "answer": "**Immerse yourself in crystal-clear audio with the Aria Pro wireless headphones.** Experience superior noise cancellation that blocks out distractions, letting you focus on what matters. Enjoy rich, detailed sound and exceptional comfort, perfect for work, travel, or simply unwinding.  Aria Pro headphones elevate your listening experience. Let's discover the perfect sound for you."
            },
        ]
    elif task == "Create your sales play":
        examples = [
             {
                 "query":"What are the action-steps for reps to take during sales cycle stages",
                 "answer": """Here's a B2B example:
Stage 1: Outbound/Inbound prospecting → Play: Send 15 LinkedIn connections a day. Make X amount of cold calls in X amount of hours.
Stage 2: Qualifying → Play: Ask prospects these specific questions. If they're qualified, set a time to speak 2 days later, if they're not qualified, send them these helpful resources.
Stage 3: Presentation → Play: Demo the service, show these testimonials, ask clarifying questions, ask for the sale at the end
Stage 4: Nurturing → Play: Follow-up 5 times within 30 days via phone and email. Send learn more materials, ask for a follow-up call.
Stage 5: Closing → Play: Send contracts digitally, only quote using the CPQ system, follow-up if nothing is signed after 3 days.
Stage 6: Onboarding → Play: Send onboarding documents after kick-off call, Make sure welcome email automation is sent."""
             },
             {
            "query": "What are the action-steps for reps to take during sales cycle stages?",
            "answer": """Here's a B2B example that emphasizes emotional connection:

            **Stage 1: Outbound/Inbound Prospecting**

            * **Playbook:**
                * **Empathy-Driven Research:**  Research the prospect's company, industry, and recent news to understand their current challenges and aspirations.
                * **Emotional Storytelling:**  Craft targeted outreach messages that connect with the prospect's emotional needs and desires (e.g., security, peace of mind, increased efficiency).
                * **Social Proof with Impact:**  Showcase customer testimonials that highlight not just the product's functionality, but also the positive emotional impact it had on the customer (e.g., reduced stress, improved teamwork).
                * **Personalized Video Introductions:**  Create short, personalized video introductions that introduce yourself and your solution in a relatable and engaging way.

            **Stage 2: Qualifying**

            * **Playbook:**
                * **Active Listening & Emotional Intelligence:**  Pay close attention to the prospect's tone, word choice, and emotional state during the discovery call.
                * **Challenge and Opportunity Framing:**  Frame the prospect's challenges as opportunities for growth and improvement, appealing to their desire for a better future.
                * **Solution as an Ally:**  Position your solution as an ally that can help them overcome their challenges and achieve their desired emotional state (e.g., feeling empowered, achieving peace of mind).
                * **Benefit-Focused Questions:**  Ask questions that uncover the emotional benefits the prospect desires from a solution (e.g., feeling confident, achieving work-life balance).

            **(Stages 3-6 would remain similar to the previous examples, focusing on presentation, nurturing, closing, and onboarding)**
            """
            }
        ]


    example_template = """
    Question: {query}
    Response: {answer}
    """

    example_prompt = PromptTemplate(
        input_variables=['query','answer'],
        template = example_template
    )

    prefix = """You are assigned with a {template_task}:
    Here are some examples:
    """

    suffix = """
    Question: {template_user_input}
    Response: """

    example_selector = LengthBasedExampleSelector(
        examples = examples,
        example_prompt= example_prompt,
        max_length = 200
    )

    new_prompt_template = FewShotPromptTemplate(
        example_selector = example_selector,
        example_prompt = example_prompt,
        prefix = prefix,
        suffix = suffix,
        input_variables=['template_user_input','template_task'],
        example_separator="\n"
    )

    response=llm(new_prompt_template.format(template_user_input=query,template_task=task))

    return response

st.set_page_config(page_title="Sales Wizard",
                    layout = 'centered',
                    initial_sidebar_state = 'collapsed')
st.header("The Ultimate Sales Playbook ✨")
task = st.selectbox(
    "Please select the task to be performed",
    ('Answer a sales question','Craft a persuasive pitch','Write product description', 'Create your sales play'),key=1)

form_input = st.text_input("Enter the context")
submit = st.button("Generate")


if submit:
    st.write(get_LLM_response(form_input, task))
