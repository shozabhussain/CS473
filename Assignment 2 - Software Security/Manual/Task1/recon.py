import frida
import sys

session = frida.attach("bot")
script = session.create_script("""
Interceptor.attach(DebugSymbol.fromName("tweet").address, {
    onEnter: function(args) {
        send(args[0].toInt32());
    }
});
""")
def on_message(message, data):
    print(message)
script.on('message', on_message)
script.load()
sys.stdin.read()