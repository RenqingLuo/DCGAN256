import torch as t
import torchvision as tv
from model256 import NetG, NetD
import random
gen_num = int(input("gen_num："))
class Config(object):

    netd_path = '/media/lrq/828CD1868CD174DF/DCGAN(pytorch)/checkpoints256/netD.pth' 
    netg_path = '/media/lrq/828CD1868CD174DF/DCGAN(pytorch)/checkpoints256/netG.pth'
    gen_img = '.png'
    gen_num = 1
    gen_search_num = 2
    gen_mean = 0.2
    gen_std = 1
    gpu = True
    ngf = 64  
    ndf = 64  
    nz = 100
opt = Config()

for gen in range(gen_num):
    Result=random.randint(1000000,100000000)
    device=t.device('cuda') if opt.gpu else t.device('cpu')
    netg, netd = NetG(opt).eval(), NetD(opt).eval()
    noises = t.randn(opt.gen_search_num, opt.nz, 1, 1).normal_(opt.gen_mean, opt.gen_std)
    noises = noises.to(device)

    map_location = lambda storage, loc: storage
    netd.load_state_dict(t.load(opt.netd_path, map_location=map_location))
    netg.load_state_dict(t.load(opt.netg_path, map_location=map_location))
    netd.to(device)
    netg.to(device)

    fake_img = netg(noises)
    scores = netd(fake_img).detach()
    indexs = scores.topk(opt.gen_num)[1]
    result = []
    for ii in indexs:
        result.append(fake_img.data[ii])
        tv.utils.save_image(t.stack(result), str(Result)+opt.gen_img, normalize=True, range=(-1, 1))
