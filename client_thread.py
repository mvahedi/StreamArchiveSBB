from subprocess import Popen, PIPE
from time import sleep
from nbstreamreader import NonBlockingStreamReader as NBSR

# run the shell as a subprocess:
p = Popen(['python', 'shell.py'],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# wrap p.stdout with a NonBlockingStreamReader object:
#nbsr = NBSR(p.stdout)
nbsr = NBSR(open("streamingdata/datgen2-test.data"))
# issue command:
p.stdin.write('command\n')
# get the output
while True:
    output = nbsr.readline(None) # 0.1 secs to let the shell output the result
    print 'reading'
    if not output:
        print '[No more data]'
        #break
    print output