import frida
import sys


# jscode：定义一个变量，用来表示要调用的js代码，可在这里面使用frida定义的js接口，如send()方法
jscode = """
    Java.perform(function(){
        console.log("hook start...");
        console.log(Module.findExportByName("libphcm.so","Java_com_ph0en1x_android_1crackme_MainActivity_getFlag"));
        Interceptor.attach(Module.findExportByName("libphcm.so","Java_com_ph0en1x_android_1crackme_MainActivity_getFlag"),{
            onEnter: function(args) {
            },
            onLeave: function(retval){
                var String_java = Java.use('java.lang.String');
                var args_4 = Java.cast(retval, String_java);
                send("getFlag()==>"+args_4);
            }
        });
    });
"""

# def message(message,data)：自定义的python函数，作用是将参数输出到控制台。函数中的两个参数是python回调接口需要的。
def printMessage(message,data):
    if message['type'] == 'send':
        print('[*] {0}'.format(message['payload']))
    else:
        print(message)

# frida.get_remote_device().attach('需要hook的app包名')：获取设备并调用attach方法通过包名指定要附加的app进程。
device = frida.get_remote_device()
session = device.attach('com.ph0en1x.android_crackme')
# script = process.create_script(jscode)：根据jscode里的js代码，创建有一个对象
script = session.create_script(jscode)
# script.on("message", message)、script.load()：将jscode里的js代码和自定义的message函数联系在一起，最后通过load来执行js脚本
script.on('message',printMessage)
script.load()
sys.stdin.read()
