# How do we plan to collaborate?
- We try to divide tasks in the meetings so that we can work individually
    - Team members can volunteer for tasks, otherwise the least-occupied person will be assigned the remaining tasks
- Meetings will preferably be held in-person, but can also be held on Discord if needed (illness, abroad etc)
- We plan to meet 1-2 times per week, preferably before or after the lectures
- We intend to not work around Easter, unless needed to meet assignment deadlines
- We use `clang-format` for the formatting _(recommended from mistral)_
- Everyone is responsible for unit testing their own code _(recommended from mistral)_
    - Use Catch2 for unit tests
    - 80% line coverage

# How do we ensure that everyone in our group stays informed about the individual contributions?
- Keep each other updated on Discord and during the meetings
- Everyone should keep their assigned issues updated on GitLab, so that others can see the progress

# How do we ensure knowledge transfer among our team members?
- Sharing tutorial / other resources with each other on Discord (e.g. "good" C++ tutorials as a thread on Discord) 
- Giving each other feedback during code reviews (e.g. Merge Requests) to improve each other's code
- Putting diagrams on the GitLab wiki to help the understanding (e.g. System Design) 
- Helping each other understand new concepts in-person, e.g. with presentations _(recommended from mistral)_

# What is our usual communication plan?
- Discord for daily communication
- Planning meeting to assign tasks (but also continuously, if someone "runs out of issues") 
- Review meeting 
- GitLab board for staying up-to-date with each other

# How will we solve conflicts?
- In a constructive matter, stay polite
- Listen to each other's arguments
- Communicate with each other, express opinions and reasoning, judgement-free 

# How do you plan to ensure responsible use of LLMs in your project and how do you transparently and traceably document the use of LLMs? 
- Document usage of LLMs
    - LLMs cannot be used for the text of the final report
    - We are mostly using LLMs for code and code comments generation, test case generation and debugging
    - Generated code: document usage in the source code file (now we can refer to the screenshot/screen recording/text file name in the llm-dialogues folder)
    - Generated text: document usage in the text file (Google Docs, Markdown) (also refer to the file name in the llm-dialogues folder)
    - The dialogue with the LLM must be stored in the repo in the /llm-dialogues folder as a screenshot/screen recording or a text file
    - Check generated content, don't simply trust it; and make sure you understand the generated code
    - Document which model has been used
    - If in doubt, consult several LLMs and choose the best result, or compare with online sources
    - Record a screencast if the assignment asks us to do so

