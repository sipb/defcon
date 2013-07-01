#!/usr/bin/python
from string import Template
from commands import getstatusoutput

print "Content-type: text/html\n"
print """
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">

body, body *{
background:black;
color: #008000;
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
width: 35em;
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
"""

defcon_value_header = """
<h1>
The current Athena defense condition is:
</h1>

<h2>
${value}
</h2>
"""

error_header = """
<h2>Error retrieving DEFCON value.</h2>
<h1>This may be due to outages in Athena or due to a problem on our end. Please check back later or check the DEFCON sign in our office window at W20-557.</h1>
<br>
"""

remctl_output = getstatusoutput('kinit -k -t /afs/sipb.mit.edu/project/defcon/etc/daemon-defcon.keytab daemon/defcon.mit.edu@ATHENA.MIT.EDU; remctl sipb-defcon get')
exit_status = remctl_output[0]
defcon_value = remctl_output[1]

if not exit_status:
    template_string = defcon_value_header
else:
    template_string = error_header

header_template = Template(template_string)
print header_template.substitute(dict(value=defcon_value))
                                      
print """
<p>
This website is maintained by the <a href="http://sipb.mit.edu/">MIT Student Information Processing Board (SIPB)</a>. The value displayed here summarizes SIPB's assessment of the current state of the MIT Athena network. A value of 5 indicates that Athena is in normal condition, a value of 4 might indicate outages, and decreasing values (nearing the minimum value 1) might indicate severe outages or security concerns.
</p>

<p>
This website does not reflect the opinions of MIT staff or administration. For questions, comments, and concerns, please contact <a href="mailto:sipb-joint-chiefs@mit.edu">sipb-joint-chiefs@mit.edu</a>.
</p>

<a href="http://sipb.mit.edu/"><img src="fuzzball.png"></a>
</body>
</html>
"""

print "<!-- [Debugging Information:] [Exit Status:] " + str(exit_status) + " [Output:] " + defcon_value + " -->"
