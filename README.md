<div align="center">
<h1>Discord_Research</h1>
</div>
<hr style="border-radius: 2%; margin-top: 60px; margin-bottom: 60px;" noshade="" size="20" width="100%">

## The Electron 
is a convenient tool for **creating desktop applications** with a web framework.  
That's why apps like Discord and Spotify use this program.

## Famous and popular apps 
use the Electron.  
Experts said **it is recommended not to run Electron**, that is, on the local machine.
Because the Chromium engine ensures protection.

## However, relatively recently, 
an **RCE vulnerability** was discovered in apps using electron.  
(It has not been patched yet.)  
RCE means, **an abbreviation of Remote Code Execution**.

## Additionally, 
the app.setAsDefaultProtocolClient  
application is vulnerable when using Windows API 1.6.16.
<div>
And Electron combines Chrome's rendering engine (Chromium)  
and Node.js into a "single runtime".
Electron applications include
</div>

<div>
  
“ATOM editor”,
“Visual Studio Code”, etc.
</div>

Then why? why? Are they using Electron?

1. “Web developers” can build cross-platform desktop applications that run on different operating systems using major JavaScript framework libraries, including React, and Vue, and without even having to learn a new language…!

2. Debugging Electron-based applications is easier than traditional desktop applications.

## Vulnerabilities/Risks of Electron and Node.js

Electron-based applications are web applications, so XSS, SQL Injection, authentication, and authorization flaws
web vulnerabilities such as

There is a vulnerability even if only Electron is used. What if node.js is also used?
If you can find a way to inject malicious JavaScript, it can even execute commands on the computer.
This means that the external application is can be stolen.
So, if you find a way to break through, you can rob any application.

#### (Sometimes some foolish people say “don’t worry about that because only Discord gets hacked”)
Fortunately, as of Electron version 5,  
we have disabled access to node.js.
But Discord ignored it.

Discord should **remove access** to the develop console on all releases,  
Set the node.js access I mentioned earlier to false as much as possible,  
They must make applications with React and Vue,  
The electron must be kept up to date,  
They should be familiar with the development guidelines.

# Conclusion
1. Must not Download Strange File X
2. Do not Click on the strange image file X  
(sometimes some people fish with a grabber they bought with money)
3. Update Electron

While researching Electron, I found out that darwin (MacOs) and Linux (Linux, linux2) are not dangerous.

This concludes the part about vulnerability research.
