""" main app entrypoint """

import terminal

def application(editor_ns):
    """ load application into editor namespace """ 

    exec("""
    null = None
    true = True
    false = False
    from context import Context
    self = Context()
    """, editor_ns)

terminal.onload(callback=application)
