# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

import os
import re
import json
import base64

def load_input():
    """ Open existing input file """
    file = open('/.__input/__inputdata.json', 'r')
    result = json.loads(file.read().strip('\0').strip())
    file.close()
    return result

def get_input(problem):
    """" Returns the specified problem answer in the form 
         problem: problem id
         Returns string, or bytes if a file is loaded
    """
    input_data = load_input()
    pbsplit = problem.split(":")
    problem_input = input_data['input'][pbsplit[0]]
    if isinstance(problem_input, dict) and "filename" in problem_input and "value" in problem_input:
        if len(pbsplit) > 1 and pbsplit[1] == 'filename':
            return problem_input["filename"]
        else:
            return base64.b64decode(problem_input["value"])
    else:
        return problem_input
    
def parse_template(input_filename, output_filename=''):
    """ Parses a template file
        Replaces all occurences of @@problem_id@@ by the value
        of the 'problem_id' key in data dictionary
        
        input_filename: file to parse
        output_filename: if not specified, overwrite input file
    """
    data = load_input()
    with open(input_filename, 'rb') as file:
        template = file.read().decode("utf-8")
    
    # Check if 'input' in data
    if not 'input' in data:
        raise ValueError("Could not find 'input' in data")
    
    # Parse template
    for field in data['input']:
        subs = ["filename", "value"] if isinstance(data['input'][field], dict) and "filename" in data['input'][field] and "value" in data['input'][field] else [""]
        for sub in subs:
            displayed_field = field + (":" if sub else "") + sub
            regex = re.compile("@([^@]*)@" + displayed_field + '@([^@]*)@')
            for prefix, postfix in set(regex.findall(template)):
                if sub == "value":
                    text = base64.b64decode(data['input'][field][sub]).decode('utf-8')
                elif sub:
                    text = data['input'][field][sub]
                else:
                    text = data['input'][field]
                rep = "\n".join([prefix + v + postfix for v in text.splitlines()])
                template = template.replace("@{0}@{1}@{2}@".format(prefix, displayed_field, postfix), rep)
    
    if output_filename == '':
        output_filename=input_filename
    
    # Ensure directory of resulting file exists
    try:
        os.makedirs(os.path.dirname(output_filename))
    except OSError as e:
        pass

    # Write file
    with open(output_filename, 'wb') as file:
        file.write(template.encode("utf-8"))
