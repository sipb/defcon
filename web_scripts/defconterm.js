/*
  jsterm.js Copyright (C) 2006 Natsuhiro Ichinose <ichinose@genome.ist.i.kyoto-u.ac.jp>
  License: GPL's
  $Id: jsterm.js,v 1.6 2006/07/13 07:59:53 ichinose Exp $
*/

var JSTerm={
  write:function(l){
    Terminal.stdout.write(l);
  },

  writeln:function(l){
    Terminal.stdout.puts(l);
  },

  puts:function(l){
    Terminal.stdout.puts(l);
  },

  require:function(url){
    var s=document.createElement("script");
    s.type="text/javascript";
    s.src=url;
    document.body.appendChild(s);
  },
  
  observe:function(element,type,callback,capture){
    if(element.addEventListener){
      element.addEventListener(type,callback,capture);
    }
    else if(element.attachEvent){
      element.attachEvent("on"+type,callback);
    }
    else{
      element["on"+type]=callback;
    }
  },

  Editor:{
    value:"",
    win:null,
    area:null,
    open:function(value){
      if(JSTerm.Editor.win&&!JSTerm.Editor.win.closed){
	if(arguments.length>0){
	  JSTerm.Editor.value=value;
	  JSTerm.Editor.area.value=value;
	}
	return;
      }
      var win=window.open("","JSTermEditor","toolbar=0,scrollbars=0,location=0,status=0,menubar=0,resizable=0,width=500,height=600");
      var area=document.createElement("textarea");

      if(arguments.length>0){
	JSTerm.Editor.value=value;
      }

      win.document.open();
      win.document.write("<html><body><textarea style=\"width:100%;height:100%\" id=\"jstermeditor\">"+JSTerm.Editor.value+"</textarea></body></html>");
      win.document.close();

      win.document.title="JSTerm.Editor";


      area.value=JSTerm.Editor.value;
      area.style.width="100%";
      area.style.height="100%";

      JSTerm.Editor.area=Terminal.gid(win.document,"jstermeditor");
      JSTerm.Editor.win=win;

      JSTerm.observe(win,"unload",function(){JSTerm.Editor.get();},true);
    },
    close:function(){
      if(JSTerm.Editor.win&&!JSTerm.Editor.win.closed){
	JSTerm.Editor.win.close();
      }
    },
    get:function(){
      if(JSTerm.Editor.win&&!JSTerm.Editor.win.closed){
	JSTerm.Editor.value=JSTerm.Editor.area.value;
      }
      return(JSTerm.Editor.value);
    }
  }
};

Terminal.header='<img src="fuzzball.png"><br>';

Terminal.initHook=function(){
  //JSTerm.RC.run();
  Terminal.stdout.flush();
  JSTerm.write("SIPB Athena Defcon Sign Terminal\n");
  JSTerm.write(" \bWarning Notice!\b\n \n This is a Student Information Processing Board computer system, which may be\n accessed and used only for authorized Board business by authorized\n personnel. Unauthorized access or use of this computer system may subject\n violators to criminal, civil, and/or administrative action.\n \n All information on this computer system may be intercepted, recorded, read,\n copied, and disclosed by and to authorized personnel for official purposes,\n including criminal investigations. Such information includes sensitive data\n encrypted to comply with confidentiality and privacy requirements. Access\n or use of this computer system by any person, whether authorized or\n unauthorized, constitutes consent to these terms. There is no right of\n privacy in this system.\n");
  enterState(0);
// Terminal.promptI="login: "
// JSTerm.state = 0
};

function sendCommand(cmd) {
	new Ajax.Request('/~defcon/command.cgi', {
		method: 'get',
		parameters: {request: 'command', command: cmd, sid: JSTerm.sid},
		onSuccess: function(transport){
			var json = transport.responseText.evalJSON();
			if (json["message"]) {
				JSTerm.puts(json["message"])
			}
			if (json["status"] == 200) {
				//JSTerm.write("% ")
				enterState(3);
			} else {
				JSTerm.puts("Command Failed ("+json["status"]+")");
				enterState(3);
			}
			Terminal.stdout.flush()
		},
		onFailure: function(transport){
			JSTerm.puts("Request Failed");
			enterState(3);
		}
	});
}

function enterState(n) {
	JSTerm.state = n
	switch (n) {
		case 0:
			Terminal.promptI="\blogin:\b "
			Terminal.stdin.regularMode()
			break
		case 1:
			Terminal.promptI="\bpassword:\b "
			Terminal.stdin.passwordMode()
			break
		case 2:
			// FIXME: use AJAX to send password
			Terminal.promptI=""
			Terminal.stdin.regularMode()
			new Ajax.Request('/~defcon/command.cgi', {
				method: 'post',
				parameters: {request: 'login', username: JSTerm.username, password: JSTerm.password},
				onSuccess: function(transport){
					var json = transport.responseText.evalJSON();
					if (json["sid"]) {
						JSTerm.sid = json["sid"];
					}
					if (json["message"]) {
						JSTerm.puts(json["message"])
					}
					if (json["status"] == 200) {
						//JSTerm.write("% ")
						enterState(3);
					} else {
						JSTerm.puts("Authentication Failed");
						enterState(0);
					}
					Terminal.stdout.flush()
				}
			});
			break
		case 3:
			Terminal.promptI="% "//"% "
			Terminal.stdin.regularMode()
			break
		case 4:
			Terminal.promptI=""
			Terminal.stdin.regularMode()
			break
	}
	Terminal.showPrompt()
	Terminal.stdout.scrollBottom()
}

Terminal.commandCallBack=function(line){
  var text=null;

  if(line.match(/^[ ]*\</)){
    JSTerm.write(line);
  }
  else{
    switch (JSTerm.state) {
      case 0:
        // login: prompt
        JSTerm.username = line
        enterState(1)
        break;
      case 1:
        // password: prompt
        JSTerm.password = line
        JSTerm.write("\n")
	enterState(2)
	break
      case 2:
	// waiting for password
        break
      case 3:
	if (line == "logout") {
		enterState(0)
	} else {
		sendCommand(line)
		enterState(4)
	}
	// send command
        break
    }
  }
  if(text!=undefined){
    try{
      JSTerm.puts(""+text);
    }
    catch(e){
      try{
	JSTerm.puts("=>error: "+e.message);
      }
      catch(e2){
	JSTerm.puts("=>error: "+e);
      }
    }
  }
};
