# Import required libraries
import re
import os
import base64
import urllib.parse
import uuid
import time
import math
import dash
import dash_table
import dash_bio as dashbio
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server
server.secret_key = '\xfd\x00R\xb5\xbd\x83_t\xed\xdf\xc4\na\x08\xf7K\xc4\xfd\xa2do3\xa5\xdd'


UPLOAD_DIRECTORY = '/PrimeDesign/reports'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@server.route('/download/<path:path>')
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

peg_design_tmp = {'pegRNA group':[],'type':[], 'spacer sequence':[],'spacer GC content':[],'PAM':[],'strand':[],'peg-to-edit distance':[],'nick-to-peg distance':[],'pegRNA extension':[], 'extension first base':[],'PBS length':[],'PBS GC content':[],'RTT length':[],'RTT GC content':[],'annotation':[],'spacer top strand oligo':[], 'spacer bottom strand oligo':[], 'pegRNA extension top strand oligo':[], 'pegRNA extension bottom strand oligo':[]}
df_tmp = pd.DataFrame.from_dict(peg_design_tmp)
 
def serve_layout():

    # session_id = str(uuid.uuid4())
    session_id = str(time.strftime("%Y%m%d_%I.%M.%S.", time.localtime())) + str(int(round(time.time() * 1000)))[-2:]

    return html.Div([

        dcc.Location(id='url', refresh=False),
        html.Div(session_id, id='session-id', style={'display': 'none'}),

        html.Div([
            html.Img(src=app.get_asset_url('primedesign_logo.png'), width = '350px', style = {'margin-bottom': '0px', 'margin-right': '20px', 'padding-left': '15px'}),

            dcc.Link('Design', href='/', style = {'color':'#6cb7ff', 'text-decoration':'none', 'margin-right':'25px', 'font-size':'18px'}),
            dcc.Link('About', href='/about', style = {'color':'#6cb7ff', 'text-decoration':'none', 'margin-right':'25px', 'font-size':'18px'}),
            dcc.Link('Help', href='/help', style = {'color':'#6cb7ff', 'text-decoration':'none', 'margin-right':'25px', 'font-size':'18px'}),

            dbc.Button(children = 'PrimeDesign GIF', outline = False, id='open', style = {'color':'#6cb7ff'}),
            dbc.Modal(
                [
                    dbc.ModalHeader("Navigating PrimeDesign"),
                    dbc.ModalBody(html.Img(src=app.get_asset_url('primedesign_demo.gif'), style = {'display':'block', 'margin-left':'auto', 'margin-right':'auto', 'width':'80%'}),),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", className="ml-auto")
                    ),
                ],
                id="modal",
            ),

            ]),

        html.Div(id='page-content')
    ])

app.layout = serve_layout

about_page = html.Div([

    html.Br(),

    html.H3('What is PrimeDesign?'),
    html.Div([
        '''PrimeDesign is a flexible and comprehensive design tool for prime editing.
        PrimeDesign can be utilized for the installation of 
        '''
        ], style = { 'display':'inline', 'color':'#6a6a6a'}),

    html.Span('substitution', style = {'color':'#1E90FF', 'display':'inline'}),
    html.Span(', ', style = {'display':'inline', 'color':'#6a6a6a'}),
    html.Span('insertion', style = {'color':'#3CB371', 'display':'inline'}),
    html.Span(', and ', style = {'display':'inline', 'color':'#6a6a6a'}),
    html.Span('deletion', style = {'color':'#DC143C', 'display':'inline'}),

    html.Div([
        ''' edits, and is generalizable for both single and combinatorial edits.
        Given an edit of interest, PrimeDesign identifies all possible prime editing guide RNAs (pegRNAs) and nicking guide RNAs (ngRNAs) within a specified parameter range for the optimization of prime editing.
        In addition to the web application, PrimeDesign is also available as a stand-alone command line tool for more flexible and higher-throughput PrimeDesign functions.
        The command line tool is available here: 
        '''
        ], style = {'display':'inline', 'color':'#6a6a6a'}),

    html.A(
            'https://github.com/pinellolab/PrimeDesign',
            id='github-link',
            href="https://github.com/pinellolab/PrimeDesign",
            target='_blank',
            style = {'text-decoration':'none', 'display':'inline'}
        ),

    html.H3('Reference'),

    html.Div([

        '''Manuscript in preparation!
        '''

        ], style = {'color':'#6a6a6a'}),

    html.H3('Contact'),

    html.Div([

        '''If you have any questions or concerns, please don't hesitate to contact us at jyhsu (at) mit.edu.
        '''

        ], style = {'color':'#6a6a6a'}),

    html.H3('Labs'),

    html.A(
            'Pinello Lab',
            id='pinellolab-link',
            href="http://pinellolab.org/",
            target='_blank',
            style = {'text-decoration':'none', 'display':'inline', 'font-size':'20px', 'color':'#6a6a6a', 'margin-right':'15px'}
        ),

    html.Label('|', style = {'font-size':'20px', 'display':'inline', 'color':'#6a6a6a'}),

    html.A(
            'Joung Lab',
            id='jounglab-link',
            href="http://www.jounglab.org/",
            target='_blank',
            style = {'text-decoration':'none', 'display':'inline', 'font-size':'20px', 'color':'#6a6a6a', 'margin-right':'15px', 'margin-left':'15px'}
        ),

    html.Label('|', style = {'font-size':'20px', 'display':'inline', 'color':'#6a6a6a'}),

    html.A(
            'Liu Lab',
            id='liulab-link',
            href="https://liugroup.us/",
            target='_blank',
            style = {'text-decoration':'none', 'display':'inline', 'font-size':'20px', 'color':'#6a6a6a', 'margin-left':'15px'}
        ),

    ], style = {'padding': '15px','margin': '0px'}),

help_page = html.Div([

    html.Br(),

    html.H3('What is PrimeDesign?'),
    html.Div([
        '''PrimeDesign is a flexible and comprehensive design tool for prime editing.
        PrimeDesign can be utilized for the installation of 
        '''
        ], style = { 'display':'inline', 'color':'#6a6a6a'}),

    html.Span('substitution', style = {'color':'#1E90FF', 'display':'inline'}),
    html.Span(', ', style = {'display':'inline', 'color':'#6a6a6a'}),
    html.Span('insertion', style = {'color':'#3CB371', 'display':'inline'}),
    html.Span(', and ', style = {'display':'inline', 'color':'#6a6a6a'}),
    html.Span('deletion', style = {'color':'#DC143C', 'display':'inline'}),

    html.Div([
        ''' edits, and is generalizable for both single and combinatorial edits.
        Given an edit of interest, PrimeDesign identifies all possible prime editing guide RNAs (pegRNAs) and nicking guide RNAs (ngRNAs) within a specified parameter range for the optimization of prime editing.
        In addition to the web application, PrimeDesign is also available as a stand-alone command line tool for more flexible and higher-throughput PrimeDesign functions.
        The command line tool is available here: 
        '''
        ], style = {'display':'inline', 'color':'#6a6a6a'}),

    html.A(
            'https://github.com/pinellolab/PrimeDesign',
            id='github-link',
            href="https://github.com/pinellolab/PrimeDesign",
            target='_blank',
            style = {'text-decoration':'none', 'display':'inline'}
        ),

    html.H3('How do you use PrimeDesign?'),

    html.H5('Input sequence'),
    html.Div([
        '''PrimeDesign only requires a single input that encodes both the reference and edit sequences. The edit encoding format is below:
        '''
        ], style = {'color':'#6a6a6a'}),

    html.Div([

        html.Br(),

        ], style = {'display':'block','line-height':'100%'}),

    html.Div([

        html.Span('Substitution', style = {'color':'#1E90FF', 'font-size':'20px'}),
        html.Span(': (reference/edit)', style = {'font-size':'20px'}),
        html.Br(),

        html.Span('Insertion', style = {'color':'#3CB371', 'font-size':'20px'}),
        html.Span(': (+insertion)', style = {'font-size':'20px'}),
        html.Br(),

        html.Span('Deletion', style = {'color':'#DC143C', 'font-size':'20px'}),
        html.Span(': (-deletion)', style = {'font-size':'20px'}),


        ], style = {'text-align':'center'}),
    
    html.Div([

        html.Br(),

        ], style = {'display':'block','line-height':'100%'}),

    html.Div([
        '''The input sequence can incorporate single or combinatorial edits by simply including the desired number of edit encodings. For example:
        '''
        ], style = {'color':'#6a6a6a'}),

    html.Div([

        html.Br(),

        ], style = {'display':'block','line-height':'100%'}),

    html.Div([

        html.Div([html.Span(['Reference sequence: '], style = {'font-weight':'bold'})], className = 'two columns'),

        html.Div([html.Span(['... CCTGCTTTCGCTGGGATCCAAGATTGGCAGCTGA'], style = {'font-family':'courier'}),
            html.Span(['A'], style = {'color':'#1E90FF', 'font-family':'courier'}),
            html.Span(['GCCG'], style = {'font-family':'courier'}),
            html.Span(['---'], style = {'color':'#3CB371', 'font-family':'courier'}),
            html.Span(['TTCC'], style = {'font-family':'courier'}),
            html.Span(['ATAG'], style = {'color':'#DC143C', 'font-family':'courier'}),
            html.Span(['TGAGTCCTTCGTCTGTGACTAACTGTGCCAAATCGTCTAGC ...'], style = {'font-family':'courier'}),
            ], className = 'ten columns'),

        ], className = 'row'),

    html.Div([

        html.Div([html.Span(['Edit sequence: '], style = {'font-weight':'bold'}),], className = 'two columns'),

        html.Div([html.Span(['... CCTGCTTTCGCTGGGATCCAAGATTGGCAGCTGA'], style = {'font-family':'courier'}),
            html.Span(['C'], style = {'color':'#1E90FF', 'font-family':'courier'}),
            html.Span(['GCCG'], style = {'font-family':'courier'}),
            html.Span(['CTT'], style = {'color':'#3CB371', 'font-family':'courier'}),
            html.Span(['TTCC'], style = {'font-family':'courier'}),
            html.Span(['----'], style = {'color':'#DC143C', 'font-family':'courier'}),
            html.Span(['TGAGTCCTTCGTCTGTGACTAACTGTGCCAAATCGTCTAGC ...'], style = {'font-family':'courier'}),
            ], className = 'ten columns'),

        ], className = 'row'),

    html.Div([

        html.Div([html.Span(['PrimeDesign input: '], style = {'font-weight':'bold'}),], className = 'two columns'),

        html.Div([html.Span(['... CCTGCTTTCGCTGGGATCCAAGATTGGCAGCTGA'], style = {'font-family':'courier'}),
            html.Span(['(A/C)'], style = {'color':'#1E90FF', 'font-family':'courier'}),
            html.Span(['GCCG'], style = {'font-family':'courier'}),
            html.Span(['(+CTT)'], style = {'color':'#3CB371', 'font-family':'courier'}),
            html.Span(['TTCC'], style = {'font-family':'courier'}),
            html.Span(['(-ATAG)'], style = {'color':'#DC143C', 'font-family':'courier'}),
            html.Span(['TGAGTCCTTCGTCTGTGACTAACTGTGCCAAATCGTCTAGC ...'], style = {'font-family':'courier'}),
            ], className = 'ten columns'),

        ], className = 'row'),

    html.Div([

        html.Br(),

        ], style = {'display':'block','line-height':'100%'}),

    html.Div([

        '''We recommend an input sequence length of >300 bp centered around the the edit(s) of interest to ensure that the complete set of pegRNAs and ngRNAs are designed.
        '''
        ], style = {'color':'#6a6a6a'}),

    html.Div([

        html.Br(),

        ], style = {'display':'block','line-height':'100%'}),

    html.H5('Navigating PrimeDesign'),

    html.Div([

        '''After you successfully construct a desired input sequence, check out the GIF below to learn how to navigate the PrimeDesign web application:
        '''

        ], style = {'color':'#6a6a6a'}),

    html.Div([

        html.Br(),

        ], style = {'display':'block','line-height':'100%'}),

    html.Img(src=app.get_asset_url('primedesign_demo.gif'), style = {'display':'block', 'margin-left':'auto', 'margin-right':'auto', 'width':'80%'}),

    ], style = {'padding': '15px','margin': '0px'}),

error_page = html.Div([

    html.Br(),
    html.Br(),
    html.Br(),

    html.H1('404 error: Page not found', style = {'text-align':'center'}),

    ]),

design_page = html.Div([

    html.Div([

        html.Div([

            html.H5('Input sequence', style = {'margin-right':'5px','display':'inline'}),
            html.Span('?', id = 'input-tooltip', style={'font-size':'11px', 'textAlign': 'center', 'color': 'white',}, className = 'dot'),

            dcc.Checklist(
                id = 'example-option',
                options=[
                    {'label': 'Substitution', 'value': 'substitution'},
                    {'label': 'Insertion', 'value': 'insertion'},
                    {'label': 'Deletion examples', 'value': 'deletion'},
                ],
                value=[],
                labelStyle={'display': 'inline'}
            ),

            dbc.Tooltip('Edit formatting examples: Substitution (ATGC/CGTA)  |  Insertion (+ATGC) or (/ATGC)  |  Deletion (-ATGC) or (ATGC/)',
                       target = 'input-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                ),

            dcc.Textarea(
                id='pe-sequence-input',
                placeholder='Enter sequence to prime edit or load example input sequence above ...\n\nEdit formatting examples: Substitution (ATGC/CGTA)  |  Insertion (+ATGC) or (/ATGC)  |  Deletion (-ATGC) or (ATGC/)',
                value='',
                style = {'width': '100%', 'margin': '0px'},
                className = 'textarea',
            ),

            html.Label(id = 'input-check', children = '', style = {'font-weight':'bold'}),
            
            ], className = 'twelve columns'),

        ], className = 'row', style = {'padding': '15px','margin': '0px'}),

    html.Div([

        html.H5('Visualize sequence'),

        dcc.Checklist(
                id = 'protein-option',
                options=[
                    {'label': 'Visualize amino acid sequence (assumes sequence is in-frame)', 'value': 'protein'},
                ],
                value=[]
            ), 

        html.Div([

            # dcc.RadioItems(
            #     id = 'sequence-option',
            #     options=[
            #         {'label': 'Reference', 'value': 'ref'},
            #         {'label': 'Edited', 'value': 'edit'},
            #     ],
            #     value='ref',
            #     labelStyle={'display': 'inline-block'}
            # ),

            html.H6('Reference DNA', style = {'margin':'0px', 'padding-bottom':'0px'}),
            html.Label('Please select pegRNA spacer(s) in design table to visualize', style = {'color':'grey', 'margin-top':'0px'}),
            dashbio.SequenceViewer(
                id = 'reference-sequence',
                sequence = ' ',
                badge =False,
                charsPerLine = 80,
                sequenceMaxHeight = '10000px',
                search = False,
                coverage = [],
                # legend = [{'name':'Substitution', 'color':'#1E90FF', 'underscore':False}, {'name':'Insertion', 'color':'#3CB371', 'underscore':False}, {'name':'Deletion', 'color':'#DC143C', 'underscore':False}, {'name':'Selected pegRNA spacer', 'color':'#d6d6d6', 'underscore':False}]
            ),

            # dcc.Checklist(
            #         id = 'reference-protein-option',
            #         options=[
            #             {'label': 'Visualize amino acid sequence', 'value': 'protein'},
            #         ],
            #         value=[]
            #     ), 

            html.Div(id = 'reference-protein-display', children = [

                html.H6('Reference Protein', style = {'margin':'0px', 'padding-bottom':'0px'}),
                dashbio.SequenceViewer(
                    id = 'reference-protein-sequence',
                    sequence = ' ',
                    badge =False,
                    charsPerLine = 80,
                    sequenceMaxHeight = '10000px',
                    search = False,
                    coverage = [],
                ),

                ], style = {'display':'none'}),

            html.Div(id='store-sequence', style={'display': 'none'}),

            html.Span('Substitution', style = {'color':'#1E90FF'}),
            html.Span(' | '),
            # html.Span('Insertion', style = {'color':'#3CB371'}),
            # html.Span(' | '),
            html.Span('Deletion', style = {'color':'#DC143C'}),
            html.Span(' | '),
            html.Span('pegRNA spacer', style = {'color':'#808080'}),

            ], style={'display': 'inline-block','border-radius': '5px','box-shadow': '3px 3px 3px lightgrey','background-color': '#fafafa','padding': '15px','margin': '0px', 'float':'left','width':'47.5%'}),
            
            html.Div([

            # dcc.RadioItems(
            #     id = 'sequence-option2',
            #     options=[
            #         {'label': 'Reference', 'value': 'ref'},
            #         {'label': 'Edited', 'value': 'edit'},
            #     ],
            #     value='ref',
            #     labelStyle={'display': 'inline-block'}
            # ),

            html.H6('Edited DNA', style = {'margin':'0px', 'padding-bottom':'0px'}),
            html.Label('Please select pegRNA extension(s) and ngRNA(s) in design tables to visualize', style = {'color':'grey', 'margin-top':'0px'}),
            dashbio.SequenceViewer(
                id = 'edit-sequence',
                sequence = ' ',
                badge =False,
                charsPerLine = 80,
                sequenceMaxHeight = '10000px',
                search = False,
                coverage = [],
                # legend = [{'name':'Substitution', 'color':'#1E90FF', 'underscore':False}, {'name':'Insertion', 'color':'#3CB371', 'underscore':False}, {'name':'Deletion', 'color':'#DC143C', 'underscore':False}, {'name':'Selected pegRNA spacer', 'color':'#d6d6d6', 'underscore':False}]
            ),

            # dcc.Checklist(
            #         id = 'edit-protein-option',
            #         options=[
            #             {'label': 'Visualize amino acid sequence', 'value': 'protein'},
            #         ],
            #         value=[]
            #     ), 

            html.Div(id = 'edit-protein-display', children = [

                html.H6('Edited Protein', style = {'margin':'0px', 'padding-bottom':'0px'}),
                dashbio.SequenceViewer(
                    id = 'edit-protein-sequence',
                    sequence = ' ',
                    badge =False,
                    charsPerLine = 80,
                    sequenceMaxHeight = '10000px',
                    search = False,
                    coverage = [],
                ),

                ], style = {'display':'none'}),

            html.Div(id='store-sequence2', style={'display': 'none'}),

            html.Span('Substitution', style = {'color':'#1E90FF'}),
            html.Span(' | '),
            html.Span('Insertion', style = {'color':'#3CB371'}),
            html.Span(' | '),
            # html.Span('Deletion', style = {'color':'#DC143C'}),
            # html.Span(' | '),
            html.Span('pegRNA extension', style = {'color':'#ffa500'}),
            html.Span(' | '),
            html.Span('ngRNA spacer', style = {'color':'#808080'}),

            ], style={'display': 'inline-block','border-radius': '5px','box-shadow': '3px 3px 3px lightgrey','background-color': '#fafafa','padding': '15px', 'margin': '0px', 'float':'right', 'width':'47.5%'}),

        ], style = {'padding-right': '15px', 'padding-left': '15px','margin': '0px'}),
    
    html.Br(),

    html.Div([

        html.Div([html.H5('Prime editing parameters', style = {'display':'inline', 'margin-right':'5px',}), html.Span('?', id = 'parameters-tooltip', style={'font-size':'11px', 'textAlign': 'center', 'color': 'white',}, className = 'dot')], className = 'three columns', style = {'padding-top':'15px'}),
        dbc.Tooltip('Interactively design pegRNAs with the parameter slides below',
               target = 'parameters-tooltip',
               placement = 'right',
               style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
         ),

        html.Div([html.H5('Design tables', style = {'display':'inline', 'margin-right':'5px',}), html.Span('?', id = 'design-tables-tooltip', style={'font-size':'11px', 'textAlign': 'center', 'color': 'white',}, className = 'dot')], className = 'nine columns', style = {'padding-top':'15px'}),
        dbc.Tooltip('Please select pegRNA spacer(s) to proceed with design of pegRNA extensions and ngRNAs',
               target = 'design-tables-tooltip',
               placement = 'right',
               style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
         ),

        ], className = 'row', style = {'padding-right': '15px', 'padding-left': '15px','margin': '0px'}),

    html.Div([

        html.Div([

            html.Div([

                html.Label(id = 'pbs-title', children = 'PBS length', style = {'font-weight':'bold', 'margin-right':'5px'}),
                html.Span('?',
                      id = 'pbs-tooltip',
                      style={'font-size':'11px', 'textAlign': 'center', 'color': 'white'},
                      className = 'dot'),

                 dbc.Tooltip('Initial recommendation: 12-14 nt',
                       target = 'pbs-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                 ),

            ], className='row', style={'display' : 'flex'}),

            html.Label(id = 'pbs-info', children = 'Primer binding site', style = {'color':'grey'}),
            dcc.RangeSlider(
                id = 'pbs-range',
                min=5,
                max=17,
                value=[12, 14],
                allowCross=False
            ),

            html.Div([

                html.Label(id = 'rtt-title', children = 'RTT length', style = {'font-weight':'bold', 'margin-right':'5px'}),
                html.Span('?',
                      id = 'rtt-tooltip',
                      style={'font-size':'11px', 'textAlign': 'center', 'color': 'white'},
                      className = 'dot'),

                 dbc.Tooltip('Initial recommendation: 10-20 nt',
                       target = 'rtt-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                 ),

            ], className='row', style={'display' : 'flex'}),

            html.Label(id = 'rtt-info', children = 'Reverse transcription template', style = {'color':'grey'}),
            dcc.RangeSlider(
                id = 'rtt-range',
                min=5,
                max=80,
                value=[10, 20],
                allowCross=False
            ),
            
            html.Div([
                html.Label(id = 'nick-dist-title', children = 'ngRNA distance', style = {'font-weight':'bold', 'margin-right':'5px'}),
                html.Span('?',
                      id = 'nick-dist-tooltip',
                      style={'font-size':'11px', 'textAlign': 'center', 'color': 'white'},
                      className = 'dot'),

                 dbc.Tooltip('Initial recommendation: 50+ bp (unless PE3b option available)',
                       target = 'nick-dist-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                 ),

            ], className='row', style={'display' : 'flex'}),

            html.Label(id = 'nick-dist-info', children = 'ngRNA to pegRNA distance', style = {'color':'grey'}),
            dcc.RangeSlider(
                id = 'nick-dist-range',
                min=0,
                max=120,
                value=[0, 100],
                allowCross=False
            ),

            html.Div([
                html.Label(id = 'remove-first-c-base', children = 'Remove extensions with C first base', style = {'font-weight':'bold', 'margin-right':'5px'}),
                html.Span('?',
                      id = 'remove-first-c-base-tooltip',
                      style={'font-size':'11px', 'textAlign': 'center', 'color': 'white'},
                      className = 'dot'),

                 dbc.Tooltip('pegRNA extensions that start with a C base may exhibit lower editing efficiencies',
                       target = 'remove-first-c-base-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                 ),

            ], className='row', style={'display' : 'flex'}),

            dcc.RadioItems(
                id = 'extfirstbase-option',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                ],
                value='yes',
                labelStyle={'display': 'inline-block'}
            ),

            html.Div([
                html.Label(id = 'silent-mutation', children = 'Disrupt PAM with silent PAM mutation', style = {'font-weight':'bold', 'margin-right':'5px'}),
                html.Span('?',
                      id = 'silent-mutation-tooltip',
                      style={'font-size':'11px', 'textAlign': 'center', 'color': 'white'},
                      className = 'dot'),

                 dbc.Tooltip(children = 'Disrupting the PAM sequence via a silent mutation may improve prime editing efficiencies for coding sequence edits',
                       target = 'silent-mutation-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                 ),

            ], className='row', style={'display' : 'flex'}),

            dcc.RadioItems(
                id = 'silentmutation-option',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'},
                ],
                value='no',
                labelStyle={'display': 'inline-block'}
            ),

            ], className = 'three columns', style={'display': 'inline-block','border-radius': '5px','box-shadow': '3px 3px 3px lightgrey','background-color': '#fafafa','padding': '15px','margin':'0px',}), #'float':'left','width':'25%'

        html.Div([

            html.Div([

                html.Div([html.H6('pegRNA spacers', style = {'display': 'inline', 'margin':'0px', 'margin-right':'5px'}), html.Span('?', id = 'pegspacer-tooltip', style={'font-size':'11px', 'textAlign': 'center', 'color': 'white',}, className = 'dot')], className = 'six columns'),

                dbc.Tooltip('Table of all possible pegRNA spacer designs given parameter ranges - Please select pegRNA spacer(s) to proceed with design',
                       target = 'pegspacer-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                ),

                html.Div([

                    html.A(
                        'Download all designs',
                        id='download-link',
                        download="PrimeDesign.csv",
                        href="",
                        target="_blank",
                        style = {'font-size':'20px', 'color':'#a6a6a6', 'text-decoration':'none'}
                    ),

                    ], className = 'six columns', style = {'text-align':'right', 'padding-bottom':'0px'}),

                ], className = 'row', style = {'display':'inline', 'margin':'0px'}),

            html.Label('Increase RTT length if no pegRNA spacer designs are available', style = {'color':'grey', 'margin-top':'0px'}),

            dash_table.DataTable(
                id = 'peg-table',
                columns = [{'name': i, 'id': i} for i in ['spacer sequence','PAM','strand','peg-to-edit distance','spacer GC content','annotation']],
                data = df_tmp.to_dict('records'),
                style_cell={'textAlign': 'left', 'padding': '5px'},
                # style_as_list_view=True,
                style_header={
                    'backgroundColor': 'white',
                    # 'fontWeight': 'bold',
                    'font-family':'HelveticaNeue',
                    'font-size':'14px'
                },
                style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll'
                },
                sort_action = 'native',
                sort_mode = 'multi',
                # filter_action = 'native',
                row_selectable = 'multi',
                style_data_conditional=[{
                    'if': {'column_id': 'annotation', 'filter_query': '{annotation} eq PAM_mutated'},
                    'backgroundColor': "#62c096",
                    'color': 'white'
                },
                {
                    'if': {'column_id': 'annotation', 'filter_query': '{annotation} eq PAM_mutated_silent_mutation'},
                    'backgroundColor': "#62c096",
                    'color': 'white'
                }]
            ),

            html.H6('pegRNA extensions', style = {'display': 'inline', 'margin':'0px', 'margin-right':'5px'}),
            html.Span('?', id = 'pegext-tooltip', style={'font-size':'11px', 'textAlign': 'center', 'color': 'white',}, className = 'dot'),

            dbc.Tooltip('Table of all possible pegRNA extensions given parameter ranges - Please select pegRNA spacer(s) to proceed with design',
                       target = 'pegext-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                ),

            html.Label('Please select pegRNA spacer(s) above to see associated extensions', style = {'color':'grey', 'margin-top':'0px'}),

            dash_table.DataTable(
                id = 'pegext-table',
                columns = [{'name': i, 'id': i} for i in ['PBS length','PBS GC content','RTT length','RTT GC content','pegRNA extension']],
                data = df_tmp.to_dict('records'),
                style_cell={'textAlign': 'left', 'padding': '5px'},
                # style_as_list_view=True,
                style_header={
                    'backgroundColor': 'white',
                    # 'fontWeight': 'bold',
                    'font-family':'HelveticaNeue',
                    'font-size':'14px'
                },
                style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll'
                },
                sort_action = 'native',
                sort_mode = 'multi',
                # filter_action = 'native',
                row_selectable = 'multi'
                ),

            html.H6('ngRNA spacers', style = {'display': 'inline', 'margin':'0px', 'margin-right':'5px'}),
            html.Span('?', id = 'ngspacer-tooltip', style={'font-size':'11px', 'textAlign': 'center', 'color': 'white',}, className = 'dot'),

            dbc.Tooltip('Table of all possible ngRNAs given parameter ranges - Please select pegRNA spacer(s) to proceed with design',
                       target = 'ngspacer-tooltip',
                       placement = 'right',
                       style = {'background-color': '#C0C0C0', 'color': '#fff','border-radius': '6px',  'padding': '1px'}
                ),

            html.Label('Please select pegRNA spacer(s) above to see associated ngRNAs', style = {'color':'grey', 'margin-top':'0px'}),

            dash_table.DataTable(
                id = 'ng-table',
                columns = [{'name': i, 'id': i} for i in ['spacer sequence','PAM','strand','nick-to-peg distance','spacer GC content','annotation']],
                data = df_tmp.to_dict('records'),
                style_cell={'textAlign': 'left', 'padding': '5px'},
                # style_as_list_view=True,
                style_header={
                    'backgroundColor': 'white',
                    # 'fontWeight': 'bold',
                    'font-family':'HelveticaNeue','font-size':'14px'

                },
                style_table={
                    'maxHeight': '300px',
                    'overflowY': 'scroll'
                },
                sort_action = 'native',
                sort_mode = 'multi',
                row_selectable = 'multi',
                # filter_action = 'native',
                style_data_conditional=[{
                    'if': {'column_id': 'annotation', 'filter_query': '{annotation} eq PE3b-seed'},
                    'backgroundColor': "#62c096",
                    'color': 'white'
                },
                {
                    'if': {'column_id': 'annotation', 'filter_query': '{annotation} eq PE3b-nonseed'},
                    'backgroundColor': "#62c096",
                    'color': 'white'
                },
                ]
            ),

            html.Div(id='store-peg-table-total', style={'display': 'none'}),
            html.Div(id='store-peg-table', style={'display': 'none'}),


            ], className = 'nine columns', style={'display': 'inline-block','border-radius': '5px','box-shadow': '3px 3px 3px lightgrey','background-color': '#fafafa','padding': '15px',}), #'float':'right','width':'70%'

        ], className = 'row', style = {'padding-right': '15px', 'padding-left': '15px','margin': '0px'}), #'margin': '0px'
    
    html.Hr(),

])

# Modal
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Download file
def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

# Multi page set up
# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):

    if pathname == '/':
        return(design_page)

    elif pathname == '/about':
        return(about_page)

    elif pathname == '/help':
        return(help_page)

    else:
        return(error_page)

# Load example data
@app.callback(Output('pe-sequence-input','value'),
    [Input('example-option', 'value')]
)

def update_input_check(example_values):
    
    if 'substitution' in example_values:
        if 'insertion' in example_values:
            if 'deletion' in example_values:
                return('CACACCTACACTGCTCGAAGTAAATATGCGAAGCGCGCGGCCTGGCCGGAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGCAATCGTAGTCCGTCAAATTCAGCTCTGTTATCCCGGGCGTTATGTGTCAAATGGCGTAGAACGGGATTGACTGTTTGACGGTAGCTGCTGAGGCGG(G/T)A(+GTAA)G(-AGAC)CCTCCGTCGGGCTATGTCACTAATACTTTCCAAACGCCCCGTACCGATGCTGAACAAGTCGATGCAGGCTCCCGTCTTTGAAAAGGGGTAAACATACAAGTGGATAGATGATGGGTAGGGGCCTCCAATACATCCAACACTCTACGCCCTCTCCAAGAGCTAGAAGGGCACCCTGCAGTTGGAAAGGG') # Return example input with substitution, insertion, and deletion edits

            else:
                return('CACACCTACACTGCTCGAAGTAAATATGCGAAGCGCGCGGCCTGGCCGGAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGCAATCGTAGTCCGTCAAATTCAGCTCTGTTATCCCGGGCGTTATGTGTCAAATGGCGTAGAACGGGATTGACTGTTTGACGGTAGCTGCTGAGGCGG(G/T)A(+GTAA)GAGACCCTCCGTCGGGCTATGTCACTAATACTTTCCAAACGCCCCGTACCGATGCTGAACAAGTCGATGCAGGCTCCCGTCTTTGAAAAGGGGTAAACATACAAGTGGATAGATGATGGGTAGGGGCCTCCAATACATCCAACACTCTACGCCCTCTCCAAGAGCTAGAAGGGCACCCTGCAGTTGGAAAGGG') # Return example input with substitution and insertion edits

        elif 'deletion' in example_values:
            return('CACACCTACACTGCTCGAAGTAAATATGCGAAGCGCGCGGCCTGGCCGGAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGCAATCGTAGTCCGTCAAATTCAGCTCTGTTATCCCGGGCGTTATGTGTCAAATGGCGTAGAACGGGATTGACTGTTTGACGGTAGCTGCTGAGGCGG(G/T)AG(-AGAC)CCTCCGTCGGGCTATGTCACTAATACTTTCCAAACGCCCCGTACCGATGCTGAACAAGTCGATGCAGGCTCCCGTCTTTGAAAAGGGGTAAACATACAAGTGGATAGATGATGGGTAGGGGCCTCCAATACATCCAACACTCTACGCCCTCTCCAAGAGCTAGAAGGGCACCCTGCAGTTGGAAAGGG') # Return example input with substitution and deletion edits

        else:
            return('CACACCTACACTGCTCGAAGTAAATATGCGAAGCGCGCGGCCTGGCCGGAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGCAATCGTAGTCCGTCAAATTCAGCTCTGTTATCCCGGGCGTTATGTGTCAAATGGCGTAGAACGGGATTGACTGTTTGACGGTAGCTGCTGAGGCGG(G/T)AGAGACCCTCCGTCGGGCTATGTCACTAATACTTTCCAAACGCCCCGTACCGATGCTGAACAAGTCGATGCAGGCTCCCGTCTTTGAAAAGGGGTAAACATACAAGTGGATAGATGATGGGTAGGGGCCTCCAATACATCCAACACTCTACGCCCTCTCCAAGAGCTAGAAGGGCACCCTGCAGTTGGAAAGGG') # Return example input with substitution edit

    elif 'insertion' in example_values:
        if 'deletion' in example_values:
            return('CACACCTACACTGCTCGAAGTAAATATGCGAAGCGCGCGGCCTGGCCGGAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGCAATCGTAGTCCGTCAAATTCAGCTCTGTTATCCCGGGCGTTATGTGTCAAATGGCGTAGAACGGGATTGACTGTTTGACGGTAGCTGCTGAGGCGGGA(+GTAA)G(-AGAC)CCTCCGTCGGGCTATGTCACTAATACTTTCCAAACGCCCCGTACCGATGCTGAACAAGTCGATGCAGGCTCCCGTCTTTGAAAAGGGGTAAACATACAAGTGGATAGATGATGGGTAGGGGCCTCCAATACATCCAACACTCTACGCCCTCTCCAAGAGCTAGAAGGGCACCCTGCAGTTGGAAAGGG') # Return example input with insertion and deletion edits

        else:
            return('CACACCTACACTGCTCGAAGTAAATATGCGAAGCGCGCGGCCTGGCCGGAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGCAATCGTAGTCCGTCAAATTCAGCTCTGTTATCCCGGGCGTTATGTGTCAAATGGCGTAGAACGGGATTGACTGTTTGACGGTAGCTGCTGAGGCGGGA(+GTAA)GAGACCCTCCGTCGGGCTATGTCACTAATACTTTCCAAACGCCCCGTACCGATGCTGAACAAGTCGATGCAGGCTCCCGTCTTTGAAAAGGGGTAAACATACAAGTGGATAGATGATGGGTAGGGGCCTCCAATACATCCAACACTCTACGCCCTCTCCAAGAGCTAGAAGGGCACCCTGCAGTTGGAAAGGG') # Return example input with insertion edit

    elif 'deletion' in example_values:
        return('CACACCTACACTGCTCGAAGTAAATATGCGAAGCGCGCGGCCTGGCCGGAGGCGTTCCGCGCCGCCACGTGTTCGTTAACTGTTGATTGGTGGCACATAAGCAATCGTAGTCCGTCAAATTCAGCTCTGTTATCCCGGGCGTTATGTGTCAAATGGCGTAGAACGGGATTGACTGTTTGACGGTAGCTGCTGAGGCGGGAG(-AGAC)CCTCCGTCGGGCTATGTCACTAATACTTTCCAAACGCCCCGTACCGATGCTGAACAAGTCGATGCAGGCTCCCGTCTTTGAAAAGGGGTAAACATACAAGTGGATAGATGATGGGTAGGGGCCTCCAATACATCCAACACTCTACGCCCTCTCCAAGAGCTAGAAGGGCACCCTGCAGTTGGAAAGGG') # Return example input with deletion edit

    else:
        return(None)

@app.callback([Output('input-check', 'children'), Output('input-check', 'style'),],
    [Input('pe-sequence-input','value')]
)

def update_input_check(input_sequence):

    if input_sequence is not None:

        input_sequence = ''.join(input_sequence.split())
        if len(input_sequence) <= 10000:
            # Check formatting is correct
            format_check = ''
            for i in input_sequence:
                if i == '(':
                    format_check += '('
                elif i == ')':
                    format_check += ')'
                elif i == '/':
                    format_check += '/'
                elif i == '+':
                    format_check += '+'
                elif i == '-':
                    format_check += '-'

            # Check composition of input sequence
            if len(input_sequence) != sum([1 if x in ['A','T','C','G','(',')','+','-','/'] else 0 for x in input_sequence.upper()]):
                sequence_check = 'Error: Input sequence contains a character not in the following list: A,T,C,G,(,),+,-,/ ...'
                sequence_check_style = {'color':'#ff4d4d'}

            else:

                # Check formatting
                if format_check.count('(') == format_check.count(')') and format_check.count('(') > 0: # Left and right parantheses equal
                    if '((' not in format_check: # Checks both directions for nested parantheses
                        if '()' not in format_check: # Checks for empty annotations
                            if sum([1 if x in format_check else 0 for x in ['++','--','//','+-','+/','-+','-/','/+','/-','/(','+(','-(',')/',')+',')-']]) == 0:
                                sequence_check = 'Success: Input sequence has correct formatting'
                                sequence_check_style = {'color':'#6bb6ff'}
                            else:
                                sequence_check = 'Error: Input sequence has more than one edit annotation per parantheses set or annotation outside of parantheses'
                                sequence_check_style = {'color':'#ff4d4d'}
                        else:
                            sequence_check = 'Error: Input sequence has empty parantheses without an edit annotation (i.e. /,  + , -)'
                            sequence_check_style = {'color':'#ff4d4d'}
                    else:
                        sequence_check = 'Error: Input sequence has nested parantheses which is not allowed'
                        sequence_check_style = {'color':'#ff4d4d'}
                else:
                    sequence_check = 'Error: Input sequence does not have full sets of parantheses'
                    sequence_check_style = {'color':'#ff4d4d'}

        else:
            sequence_check = 'Error: Input sequence has exceeded maximum length of 10kb'
            sequence_check_style = {'color':'#ff4d4d'}

    else:
        sequence_check = 'No input sequence with desired edits has been provided'
        sequence_check_style = {'color':'#ff4d4d'}

    return(sequence_check, sequence_check_style)

@app.callback([Output('reference-sequence', 'sequence'), Output('reference-sequence', 'coverage'), Output('reference-protein-sequence', 'sequence'), Output('reference-protein-sequence', 'coverage'), Output('edit-sequence', 'sequence'), Output('edit-sequence', 'coverage'), Output('edit-protein-sequence', 'sequence'), Output('edit-protein-sequence', 'coverage')],
    [Input('input-check','children'), Input('peg-table','selected_rows'), Input('pegext-table','selected_rows'), Input('ng-table','selected_rows')],
    state = [State('pe-sequence-input','value'), State('store-peg-table', 'children'), State('store-peg-table-total', 'children')]
)

def update_reference_sequence(input_check, selected_rows_peg, selected_rows_pegext, selected_rows_ng, input_sequence, store_peg_table, store_peg_table_total):

    annotations_ref = []
    annotations_edit = []
    annotations_aa_ref = []
    annotations_aa_edit = []

    if input_sequence is not None:
        input_sequence = ''.join(input_sequence.split())
        reference_sequence = input_sequence
        edit_sequence = input_sequence
        editformat2sequence_ref = {}
        editformat2sequence_edit = {}
        index_shift_ref = 0
        index_shift_edit = 0

        if 'Success' in input_check:

            edit_idxs = [[m.start(), m.end()] for m in re.finditer('\(.*?\)', input_sequence)]
            for edit_idx in edit_idxs:

                edit = input_sequence[edit_idx[0]:edit_idx[1]]
                edit_length = edit_idx[1] - edit_idx[0]

                # Create edit format and number to sequence map
                if '/' in edit:
                    editformat2sequence_ref[edit] = edit.split('/')[0].replace('(','')

                    if len(edit.split('/')[1].replace(')','')) == 0:
                        annotations_ref.append({'start':edit_idx[0] - index_shift_ref, 'end':edit_idx[0] - index_shift_ref + len(edit.split('/')[0].replace('(','')), 'color':'#DC143C', 'bgcolor':'#fbe7eb', 'underscore':True})
                    else:
                        annotations_ref.append({'start':edit_idx[0] - index_shift_ref, 'end':edit_idx[0] - index_shift_ref + len(edit.split('/')[0].replace('(','')), 'color':'#1E90FF', 'bgcolor':'#e8f3ff', 'underscore':True})
                    
                    aa_start = math.floor(float(edit_idx[0] - index_shift_ref)/3.0)
                    aa_stop = math.ceil(float(edit_idx[0] - index_shift_ref + len(edit.split('/')[0].replace('(','')))/3.0)

                    annotation_entry = {'start':aa_start, 'end':aa_stop, 'color':'#1E90FF', 'bgcolor':'#e8f3ff', 'underscore':True}
                    if annotation_entry not in annotations_aa_ref:
                        annotations_aa_ref.append(annotation_entry)
                    
                    index_shift_ref += edit_length - len(edit.split('/')[0].replace('(',''))

                elif '+' in edit:
                    editformat2sequence_ref[edit] = ''
                    annotations_ref.append({'start':edit_idx[0] - index_shift_ref, 'end':edit_idx[0] - index_shift_ref, 'color':'#3CB371', 'bgcolor':'#ebf7f0', 'underscore':True})

                    # aa_start = math.floor(float(edit_idx[0] - index_shift)/3.0)
                    # aa_stop = math.ceil(float(edit_idx[0] - index_shift)/3.0)
                    # annotations_aa.append({'start':aa_start, 'end':aa_stop, 'color':'#3CB371', 'bgcolor':'#ebf7f0', 'underscore':True})

                    index_shift_ref += edit_length

                elif '-' in edit:
                    editformat2sequence_ref[edit] = edit.split('-')[1].replace(')','')
                    annotations_ref.append({'start':edit_idx[0] - index_shift_ref, 'end':edit_idx[0] - index_shift_ref + len(edit.split('-')[1].replace(')','')), 'color':'#DC143C', 'bgcolor':'#fbe7eb', 'underscore':True})

                    aa_start = math.floor(float(edit_idx[0] - index_shift_ref)/3.0)
                    aa_stop = math.ceil(float(edit_idx[0] - index_shift_ref + len(edit.split('-')[1].replace(')','')))/3.0)

                    annotation_entry = {'start':aa_start, 'end':aa_stop, 'color':'#DC143C', 'bgcolor':'#fbe7eb', 'underscore':True}
                    if annotation_entry not in annotations_aa_ref:
                        annotations_aa_ref.append(annotation_entry)

                    index_shift_ref += edit_length - len(edit.split('-')[1].replace(')',''))

                # Create edit format and number to sequence map
                if '/' in edit:
                    editformat2sequence_edit[edit] = edit.split('/')[1].replace(')','')

                    if len(edit.split('/')[0].replace('(','')) == 0:
                        annotations_edit.append({'start':edit_idx[0] - index_shift_edit, 'end':edit_idx[0] - index_shift_edit + len(edit.split('/')[1].replace(')','')), 'color':'#3CB371', 'bgcolor':'#ebf7f0', 'underscore':True})
                    else:
                        annotations_edit.append({'start':edit_idx[0] - index_shift_edit, 'end':edit_idx[0] - index_shift_edit + len(edit.split('/')[1].replace(')','')), 'color':'#1E90FF', 'bgcolor':'#e8f3ff', 'underscore':True})

                    aa_start = math.floor(float(edit_idx[0] - index_shift_edit)/3.0)
                    aa_stop = math.ceil(float(edit_idx[0] - index_shift_edit + len(edit.split('/')[1].replace(')','')))/3.0)

                    annotation_entry = {'start':aa_start, 'end':aa_stop, 'color':'#1E90FF', 'bgcolor':'#e8f3ff', 'underscore':True}
                    if annotation_entry not in annotations_aa_edit:
                        annotations_aa_edit.append(annotation_entry)

                    index_shift_edit += edit_length - len(edit.split('/')[1].replace(')',''))

                elif '+' in edit:
                    editformat2sequence_edit[edit] = edit.split('+')[1].replace(')','')
                    annotations_edit.append({'start':edit_idx[0] - index_shift_edit, 'end':edit_idx[0] - index_shift_edit + len(edit.split('+')[1].replace(')','')), 'color':'#3CB371', 'bgcolor':'#ebf7f0', 'underscore':True})

                    aa_start = math.floor(float(edit_idx[0] - index_shift_edit)/3.0)
                    aa_stop = math.ceil(float(edit_idx[0] - index_shift_edit + len(edit.split('+')[1].replace(')','')))/3.0)

                    annotation_entry = {'start':aa_start, 'end':aa_stop, 'color':'#3CB371', 'bgcolor':'#ebf7f0', 'underscore':True}
                    if annotation_entry not in annotations_aa_edit:
                        annotations_aa_edit.append(annotation_entry)

                    index_shift_edit += edit_length -len(edit.split('+')[1].replace(')',''))

                elif '-' in edit:
                    editformat2sequence_edit[edit] = ''
                    annotations_edit.append({'start':edit_idx[0] - index_shift_edit, 'end':edit_idx[0] - index_shift_edit, 'color':'#DC143C', 'bgcolor':'#fbe7eb', 'underscore':True})

                    # aa_start = math.floor(float(edit_idx[0] - index_shift)/3.0)
                    # aa_stop = math.ceil(float(edit_idx[0] - index_shift)/3.0)
                    # annotations_aa.append({'start':aa_start, 'end':aa_stop, 'color':'#DC143C', 'bgcolor':'#fbe7eb', 'underscore':True})

                    index_shift_edit += edit_length

            for edit in editformat2sequence_ref:
                reference_sequence = reference_sequence.replace(edit, editformat2sequence_ref[edit])

            for edit in editformat2sequence_edit:
                edit_sequence = edit_sequence.replace(edit, editformat2sequence_edit[edit])

            aa_sequence_ref = sequencetoaa(reference_sequence)
            aa_sequence_edit = sequencetoaa(edit_sequence)

            # print(aa_sequence_ref)
            # print(aa_sequence_edit)

            # Visualizing pegRNA spacer in reference sequence
            try:
                current_annotation_ranges = []
                for annotation in annotations_ref:
                    current_annotation_ranges.append([annotation['start'], annotation['end']])

                df_peg = pd.read_json(store_peg_table, orient='split')
                spacer_sequences = list(df_peg.loc[selected_rows_peg, 'spacer sequence'].values)

                # Annotate pegRNA spacer sequences
                for spacer_sequence in spacer_sequences:

                    try:
                        start_idx = re.search(spacer_sequence, reference_sequence, re.IGNORECASE).start()
                        stop_idx = start_idx + len(spacer_sequence)
                        for i in range(start_idx, stop_idx):
                            if sum([1 if (x[0] <= i < x[1]) else 0 for x in current_annotation_ranges]) == 0:
                                annotations_ref.append({'start':i, 'end':i + 1, 'bgcolor':'#dedede'})
                                current_annotation_ranges.append([i, i + 1])

                    except:
                        start_idx = re.search(reverse_complement(spacer_sequence), reference_sequence, re.IGNORECASE).start()
                        stop_idx = start_idx + len(spacer_sequence)
                        for i in range(start_idx, stop_idx):
                            if sum([1 if (x[0] <= i < x[1]) else 0 for x in current_annotation_ranges]) == 0:
                                annotations_ref.append({'start':i, 'end':i + 1, 'bgcolor':'#dedede'})
                                current_annotation_ranges.append([i, i + 1])

            except:
                pass

            # Visualizing pegRNA extension in edit sequence
            try:
                current_annotation_ranges = []
                for annotation in annotations_edit:
                    current_annotation_ranges.append([annotation['start'], annotation['end']])

                df_peg = pd.read_json(store_peg_table, orient='split')
                df_peg_total = pd.read_json(store_peg_table_total, orient='split')

                peg_group = list(df_peg.loc[selected_rows_peg, 'spacer sequence'].values)
                df_pegext = df_peg_total[df_peg_total['spacer sequence'].isin(peg_group)]
                df_pegext = df_pegext[df_pegext['type'] == 'pegRNA']
                df_pegext = df_pegext[['PBS length','PBS GC content','RTT length','RTT GC content','pegRNA extension']].drop_duplicates()
                df_pegext.reset_index(drop=True, inplace=True)
                pegext_sequences = list(df_pegext.loc[selected_rows_pegext, 'pegRNA extension'].values)

                # Annotate pegRNA spacer sequences
                for pegext_sequence in pegext_sequences:

                    try:
                        start_idx = re.search(pegext_sequence, edit_sequence, re.IGNORECASE).start()
                        stop_idx = start_idx + len(pegext_sequence)
                        for i in range(start_idx, stop_idx):
                            if sum([1 if (x[0] <= i < x[1]) else 0 for x in current_annotation_ranges]) == 0:
                                annotations_edit.append({'start':i, 'end':i + 1, 'bgcolor':'#ffdb99'})
                                current_annotation_ranges.append([i, i + 1])

                    except:
                        start_idx = re.search(reverse_complement(pegext_sequence), edit_sequence, re.IGNORECASE).start()
                        stop_idx = start_idx + len(pegext_sequence)
                        for i in range(start_idx, stop_idx):
                            if sum([1 if (x[0] <= i < x[1]) else 0 for x in current_annotation_ranges]) == 0:
                                annotations_edit.append({'start':i, 'end':i + 1, 'bgcolor':'#ffdb99'})
                                current_annotation_ranges.append([i, i + 1])

            except:
                pass

            # Visualizing ngRNA spacer in edit sequence
            try:
                current_annotation_ranges = []
                for annotation in annotations_edit:
                    current_annotation_ranges.append([annotation['start'], annotation['end']])

                df_peg = pd.read_json(store_peg_table, orient='split')
                df_peg_total = pd.read_json(store_peg_table_total, orient='split')

                peg_group = list(df_peg.loc[selected_rows_peg, 'pegRNA group'].values)
                df_ng = df_peg_total[df_peg_total['pegRNA group'].isin(peg_group)]
                df_ng = df_ng[df_ng['type'] == 'ngRNA']
                df_ng = df_ng[['spacer sequence','PAM','strand','nick-to-peg distance','spacer GC content','annotation']].drop_duplicates()
                df_ng.reset_index(drop=True, inplace=True)
                ngRNA_sequences = list(df_ng.loc[selected_rows_ng, 'spacer sequence'].values)

                # Annotate pegRNA spacer sequences
                for ngRNA_sequence in ngRNA_sequences:

                    try:
                        start_idx = re.search(ngRNA_sequence, edit_sequence, re.IGNORECASE).start()
                        stop_idx = start_idx + len(ngRNA_sequence)
                        for i in range(start_idx, stop_idx):
                            if sum([1 if (x[0] <= i < x[1]) else 0 for x in current_annotation_ranges]) == 0:
                                annotations_edit.append({'start':i, 'end':i + 1, 'bgcolor':'#d6d6d6'})
                                current_annotation_ranges.append([i, i + 1])

                    except:
                        start_idx = re.search(reverse_complement(ngRNA_sequence), edit_sequence, re.IGNORECASE).start()
                        stop_idx = start_idx + len(ngRNA_sequence)
                        for i in range(start_idx, stop_idx):
                            if sum([1 if (x[0] <= i < x[1]) else 0 for x in current_annotation_ranges]) == 0:
                                annotations_edit.append({'start':i, 'end':i + 1, 'bgcolor':'#d6d6d6'})
                                current_annotation_ranges.append([i, i + 1])

            except:
                pass

        else:
            reference_sequence = ' '
            edit_sequence = ' '
            aa_sequence_ref = ' '
            aa_sequence_edit = ' '

    else:
        reference_sequence = ' '
        edit_sequence = ' '
        aa_sequence_ref = ' '
        aa_sequence_edit = ' '

    return(reference_sequence, annotations_ref, aa_sequence_ref, annotations_aa_ref, edit_sequence, annotations_edit, aa_sequence_edit, annotations_aa_edit)

# Visualize protein sequence
@app.callback([Output('reference-protein-display', 'style'), Output('edit-protein-display', 'style')],
    [Input('protein-option','value')]
)

def protein_display(protein_option):

    if 'protein' in protein_option:
        return({'display':'block'}, {'display':'block'})
    else:
        return({'display':'none'}, {'display':'none'})

@app.callback(Output('pbs-title', 'children'),
    [Input('pbs-range','value')]
)

def update_pbs_title(pbs_range):
    return('PBS length: %s - %s nt' % (pbs_range[0], pbs_range[1]))

@app.callback(Output('rtt-title', 'children'),
    [Input('rtt-range','value')]
)

def update_pbs_title(rtt_range):
    return('RTT length: %s - %s nt' % (rtt_range[0], rtt_range[1]))

@app.callback(Output('nick-dist-title', 'children'),
    [Input('nick-dist-range','value')]
)

def update_pbs_title(nick_dist_range):
    return('Nicking distance: %s - %s bp' % (nick_dist_range[0], nick_dist_range[1]))

### Section to run pegDesigner code

# Helper functions
def gc_content(sequence):
    sequence = sequence.upper()
    GC_count = sequence.count('G') + sequence.count('C')
    GC_content = float(GC_count)/float(len(sequence))

    return("%.2f" % GC_content)

# IUPAC code map
iupac2bases_dict = {'A':'A','T':'T','C':'C','G':'G','a':'a','t':'t','c':'c','g':'g',
'R':'[AG]','Y':'[CT]','S':'[GC]','W':'[AT]','K':'[GT]','M':'[AC]','B':'[CGT]','D':'[AGT]','H':'[ACT]','V':'[ACG]','N':'[ACTG]',
'r':'[ag]','y':'[ct]','s':'[gc]','w':'[at]','k':'[gt]','m':'[ac]','b':'[cgt]','d':'[agt]','h':'[act]','v':'[acg]','n':'[actg]',
'(':'(',')':')','+':'+','-':'-','/':'/'}

def iupac2bases(iupac):

    try:
        bases = iupac2bases_dict[iupac]
    except:
        logger.error('Symbol %s is not within the IUPAC nucleotide code ...' % str(iupac))
        sys.exit(1)

    return(bases)

# Reverse complement function
def reverse_complement(sequence):
    sequence = sequence
    new_sequence = ''
    for base in sequence:
        if base == 'A':
            new_sequence += 'T'
        elif base == 'T':
            new_sequence += 'A'
        elif base == 'C':
            new_sequence += 'G'
        elif base == 'G':
            new_sequence += 'C'
        if base == 'a':
            new_sequence += 't'
        elif base == 't':
            new_sequence += 'a'
        elif base == 'c':
            new_sequence += 'g'
        elif base == 'g':
            new_sequence += 'c'
        elif base == '[':
            new_sequence += ']'
        elif base == ']':
            new_sequence += '['
        elif base == '+':
            new_sequence += '+'
        elif base == '-':
            new_sequence += '-'
        elif base == '/':
            new_sequence += '/'
        elif base == '(':
            new_sequence += ')'
        elif base == ')':
            new_sequence += '('
    return(new_sequence[::-1])

# Amino acid code
codon_dict = {
    'GGG':['Gly','G', 0.25],'GGA':['Gly','G', 0.25],'GGT':['Gly','G', 0.16],'GGC':['Gly','G', 0.34],
    'GAG':['Glu','E', 0.58],'GAA':['Glu','E', 0.42],'GAT':['Asp','D', 0.46],'GAC':['Asp','D', 0.54],
    'GTG':['Val','V', 0.47],'GTA':['Val','V', 0.11],'GTT':['Val','V', 0.18],'GTC':['Val','V', 0.24],
    'GCG':['Ala','A', 0.11],'GCA':['Ala','A', 0.23],'GCT':['Ala','A', 0.26],'GCC':['Ala','A', 0.4],
    'AGG':['Arg','R', 0.2],'AGA':['Arg','R', 0.2],'AGT':['Ser','S', 0.15],'AGC':['Ser','S', 0.24],
    'AAG':['Lys','K', 0.58],'AAA':['Lys','K', 0.42],'AAT':['Asn','N', 0.46],'AAC':['Asn','N', 0.54],
    'ATG':['Met','M', 1],'ATA':['Ile','I', 0.16],'ATT':['Ile','I', 0.36],'ATC':['Ile','I', 0.48],
    'ACG':['Thr','T', 0.12],'ACA':['Thr','T', 0.28],'ACT':['Thr','T', 0.24],'ACC':['Thr','T', 0.36],
    'TGG':['Trp','W', 1],'TGA':['End','X', 0.52],'TGT':['Cys','C', 0.45],'TGC':['Cys','C', 0.55],
    'TAG':['End','X', 0.2],'TAA':['End','X', 0.28],'TAT':['Tyr','Y', 0.43],'TAC':['Tyr','Y', 0.57],
    'TTG':['Leu','L', 0.13],'TTA':['Leu','L', 0.07],'TTT':['Phe','F', 0.45],'TTC':['Phe','F', 0.55],
    'TCG':['Ser','S', 0.06],'TCA':['Ser','S', 0.15],'TCT':['Ser','S', 0.18],'TCC':['Ser','S', 0.22],
    'CGG':['Arg','R', 0.21],'CGA':['Arg','R', 0.11],'CGT':['Arg','R', 0.08],'CGC':['Arg','R', 0.19],
    'CAG':['Gln','Q', 0.75],'CAA':['Gln','Q', 0.25],'CAT':['His','H', 0.41],'CAC':['His','H', 0.59],
    'CTG':['Leu','L', 0.41],'CTA':['Leu','L', 0.07],'CTT':['Leu','L', 0.13],'CTC':['Leu','L', 0.2],
    'CCG':['Pro','P', 0.11],'CCA':['Pro','P', 0.27],'CCT':['Pro','P', 0.28],'CCC':['Pro','P', 0.33],
}

# Create codon swap dictionaries
aa2codon = {}
for codon in codon_dict:
    if codon_dict[codon][1] not in aa2codon:
        aa2codon[codon_dict[codon][1]] = []

    aa2codon[codon_dict[codon][1]].append([codon, codon_dict[codon][2]])

codon_swap_0 = {}
codon_swap_1_1 = {}
codon_swap_1_2 = {}
codon_swap_2 = {}
for codon in codon_dict:

    codon_swap_0[codon] = []
    codon_swap_1_1[codon] = []
    codon_swap_1_2[codon] = []
    codon_swap_2[codon] = []

    for other_codon in aa2codon[codon_dict[codon][1]]:

        # Check if PAM disrupted with silent mutations
        if codon[1:] != other_codon[0][1:]:
            codon_swap_0[codon].append(other_codon)

        if codon[2:] != other_codon[0][2:]:
            codon_swap_1_1[codon].append(other_codon)

        if codon[:1] != other_codon[0][:1]:
            codon_swap_1_2[codon].append(other_codon)

        if codon[:2] != other_codon[0][:2]:
            codon_swap_2[codon].append(other_codon)

for codon in codon_dict:
    codon_swap_0[codon] = sorted(codon_swap_0[codon], key = lambda x: x[1], reverse = True)
    codon_swap_1_1[codon] = sorted(codon_swap_1_1[codon], key = lambda x: x[1], reverse = True)
    codon_swap_1_2[codon] = sorted(codon_swap_1_2[codon], key = lambda x: x[1], reverse = True)
    codon_swap_2[codon] = sorted(codon_swap_2[codon], key = lambda x: x[1], reverse = True)

def sequencetoaa(sequence):
    sequence = sequence.upper()
    codon_list = [sequence[i:i+3] for i in range(0, len(sequence), 3)]
    if len(codon_list[-1]) != 3:
        codon_list = codon_list[:-1]
    aa_sequence = ''.join(map(str, [codon_dict[x][1] for x in codon_list]))
    return(aa_sequence)

# Extract reference and edited sequence information
def process_sequence(input_sequence):

    input_sequence = ''.join(input_sequence.split())

    # Check formatting is correct
    format_check = ''
    for i in input_sequence:
        if i == '(':
            format_check += '('
        elif i == ')':
            format_check += ')'
        elif i == '/':
            format_check += '/'
        elif i == '+':
            format_check += '+'
        elif i == '-':
            format_check += '-'

    # Check composition of input sequence
    if len(input_sequence) != sum([1 if x in ['A','T','C','G','(',')','+','-','/'] else 0 for x in input_sequence.upper()]):
        logger.error('Input sequence %s contains a character not in the following list: A,T,C,G,(,),+,-,/ ...' % str(input_sequence))
        sys.exit(1)

    # Check formatting
    if format_check.count('(') == format_check.count(')') and format_check.count('(') > 0: # Left and right parantheses equal
        if '((' not in format_check: # Checks both directions for nested parantheses
            if '()' not in format_check: # Checks for empty annotations
                if sum([1 if x in format_check else 0 for x in ['++','--','//','+-','+/','-+','-/','/+','/-','/(','+(','-(',')/',')+',')-']]) == 0:
                    pass
                else:
                    logger.error('Input sequence %s has more than one edit annotation per parantheses set (i.e. //,  +- , -/, etc.) ...' % str(input_sequence))
                    sys.exit(1)
            else:
                logger.error('Input sequence %s has empty parantheses without an edit annotation (i.e. /,  + , -) ...' % str(input_sequence))
                sys.exit(1)
        else:
            logger.error('Input sequence %s has nested parantheses which is not allowed ...' % str(input_sequence))
            sys.exit(1)
    else:
        logger.error('Input sequence %s does not have full sets of parantheses ...' % str(input_sequence))
        sys.exit(1)

    # Create mapping between input format and reference and edit sequence
    editformat2sequence = {}
    edits = re.findall('\(.*?\)', input_sequence)
    for edit in edits:
        if '/' in edit:
            editformat2sequence[edit] = [edit.split('/')[0].replace('(',''), edit.split('/')[1].replace(')','')]
        elif '+' in edit:
            editformat2sequence[edit] = ['' , edit.split('+')[1].replace(')','')]
        elif '-' in edit:
            editformat2sequence[edit] = [edit.split('-')[1].replace(')',''), '']

    # Create mapping between edit number and reference and edit sequence
    editformat2sequence = {}
    editnumber2sequence = {}
    edit_idxs = [[m.start(), m.end()] for m in re.finditer('\(.*?\)', input_sequence)]
    edit_counter = 1
    for edit_idx in edit_idxs:
        edit = input_sequence[edit_idx[0]:edit_idx[1]]

        # Create edit format and number to sequence map
        if '/' in edit:
            editformat2sequence[edit] = [edit.split('/')[0].replace('(',''), edit.split('/')[1].replace(')','').lower(), edit_counter]
            editnumber2sequence[edit_counter] = [edit.split('/')[0].replace('(',''), edit.split('/')[1].replace(')','').lower()]

        elif '+' in edit:
            editformat2sequence[edit] = ['' , edit.split('+')[1].replace(')','').lower(), edit_counter]
            editnumber2sequence[edit_counter] = ['' , edit.split('+')[1].replace(')','').lower()]

        elif '-' in edit:
            editformat2sequence[edit] = [edit.split('-')[1].replace(')',''), '', edit_counter]
            editnumber2sequence[edit_counter] = [edit.split('-')[1].replace(')',''), '']

        edit_counter += 1

    edit_start = min([i.start() for i in re.finditer('\(', input_sequence)])
    edit_stop = max([i.start() for i in re.finditer('\)', input_sequence)])

    edit_span_sequence_w_ref = input_sequence[edit_start:edit_stop + 1]
    edit_span_sequence_w_edit = input_sequence[edit_start:edit_stop + 1]
    for edit in editformat2sequence:
        edit_span_sequence_w_ref = edit_span_sequence_w_ref.replace(edit, editformat2sequence[edit][0])
        edit_span_sequence_w_edit = edit_span_sequence_w_edit.replace(edit, editformat2sequence[edit][1])

    edit_start_in_ref = re.search('\(', input_sequence).start()
    edit_stop_in_ref_rev = re.search('\)', input_sequence[::-1]).start()

    edit_span_length_w_ref = len(edit_span_sequence_w_ref)
    edit_span_length_w_edit = len(edit_span_sequence_w_edit)

    reference_sequence = input_sequence
    edit_sequence = input_sequence
    editnumber_sequence = input_sequence
    for edit in editformat2sequence:
        reference_sequence = reference_sequence.replace(edit, editformat2sequence[edit][0])
        edit_sequence = edit_sequence.replace(edit, editformat2sequence[edit][1])
        editnumber_sequence = editnumber_sequence.replace(edit, str(editformat2sequence[edit][2]))

    return(editformat2sequence, editnumber2sequence, reference_sequence, edit_sequence, editnumber_sequence, edit_span_length_w_ref, edit_span_length_w_edit, edit_start_in_ref, edit_stop_in_ref_rev)


@app.callback([Output('peg-table', 'data'), Output('store-peg-table-total', 'children'), Output('store-peg-table', 'children')],
    [Input('input-check','children'), Input('pbs-range','value'), Input('rtt-range','value'), Input('nick-dist-range','value'), Input('extfirstbase-option','value'), Input('silentmutation-option','value')],
    state = [State('pe-sequence-input','value'), State('session-id', 'children')]
)

def run_pegDesigner(input_check, pbs_range, rtt_range, nicking_distance_range, extfirstbase_filter, silent_mutation, input_sequence, session_id):

    target_design = {}
    peg_design = {'pegRNA group':[],'type':[], 'spacer sequence':[],'spacer GC content':[],'PAM':[],'strand':[],'peg-to-edit distance':[],'nick-to-peg distance':[],'pegRNA extension':[], 'extension first base':[],'PBS length':[],'PBS GC content':[],'RTT length':[],'RTT GC content':[],'annotation':[],'spacer top strand oligo':[], 'spacer bottom strand oligo':[], 'pegRNA extension top strand oligo':[], 'pegRNA extension bottom strand oligo':[]}

    if 'Success' in input_check:

        input_sequence = ''.join(input_sequence.split())
        pe_format = 'NNNNNNNNNNNNNNNNN/NNN[NGG]'
        nicking_distance_minimum = nicking_distance_range[0]
        nicking_distance_maximum = nicking_distance_range[1]
        pbs_length_list = list(range(pbs_range[0], pbs_range[1] + 1))
        rtt_length_list = list(range(rtt_range[0], rtt_range[1] + 1))
        target_sequence = input_sequence#.upper()
        target_name = 'user-input'

        target_sequence = target_sequence.upper()
        editformat2sequence, editnumber2sequence, reference_sequence, edit_sequence, editnumber_sequence, edit_span_length_w_ref, edit_span_length_w_edit, edit_start_in_ref, edit_stop_in_ref_rev = process_sequence(target_sequence)

        # Initialize dictionary for the design of pegRNA spacers for each target sequence and intended edit(s)
        target_design[target_name] = {'target_sequence':target_sequence, 'editformat2sequence': editformat2sequence, 'editnumber2sequence': editnumber2sequence, 'reference_sequence': reference_sequence, 'edit_sequence': edit_sequence, 'editnumber_sequence': editnumber_sequence, 'edit_span_length': [edit_span_length_w_ref, edit_span_length_w_edit], 'edit_start_in_ref': edit_start_in_ref, 'edit_stop_in_ref_rev': edit_stop_in_ref_rev, 'pegRNA':{'+':[], '-':[]}, 'ngRNA':{'+':[], '-':[]}}

        # Find indices but shift when removing annotations
        cut_idx = re.search('/', pe_format).start()
        pam_start_idx = re.search('\[', pe_format).start()
        pam_end_idx = re.search('\]', pe_format).start()

        # Find pam and total PE format search length
        pam_length = pam_end_idx - pam_start_idx - 1
        pe_format_length = len(pe_format) - 3

        # Check if cut site is left of PAM
        if cut_idx < pam_start_idx:

            # Shift indices with removal of annotations
            pam_start_idx = pam_start_idx - 1
            pam_end_idx = pam_end_idx - 2
            spacer_start_idx = 0
            spacer_end_idx = pam_start_idx

        else:
            pam_end_idx = pam_end_idx - 1
            cut_idx = cut_idx - 2
            spacer_start_idx = pam_end_idx
            spacer_end_idx = len(pe_format) - 3

        # Remove annotations and convert into regex
        pe_format_rm_annotation = pe_format.replace('/', '').replace('[', '').replace(']', '')

        # Create PE format and PAM search sequences
        pe_format_search_plus = ''
        for base in pe_format_rm_annotation:
            pe_format_search_plus += iupac2bases(base)
        pe_format_search_minus = reverse_complement(pe_format_search_plus)

        pam_search = ''
        pam_sequence = pe_format_rm_annotation[pam_start_idx:pam_end_idx]
        for base in pam_sequence:
            pam_search += iupac2bases(base)

        ##### Initialize data storage for output
        counter = 1
        for target_name in target_design:

            # pegRNA spacer search for (+) and (-) strands with reference sequence
            reference_sequence = target_design[target_name]['reference_sequence']
            find_guides_ref_plus = [[m.start()] for m in re.finditer('(?=%s)' % pe_format_search_plus, reference_sequence, re.IGNORECASE)]
            find_guides_ref_minus = [[m.start()] for m in re.finditer('(?=%s)' % pe_format_search_minus, reference_sequence, re.IGNORECASE)]

            # pegRNA spacer search for (+) and (-) strands with edit number sequence
            editnumber_sequence = target_design[target_name]['editnumber_sequence']
            find_guides_editnumber_plus = [[m.start()] for m in re.finditer('(?=%s)' % pam_search.replace('[', '[123456789'), editnumber_sequence, re.IGNORECASE)]
            find_guides_editnumber_minus = [[m.start()] for m in re.finditer('(?=%s)' % reverse_complement(pam_search).replace('[', '[123456789'), editnumber_sequence, re.IGNORECASE)]

            # Find pegRNA spacers targeting (+) strand
            if find_guides_ref_plus:

                for match in find_guides_ref_plus:

                    # Extract matched sequences and annotate type of prime editing
                    full_search = reference_sequence[match[0]:match[0] + pe_format_length]
                    spacer_sequence = full_search[spacer_start_idx:spacer_end_idx]
                    extension_core_sequence = full_search[:cut_idx]
                    downstream_sequence_ref = full_search[cut_idx:]
                    downstream_sequence_length = len(downstream_sequence_ref)
                    pam_ref = full_search[pam_start_idx:pam_end_idx]

                    # Check to see if the extended non target strand is conserved in the edited strand
                    try:
                        extension_core_start_idx, extension_core_end_idx = re.search(extension_core_sequence, edit_sequence).start(), re.search(extension_core_sequence, edit_sequence).end()
                        downstream_sequence_edit = edit_sequence[extension_core_end_idx:extension_core_end_idx + downstream_sequence_length]
                        pam_edit = edit_sequence[extension_core_start_idx:extension_core_start_idx + pe_format_length][pam_start_idx:pam_end_idx]
                        
                        ## Annotate pegRNA
                        # Check if PAM is mutated relative to reference sequence
                        if pam_ref == pam_edit.upper():
                            pe_annotate = 'PAM_intact'

                        else:
                            # Check to see if mutation disrupts degenerate base positions within PAM
                            if re.search(pam_search, pam_edit.upper()):
                                pe_annotate = 'PAM_intact'

                            else:
                                pe_annotate = 'PAM_mutated'

                        # Store pegRNA spacer
                        nick_ref_idx = match[0] + cut_idx
                        nick_edit_idx = extension_core_start_idx + cut_idx
                        target_design[target_name]['pegRNA']['+'].append([nick_ref_idx, nick_edit_idx, full_search, spacer_sequence, pam_ref, pam_edit, pe_annotate])

                    except:
                        continue

            # Find pegRNA spacers targeting (-) strand
            if find_guides_ref_minus:

                for match in find_guides_ref_minus:

                    # Extract matched sequences and annotate type of prime editing
                    full_search = reference_sequence[match[0]:match[0] + pe_format_length]
                    spacer_sequence = full_search[pe_format_length - spacer_end_idx:pe_format_length - spacer_start_idx]
                    extension_core_sequence = full_search[pe_format_length - cut_idx:]
                    downstream_sequence_ref = full_search[:pe_format_length - cut_idx]
                    downstream_sequence_length = len(downstream_sequence_ref)
                    pam_ref = full_search[pe_format_length - pam_end_idx:pe_format_length - pam_start_idx]

                    # Check to see if the extended non target strand is conserved in the edited strand
                    try:
                        extension_core_start_idx, extension_core_end_idx = re.search(extension_core_sequence, edit_sequence).start(), re.search(extension_core_sequence, edit_sequence).end()
                        downstream_sequence_edit = edit_sequence[extension_core_start_idx - downstream_sequence_length:extension_core_start_idx]
                        pam_edit = edit_sequence[extension_core_end_idx - pe_format_length:extension_core_end_idx][pe_format_length - pam_end_idx:pe_format_length - pam_start_idx]
                        
                        ## Annotate pegRNA
                        # Check if PAM is mutated relative to reference sequence
                        if pam_ref == pam_edit.upper():
                            pe_annotate = 'PAM_intact'

                        else:
                            # Check to see if mutation disrupts degenerate base positions within PAM
                            if re.search(reverse_complement(pam_search), pam_edit.upper()):
                                pe_annotate = 'PAM_intact'

                            else:
                                pe_annotate = 'PAM_mutated'

                        # Store pegRNA spacer
                        nick_ref_idx = match[0] + (pe_format_length - cut_idx)
                        nick_edit_idx = extension_core_start_idx - downstream_sequence_length + (pe_format_length - cut_idx)
                        target_design[target_name]['pegRNA']['-'].append([nick_ref_idx, nick_edit_idx, full_search, spacer_sequence, pam_ref, pam_edit, pe_annotate])

                    except:
                        continue

            # Find ngRNA spacers targeting (+) strand
            if find_guides_editnumber_plus:

                for match in find_guides_editnumber_plus:

                    # Extract matched sequences and annotate type of prime editing
                    full_search = editnumber_sequence[:match[0] + pam_length]
                    
                    full_search2ref = full_search
                    full_search2edit = full_search
                    for edit_number in editnumber2sequence:
                        full_search2ref = full_search2ref.replace(str(edit_number), editnumber2sequence[edit_number][0])
                        full_search2edit = full_search2edit.replace(str(edit_number), editnumber2sequence[edit_number][1])

                    if len(full_search2edit[-pe_format_length:]) == pe_format_length:

                        # Identify ngRNA sequence information from edit sequence
                        full_search_edit = full_search2edit[-pe_format_length:]
                        spacer_sequence_edit = full_search_edit[spacer_start_idx:spacer_end_idx]
                        pam_edit = full_search_edit[pam_start_idx:pam_end_idx]

                        # Use reference sequence to find nick index
                        full_search_ref = full_search2ref[-pe_format_length:]
                        spacer_sequence_ref = full_search_ref[spacer_start_idx:spacer_end_idx]
                        pam_ref = full_search_ref[pam_start_idx:pam_end_idx]

                        # Annotate ngRNA
                        if spacer_sequence_edit.upper() == spacer_sequence_ref.upper():
                            ng_annotate = 'PE3'
                        else:
                            if spacer_sequence_edit.upper()[-10:] == spacer_sequence_ref.upper()[-10:]:
                                ng_annotate = 'PE3b-nonseed'
                            else:
                                ng_annotate = 'PE3b-seed'

                        # Store ngRNA spacer
                        nick_ref_idx = re.search(full_search_ref, reference_sequence).end() - (pe_format_length - cut_idx)
                        target_design[target_name]['ngRNA']['+'].append([nick_ref_idx, full_search_edit, spacer_sequence_edit, pam_edit, ng_annotate])

            # Find ngRNA spacers targeting (-) strand
            if find_guides_editnumber_minus:

                for match in find_guides_editnumber_minus:

                    # Extract matched sequences and annotate type of prime editing
                    full_search = editnumber_sequence[match[0]:]
                    
                    full_search2ref = full_search
                    full_search2edit = full_search
                    for edit_number in editnumber2sequence:
                        full_search2ref = full_search2ref.replace(str(edit_number), editnumber2sequence[edit_number][0])
                        full_search2edit = full_search2edit.replace(str(edit_number), editnumber2sequence[edit_number][1])

                    if len(full_search2edit[:pe_format_length]) == pe_format_length:

                        # Identify ngRNA sequence information from edit sequence
                        full_search_edit = full_search2edit[:pe_format_length]
                        spacer_sequence_edit = full_search_edit[pe_format_length - spacer_end_idx:pe_format_length - spacer_start_idx]
                        pam_edit = full_search_edit[pe_format_length - pam_end_idx:pe_format_length - pam_start_idx]

                        # Use reference sequence to find nick index
                        full_search_ref = full_search2ref[:pe_format_length]
                        spacer_sequence_ref = full_search_ref[pe_format_length - spacer_end_idx:pe_format_length - spacer_start_idx]
                        pam_ref = full_search_ref[pe_format_length - pam_end_idx:pe_format_length - pam_start_idx]

                        # Annotate ngRNA
                        if spacer_sequence_edit.upper() == spacer_sequence_ref.upper():
                            ng_annotate = 'PE3'
                        else:
                            if spacer_sequence_edit.upper()[:10] == spacer_sequence_ref.upper()[:10]:
                                ng_annotate = 'PE3b-nonseed'
                            else:
                                ng_annotate = 'PE3b-seed'

                        # Store ngRNA spacer
                        nick_ref_idx = re.search(full_search_ref, reference_sequence).start() + (pe_format_length - cut_idx)
                        target_design[target_name]['ngRNA']['-'].append([nick_ref_idx, full_search_edit, spacer_sequence_edit, pam_edit, ng_annotate])

            # Grab index information of edits to introduce to target sequence
            edit_start_in_ref = int(target_design[target_name]['edit_start_in_ref'])
            edit_stop_in_ref_rev = int(target_design[target_name]['edit_stop_in_ref_rev'])
            edit_span_length_w_ref = int(target_design[target_name]['edit_span_length'][0])
            edit_span_length_w_edit = int(target_design[target_name]['edit_span_length'][1])

            # Design pegRNAs targeting the (+) strand
            counter = 1
            counted = []
            for peg_plus in target_design[target_name]['pegRNA']['+']:

                pe_nick_ref_idx, pe_nick_edit_idx, pe_full_search, pe_spacer_sequence, pe_pam_ref, pe_pam_edit, pe_annotate = peg_plus
                pegid = '_'.join(map(str, [pe_nick_ref_idx, pe_spacer_sequence, pe_pam_ref, pe_annotate, '+']))

                pe_annotate_constant = pe_annotate

                # See if pegRNA spacer can introduce all edits
                nick2edit_length = edit_start_in_ref - pe_nick_ref_idx
                if nick2edit_length >= 0:

                    # Loop through RTT lengths
                    for rtt_length in rtt_length_list:

                        # See if RT length can reach entire edit
                        nick2lastedit_length = nick2edit_length + edit_span_length_w_edit
                        if nick2lastedit_length < rtt_length:

                            # Loop through PBS lengths
                            for pbs_length in pbs_length_list:
                                pe_pam_ref_silent_mutation = ''

                                # Construct pegRNA extension to encode intended edit(s)

                                # Patch for NGG PAMs - may need to build something more generalizable in the future
                                if silent_mutation == 'yes':
                                    
                                    if pe_annotate_constant == 'PAM_intact':

                                        nick_aa_index = int(pe_nick_edit_idx)%3
                                        
                                        if nick_aa_index == 0:
                                            original_codon = edit_sequence[pe_nick_edit_idx + 3:pe_nick_edit_idx + 6].upper()

                                            if len(codon_swap_0[original_codon.upper()]) > 1:
                                                new_codon = codon_swap_0[original_codon][0][0].lower()
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + 3] + new_codon + edit_sequence[pe_nick_edit_idx + 6:pe_nick_edit_idx + rtt_length])
                                                pe_pam_ref_silent_mutation = pe_pam_ref + '-to-' + new_codon
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            else:
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + rtt_length])

                                        elif nick_aa_index == 1:
                                            original_codon_1 = edit_sequence[pe_nick_edit_idx + 2:pe_nick_edit_idx + 5].upper()
                                            original_codon_2 = edit_sequence[pe_nick_edit_idx + 5:pe_nick_edit_idx + 8].upper()

                                            if len(codon_swap_1_1[original_codon_1.upper()]) > 1:
                                                new_codon = codon_swap_1_1[original_codon_1][0][0].lower()
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + 2] + new_codon + edit_sequence[pe_nick_edit_idx + 5:pe_nick_edit_idx + rtt_length])
                                                pe_pam_ref_silent_mutation = pe_pam_ref + '-to-' + new_codon[1:] + original_codon_2[:1].lower()
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            elif len(codon_swap_1_2[original_codon_2.upper()]) > 1:
                                                new_codon = codon_swap_1_2[original_codon_2][0][0].lower()
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + 5] + new_codon + edit_sequence[pe_nick_edit_idx + 8:pe_nick_edit_idx + rtt_length])
                                                pe_pam_ref_silent_mutation = pe_pam_ref + '-to-' + original_codon_1[1:].lower() + new_codon[:1]
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            else:
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + rtt_length])

                                        elif nick_aa_index == 2:
                                            original_codon = edit_sequence[pe_nick_edit_idx + 4:pe_nick_edit_idx + 7].upper()

                                            if len(codon_swap_2[original_codon.upper()]) > 1:
                                                new_codon = codon_swap_2[original_codon][0][0].lower()
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + 4] + new_codon + edit_sequence[pe_nick_edit_idx + 7:pe_nick_edit_idx + rtt_length])
                                                pe_pam_ref_silent_mutation = pe_pam_ref + '-to-' + edit_sequence[pe_nick_edit_idx + 3:pe_nick_edit_idx + 4].lower() + new_codon[:2]
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            else:
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + rtt_length])

                                    else:
                                        pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + rtt_length])

                                else:
                                    pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + rtt_length])

                                # Check to see if pegRNA extension is within input sequence
                                if len(pegRNA_ext) == (pbs_length + rtt_length):

                                    peg_design['pegRNA group'].append(counter)
                                    peg_design['type'].append('pegRNA')
                                    peg_design['spacer sequence'].append(pe_spacer_sequence)
                                    peg_design['spacer GC content'].append(gc_content(pe_spacer_sequence))

                                    if pe_pam_ref_silent_mutation == '':
                                        peg_design['PAM'].append(pe_pam_ref)
                                    else:
                                        peg_design['PAM'].append(pe_pam_ref_silent_mutation)

                                    peg_design['strand'].append('+')
                                    peg_design['peg-to-edit distance'].append(nick2lastedit_length)
                                    peg_design['nick-to-peg distance'].append('')
                                    peg_design['pegRNA extension'].append(pegRNA_ext)
                                    peg_design['extension first base'].append(pegRNA_ext[0])
                                    peg_design['PBS length'].append(pbs_length)
                                    peg_design['PBS GC content'].append(gc_content(pegRNA_ext[rtt_length:]))
                                    peg_design['RTT length'].append(rtt_length)
                                    peg_design['RTT GC content'].append(gc_content(pegRNA_ext[:rtt_length]))
                                    peg_design['annotation'].append(pe_annotate)
                                    peg_design['spacer top strand oligo'].append('caccG' + pe_spacer_sequence[1:] + 'gtttt')
                                    peg_design['spacer bottom strand oligo'].append('ctctaaaac' + reverse_complement('G' + pe_spacer_sequence[1:]))
                                    peg_design['pegRNA extension top strand oligo'].append('gtgc' + pegRNA_ext)
                                    peg_design['pegRNA extension bottom strand oligo'].append('aaaa' + reverse_complement(pegRNA_ext))

                                    counted.append(counter)

                    # Create ngRNAs targeting (-) strand for (+) pegRNAs
                    if counter in counted:
                        for ng_minus in target_design[target_name]['ngRNA']['-']:
                            ng_nick_ref_idx, ng_full_search_edit, ng_spacer_sequence_edit, ng_pam_edit, ng_annotate = ng_minus
                            nick_distance = ng_nick_ref_idx - pe_nick_ref_idx
                            if (abs(nick_distance) >= nicking_distance_minimum) and (abs(nick_distance) <= nicking_distance_maximum):

                                peg_design['pegRNA group'].append(counter)
                                peg_design['type'].append('ngRNA')
                                peg_design['spacer sequence'].append(reverse_complement(ng_spacer_sequence_edit))
                                peg_design['spacer GC content'].append(gc_content(reverse_complement(ng_spacer_sequence_edit)))
                                peg_design['PAM'].append(reverse_complement(ng_pam_edit))
                                peg_design['strand'].append('-')
                                peg_design['peg-to-edit distance'].append('')
                                peg_design['nick-to-peg distance'].append(nick_distance)
                                peg_design['pegRNA extension'].append('')
                                peg_design['extension first base'].append('')
                                peg_design['PBS length'].append('')
                                peg_design['PBS GC content'].append('')
                                peg_design['RTT length'].append('')
                                peg_design['RTT GC content'].append('')
                                peg_design['annotation'].append(ng_annotate)
                                peg_design['spacer top strand oligo'].append('caccG' + reverse_complement(ng_spacer_sequence_edit)[1:])
                                peg_design['spacer bottom strand oligo'].append('aaac' + reverse_complement('G' + reverse_complement(ng_spacer_sequence_edit)[1:]))
                                peg_design['pegRNA extension top strand oligo'].append('')
                                peg_design['pegRNA extension bottom strand oligo'].append('')

                        counter += 1

            # Design pegRNAs targeting the (-) strand
            for peg_minus in target_design[target_name]['pegRNA']['-']:

                pe_nick_ref_idx, pe_nick_edit_idx, pe_full_search, pe_spacer_sequence, pe_pam_ref, pe_pam_edit, pe_annotate = peg_minus
                pegid = '_'.join(map(str, [pe_nick_ref_idx, pe_spacer_sequence, pe_pam_ref, pe_annotate, '-']))

                pe_annotate_constant = pe_annotate

                # See if pegRNA spacer can introduce all edits
                nick2edit_length = edit_stop_in_ref_rev - (len(reference_sequence) - pe_nick_ref_idx)
                if nick2edit_length >= 0:

                    # Loop through RTT lengths
                    for rtt_length in rtt_length_list:

                        # See if RT length can reach entire edit
                        nick2lastedit_length = nick2edit_length + edit_span_length_w_edit
                        if nick2lastedit_length < rtt_length:

                            # Loop through PBS lengths
                            for pbs_length in pbs_length_list:
                                pe_pam_ref_silent_mutation = ''

                                # Construct pegRNA extension to encode intended edit(s)
                                # pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx + pbs_length]

                                # Patch for NGG PAMs - may need to build something more generalizable in the future
                                if silent_mutation == 'yes':
                                    
                                    if pe_annotate_constant == 'PAM_intact':

                                        nick_aa_index = int(pe_nick_edit_idx)%3
                                        
                                        if nick_aa_index == 0:
                                            original_codon = edit_sequence[pe_nick_edit_idx - 6:pe_nick_edit_idx - 3].upper()

                                            if len(codon_swap_2[original_codon.upper()]) > 1:
                                                new_codon = codon_swap_2[original_codon][0][0].lower()
                                                pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx - 6] + new_codon + edit_sequence[pe_nick_edit_idx - 3:pe_nick_edit_idx + pbs_length]
                                                pe_pam_ref_silent_mutation = reverse_complement(pe_pam_ref) + '-to-' + reverse_complement(new_codon)
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            else:
                                                pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx + pbs_length]

                                        elif nick_aa_index == 1:
                                            original_codon = edit_sequence[pe_nick_edit_idx - 7:pe_nick_edit_idx - 4].upper()

                                            if len(codon_swap_0[original_codon.upper()]) > 1:
                                                new_codon = codon_swap_0[original_codon][0][0].lower()
                                                pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx - 7] + new_codon + edit_sequence[pe_nick_edit_idx - 4:pe_nick_edit_idx + pbs_length]
                                                pe_pam_ref_silent_mutation = reverse_complement(pe_pam_ref) + '-to-' + reverse_complement(new_codon[1:] + edit_sequence[pe_nick_edit_idx - 4:pe_nick_edit_idx - 3].lower())
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            else:
                                                pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx + pbs_length]

                                        elif nick_aa_index == 2:
                                            original_codon_1 = edit_sequence[pe_nick_edit_idx - 8:pe_nick_edit_idx - 5].upper()
                                            original_codon_2 = edit_sequence[pe_nick_edit_idx - 5:pe_nick_edit_idx - 2].upper()

                                            if len(codon_swap_1_1[original_codon_1.upper()]) > 1:
                                                new_codon = codon_swap_1_1[original_codon_1][0][0].lower()
                                                pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx - 8] + new_codon + edit_sequence[pe_nick_edit_idx - 5:pe_nick_edit_idx + pbs_length]
                                                pe_pam_ref_silent_mutation = reverse_complement(pe_pam_ref) + '-to-' + reverse_complement(new_codon[2:] + original_codon_2[:2].lower())
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            elif len(codon_swap_1_2[original_codon_2.upper()]) > 1:
                                                new_codon = codon_swap_1_2[original_codon_2][0][0].lower()
                                                pegRNA_ext = reverse_complement(edit_sequence[pe_nick_edit_idx - pbs_length:pe_nick_edit_idx + 5] + new_codon + edit_sequence[pe_nick_edit_idx + 8:pe_nick_edit_idx + rtt_length])
                                                pe_pam_ref_silent_mutation = reverse_complement(pe_pam_ref) + '-to-' + reverse_complement(original_codon_1[2:].lower() + new_codon[:2])
                                                pe_annotate = 'PAM_mutated_silent_mutation'

                                            else:
                                                pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx + pbs_length]

                                    else:
                                        pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx + pbs_length]

                                else:
                                    pegRNA_ext = edit_sequence[pe_nick_edit_idx - rtt_length:pe_nick_edit_idx + pbs_length] ########

                                # Check to see if pegRNA extension is within input sequence
                                if len(pegRNA_ext) == (pbs_length + rtt_length):

                                    peg_design['pegRNA group'].append(counter)
                                    peg_design['type'].append('pegRNA')
                                    peg_design['spacer sequence'].append(reverse_complement(pe_spacer_sequence))
                                    peg_design['spacer GC content'].append(gc_content(reverse_complement(pe_spacer_sequence)))

                                    if pe_pam_ref_silent_mutation == '':
                                        peg_design['PAM'].append(reverse_complement(pe_pam_ref))
                                    else:
                                        peg_design['PAM'].append(pe_pam_ref_silent_mutation)

                                    peg_design['strand'].append('-')
                                    peg_design['peg-to-edit distance'].append(nick2lastedit_length)
                                    peg_design['nick-to-peg distance'].append('')
                                    peg_design['pegRNA extension'].append(pegRNA_ext)
                                    peg_design['extension first base'].append(pegRNA_ext[0])
                                    peg_design['PBS length'].append(pbs_length)
                                    peg_design['PBS GC content'].append(gc_content(pegRNA_ext[rtt_length:]))
                                    peg_design['RTT length'].append(rtt_length)
                                    peg_design['RTT GC content'].append(gc_content(pegRNA_ext[:rtt_length]))
                                    peg_design['annotation'].append(pe_annotate)
                                    peg_design['spacer top strand oligo'].append('caccG' + reverse_complement(pe_spacer_sequence)[1:] + 'gtttt')
                                    peg_design['spacer bottom strand oligo'].append('ctctaaaac' + reverse_complement('G' + reverse_complement(pe_spacer_sequence)[1:]))
                                    peg_design['pegRNA extension top strand oligo'].append('gtgc' + pegRNA_ext)
                                    peg_design['pegRNA extension bottom strand oligo'].append('aaaa' + reverse_complement(pegRNA_ext))

                                    counted.append(counter)

                    # Create ngRNAs targeting (+) strand for (-) pegRNAs
                    if counter in counted:
                        for ng_plus in target_design[target_name]['ngRNA']['+']:
                            ng_nick_ref_idx, ng_full_search_edit, ng_spacer_sequence_edit, ng_pam_edit, ng_annotate = ng_plus
                            nick_distance = ng_nick_ref_idx - pe_nick_ref_idx
                            if (abs(nick_distance) >= nicking_distance_minimum) and (abs(nick_distance) <= nicking_distance_maximum):

                                peg_design['pegRNA group'].append(counter)
                                peg_design['type'].append('ngRNA')
                                peg_design['spacer sequence'].append(ng_spacer_sequence_edit)
                                peg_design['spacer GC content'].append(gc_content(ng_spacer_sequence_edit))
                                peg_design['PAM'].append(ng_pam_edit)
                                peg_design['strand'].append('+')
                                peg_design['peg-to-edit distance'].append('')
                                peg_design['nick-to-peg distance'].append(nick_distance)
                                peg_design['pegRNA extension'].append('')
                                peg_design['extension first base'].append('')
                                peg_design['PBS length'].append('')
                                peg_design['PBS GC content'].append('')
                                peg_design['RTT length'].append('')
                                peg_design['RTT GC content'].append('')
                                peg_design['annotation'].append(ng_annotate)
                                peg_design['spacer top strand oligo'].append('caccG' + ng_spacer_sequence_edit[1:])
                                peg_design['spacer bottom strand oligo'].append('aaac' + reverse_complement('G' + ng_spacer_sequence_edit[1:]))
                                peg_design['pegRNA extension top strand oligo'].append('')
                                peg_design['pegRNA extension bottom strand oligo'].append('')

                        counter += 1

        df = pd.DataFrame.from_dict(peg_design)

    else:
        df = {'pegRNA group':[],'type':[], 'spacer sequence':[],'spacer GC content':[],'PAM':[],'strand':[],'peg-to-edit distance':[],'nick-to-peg distance':[],'pegRNA extension':[], 'extension first base':[],'PBS length':[],'PBS GC content':[],'RTT length':[],'RTT GC content':[],'annotation':[],'spacer top strand oligo':[], 'spacer bottom strand oligo':[], 'pegRNA extension top strand oligo':[], 'pegRNA extension bottom strand oligo':[]}
        df = pd.DataFrame.from_dict(peg_design)

    if extfirstbase_filter == 'yes':
        df = df[df['extension first base'] != 'C']
        df.reset_index(drop=True, inplace=True)

    df_pegs = df[df['type'] == 'pegRNA']
    df_pegs = df_pegs[['pegRNA group','spacer sequence','PAM','strand','peg-to-edit distance','spacer GC content','annotation']].drop_duplicates()
    df_pegs = df_pegs.sort_values('peg-to-edit distance')
    df_pegs.reset_index(drop=True, inplace=True)

    df.to_csv('/PrimeDesign/reports/PrimeDesign_%s.csv' % session_id)

    return(df_pegs.to_dict('records'), df.to_json(date_format='iso', orient='split'), df_pegs.to_json(date_format='iso', orient='split'))

# Trigger pegRNA extension and ngRNA tables with pegRNA spacer selection
@app.callback(Output('pegext-table', 'data'),
    [Input('peg-table','selected_rows'), Input('store-peg-table-total', 'children'), Input('store-peg-table', 'children')]
)

def update_pegext_table(selected_row, store_peg_table_total, store_peg_table):

    try:
        # Open up stored peg table
        df_peg = pd.read_json(store_peg_table, orient='split')
        df_peg_total = pd.read_json(store_peg_table_total, orient='split')

        spacer_sequence = list(df_peg.loc[selected_row, 'spacer sequence'].values)
        df_pegext = df_peg_total[df_peg_total['spacer sequence'].isin(spacer_sequence)]
        df_pegext = df_pegext[df_pegext['type'] == 'pegRNA']
        df_pegext = df_pegext[['PBS length','PBS GC content','RTT length','RTT GC content','pegRNA extension']].drop_duplicates()
        df_pegext.reset_index(drop=True, inplace=True)

    except:
        df_pegext = {'pegRNA group':[],'type':[], 'spacer sequence':[],'spacer GC content':[],'PAM':[],'strand':[],'peg-to-edit distance':[],'nick-to-peg distance':[],'pegRNA extension':[], 'extension first base':[],'PBS length':[],'PBS GC content':[],'RTT length':[],'RTT GC content':[],'annotation':[],'spacer top strand oligo':[], 'spacer bottom strand oligo':[], 'pegRNA extension top strand oligo':[], 'pegRNA extension bottom strand oligo':[]}
        df_pegext = pd.DataFrame.from_dict(df_pegext)

    return(df_pegext.to_dict('records'))

@app.callback(Output('ng-table', 'data'),
    [Input('peg-table','selected_rows'), Input('store-peg-table-total', 'children'), Input('store-peg-table', 'children')]
)

def update_ng_table(selected_row, store_peg_table_total, store_peg_table):

    try:
        # Open up stored peg table
        df_peg = pd.read_json(store_peg_table, orient='split')
        df_peg_total = pd.read_json(store_peg_table_total, orient='split')

        peg_group = list(df_peg.loc[selected_row, 'pegRNA group'].values)
        df_ng = df_peg_total[df_peg_total['pegRNA group'].isin(peg_group)]
        df_ng = df_ng[df_ng['type'] == 'ngRNA']
        df_ng = df_ng[['spacer sequence','PAM','strand','nick-to-peg distance','spacer GC content','annotation']].drop_duplicates()
        df_ng.reset_index(drop=True, inplace=True)

    except:
        df_ng = {'pegRNA group':[],'type':[], 'spacer sequence':[],'spacer GC content':[],'PAM':[],'strand':[],'peg-to-edit distance':[],'nick-to-peg distance':[],'pegRNA extension':[], 'extension first base':[],'PBS length':[],'PBS GC content':[],'RTT length':[],'RTT GC content':[],'annotation':[],'spacer top strand oligo':[], 'spacer bottom strand oligo':[], 'pegRNA extension top strand oligo':[], 'pegRNA extension bottom strand oligo':[]}
        df_ng = pd.DataFrame.from_dict(df_ng)

    return(df_ng.to_dict('records'))

@app.callback(Output('download-link', 'href'),
    [Input('input-check','children')],
    state = [State('session-id', 'children')]
)
def update_download_link(input_check, session_id):
    return('/download/PrimeDesign_%s.csv' % session_id)

if __name__ == '__main__':
    app.run_server(debug = True, port = 9994, host = '0.0.0.0')
    # app.run_server(debug=True)