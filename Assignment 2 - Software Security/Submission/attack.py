import frida
import sys

session = frida.attach("bot")
script = session.create_script("""
Interceptor.attach(ptr(DebugSymbol.fromName("tweet").address), {
    onEnter: function(args) {
        //to give an argument 10 instead write args[0] = ptr(10);
        //0 it seems is not an interesting argument
        args[0] = ptr(10);
    }
});
""" )

script.load()
sys.stdin.read()