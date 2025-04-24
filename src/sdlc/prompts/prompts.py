USERSTORY_GEN_INSTRNS="""You are tasked with creating a detailed user story based on the given user requirements.
Provide a single title for the user story and add all details expected from the requirements. Follow these instructions carefully:

1. **Review** the given user requirements carefully:
{user_requirements}

2. **Format the output using Markdown**.

3. **Do not include any preamble** before listing the user stories.
"""
USERSTORY_MODIFY_INSTRNS="""You are tasked with modifying the existing user stories based on the given user feedback.
Follow these instructions carefully:

1. Modify the already generated user stories  based on editorial feedback.Keep the general outline of the already generated user stories :
   - Previously generated user stories:  
   {user_stories}  
   - Editorial feedback:  
   {user_stories_review}

2. **Format the output using Markdown**.

3. **Do not include any preamble** before listing the user stories.
"""

DESIGNDOCS_GEN_INSTRNS="""
You are tasked with creating a **comprehensive design document** based on the given user stories. Follow these instructions carefully:  

1. **Review the given user stories carefully:**  
   {user_stories}  

2. **Structure the design document as follows:**  
   - **Introduction:** Provide a high-level summary of the system.  
   - **System Overview:** Describe the core functionality and scope.  
   - **Functional Requirements:** List detailed functional requirements derived from the user stories.  
   - **Use Cases:** Define key use cases and user interactions with the system.  
   - **Architecture Design:** Include a high-level architecture diagram in Markdown mermaid format.  
   - **Technology Stack:** Specify the programming languages, frameworks, and tools used.  
   - **Database Schema:** Define tables, relationships, and key constraints.  
   - **API Specifications:** Outline RESTful or GraphQL endpoints with request/response formats.  
   - **Deployment Strategy:** Explain CI/CD pipelines, hosting, and cloud infrastructure.  
   - **Security Considerations:** Detail authentication, authorization, and data protection measures.  
   - **Code Considerations:** Describe how the front-end and back-end code will be structured.  

3. **Return the final software design document in Markdown format.**  
   - Embed the **architecture diagram** as a Mermaid diagram.  
   - Ensure it covers all coding aspects, including front-end and back-end implementation details.  

"""

DESIGN_MODIFY_INSTRNS="""You are tasked with modifying the existing design documents based on the given user feedback.
Follow these instructions carefully:

1. Modify the already generated design documents based on editorial feedback.Keep the general outline of the already generated design documents :
   - Previously generated design documents:  
   {design_documents}  
   - Editorial feedback:  
   {design_review}

2. **Format the output using Markdown**.

3. **Do not include any preamble** before listing the design documents.
"""


CODE_ORCHESTRATOR__INSTRNS="""
Generate a production-level code architecture plan based on the provided design document : {design_documents}.
Follow these instructions carefully to ensure a structured and well-organized folder hierarchy:
1. Define the sub folder structure based on the design documents for placing files of related functionalities.
2. Determine file structure: Generate unique file names with appropriate extensions based on all functionalities specified in the design document.Limit the number of files to 10 or lower as applicable.
3. Group related files into subfolders based on their functionality.
4. Ensure correct naming convention:
- For each file, include its full path within the "name" key 
- Ensure every file is assigned to a subfolder when applicable.Multiple files can come under a single subfolder.
- Try to limit subfolder count to maximum of 5 or lower as applicable
5. Provide meaningful descriptions: Each file should have a clear and concise description under the "description" key, explaining its purpose and role in the system.
6. Output format: Return a JSON object containing multiple file entries, each with "name" and "description" keys for multiple files
7. Production-ready best practices: Ensure the folder structure is scalable, modular, aligning with industry standards for production environments.
"""

CODE_GEN_INSTRUCTIONS="""
Generate code contents for the code file based on the details given  file name: {codefilename} and description: {codefiledescription}.
Follow the below instructions carefully.
1. Check for any optional feedback {code_review} and generate the code accordingly.
2. Return the 'name' and 'code' for the file in JSON format.
"""

FILE_MODIFY_INSTRNS="""
Examine the code review feedback provided :{code_review}.
The existing code file names with the descriptions is as provided : {codefiletypes}
Identify the code file names that need modifications based on the descriptions and feedback provided.
If feedback requires new files to be added,provide file name and description accordingly.
Return the files to be modified with names and descriptions as a JSON object 
"""

SUMMARIZE_DESIGN_DOCS="""
Summarize the following **detailed design document** : {design_documents} to extract only the most relevant information for code review.
### **Output Format**
Provide a structured summary focusing on:
1. **System Overview**: A brief summary of the system’s purpose and functionality.
2. **Functional Requirements**: Key expected features and functionalities.
3. **Technical Requirements**: Technologies, frameworks, database structures, and any architectural constraints.
4. **Code Structure**: Expected file organization, naming conventions, and module breakdown.
5. **Security & Performance Considerations**: Any key performance optimizations or security best practices.

Return the response in **concise bullet points** to facilitate quick comparison with the generated code.Limit the word count to a maximum of 500 and make it concise.
"""

CODE_REVIEW_INSTRNS = """
You are reviewing the generated code to ensure it aligns with the design document: {design_documents}. 
Identify discrepancies, suggest modifications, and determine if new files are required based on the already generated code: {generated_code}.

Follow the below instructions:
1. Compare the generated code against the design document to identify any missing, incorrect, or incomplete implementations.
2. Ensure all functionalities described in the design document are correctly implemented.
3. Verify adherence to architecture, logic, and expected behavior.
4. Determine required modifications or if any functionality is missing. List the file names that need modifications and clearly describe the required changes.
5. Do not use Markdown formatting, bullet points, titles, or special characters. Provide a clear, structured response in plain text.
6. Output format:
   - List the names of the files that need modifications.
   - Provide a clear explanation of the issues in each file.
   - Describe specifically what needs to be added, removed, or changed.
   - Use simple sentences and paragraphs without special formatting.
"""

SECURITY_REVIEW_INSTRNS="""
You are a security expert tasked with reviewing the security of a set of generated code files : {generated_code} where

- The keys represent file names with extensions (e.g., "app.py", "index.js", "config.yaml").
- The values contain the source code of each file.

Your task:
1. Analyze each file for security vulnerabilities.
2. Identify common security risks, including but not limited to:
   - Hardcoded credentials, API keys, or secrets.
   - Injection vulnerabilities (SQL injection, command injection, XSS, etc.).
   - Insecure authentication or missing authorization checks.
   - Use of outdated or vulnerable dependencies.
   - Weak cryptographic practices.
   - Improper input validation and sanitization.
   - Insecure file handling or deserialization risks.
   - Lack of logging or excessive logging of sensitive data.
   - Misconfigured security settings in configuration files.

Format your response in **Markdown** without any preamble:
"""

TESTCASES_GEN_INSTRNS="""
You are an expert in software testing and test case generation. Given a design document containing functional, technical, and structural requirements, generate a consolidated test case table. Each test case should include key attributes like test scenario, test steps, expected result, and test type.

Input:
The design document contains the following details:{design_documents}

Functional Requirements - Describe how the system should behave.

Technical Requirements - Specify implementation details, integrations, and constraints.

Structural Requirements - Define architectural and infrastructure-level details.

Output Format (Table Format) without a preamble:
Provide a structured response in a tabular format with the following columns:

Test Case ID - Unique identifier for the test case.

Use Case - The specific use case being tested.

Test Scenario - A brief description of what is being tested.

Test Steps - Step-by-step procedure to execute the test.

Expected Result - The anticipated system behavior after execution.

Test Type - Functional, Integration, Structural, or Performance.
"""

DEPLOYMENT_INSTRUCTIONS="""
You are an SDLC deployment assistant. You will be given a software design document.

Your task is to:

1. **Analyze the document** and determine if it includes any deployment-related preferences or decisions. Look for:
   - Platforms (e.g., AWS, Heroku, Vercel, Netlify, Docker, Kubernetes, etc.)
   - Hosting types (e.g., static, containerized, serverless)
   - Infrastructure details (e.g., EC2, S3, Cloud Run, etc.)
   - CI/CD or version control notes relevant to deployment

2. If **deployment is mentioned**, extract the method or platform clearly.

3. If **no deployment is mentioned**, pick a **suitable and commonly used deployment platform at random** (such as Heroku, Netlify, or AWS EC2) based on the application's likely needs.

4. Provide **clear deployment steps** for the identified or assumed deployment method.

### Input:
{design_document}

### Output:
- **Detected or Assumed Deployment Method:** <deployment_type_or_platform>
- **Deployment Steps:**
  1. ...
  2. ...
  3. ...

"""

MONITORING_FB_INSTRNS="""
You are an experienced DevOps and SRE (Site Reliability Engineering) expert.

Below are the deployment instructions for a software application. Your task is to generate actionable, concise, and technically sound instructions for:

1. **Monitoring** the system after deployment.
2. **Collecting and analyzing feedback**, including error logs, user input, and performance metrics.

---  
### Deployment Instructions:
{deployment_instructions}

---

### Output Format:

## Monitoring Instructions
- (bullet point list of what and how to monitor based on deployment details)

## Feedback Collection Instructions
- (bullet point list of how feedback should be collected and reviewed post-deployment)

Focus on tools, logs, services, metrics, and automation where applicable.

"""

MAINTANENCE_INSTRNS="""
You are assisting with software maintenance based on user feedback.

Optional Feedback Received:
{user_feedback}
If no feedback received, respond that no user feedback for maintanence received and generate a project-specific maintenance plan.
Else, if feedback received,based on this feedback, analyze the likely issue and generate a project-specific maintenance plan that includes:

- Summary of the problem

- Likely cause or affected area

- Recommended fix or update

- Tests or documentation to update

- Any potential security or deployment impact

Output is in markdown format as follows:

## Maintenance Plan

### User Feedback
"{user_feedback}"

### Likely Cause
...

### Suggested Fix or Update
...

### Tests & Docs
...

### Security / Deployment Notes
...
"""