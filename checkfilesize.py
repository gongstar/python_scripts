import os

def walk_dir(dir,fileinfo,topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            filename = os.path.join(root,name)
            print filename,os.path.getsize(filename)
            fileinfo.write(filename+ '\n')
            if os.path.getsize(filename) < 1024:
                os.remove(filename)
        

        
        for name in dirs:
            filename = os.path.join(root,name)
            print filename,os.path.getsize(filename)
            fileinfo.write('  ' + filename + '\n')
            if os.path.getsize(filename) < 1024:
                os.remove(filename)


flist = open("list.txt","wb")
walk_dir("lrec_2014",flist)
flist.close()
