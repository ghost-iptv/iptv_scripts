'''
Drag and drop various files formats (playlists like .m3u, .m3u8) to m3u_2_mpcpl.py to convert them to MPC-HC's playlists 
Binary for Windows [m3u_2_mpcpl.exe]>> https://gofile.io/?c=3tdaL3
'''
from sys import argv
for file in sys.argv[1:]:
    mpcpl=['MPCPLAYLIST\n']
    j=0
    with open(file, 'r') as f: m3u = [s for s in f.read().splitlines() if s.strip()]
    for i in range(0, len(m3u)):
        if m3u[i].startswith(('http://', 'https://', 'file://', 'rtsp://', 'rtmp://', 'mms://', 'ftp://', 'udp://')) :
            mpcpl.append('{j},type,0\n{j},label,{name}\n{j},filename,{link}\n'.format(j=j, name=m3u[i-1].split(',', 1)[1].strip(), link=m3u[i]))
            j+=1
    if len(mpcpl)>=2:
        with open(file.rsplit('.', 1)[0]+'.mpcpl', 'w+') as f:
            f.write('\n'.join(mpcpl))
