import nrrd
fid = '/home/nick/Dropbox/data/allenbrain/ccf/average_template_25.nrrd'
a = nrrd.read(fid)

aid = '/home/nick/Dropbox/data/allenbrain/ccf/annotation_25.nrrd'
b = nrrd.read(aid)

imshow(a[0][:,150,:])
imshow(b[0][:,150,:])
