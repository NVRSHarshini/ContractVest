from dash import dcc, html
from dash.dependencies import Input, Output, State
import io
import fitz  # PyMuPDF library for PDF processing
from docx import Document
import pandas as pd
import dash
# With these lines

import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import fitz
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import base64

import dash_bootstrap_components as dbc
import openai
import openpyxl

import json
# OpenAI API key
openai.api_key = ('')

df = pd.DataFrame()


# Custom colors
table_header_color = '#427D9D'
border_color = '#9BBEC8'
pie_chart_colors = ['#164863', '#9BBEC8']

# Create Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)



# Global variables to store file contents
mca_contents = None
checklist_contents = None

# Layout
app.layout = html.Div(children=[
    # Top bar with colored background for app name
    html.Div(
        className='app-header',
        style={
            'font-family': 'Roboto, sans-serif',
            'background-color': '#164863',
            'padding': '10px',
            'color': 'white',
        },
        children=[
            html.H1('ContractVest V1.0', style={'margin': '0px', 'text-align': 'center'}),
            html.Br(),
            html.P('Bullet Proof Your Contractual Agreements', style={'text-align': 'center'}),
        ]
    ),

    # File Upload Section
    html.Div(className='container', children=[
        html.Div(className='file-upload-container', children=[
            # MCA File Upload
            html.Div(className='file-upload', children=[
                dcc.Upload(
                    id='upload-mca',
                    children=[
                        html.Div([
                            'Drag and Drop your ',
                            html.Strong('Contract'),
                            ' files here Or click to browse',
                            html.Button('Upload File', style={
                                'margin-left': '350px',
                                'background-image': 'linear-gradient(-180deg, #37AEE2 0%, #1E96C8 100%)',
                                'border-radius': '.5rem',
                                'box-sizing': 'border-box',
                                'color': '#FFFFFF',
                                'font-size': '20px',
                                'justify-content': 'center',
                                'text-decoration': 'none',
                                'border': '0',
                                'cursor': 'pointer',
                                'user-select': 'none',
                                'height': '50px',
                                'width': '150px',
                                'lineHeight': '40px',
                            })
                        ])
                    ],
                    style={
                        'width': '100%',
                        'height': '63px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'backgroundColor': '#9BBEC8',
                        'textAlign': 'center',
                        'margin': '20px',
                        'font-size': '20px'

                    },
                    multiple=False
                ),

                dbc.Alert(
                    id="mca_alert",
                    is_open=False,
                    duration=2000,
                    fade=True,
                    style={'margin-left': '50px'}
                ),
            ], style={'padding-bottom': '30px'}, ),

            # Checklist File Upload
            html.Div(className='file-upload', children=[
                dcc.Upload(
                    id='upload-checklist',
                    children=[
                        html.Div([
                            'Drag and Drop your ',
                            html.Strong('Checklist'),
                            ' file here Or click to browse',
                            html.Button('Upload File', style={
                                'margin-left': '350px',
                                'background-image': 'linear-gradient(-180deg, #37AEE2 0%, #1E96C8 100%)',
                                'border-radius': '.5rem',
                                'box-sizing': 'border-box',
                                'color': '#FFFFFF',
                                'font-size': '20px',
                                'justify-content': 'center',
                                'text-decoration': 'none',
                                'border': '0',
                                'cursor': 'pointer',
                                'user-select': 'none',
                                'height': '50px',
                                'width': '150px',
                                'lineHeight': '40px',
                            })
                        ])
                    ],
                    style={
                        'width': '100%',
                        'height': '69px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'backgroundColor': '#9BBEC8',
                        'textAlign': 'center',
                        'margin': '20px',
                        'font-size': '20px',
                    },
                    multiple=False
                ),

                dbc.Alert(
                    id="checklist-success-alert",
                    is_open=False,
                    duration=2000,
                    fade=True,
                    style={'margin-left': '50px'}
                ),
            ], style={'padding-bottom': '50px'}, ),

        ], style={
            'display': 'center',
            'padding-top': '120px'
        }),
        # Submit Button
        html.Button('Run Checklist', id='submit-button', n_clicks=0, style={
            'position': 'relative',
            'left': '560px',
            'background-image': 'linear-gradient(-180deg, #37AEE2 0%, #1E96C8 100%)',
            'border-radius': '.5rem',
            'box-sizing': 'border-box',
            'color': '#FFFFFF',
            'font-size': '20px',
            'justify-content': 'center',
            'text-decoration': 'none',
            'border': '0',
            'cursor': 'pointer',
            'user-select': 'none',
            'width': '200px',  # Adjust the width as needed
            'height': '50px',  # Adjust the height as needed
        }),
        
        dbc.Alert(
            id="Nofile",
            is_open=False,
            duration=3000,
            fade=True,
            style={
           'width': '50%',  
           'background-color': '#ff4757',  
           'color': 'white',  
           'margin': 'auto',  
           'margin-top': '20px',  
           'text-align': 'center',  
       })
        

    ]),
            # Add loading spinner and results container
       dcc.Loading(
            id="loading",
            type="circle",
            children=[
                html.Div(id='loading-output'),
                # Collapsible div
                html.Div(id='printedContent'),
            ],
            style={'marginTop': '50px'}
        ),
  
])

            
                
            
            
            
#..............all functions.....

def process_pdf_content(pdf_data):
    try:
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page_number in range(doc.page_count):
            page = doc[page_number]
            text += page.get_text()
            print("from pdf_converter",text)
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def upload_excel_as_df(file_content):
    try:
        # Assuming file_content is bytes
        print("from upload as df_checklist:",pd.read_excel(io.BytesIO(file_content), engine='openpyxl'))
        return pd.read_excel(io.BytesIO(file_content), engine='openpyxl')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

'''
def query_openai(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",  
            prompt=prompt,
            temperature=0,
            max_tokens=750
        )
        return response['choices'][0]['text']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
      
def create_analysis_prompt(checklist_items, contract_text):
    prompt = ("Analyze the uploaded Contractual Agreement file and determine if the checklist items in the uploaded Excel File are satsified or not. "
              "For each item provide in-depth analysis."
              "Even if the clause is explicitly included in the agreement, the analysis and sugessted amendments/improvements must also be done accordingly. "
              "The exact section number based on the category/clause/sub-clause of the checklist items from the contractual agreement must be mentioned for every checklist item. "
              "It is very critical that you answer only as the above object and JSON stringify it as a single string. "
              "Don't include any other verbose explanations and don't include the markdown syntax anywhere.\n\n")
    prompt += "Example of format with proper spacing:\n"
    prompt += '{\n'
    prompt += '  "Checklist Item 1: Clause for pre-existing IP": {\n'
    prompt += '    "S.No": "1",\n'
    prompt += '    "Status": "Satisfied/Not satisfied",\n'
    prompt += '    "Category": "Intellectual Property Rights",\n'
    prompt += '    "Section Number": "4.1.1",\n'
    prompt += '    "Analysis": "Your analysis here",\n'
    prompt += '    "Suggestions": "Your suggested amendment here"\n'
    prompt += '  },\n'
    prompt += '  "Checklist Item 2: Limitation of Libaility should be limited": {\n'
    prompt += '    "S.No": "2",\n'
    prompt += '    "Status": "Satisfied/Not satisfied",\n'
    prompt += '    "Category": "Libaility",\n'
    prompt += '    "Section Number": "6",\n'
    prompt += '    "Analysis": "Your analysis here",\n'
    prompt += '    "Suggestions": "Your suggested amendment here"\n'
    prompt += '  }\n'
    prompt += '}\n\n'
 
    prompt += "Checklist Items:\n"
    for item in checklist_items:
        prompt += f"- {item}\n"
 
    prompt += "\nContractual Agreement (Excerpt):\n" + contract_text + "\n\n"
    prompt += "Begin your JSON analysis below:\n-----------------------------\n"
    return prompt

def parse_openai_response(response_text):
    print(response_text)
    try:
        response_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return pd.DataFrame(columns=['S.No', 'Status', 'Category', 'Section Number', 'Analysis', 'Suggestions'])

    serial_no = 1
    rows = []

    for item, details in response_data.items():
        row = {
            "S.No": details.get("S.No", serial_no),
            "Category": details.get("Category", "Unknown"),
            "Checklist Item": item,
            "Status": details.get("Status", ""),
            "Section Number": details.get("Section Number", ""),
            "Analysis": details.get("Analysis", ""),
            "Suggestions": details.get("Suggestions", "")
        }
        rows.append(row)
        serial_no += 1

    df = pd.DataFrame(rows)
    print(df)
    return df


  '''
  
def query_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "system", "content": "You are a helpful assistant that analyzes contracts."}, {"role": "user", "content": prompt}],
        )

        # Extract the generated content from the response
        generated_content = response['choices'][0]['message']['content']

       
        return generated_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
'''
q:if the uploaded cheklist items are fulfilled/satisfied
cont:smart AI/legal responsible for verifying if the uploaded conrtractual doc fulfills the checklist criteria 
info---sno.same as cheklist items 
        sta:satisfied with suggtn
        

'''


def create_analysis_prompt(checklist_items, contract_text):
    prompt_text = {
    "question": (f'Analyze the Contractual Agreement "{contract_text}" and determine the satisfaction of each checklist item from the uploaded Excel file "{checklist_items}". '),
    "context": "You are a smart legal Assistant responsible for verifying and analyzing if the contractual documentsfulfills the checklist criteria.",
    "information": "These are the details of output schema:"
                    'Checklist Item 1: provide the checklist items from uploaded Excel": {\n'
                    '    "S.No": "same from {checklist_items}",\n'
                    '    "Status": "Satisfied/Not satisfied based on the analysis",\n'
                    '    "Category": "category of checklist item same from {checklist_items}",\n'
                    '    "Section Number": "If satisfied, provide the section number",\n'
                    '    "Analysis": "Your analysis here",\n'
                    '    "Suggestions": "Your suggested amendment here"\n'
                    '  },\n'    ,
    "instruction":"Provide detailed analysis for each item, including suggestions for amendments or improvements, even if clauses are already included. "
                   '"Ensure to mention ACCURATE section numbers for all checklist items."'
                   '"Mention the exact section numbers from the contract relevant to each checklist item. "'
                   '"Provide analysis only for checklist items present in the uploaded Excel file. "'
                   '"Format the response in a structured JSON format with each item as a key, including analysis, suggestions,do not include any other verbose explanations "'
                   ' Example of format with proper spacing:\n'
                   '{\n'
                   '  "Checklist Item 1: Clause for pre-existing IP": {\n'
                   '    "S.No": "1",\n'
                   '    "Status": "Satisfied",\n'
                   '    "Category": "Intellectual Property Rights",\n'
                   '    "Section Number": "4.1.1",\n'
                   '    "Analysis": "Your analysis here",\n'
                   '    "Suggestions": "Your suggested amendment here"\n'
                   '  },\n'
                   '  "Checklist Item 2: Limitation of Liability should be limited": {\n'
                   '    "S.No": "2",\n'
                   '    "Status": "Not satisfied",\n'
                   '    "Category": "Liability",\n'
                   '    "Section Number": "6",\n'
                   '    "Analysis": "Your analysis here",\n'
                   '    "Suggestions": "Your suggested amendment here"\n'
                   '  }\n'
                   '}\n\n'
    "ResponseFormat:\n"
                    'The extracted elements should be in the following JSON format: The output should be a\n'
                    'markdown code snippet formatted in the following schema, including the leading and '
                    '    trailing "```json" and "```":'
                    '    ```json'                       
                 
                    '{\n'
                    '  "Checklist Item 1: "string"//Checklist category": {\n'
                    '    "S.No": "integer"//,\n'
                    '    "Status": "string"// "Satisfied/Not satisfied",\n'
                    '    "Category":  "string"//"Intellectual Property Rights",\n'
                    '    "Section Number":  "string"//"If satisfied, provide the section number",\n'
                    '    "Analysis":  "string"//"Your analysis here",\n'
                    '    "Suggestions":  "string"//"Your suggested amendment here"\n'
                    '  },\n'
                    
                    '}'
                    '```'
                     '  I want you to extract the features all the columns as a key-value pair like mentioned above '
                     '   in a JSON string'
                    '```'

                   
                   ,}
      # You can add more information or prompts as needed
      

    for item in checklist_items:
        prompt_text["instruction"] += f"- {item}\n"

    prompt_text["instruction"] += ("\nContractual Agreement (Excerpt):\n" + contract_text + "\n\n"
                                   "Begin your JSON analysis below:\n-----------------------------\n")

    return json.dumps(prompt_text)

import json
import pandas as pd

import json
import pandas as pd

def parse_openai_response(response_text):
    try:
        # Find the index where the JSON content begins
        json_start_index = response_text.find("{")
        
        # Check if JSON content is found
        if json_start_index != -1:
            # Extract the JSON content
            json_content = response_text[json_start_index:]
            
            # Remove any trailing characters after the JSON
            json_content = json_content.rstrip('\n').rstrip('```')
            
            # Parse the JSON
            response_data = json.loads(json_content)
        else:
            raise ValueError("No JSON content found in the response.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return pd.DataFrame(columns=['S.No', 'Status', 'Category', 'Section Number', 'Analysis', 'Suggestions'])

    serial_no = 1
    rows = []

    for item, details in response_data.items():
        row = {
            "S.No": details.get("S.No", serial_no),
            "Category": details.get("Category", "Unknown"),
            "Checklist Item": item,
            "Status": details.get("Status", ""),
            "Section Number": details.get("Section Number", ""),
            "Analysis": details.get("Analysis", ""),
            "Suggestions": details.get("Suggestions", "")
        }
        rows.append(row)
        serial_no += 1

    df = pd.DataFrame(rows)
    print(df)
    return df


'''
def parse_openai_response(response_text):
    print(response_text)
    try:
        # Remove the "response ```json" prefix if present
        response_text = response_text.replace("response ```json", "").strip()
        
        # Parse the JSON
        response_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return pd.DataFrame(columns=['S.No', 'Status', 'Category', 'Section Number', 'Analysis', 'Suggestions'])

    serial_no = 1
    rows = []

    for item, details in response_data.items():
        row = {
            "S.No": details.get("S.No", serial_no),
            "Category": details.get("Category", "Unknown"),
            "Checklist Item": item,
            "Status": details.get("Status", ""),
            "Section Number": details.get("Section Number", ""),
            "Analysis": details.get("Analysis", ""),
            "Suggestions": details.get("Suggestions", "")
        }
        rows.append(row)
        serial_no += 1

    df = pd.DataFrame(rows)
    print(df)
    return df

    print(response_text)
    try:
        response_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return pd.DataFrame(columns=['S.No', 'Status', 'Category', 'Section Number', 'Analysis', 'Suggestions'])

    serial_no = 1
    rows = []

    for item, details in response_data.items():
        row = {
            "S.No": details.get("S.No", serial_no),
            "Category": details.get("Category", "Unknown"),
            "Checklist Item": item,
            "Status": details.get("Status", ""),
            "Section Number": details.get("Section Number", ""),
            "Analysis": details.get("Analysis", ""),
            "Suggestions": details.get("Suggestions", "")
        }
        rows.append(row)
        serial_no += 1

    df = pd.DataFrame(rows)
    print(df)
    return df
'''
#....................

#....................#

#.#
#.........callbacks.....

# Callback to update collapsible div contents on button click
@app.callback(
    Output("printedContent", "children"),
    [Input("submit-button", "n_clicks")],
    [State("upload-mca", "contents"),
     State("upload-checklist", "contents"),
     State("upload-mca", "filename"),
     State("upload-checklist", "filename")]
)
def update_collapsible_content(n_clicks, mca_contents, checklist_contents, mca_filename, checklist_filename):
    if n_clicks is None or n_clicks <= 0:
        raise PreventUpdate

    # Check if MCA file and checklist file are uploaded
    if mca_contents is None or checklist_contents is None:
        # Display alert if files are not uploaded
        alert_text = "Please upload Contract agreement  and Checklist file before running the checklist."
        return html.Div(dbc.Alert(
            id="Nofile",
            is_open=False,
            duration=3000,
            fade=True,
            children=alert_text,
            style={
            'width': '50%',  
            'background-color': '#ff4757',  
            'color': 'white',  
            'margin': 'auto',  
            'margin-top': '20px',  
            'text-align': 'center',  
        }
        ))

    try:
        # Decode file contents
        mca_content_decoded = process_pdf_content(base64.b64decode(mca_contents.split(",")[1]))
        checklist_content_decoded = upload_excel_as_df(base64.b64decode(checklist_contents.split(",")[1]))

        # Extract information from filenames
        contract_file_name = mca_filename  # Use the MCA filename as contract_file_name
        checklist_file_name = checklist_filename

        # Generate the prompt for analysis
        prompt = create_analysis_prompt(checklist_content_decoded, mca_content_decoded)

        # Query OpenAI and print the response
        response = query_openai(prompt)
        print("response", response)
        # Parse OpenAI response
        analysis_results = parse_openai_response(response)

        # Update the DataFrame with the OpenAI analysis results
        if isinstance(analysis_results, pd.DataFrame) and not analysis_results.empty:
            df = analysis_results
        else:
            df = pd.DataFrame(columns=['S.No', 'Status', 'Category', 'Section Number', 'Analysis', 'Suggestions'])
        # Extract information for display
        num_checklist_items = len(checklist_content_decoded)  # Example: Number of rows in the checklist dataframe
        num_satisfied = df[df['Status'] == 'Satisfied'].shape[0]  # Example: Count of 'Satisfied' rows in the result dataframe
        num_unsatisfied = df[df['Status'] == 'Unsatisfied'].shape[0]  # Example: Count of 'Unsatisfied' rows

        # Further processing of the OpenAI response and updating the displayed content
        updated_content = html.Div(
            children=[
                dcc.Loading(
                    id="loading-output",
                    type="circle",
                    children=[
                        # Table
                        html.Div(
                            children=[
                                html.H2('Results',
                                        style={'background-color': table_header_color, 'color': 'white',
                                               'text-align': 'center',
                                               'width': '80%', 'margin': '0 auto 5px'}),

                                html.Table(
                                    # Header
                                    [html.Tr([html.Th(col, style={'font-size': '20px'}) for col in df.columns],
                                             style={'background-color': '#55a2bc', 'color': 'white',
                                                    'text-align': 'center'})] +
                                    # Body
                                    [html.Tr([html.Td(value, style={'padding': '10px', 'border': f'1px solid {border_color}'})
                                              for value in row]) for row in df.values],
                                    style={'width': '80%', 'margin': '0 auto', 'border-spacing': '0 10px',
                                           'text-align': 'left'},  # Center the table, add gap between rows
                                ),

                            ],
                            style={'width': '97%', 'margin': '30px', 'text-align': 'center'}  # Center the entire content
                        ),
                        html.Div(
                            # Percentages Header
                            html.H2('Checklist Verification Statistics',
                                    style={'background-color': table_header_color, 'color': 'white',
                                           'text-align': 'center',
                                           'width': '80%', 'margin': '0 auto 5px'}),
                            style={'width': '97%', 'margin': '30px', 'text-align': 'center'}  # Center the entire content
                        ),
                        # Pie Chart
                        html.Div(
                            children=[
                                html.P(f"Contract File: {mca_filename}", style={'margin':'0px','text-align': 'center'}),
                                html.P(f"Number of Checklist Items: {num_checklist_items}", style={'margin':'0px','text-align': 'center'}),
                                html.P(f"Number of Satisfied Items: {num_satisfied}", style={'text-align': 'center'}),
                                html.P(f"Number of Unsatisfied Items: {num_unsatisfied}", style={'text-align': 'center'}),

                                # Pie Chart
                                dcc.Graph(
                                    figure={
                                        'data': [
                                            {
                                                'labels': ['Satisfied', 'Not Satisfied'],
                                                'values': df['Status'].value_counts().values.tolist(),
                                                'type': 'pie',
                                                'marker': {'colors': pie_chart_colors}
                                            },
                                        ],
                                        'layout': {
                                            'legend': {'orientation': 'h', 'x': 0.43, 'y': -0.2},
                                        },
                                    },
                                    style={'position': 'relative', 'left': '35px', 'top': '-20px'}
                                ),
                            ],
                            style={'marginTop': '50px', 'text-align': 'center'}
                        ),
                    ],
                ),
            ],
        )

        return updated_content


    except Exception as e:
        # Handle errors and display a generic error message
        #print(f"An error occurred: {e}")
        #error_message = "An error occurred during analysis. Please try again later."
        return html.Div( dbc.Alert(
            id="Nofile",
            is_open=False,
            duration=3000,
            fade=True,
            style={
           'width': '50%',  # Adjust the width as needed
           'background-color': '#ff4757',  # Change the background color to red
           'color': 'white',  # Change the text color if needed
           'margin': 'auto',  # Center the alert box horizontally
           'margin-top': '20px',  # Add margin-top to center vertically (adjust as needed)
           'text-align': 'center',  # Center the text inside the alert box
       }
        ),)




#..............................
# MCA upload callback
@app.callback(
    [Output("mca_alert", "is_open"), Output("mca_alert", "children")],
    [Input("upload-mca", "contents")],
    [State("upload-mca", "filename")],
)
def upload_mca_file(contents, filename):
    global mca_contents
    if not contents:
        raise PreventUpdate

    mca_contents = contents  # Update global variable
    print("contents mca:",type(contents))
    alert_text = f"{filename} uploaded successfully!"
    alert_color = "success"

    return contents, alert_text

# Checklist upload callback
@app.callback(
    [Output("checklist-success-alert", "is_open"), Output("checklist-success-alert", "children")],
    [Input("upload-checklist", "contents")],
    [State("upload-checklist", "filename")],
)
def upload_checklist_file(contents, filename):
    global checklist_contents
    if not contents:
        raise PreventUpdate

    checklist_contents = contents
    print("con checkl",type(contents))# Update global variable
    alert_text = f"{filename} uploaded successfully! "
    alert_color = "success"

    return contents, alert_text

# Callback to display an alert when no file is uploaded but "Run Checklist" is clicked
@app.callback(
    [Output("Nofile", "is_open"), Output("Nofile", "children")],
    [Input("submit-button", "n_clicks")],
    [State("upload-mca", "contents"),
     State("upload-checklist", "contents")]
)
def check_file_upload(n_clicks, mca_contents, checklist_contents):
    if n_clicks is None or n_clicks <= 0:
        raise PreventUpdate

    # Check if MCA file and checklist file are uploaded
    if mca_contents is None or checklist_contents is None:
        # Display alert if files are not uploaded
        alert_text = "Please upload Contract agreement  and Checklist file before running the checklist."
        return True, alert_text
    else:
        # Continue with the checklist analysis
        return False, ""


#.........................

if __name__ == '__main__':
    app.run_server(debug=True, port='2801')