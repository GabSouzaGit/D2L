from pprint import pprint

def wait_template(template, params):
    template["value"] = params["time"]
    return template

def pause_template(template, params):
    template["value"] = 'Pressione ["ENTER"] para continuar.'
    return template


