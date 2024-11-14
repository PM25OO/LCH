from Crypto.Util.number import inverse, long_to_bytes

def decrypt(enc, n, r, e=0x10001):
    # 计算 p * q
    pq = n // r
    
    # 计算 φ(n)
    phi_n = (pq - 1) * (r - 1)

    # 计算私钥 d
    d = inverse(e, phi_n)

    # 解密
    m = pow(enc, d, n)

    # 转换为字节
    return long_to_bytes(m)

# 使用示例
enc=723852783280738670480862714539930471206939893387495374728807180928170040855445891876810152632955342925014279753160237062072474054700560233898909394660490417632359569741750996883510364768373221969675772754669122369566358450338385168773138314820585004035768091977722782401857159018172832310997238672686489673301275835666185334359440075342023104052558774817610657317712163890486732346022302079976379774662502846938697679087577185012936829232473041039386591195506904
n=1663583718094586730837451748197058032299522651473749641525054459117962450366426552675301008375169274854239719363619010550610813358797722073028646262079949376791163787495017908867587786603253099311821587419560840823468234767300147535415690186105742236879949466671166970831924025155128203812581040394001877726028195237104454298243118210958199326272015188952263905737483290217215401661276221805846653080307153556341632104170784327132954510682061648111287792991570953
r=13330426831159459811337415563218112943686597186286589889452627328687746155576648596965790144956729749034192620309865207119116653586528504831428976675766211

flag = decrypt(enc, n, r)
print(flag)