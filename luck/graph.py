
'REQUIRE_APT_GRAPHVIZ_DOT_BINARY'
from luck.header import os_stat_safe
# from luck.graph import rules_to_graph
from graphviz import Digraph
# from graphviz import nohtml
import graphviz
import jinja2
from jinja2 import Template, StrictUndefined
import os

def jinja2_format(s,**context):
    # d = context.copy()
    d = __builtins__.copy()
    d.update(context)
    # .update(__builtins__)
    return Template(s,undefined=StrictUndefined).render(**d)

def rule_to_label( filename, ruletype, filesize):
    import os
    fmt = '''<       
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        {#
          <TR>
            <TD ALIGN="LEFT" BGCOLOR="lightblue">attr</TD>
            <TD ALIGN="LEFT" BGCOLOR="lightblue">type</TD>
            <TD ALIGN="LEFT" BGCOLOR="lightblue">value</TD>
          </TR>
        #} 
          <TR>
            <TD ALIGN="LEFT" BGCOLOR="lightblue"> filename </TD>
            <TD ALIGN="LEFT" BGCOLOR="white" HREF="{{filename}}">
              <FONT COLOR="{% if os.path.exists(filename) %}blue{%else%}black{%endif%}"><U>{{filename}}</U></FONT></TD> 
          </TR>




          <TR>
            <TD ALIGN="LEFT" BGCOLOR="lightblue"> filesize </TD>
            <TD ALIGN="LEFT" BGCOLOR="white">{{filesize}}</TD>
          </TR>

          <TR>
            <TD ALIGN="LEFT" BGCOLOR="lightblue"> ruletype </TD>
            <TD ALIGN="LEFT" BGCOLOR="white">{{ruletype}}</TD>
          </TR>

        </TABLE>
    >'''
    return jinja2_format(fmt , **locals())



def rules_to_graph(rules, g, output_file, output_format):
    _ = '''
    Use RELATIVE path when plotting graph
    '''
    if g is None:
        g = Digraph('G', strict=True,
            # graph_attr=dict(
            # autosize="false", 
            # size="25.7,8.3!", resolution="100"
            # )
        )
        g.attr(rankdir='RL')    
    for v in rules:
        PWD = os.getcwd()
        for _output in v.output.split():
            _output = os.path.relpath( _output, PWD)
            filesize = os_stat_safe( _output).st_size
            if v.input:
                g.node( _output,  
                    label = rule_to_label(_output, type(v).__name__, filesize=filesize),
                    # level="middle_or_sink"),
                    shape='plaintext')      
            else:
                g.node( _output,  
                    label = rule_to_label(_output, type(v).__name__, filesize=filesize),
                    shape='plaintext')      
                continue
            for _input in v.input.split():
                _input  = os.path.relpath(_input,PWD)
                g.edge( _input, _output)
                # v.output, _input)
                # pprint([v.output,  rule_to_label(v)])
    if output_file is not None:
        res = g.render(filename = output_file, format = output_format)
        return res
    else:
        return g
