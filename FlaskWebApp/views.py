from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import random
from openai import OpenAI
from dotenv import load_dotenv
import os
##the api key is stored in the .env file, this code just in case the api is not found
def configure():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        raise ValueError("API key not found. Please check your .env file and ensure the 'OPENAI_API_KEY' is set.")
    return api_key


api_key = configure()


client = OpenAI(api_key=api_key)


views = Blueprint('views', __name__)

chat_history_list = [] # even index are user message, odd index are bot message
for i in range(8):
    temp = []
    chat_history_list.append(temp)

index_list = [0,1,2,3,4,5,6,7]
scenarios = [
    {'title': 'Scenario 1: Goal Setting', 
     'description': 'Description: You have been feeling overwhelmed and discouraged lately due to depression. You want to take steps to improve your daily life and know that setting small, achievable goals can be a helpful way to start. But, you are unsure where to begin or what kind of goals would be both realistic and supportive.', 
     'task': 'Task: Use ChatGPT to help you brainstorm a list of 3-5 realistic, short-term goals that can boost your mood and help you manage your day-to-day life while living with depression. As you interact with ChatGPT, consider discussing strategies for setting achievable goals, tracking progress, and making adjustments as needed.'},

    {'title': 'Scenario 2: Discussing depression with those you trust', 
     'description': 'Description: You have been living with depression. You want to explain what you are going through to someone you trust – a friend, family member, or partner. You hope this conversation will help them understand you better and give you the support you need, but you are not sure how to start.', 
     'task': 'Task: Use ChatGPT to get advice on how to have a conversation about your depression with someone you trust. Focus on getting tips for starting the conversation, explaining your experience, and asking for support.'},

    {'title': 'Scenario 3: Leaving the house regularly', 
     'description': 'Description: Depression has been making you want to stay inside. You know getting out more could help, but it feels hard. Planning activities, or even just going outside, can seem overwhelming. Yet, you want to find ways to make small outings part of your life.', 
     'task': 'Task: Talk to ChatGPT about how to start getting out of the house more often to help manage your depression, focusing on easy activities, motivation, planning, setting expectations, and tracking progress.'},
    {'title': 'Scenario 4: Finding a different therapist when there is limited progress', 
     'description': 'Description: You have been in therapy for a while. It helped at first, but lately, you feel stuck. The things that used to work do not seem to help anymore. You are thinking about finding a new therapist who might have a fresh perspective. But, starting over feels overwhelming, and you are not sure how to find the right person.', 
     'task': 'Task: Use ChatGPT to get advice on how to know when it it time to find a new therapist, what to look for in a new therapist, and how to navigate the process of switching therapists.'},

    {'title': 'Scenario 5: Healthy eating', 
     'description': 'Description: You have been struggling with depression, and you know that your eating habits might be contributing to your low mood. You often reach for comfort foods or skip meals when you are feeling down, but you want to make healthier choices to support your mental health. However, making changes to your diet feels overwhelming, and you are not sure where to start.', 
     'task': 'Task: Use ChatGPT to get advice on how to make small, manageable changes to your eating habits that can help you better manage your depression symptoms.'},

    {'title': 'Scenario 6: Explaining depression to partner/family', 
     'description': 'Description: You have been dealing with depression for a while, but you have not fully explained what you are going through to your partner or a close family member. You want to help them understand your experience better, so they can offer the support you need. However, you are not sure how to start the conversation or what to say without overwhelming them or making them worry.', 
     'task': 'Task: Use ChatGPT to get advice on how to have an open and honest conversation with your partner or a family member about your depression experience.'},

    {'title': 'Scenario 7: Recalling positive memories', 
     'description': 'Description: You have been struggling with depression, and lately, it feels like your mind is constantly focused on negative thoughts and experiences. You want to find a way to shift your mindset and remember the positive moments in your life, hoping that this will help improve your mood and give you a more balanced perspective. However, when you are feeling down, it can be challenging to recall happy memories or find the motivation to focus on the good things.', 
     'task': 'Task: Use ChatGPT to get advice on how to effectively recall and engage with positive memories as a way to help manage your depression symptoms.'},

    {'title': 'Scenario 8: Finding information about depression', 
     'description': 'Description: You have recently been diagnosed with depression, and you want to learn more about the condition to better understand your symptoms and treatment options. However, with so much information available online, it can be overwhelming and challenging to know where to start or which sources to trust. You want to find reliable, accurate information that can help you make informed decisions about your mental health care.', 
     'task': 'Task: Use ChatGPT to get guidance on finding trustworthy and relevant information about depression.'}
]
scenario_primary = [
    {'title': 'Scenario 1: Goal Setting', 
     'description': 'Description: You have been feeling overwhelmed and discouraged lately due to depression. You want to take steps to improve your daily life and know that setting small, achievable goals can be a helpful way to start. But, you are unsure where to begin or what kind of goals would be both realistic and supportive.', 
     'task': 'Task: Use ChatGPT to help you brainstorm a list of 3-5 realistic, short-term goals that can boost your mood and help you manage your day-to-day life while living with depression. As you interact with ChatGPT, consider discussing strategies for setting achievable goals, tracking progress, and making adjustments as needed.'},

    {'title': 'Scenario 2: Discussing depression with those you trust', 
     'description': 'Description: You have been living with depression. You want to explain what you are going through to someone you trust – a friend, family member, or partner. You hope this conversation will help them understand you better and give you the support you need, but you are not sure how to start.', 
     'task': 'Task: Use ChatGPT to get advice on how to have a conversation about your depression with someone you trust. Focus on getting tips for starting the conversation, explaining your experience, and asking for support.'},

    {'title': 'Scenario 3: Leaving the house regularly', 
     'description': 'Description: Depression has been making you want to stay inside. You know getting out more could help, but it feels hard. Planning activities, or even just going outside, can seem overwhelming. Yet, you want to find ways to make small outings part of your life.', 
     'task': 'Task: Talk to ChatGPT about how to start getting out of the house more often to help manage your depression, focusing on easy activities, motivation, planning, setting expectations, and tracking progress.'},
    {'title': 'Scenario 4: Finding a different therapist when there is limited progress', 
     'description': 'Description: You have been in therapy for a while. It helped at first, but lately, you feel stuck. The things that used to work do not seem to help anymore. You are thinking about finding a new therapist who might have a fresh perspective. But, starting over feels overwhelming, and you are not sure how to find the right person.', 
     'task': 'Task: Use ChatGPT to get advice on how to know when it it time to find a new therapist, what to look for in a new therapist, and how to navigate the process of switching therapists.'}
]
scenario_secondary = [
    {'title': 'Scenario 5: Healthy eating', 
     'description': 'Description: You have been struggling with depression, and you know that your eating habits might be contributing to your low mood. You often reach for comfort foods or skip meals when you are feeling down, but you want to make healthier choices to support your mental health. However, making changes to your diet feels overwhelming, and you are not sure where to start.', 
     'task': 'Task: Use ChatGPT to get advice on how to make small, manageable changes to your eating habits that can help you better manage your depression symptoms.'},

    {'title': 'Scenario 6: Explaining depression to partner/family', 
     'description': 'Description: You have been dealing with depression for a while, but you have not fully explained what you are going through to your partner or a close family member. You want to help them understand your experience better, so they can offer the support you need. However, you are not sure how to start the conversation or what to say without overwhelming them or making them worry.', 
     'task': 'Task: Use ChatGPT to get advice on how to have an open and honest conversation with your partner or a family member about your depression experience.'},

    {'title': 'Scenario 7: Recalling positive memories', 
     'description': 'Description: You have been struggling with depression, and lately, it feels like your mind is constantly focused on negative thoughts and experiences. You want to find a way to shift your mindset and remember the positive moments in your life, hoping that this will help improve your mood and give you a more balanced perspective. However, when you are feeling down, it can be challenging to recall happy memories or find the motivation to focus on the good things.', 
     'task': 'Task: Use ChatGPT to get advice on how to effectively recall and engage with positive memories as a way to help manage your depression symptoms.'},

    {'title': 'Scenario 8: Finding information about depression', 
     'description': 'Description: You have recently been diagnosed with depression, and you want to learn more about the condition to better understand your symptoms and treatment options. However, with so much information available online, it can be overwhelming and challenging to know where to start or which sources to trust. You want to find reliable, accurate information that can help you make informed decisions about your mental health care.', 
     'task': 'Task: Use ChatGPT to get guidance on finding trustworthy and relevant information about depression.'}
]

@views.route('/', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

#@views.route('/without/<int:participant_id>', methods=['GET', 'POST'])
#def without_chatbot(participant_id):
#    return render_template("without.html", participant_id=participant_id)
@views.route('/submit', methods=['POST'])
def submit():
    context_choice = request.form.get('contextChoice')
    participant_id = request.form.get('participantId')

    if context_choice == 'with':
        #
        return redirect(url_for('views.scenario_page', participant_id=participant_id,scenario_id=0))
    elif context_choice == 'without':
        return redirect(url_for('views.scenario_page_without', participant_id=participant_id,scenario_id=0))
   
# ####################################################################################
user_chat_history = {}


@views.route('/with/<int:participant_id>/<scenario_id>', methods=['GET', 'POST'])
def scenario_page(scenario_id, participant_id):
    context_choice = 'with'
    scenario_id = int(scenario_id)
    scenario = scenarios[scenario_id]
    new_s_id = scenario_id

    visited_scenarios = session.get(f'visited_scenarios_{participant_id}', [])

    if request.method == 'POST':
        message = ''
        if request.form.get('message-input'):
            message = request.form.get('message-input')
            
            # Check if the participant ID exists in the user_chat_history dictionary
            if participant_id not in user_chat_history:
                user_chat_history[participant_id] = {}
            
            # Check if the scenario ID exists for the participant
            if scenario_id not in user_chat_history[participant_id]:
                user_chat_history[participant_id][scenario_id] = []
            
            user_chat_history[participant_id][scenario_id].append({"Question": message})
            bot_response = chatbot_with(user_chat_history[participant_id][scenario_id], message, scenario)
            formatted_response = bot_response.replace('\n', '<br>').replace('**', '').replace('###', '')
            user_chat_history[participant_id][scenario_id].append({"Response": formatted_response})
            save_data_for_with(participant_id, context_choice, scenario_id, user_chat_history[participant_id][scenario_id])
            return jsonify({"bot_response": formatted_response})
        else:
            visited_scenarios.append(scenario_id)
            session[f'visited_scenarios_{participant_id}'] = visited_scenarios
            unvisited_scenarios = [i for i in range(8) if i not in visited_scenarios]
            if len(unvisited_scenarios) == 0:
                session.pop(f'visited_scenarios_{participant_id}', None)
                return render_template("thanks.html")
            new_s_id = unvisited_scenarios[random.randint(0, len(unvisited_scenarios)-1)]
            return redirect(url_for('views.scenario_page', scenario_id=new_s_id, participant_id=participant_id))

    # Retrieve the chat history for the specific participant and scenario
    chat_history = user_chat_history.get(participant_id, {}).get(scenario_id, [])

    return render_template("with.html", participant_id=participant_id, chat_history=chat_history,
                           scenario=scenario, scenario_id=new_s_id)
###pass scenario as a parameter 
def chatbot_with(chat_history_list, message, scenario):
    # Assume chat_history_list is a list of dictionaries, each containing 'role' and 'content' keys
    messages = [
        {"role": "system","content": "You are a mental health chatbot"},
        {"role": "system", "content": str(scenario)},
        {"role": "system", "content": str(chat_history_list)},
        {"role": "user", "content": str(message)}
    ]

    response = client.chat.completions.create(model="gpt-4-turbo-preview",
    messages=messages)
    
    bot_response = response.choices[0].message.content
    
    return bot_response
####################################################################################
#need a function to save data to csv.file: 1. participant_id, 2. chatbot type 3. scenario_id, 4. chat_history_list
def save_data_for_with(participant_id, context_choice, scenario_id, chat_history_list):
    with open('data_with.csv', 'a') as f: 
        f.write(f"{participant_id},{context_choice}, {scenario_id},{chat_history_list}\n")

    

   
#######without context######
@views.route('/without/<int:participant_id>/<scenario_id>', methods=['GET', 'POST'])
def scenario_page_without(scenario_id, participant_id):
    context_choice = 'without'
    scenario_id = int(scenario_id)
    scenario = scenarios[scenario_id]
    new_s_id = scenario_id

    visited_scenarios = session.get(f'visited_scenarios_{participant_id}', [])

    if request.method == 'POST':
        message = ''
        if request.form.get('message-input'):
            message = request.form.get('message-input')
            
            # Check if the participant ID exists in the user_chat_history dictionary
            if participant_id not in user_chat_history:
                user_chat_history[participant_id] = {}
            
            # Check if the scenario ID exists for the participant
            if scenario_id not in user_chat_history[participant_id]:
                user_chat_history[participant_id][scenario_id] = []
            
            user_chat_history[participant_id][scenario_id].append({"Question": message})
            bot_response = chatbot_without(user_chat_history[participant_id][scenario_id], message)
            formatted_response = bot_response.replace('\n', '<br>').replace('**', '').replace('###', '')
            user_chat_history[participant_id][scenario_id].append({"Response": formatted_response})
            save_data_for_without(participant_id, context_choice, scenario_id, user_chat_history[participant_id][scenario_id])
            return jsonify({"bot_response": formatted_response})
        else:
            visited_scenarios.append(scenario_id)
            session[f'visited_scenarios_{participant_id}'] = visited_scenarios
            unvisited_scenarios = [i for i in range(8) if i not in visited_scenarios]
            if len(unvisited_scenarios) == 0:
                session.pop(f'visited_scenarios_{participant_id}', None)
                return render_template("thanks.html")
            new_s_id = unvisited_scenarios[random.randint(0, len(unvisited_scenarios)-1)]
            return redirect(url_for('views.scenario_page_without', scenario_id=new_s_id, participant_id=participant_id))

    # Retrieve the chat history for the specific participant and scenario
    chat_history = user_chat_history.get(participant_id, {}).get(scenario_id, [])

    return render_template("without.html", participant_id=participant_id, chat_history=chat_history,
                           scenario=scenario, scenario_id=new_s_id)
###do not need to pass parameter to this function
def chatbot_without(chat_history_list, message):
   
    messages = [
        {"role": "system","content": "You are a mental health chatbot"},
        #{"role": "system", "content": str(scenario)},
        {"role": "system", "content": str(chat_history_list)},
        {"role": "user", "content": str(message)}
    ]

    response = client.chat.completions.create(model="gpt-4-turbo-preview",
    messages=messages)
    
    bot_response = response.choices[0].message.content
    
    return bot_response
####################################################################################
#need a function to save data to csv.file: 1. participant_id, 2. chatbot type 3. scenario_id, 4. chat_history_list
def save_data_for_without(participant_id, context_choice, scenario_id, chat_history_list):
    with open('data_without.csv', 'a') as f: 
        f.write(f"{participant_id},{context_choice}, {scenario_id},{chat_history_list}\n")