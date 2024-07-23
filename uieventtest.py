import time
from webview import webview

permission_granted = False

def check_permission(element_id, event_type):
    global permission_granted
    print(f"UI event: {event_type} on element {element_id}")
    if element_id == "default_permission_button" and event_type == "click":
        print("User granted permissions")
        permission_granted = True


webview.configure(host="localhost", port=5051, debug=True)
webview.set_ui_event_callback(check_permission)
webview.start_webview()

while True:
    if permission_granted:
        webview.update_view("Permissions granted. You can now use the application.")
        time.sleep(1)
        i = 0
        # Now you can start using other features like audio playback or recording
        while True:
            webview.update_view("<h1>This is a counter running after permission grant {i}.</h1>")
            i+=1
            time.sleep(1)


    