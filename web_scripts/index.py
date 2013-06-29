#!/usr/bin/python
from string import Template
from commands import getstatusoutput

template_string = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!-- $$Id: jsterm.html,v 1.2 2006/04/21 18:13:41 ichinose Exp $$ -->
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">

body, body *{
background:black;
color:green;
scrollbar-base-color: #000000;
scrollbar-arrow-color: #006400;
scrollbar-3dlight-color: #006400;
scrollbar-darkshadow-color: #006400;
scrollbar-face-color: #000000;
scrollbar-highlight-color: #000000;
scrollbar-shadow-color: #000000;
}

a{
color: #00FF00;
}

img{
display: block;
margin-left: auto;
margin-right: auto;
}

em {
color: #00FF00;
font-weight: bold;
font-style: normal;
}

h1{
margin-left: auto;
margin-right: auto;
font-family:"Monaco", monospace;
font-size: 16pt;
text-align: center;
}

h2{
margin-left: auto;
margin-right: auto;
font-family:"Monaco", monospace;
font-size: 28pt;
text-align: center;
}

p{
margin-left: auto;
margin-right: auto;
width: 35em;
font-family:"Monaco", monospace;
font-size: 12pt;
text-align: left;
}

</style>
<title>SIPB Athena DEFCON</title>
</head>

<body>
<h1>
The current Athena defense condition is:
</h1>

<h2>
${value}
</h2>

<p>
This website is maintained by the <a href="http://sipb.mit.edu/">MIT Student Information Processing Board (SIPB)</a>. The value displayed here summarizes SIPB's assessment of the current state of the MIT Athena network. A value of 5 indicates that Athena is in normal condition, a value of 4 might indicate outages, and decreasing values (nearing the minimum value 1) might indicate severe outages or security concerns.
</p>

<p>
This website does not reflect the opinions of MIT staff or administration. For questions, comments, and concerns, please contact <a href="mailto:sipb-joint-chiefs@mit.edu">sipb-joint-chiefs@mit.edu</a>.
</p>

<img src="fuzzball.png">
</body>
</html>
"""

template = Template(template_string)
defcon_value = getstatusoutput('remctl sipb-defcon get')[1]
print "Content-type: text/html\n"
print template.substitute(dict(value=defcon_value))
