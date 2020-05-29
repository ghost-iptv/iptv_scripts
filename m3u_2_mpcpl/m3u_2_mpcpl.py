import os
for file in os.listdir(os.getcwd()):
    if file.endswith('.m3u'):
        with open(file, 'r') as f: m3u = [s for s in f.read().splitlines() if s.strip()]
        with open(file.rsplit('.', 1)[0]+'.mpcpl', 'w+') as f:
            f.write('MPCPLAYLIST\n')
            for i in range(0, len(m3u)):
                if m3u[i].startswith(('http://', 'https://', 'file://', 'rtsp://', 'rtmp://', 'mms://', 'ftp://', 'udp://')):
                    f.write('{i},type,0\n{i},label,{name}\n{i},filename,{link}\n'.format(i=i//2, name=m3u[i-1].split(',', 1)[1].strip(), link=m3u[i]))
